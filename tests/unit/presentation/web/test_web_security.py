"""Security tests of the Flask site: headers, escaping, URLs, read-only behaviour."""

import ast
import re
from pathlib import Path
from typing import NoReturn

import pytest
from flask.testing import FlaskClient

from fakes import InMemoryDataFileReader
from portfolio.application.dto.link_item import LinkItem
from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.constants import ROUTE_ABOUT, ROUTE_HOME, ROUTE_STYLESHEET
from sample_data import make_about_page, make_card, make_home_page
from web_app import make_client, make_test_app

SOURCE = Path(__file__).resolve().parents[4] / "src" / "portfolio"
SCRIPT = "<script>alert(1)</script>"
ESCAPED_SCRIPT = "&lt;script&gt;alert(1)&lt;/script&gt;"
EXPECTED_HEADERS = {
    "Content-Security-Policy": "default-src 'self'",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
}


def failing_read() -> NoReturn:
    raise DataSourceError("disk on fire")


def client() -> FlaskClient:
    return make_client(images=InMemoryDataFileReader({"a.svg": b"<svg/>"}))


@pytest.mark.parametrize(
    ("method", "path", "status"),
    [
        ("GET", ROUTE_HOME, 200),
        ("GET", ROUTE_ABOUT, 200),
        ("GET", ROUTE_STYLESHEET, 200),
        ("GET", "/images/a.svg", 200),
        ("HEAD", ROUTE_HOME, 200),
        ("GET", "/nothing", 404),
        ("GET", "/images/none.svg", 404),
        ("GET", "/images/../a.svg", 404),
        ("POST", ROUTE_HOME, 405),
        ("DELETE", "/images/a.svg", 405),
    ],
)
def test_every_response_carries_the_security_headers(
    method: str, path: str, status: int
) -> None:
    response = client().open(path, method=method, buffered=True)

    assert response.status_code == status
    for name, value in EXPECTED_HEADERS.items():
        assert response.headers[name] == value


def test_a_failed_read_page_carries_the_security_headers() -> None:
    response = make_client(home_page=failing_read).get(ROUTE_HOME)

    assert response.status_code == 500
    for name, value in EXPECTED_HEADERS.items():
        assert response.headers[name] == value


def test_the_policy_allows_only_the_site_itself() -> None:
    policy = client().get(ROUTE_HOME).headers["Content-Security-Policy"]

    assert policy == "default-src 'self'"
    assert "unsafe" not in policy


def test_the_application_is_not_in_debug_mode() -> None:
    app = make_test_app()

    assert app.debug is False
    assert app.config["DEBUG"] is False
    assert app.config["TESTING"] is False


def test_the_application_has_no_secret_key_and_sets_no_cookie() -> None:
    app = make_test_app(images=InMemoryDataFileReader({"a.svg": b"<svg/>"}))
    test_client = app.test_client()

    assert not app.secret_key
    for path in (ROUTE_HOME, ROUTE_ABOUT, ROUTE_STYLESHEET, "/images/a.svg", "/nope"):
        response = test_client.get(path, buffered=True)
        assert "Set-Cookie" not in response.headers
    assert test_client.post(ROUTE_HOME).headers.get("Set-Cookie") is None


def test_the_application_has_no_route_that_writes() -> None:
    app = make_test_app()

    methods = {
        method for rule in app.url_map.iter_rules() for method in rule.methods or set()
    }
    assert methods == {"GET", "HEAD"}
    assert {rule.rule for rule in app.url_map.iter_rules()} == {
        ROUTE_HOME,
        ROUTE_ABOUT,
        ROUTE_STYLESHEET,
        "/images/<path:file>",
    }


def test_autoescape_is_on_for_the_templates() -> None:
    app = make_test_app()

    for name in ("layout.html", "home.html", "about.html", "error.html"):
        assert callable(app.jinja_env.autoescape)
        assert app.jinja_env.autoescape(name) is True


def test_hostile_project_text_is_shown_as_text() -> None:
    card = make_card(
        title=SCRIPT,
        kind=SCRIPT,
        description=f'"><img src=x onerror=alert(1)> {SCRIPT}',
        tags=(SCRIPT,),
        skills=(SCRIPT,),
    )

    html = make_client(home_page=make_home_page((card,))).get(ROUTE_HOME).text

    assert "<script>" not in html
    assert "<img src=x" not in html
    assert html.count(ESCAPED_SCRIPT) >= 5
    assert "&#34;&gt;&lt;img src=x onerror=alert(1)&gt;" in html


def test_a_hostile_title_is_escaped_in_the_alt_text_of_the_image() -> None:
    card = make_card(title='x" onload="alert(1)', image_url="images/a.svg")

    html = make_client(home_page=make_home_page((card,))).get(ROUTE_HOME).text

    assert 'alt="x&#34; onload=&#34;alert(1)"' in html
    assert ' onload="alert(1)"' not in html


def test_hostile_profile_text_is_shown_as_text() -> None:
    page = make_about_page(
        name=SCRIPT,
        headline=SCRIPT,
        summary=SCRIPT,
        skills=(SCRIPT,),
        links=(LinkItem(SCRIPT, "https://example.com"),),
        initials="<b>",
    )

    html = make_client(about_page=page).get(ROUTE_ABOUT).text

    assert "<script>" not in html
    assert "<b>" not in html
    assert html.count(ESCAPED_SCRIPT) >= 5
    assert "&lt;b&gt;" in html


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "JaVaScRiPt:alert(1)",
        " javascript:alert(1)",
        "data:text/html,<script>alert(1)</script>",
        "vbscript:msgbox(1)",
        "//evil.example/x",
        "https:///nohost",
        "http://example.com/a\\b",
    ],
)
def test_an_unsafe_link_is_replaced_by_a_harmless_one(url: str) -> None:
    card = make_card(source_code_url=url)
    page = make_about_page(links=(LinkItem("Me", url),))

    home = make_client(home_page=make_home_page((card,))).get(ROUTE_HOME).text
    about = make_client(about_page=page).get(ROUTE_ABOUT).text

    assert 'class="card-link" href="#"' in home
    assert '<li><a href="#" rel="noopener noreferrer">Me</a></li>' in about
    assert "javascript" not in (home + about).lower()
    assert "evil.example" not in home + about


@pytest.mark.parametrize(
    "image",
    [
        "javascript:alert(1)",
        "data:image/png;base64,AAAA",
        "../secret.png",
        "/etc/a.png",
    ],
)
def test_an_unsafe_image_gives_a_placeholder_and_no_src(image: str) -> None:
    card = make_card(title="Safe", image_url=image)
    page = make_about_page(photo_url=image)

    home = make_client(home_page=make_home_page((card,))).get(ROUTE_HOME).text
    about = make_client(about_page=page).get(ROUTE_ABOUT).text

    assert "<img" not in home + about
    assert "card-placeholder" in home
    assert "avatar-initials" in about


def test_the_pages_have_no_inline_style_and_no_script() -> None:
    test_client = client()

    for path in (ROUTE_HOME, ROUTE_ABOUT, "/nope"):
        html = test_client.get(path).text.lower()
        assert " style=" not in html
        assert "<style" not in html
        assert "<script" not in html
        assert " onclick=" not in html


def test_the_templates_have_no_inline_style_and_no_script() -> None:
    for template in (SOURCE / "presentation" / "templates").glob("*.html"):
        text = template.read_text(encoding="utf-8").lower()
        assert " style=" not in text
        assert "<style" not in text
        assert "<script" not in text


def test_the_templates_never_mark_text_as_safe() -> None:
    templates = list((SOURCE / "presentation" / "templates").glob("*.html"))

    assert templates
    for template in templates:
        text = template.read_text(encoding="utf-8")
        assert re.search(r"\|\s*safe\b", text) is None
        assert re.search(r"\{%-?\s*autoescape\s+(false|off)", text) is None


def markup_uses(path: Path) -> list[str]:
    """The places in a source file that mark text as safe HTML."""
    found: list[str] = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module == "markupsafe":
            found.append(f"{path.name}: from markupsafe")
        if isinstance(node, ast.Import) and any(
            alias.name == "markupsafe" for alias in node.names
        ):
            found.append(f"{path.name}: import markupsafe")
        if isinstance(node, ast.Name) and node.id in {
            "Markup",
            "render_template_string",
        }:
            found.append(f"{path.name}: {node.id}")
        if isinstance(node, ast.Attribute) and node.attr in {
            "Markup",
            "render_template_string",
        }:
            found.append(f"{path.name}: {node.attr}")
        if isinstance(node, ast.alias) and node.name in {
            "Markup",
            "render_template_string",
        }:
            found.append(f"{path.name}: import {node.name}")
        if isinstance(node, ast.Constant) and node.value == "safe":
            found.append(f"{path.name}: the name 'safe'")
    return found


def test_no_source_file_uses_markup_or_the_safe_filter() -> None:
    files = sorted(SOURCE.rglob("*.py"))

    assert files
    assert [use for path in files for use in markup_uses(path)] == []


def test_the_markup_search_finds_what_it_looks_for(tmp_path: Path) -> None:
    sample = tmp_path / "bad.py"
    sample.write_text(
        "from markupsafe import Markup\nx = Markup('<b>')\nfilters['safe'] = str\n",
        encoding="utf-8",
    )

    uses = markup_uses(sample)

    assert "bad.py: from markupsafe" in uses
    assert "bad.py: Markup" in uses
    assert "bad.py: the name 'safe'" in uses
