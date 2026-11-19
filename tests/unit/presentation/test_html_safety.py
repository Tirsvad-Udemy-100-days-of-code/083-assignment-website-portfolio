"""Unit tests of the escaping and URL helpers of the views."""

import pytest

from portfolio.constants import FALLBACK_URL
from portfolio.presentation.views.html_safety import escape, is_safe_url, safe_url


def test_escape_replaces_markup_and_quotes() -> None:
    assert escape("<b>\"Tom\" & 'Jerry'</b>") == (
        "&lt;b&gt;&quot;Tom&quot; &amp; &#x27;Jerry&#x27;&lt;/b&gt;"
    )


def test_escape_keeps_unicode() -> None:
    assert escape("Blåbærgrød 東京") == "Blåbærgrød 東京"


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/a?b=1&c=2",
        "http://example.com",
        "HTTPS://EXAMPLE.COM",
        "page.html",
        "/about.html",
        "../images/a.png",
        "#top",
    ],
)
def test_safe_url_keeps_http_https_and_relative_urls(url: str) -> None:
    assert safe_url(url) == url


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "JavaScript:alert(1)",
        " javascript:alert(1)",
        "java\tscript:alert(1)",
        "data:text/html;base64,AAAA",
        "vbscript:msgbox(1)",
        "file:///etc/passwd",
        "//evil.example.com/x",
        "/\\evil.example.com",
        "https:evil",
        "https://",
        "",
        "   ",
        "http://exa\nmple.com",
    ],
)
def test_safe_url_replaces_everything_else_with_a_fallback(url: str) -> None:
    assert safe_url(url) == FALLBACK_URL
    assert not is_safe_url(url)


def test_safe_url_strips_surrounding_space() -> None:
    assert safe_url("  https://example.com  ") == "https://example.com"
