"""Unit tests of the HTML site renderer."""

from portfolio.constants import STYLESHEET_FILE_NAME
from portfolio.presentation.html_site_renderer import HtmlSiteRenderer
from sample_data import make_about_page, make_home_page


def test_renderer_renders_the_home_page_as_a_document() -> None:
    page = HtmlSiteRenderer().render_home(make_home_page())
    assert page.startswith("<!DOCTYPE html>")
    assert "Weather app" in page


def test_renderer_renders_the_about_page_as_a_document() -> None:
    page = HtmlSiteRenderer().render_about(make_about_page())
    assert page.startswith("<!DOCTYPE html>")
    assert "Ada Lovelace" in page


def test_renderer_reads_the_packaged_stylesheet() -> None:
    css = HtmlSiteRenderer().stylesheet()
    assert "minmax(260px, 1fr)" in css
    assert "prefers-color-scheme: dark" in css
    assert "max-width: 600px" in css


def test_stylesheet_flips_the_card_on_pointer_and_keyboard_focus() -> None:
    css = HtmlSiteRenderer().stylesheet()
    assert ".flip-card:hover .flip-card-inner" in css
    assert ".flip-card:focus-within .flip-card-inner" in css
    assert ".flip-card:focus .flip-card-inner" in css
    assert "rotateY(180deg)" in css
    assert "transform-style: preserve-3d" in css
    assert "-webkit-transform-style: preserve-3d" in css
    assert "backface-visibility: hidden" in css
    assert "-webkit-backface-visibility: hidden" in css
    assert ".flip-card:focus-visible" in css


def test_stylesheet_stops_the_animation_when_the_visitor_prefers_reduced_motion() -> (
    None
):
    css = HtmlSiteRenderer().stylesheet()
    _, _, rule = css.partition("@media (prefers-reduced-motion: reduce)")
    assert rule
    assert "transition: none" in rule.split("@media")[0]


def test_stylesheet_styles_the_avatar() -> None:
    css = HtmlSiteRenderer().stylesheet()
    assert ".avatar" in css
    assert "border-radius: 50%" in css


def test_stylesheet_uses_no_external_resource() -> None:
    css = HtmlSiteRenderer().stylesheet()
    assert "http://" not in css
    assert "https://" not in css
    assert "@import" not in css
    assert STYLESHEET_FILE_NAME  # the file name is the one the layout links to
