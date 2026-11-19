"""Unit tests of the URL checks the templates use."""

import pytest

from portfolio.presentation.web.safe_urls import image_src, is_safe_url, safe_url


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com",
        "http://example.com/a?b=c#d",
        "HTTPS://EXAMPLE.COM",
        "  https://example.com  ",
        "page.html",
        "/relative/path",
    ],
)
def test_a_web_address_or_a_relative_path_is_safe(url: str) -> None:
    assert is_safe_url(url) is True


@pytest.mark.parametrize(
    "url",
    [
        "",
        "   ",
        "javascript:alert(1)",
        "JAVASCRIPT:alert(1)",
        "data:text/html,x",
        "ftp://example.com",
        "file:///etc/passwd",
        "https:",
        "https:///path",
        "//example.com",
        "a\b",
        "http://[::1",
        "https://example.com/\nx",
        "https://example.com/\x00",
    ],
)
def test_other_urls_are_not_safe(url: str) -> None:
    assert is_safe_url(url) is False


def test_safe_url_strips_a_safe_url_and_replaces_an_unsafe_one() -> None:
    assert safe_url("  https://example.com  ") == "https://example.com"
    assert safe_url("javascript:alert(1)") == "#"
    assert safe_url("") == "#"


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("images/a.svg", "/images/a.svg"),
        ("images/sub/a.PNG", "/images/sub/a.PNG"),
        ("images/my photo.jpg", "/images/my%20photo.jpg"),
        ("images/a%b.png", "/images/a%25b.png"),
        ("https://example.com/a.png", "https://example.com/a.png"),
        ("  http://example.com/a.png ", "http://example.com/a.png"),
    ],
)
def test_image_src_maps_local_images_and_keeps_web_addresses(
    url: str, expected: str
) -> None:
    assert image_src(url) == expected


@pytest.mark.parametrize(
    "url",
    [
        None,
        "",
        "  ",
        "javascript:alert(1)",
        "data:image/png;base64,AAAA",
        "../images/a.png",
        "images/../a.png",
        "/etc/a.png",
        "C:/a.png",
        "photos/a.png",
        "images/a.txt",
        "images/a.png?x=1",
        "images\a.png",
        "//example.com/a.png",
    ],
)
def test_image_src_gives_none_for_everything_else(url: str | None) -> None:
    assert image_src(url) is None
