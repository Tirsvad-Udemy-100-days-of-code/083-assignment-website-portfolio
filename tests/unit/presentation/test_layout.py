"""Unit tests of the shared page layout."""

from portfolio.constants import (
    ABOUT_PAGE_FILE_NAME,
    FOOTER_TEXT,
    HOME_PAGE_FILE_NAME,
    NAV_ABOUT_LABEL,
    NAV_HOME_LABEL,
    STYLESHEET_FILE_NAME,
)
from portfolio.presentation.views.layout import render_page


def test_layout_has_header_navigation_and_footer() -> None:
    page = render_page("Portfolio", "Home", "<p>body</p>", HOME_PAGE_FILE_NAME)
    assert '<a class="site-title" href="index.html">Portfolio</a>' in page
    assert f'<a href="{HOME_PAGE_FILE_NAME}" aria-current="page">' in page
    assert f'<a href="{ABOUT_PAGE_FILE_NAME}">{NAV_ABOUT_LABEL}</a>' in page
    assert f"{NAV_HOME_LABEL}</a>" in page
    assert FOOTER_TEXT in page
    assert "<p>body</p>" in page


def test_layout_links_the_stylesheet_and_sets_the_title() -> None:
    page = render_page("Portfolio", "About", "", ABOUT_PAGE_FILE_NAME)
    assert f'<link rel="stylesheet" href="{STYLESHEET_FILE_NAME}">' in page
    assert "<title>About | Portfolio</title>" in page
    assert '<meta name="viewport"' in page


def test_layout_marks_only_the_current_page() -> None:
    page = render_page("Portfolio", "About", "", ABOUT_PAGE_FILE_NAME)
    assert page.count("aria-current") == 1
    assert f'<a href="{ABOUT_PAGE_FILE_NAME}" aria-current="page">' in page


def test_layout_escapes_the_site_and_page_title() -> None:
    page = render_page("<script>x</script>", "<i>y</i>", "", HOME_PAGE_FILE_NAME)
    assert "<script>" not in page
    assert "&lt;i&gt;y&lt;/i&gt; | &lt;script&gt;x&lt;/script&gt;" in page


def test_layout_contains_no_year() -> None:
    page = render_page("Portfolio", "Home", "", HOME_PAGE_FILE_NAME)
    assert "20" not in FOOTER_TEXT
    assert "&copy;" not in page
