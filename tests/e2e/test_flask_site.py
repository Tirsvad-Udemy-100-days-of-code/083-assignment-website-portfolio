"""End-to-end tests of the Flask site: a real server on a free port, real HTTP."""

import threading
import urllib.error
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

import pytest
from flask import Flask

from portfolio import __main__ as entry_point
from portfolio.constants import (
    DEFAULT_DATA_DIR,
    DEFAULT_HOST,
    EXIT_DATA_ERROR,
    EXIT_OK,
)
from portfolio.presentation.web.server import create_server

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DATA = PROJECT_ROOT / DEFAULT_DATA_DIR
TIMEOUT_SECONDS = 5
HEADERS = {
    "Content-Security-Policy": "default-src 'self'",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
}


@dataclass(frozen=True)
class Reply:
    status: int
    headers: dict[str, str]
    body: bytes

    @property
    def text(self) -> str:
        return self.body.decode("utf-8")


@dataclass(frozen=True)
class Site:
    """A running server and the database it reads."""

    port: int
    database: Path

    def request(
        self, path: str, method: str = "GET", data: bytes | None = None
    ) -> Reply:
        url = f"http://{DEFAULT_HOST}:{self.port}{path}"
        request = urllib.request.Request(url, data=data, method=method)
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:  # noqa: S310
                return Reply(response.status, dict(response.headers), response.read())
        except urllib.error.HTTPError as error:
            with error:
                return Reply(error.code, dict(error.headers), error.read())

    def get(self, path: str) -> Reply:
        return self.request(path)


def command(*arguments: str) -> int:
    return entry_point.main(list(arguments))


def add_project(database: Path, title: str) -> int:
    return command(
        "project",
        "add",
        "--db",
        str(database),
        "--title",
        title,
        "--kind",
        "Web app",
        "--description",
        "Shows the weather.",
        "--source-code-url",
        "https://example.com/weather",
        "--tag",
        "Flask",
    )


def import_sample(path: Path) -> None:
    assert command("init", "--db", str(path)) == EXIT_OK
    assert command("import", "--db", str(path), "--data", str(SAMPLE_DATA)) == EXIT_OK


@contextmanager
def running(database: Path) -> Iterator[Site]:
    app = entry_point.create_site(database, SAMPLE_DATA)
    server = create_server(app, DEFAULT_HOST, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield Site(server.server_port, database)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=TIMEOUT_SECONDS)


@pytest.fixture
def database(tmp_path: Path) -> Path:
    path = tmp_path / "portfolio.db"
    import_sample(path)
    return path


@pytest.fixture
def site(database: Path) -> Iterator[Site]:
    """A server of its own database, for the tests that change the data."""
    with running(database) as started:
        yield started


@pytest.fixture(scope="module")
def reading_site(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Site]:
    """One server for the tests that only read; they never change the data."""
    path = tmp_path_factory.mktemp("reading") / "portfolio.db"
    import_sample(path)
    with running(path) as started:
        yield started


def test_the_server_takes_a_free_port_and_listens_on_loopback(
    reading_site: Site,
) -> None:
    assert reading_site.port > 0
    assert reading_site.get("/").status == 200


def test_the_home_page_shows_the_projects_of_the_database(reading_site: Site) -> None:
    reply = reading_site.get("/")

    assert reply.status == 200
    assert reply.headers["Content-Type"].startswith("text/html")
    assert "Prime Number Benchmark" in reply.text
    assert reply.text.count('<article class="flip-card"') == 6
    assert 'src="/images/prime-numbers-c.svg"' in reply.text
    assert '<a href="/" aria-current="page">Home</a>' in reply.text


def test_the_about_page_shows_the_profile_of_the_database(reading_site: Site) -> None:
    reply = reading_site.get("/about")

    assert reply.status == 200
    assert "Jens Tirsvad Nielsen" in reply.text
    assert (
        "Systems Developer | Building reliable software | Always learning and adapting"
        in reply.text
    )
    assert (
        '<a href="https://www.linkedin.com/in/tirsvad74/" '
        'rel="noopener noreferrer">LinkedIn</a>'
    ) in reply.text
    assert '<img class="avatar" src="/images/profile.jpg"' in reply.text
    assert '<a href="/about" aria-current="page">About</a>' in reply.text


def test_the_stylesheet_is_served(reading_site: Site) -> None:
    reply = reading_site.get("/static/style.css")

    assert reply.status == 200
    assert reply.headers["Content-Type"].startswith("text/css")
    assert "grid-template-columns" in reply.text


@pytest.mark.parametrize("name", ["profile.jpg", "prime-numbers-c.svg"])
def test_the_images_of_the_data_folder_are_served_unchanged(
    reading_site: Site, name: str
) -> None:
    reply = reading_site.get(f"/images/{name}")

    assert reply.status == 200
    assert reply.body == (SAMPLE_DATA / "images" / name).read_bytes()
    assert reply.headers["X-Content-Type-Options"] == "nosniff"


def test_the_content_type_follows_the_file_ending(reading_site: Site) -> None:
    assert (
        reading_site.get("/images/profile.jpg").headers["Content-Type"] == "image/jpeg"
    )
    assert (
        reading_site.get("/images/blazor-sign-in.svg")
        .headers["Content-Type"]
        .startswith("image/svg+xml")
    )


@pytest.mark.parametrize(
    "path", ["/", "/about", "/static/style.css", "/images/profile.jpg"]
)
def test_head_gives_the_headers_of_get_and_no_body(
    reading_site: Site, path: str
) -> None:
    reply = reading_site.request(path, method="HEAD")

    assert reply.status == 200
    assert reply.body == b""
    assert int(reply.headers["Content-Length"]) == len(reading_site.get(path).body)


@pytest.mark.parametrize(
    "path",
    [
        "/nothing",
        "/index.html",
        "/about.html",
        "/static/other.css",
        "/images/missing.png",
        "/images/../data/projects.json",
        "/images/..%2fprojects.json",
        "/images/%2e%2e/projects.json",
        "/images/projects.json",
    ],
)
def test_other_addresses_give_a_plain_404(reading_site: Site, path: str) -> None:
    reply = reading_site.get(path)

    assert reply.status == 404
    assert "<h1>404 Not Found</h1>" in reply.text
    assert "Traceback" not in reply.text
    assert "File " not in reply.text


@pytest.mark.parametrize("method", ["POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@pytest.mark.parametrize(
    "path", ["/", "/about", "/static/style.css", "/images/profile.jpg"]
)
def test_other_methods_give_a_plain_405(
    reading_site: Site, method: str, path: str
) -> None:
    reply = reading_site.request(path, method=method, data=b"x=1")

    assert reply.status == 405
    assert reply.headers["Allow"] == "GET, HEAD"
    assert "<h1>405 Method Not Allowed</h1>" in reply.text
    assert "Traceback" not in reply.text


def test_a_post_does_not_change_the_database(reading_site: Site) -> None:
    before = reading_site.database.read_bytes()

    reading_site.request("/", method="POST", data=b"title=x")
    reading_site.request("/about", method="PUT", data=b"name=x")

    assert reading_site.database.read_bytes() == before


@pytest.mark.parametrize(
    "path", ["/", "/about", "/static/style.css", "/images/profile.jpg", "/nothing"]
)
def test_every_real_response_carries_the_security_headers(
    reading_site: Site, path: str
) -> None:
    reply = reading_site.get(path)

    for name, value in HEADERS.items():
        assert reply.headers[name] == value
    assert "Set-Cookie" not in reply.headers


def test_a_405_response_carries_the_security_headers(reading_site: Site) -> None:
    reply = reading_site.request("/", method="POST", data=b"")

    for name, value in HEADERS.items():
        assert reply.headers[name] == value


def test_an_added_project_shows_on_the_next_request_without_a_restart(
    site: Site,
) -> None:
    assert "Weather app" not in site.get("/").text

    assert add_project(site.database, "Weather app") == EXIT_OK

    reply = site.get("/")
    assert "Weather app" in reply.text
    assert '<li class="tag">Flask</li>' in reply.text
    assert reply.text.count('<article class="flip-card"') == 7


def test_a_changed_project_shows_on_the_next_request(site: Site) -> None:
    code = command(
        "project",
        "set",
        "Prime Number Benchmark",
        "--db",
        str(site.database),
        "--new-title",
        "Primes",
    )

    assert code == EXIT_OK
    html = site.get("/").text
    assert "Primes" in html
    assert "Prime Number Benchmark" not in html


def test_a_removed_project_is_gone_on_the_next_request(site: Site) -> None:
    assert "Prime Number Benchmark" in site.get("/").text

    code = command(
        "project", "remove", "Prime Number Benchmark", "--db", str(site.database)
    )

    assert code == EXIT_OK
    assert "Prime Number Benchmark" not in site.get("/").text


def test_a_changed_profile_shows_on_the_next_request(site: Site) -> None:
    code = command(
        "profile", "set", "--db", str(site.database), "--headline", "Fresh headline"
    )

    assert code == EXIT_OK
    assert "Fresh headline" in site.get("/about").text


def test_a_hostile_project_is_shown_as_text(site: Site) -> None:
    code = command(
        "project",
        "add",
        "--db",
        str(site.database),
        "--title",
        "<script>alert(1)</script>",
        "--kind",
        "<b>Web</b>",
        "--description",
        "<img src=x onerror=alert(1)>",
        "--source-code-url",
        "https://example.com/x",
    )

    assert code == EXIT_OK
    html = site.get("/").text
    assert "<script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "<img src=x" not in html
    assert "&lt;b&gt;Web&lt;/b&gt;" in html


def test_serve_with_a_missing_database_names_init_and_import(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "data" / "portfolio.db"

    code = command("serve", "--db", str(missing), "--port", "0")

    captured = capsys.readouterr()
    assert code == EXIT_DATA_ERROR
    assert captured.out == ""
    assert captured.err.startswith("error: database ")
    assert str(missing) in captured.err
    assert "python -m portfolio init" in captured.err
    assert "python -m portfolio import" in captured.err
    assert captured.err.count("\n") == 1
    assert "Traceback" not in captured.err
    assert not missing.exists()


def test_serve_with_a_file_that_is_not_a_database_gives_one_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    broken = tmp_path / "portfolio.db"
    broken.write_text("This is not a SQLite database. " * 20, encoding="utf-8")

    code = command("serve", "--db", str(broken), "--port", "0")

    captured = capsys.readouterr()
    assert code == EXIT_DATA_ERROR
    assert "python -m portfolio init" in captured.err
    assert captured.err.count("\n") == 1


def test_serve_with_a_database_that_has_no_data_asks_for_an_import(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "portfolio.db"
    assert command("init", "--db", str(path)) == EXIT_OK
    capsys.readouterr()

    code = command("serve", "--db", str(path), "--port", "0")

    captured = capsys.readouterr()
    assert code == EXIT_DATA_ERROR
    assert "python -m portfolio import" in captured.err
    assert captured.err.count("\n") == 1


def test_serve_hands_the_site_of_the_database_to_the_server(
    database: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    started: list[tuple[Flask, str, int]] = []

    def fake_serve_app(app: Flask, host: str, port: int) -> None:
        started.append((app, host, port))

    monkeypatch.setattr(entry_point, "serve_app", fake_serve_app)

    code = command("serve", "--db", str(database), "--data", str(SAMPLE_DATA))

    assert code == EXIT_OK
    assert [(host, port) for _, host, port in started] == [(DEFAULT_HOST, 8000)]
    with started[0][0].test_client() as client:
        assert client.get("/").status_code == 200
