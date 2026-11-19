"""Unit tests of the about view."""

from portfolio.application.dto.link_item import LinkItem
from portfolio.constants import LINKS_HEADING, SKILLS_HEADING
from portfolio.presentation.views.about_view import render_about_page
from sample_data import make_about_page


def test_about_view_shows_name_headline_summary_skills_and_links() -> None:
    page = render_about_page(make_about_page())
    assert "<h1>Ada Lovelace</h1>" in page
    assert "Software developer" in page
    assert "Builds small, tested programs." in page
    assert SKILLS_HEADING in page
    assert "<li>Python</li>" in page
    assert "<li>Testing</li>" in page
    assert LINKS_HEADING in page
    assert (
        '<a href="https://example.com/me" rel="noopener noreferrer">GitHub</a>' in page
    )


def test_about_view_marks_the_about_link_of_the_navigation() -> None:
    page = render_about_page(make_about_page())
    assert '<a href="about.html" aria-current="page">About</a>' in page


def test_about_view_escapes_markup_in_every_text() -> None:
    about = make_about_page(
        name="<script>n</script>",
        headline="<em>h</em>",
        summary="a & b <u>c</u>",
        skills=("<b>skill</b>",),
        links=(LinkItem("<i>label</i>", 'https://example.com/"><script>'),),
    )
    page = render_about_page(about)
    assert "<script>" not in page
    for raw in ("<em>", "<u>", "<b>skill", "<i>label"):
        assert raw not in page
    assert "a &amp; b &lt;u&gt;c&lt;/u&gt;" in page


def test_about_view_replaces_an_unsafe_link_url() -> None:
    about = make_about_page(links=(LinkItem("Click", "javascript:alert(1)"),))
    page = render_about_page(about)
    assert "javascript:" not in page
    assert '<a href="#" rel="noopener noreferrer">Click</a>' in page


def test_about_view_shows_a_page_without_links() -> None:
    page = render_about_page(make_about_page(links=()))
    assert '<ul class="links">' in page
