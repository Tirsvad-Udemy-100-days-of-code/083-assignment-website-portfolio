"""Unit tests of the home view."""

from portfolio.constants import EMPTY_STATE_TEXT, HOME_HEADING, SOURCE_CODE_LABEL
from portfolio.presentation.views.home_view import render_home_page
from sample_data import make_card, make_home_page


def test_home_view_shows_a_card_with_all_its_parts() -> None:
    page = render_home_page(make_home_page())
    assert HOME_HEADING in page
    assert '<h2 class="card-title">Weather app</h2>' in page
    assert '<span class="badge">Web app</span>' in page
    assert "Shows the weather of a city." in page
    assert 'src="https://example.com/weather.png"' in page
    assert (
        f'href="https://example.com/weather" rel="noopener noreferrer">'
        f"{SOURCE_CODE_LABEL}</a>"
    ) in page


def test_home_view_shows_one_card_per_project() -> None:
    cards = (make_card(title="One"), make_card(title="Two"), make_card(title="Three"))
    page = render_home_page(make_home_page(cards))
    assert page.count('<article class="card">') == 3
    assert EMPTY_STATE_TEXT not in page


def test_home_view_omits_the_image_when_there_is_none() -> None:
    page = render_home_page(make_home_page((make_card(image_url=""),)))
    assert "<img" not in page


def test_home_view_omits_an_unsafe_image() -> None:
    card = make_card(image_url="javascript:alert(1)")
    assert "<img" not in render_home_page(make_home_page((card,)))


def test_home_view_shows_an_empty_state_without_projects() -> None:
    page = render_home_page(make_home_page(()))
    assert EMPTY_STATE_TEXT in page
    assert "<article" not in page


def test_home_view_escapes_markup_in_every_text() -> None:
    card = make_card(
        title="<script>alert('t')</script>",
        kind="<b>kind</b>",
        description='"><img src=x onerror=alert(1)>',
        image_url='https://example.com/a.png" onerror="alert(1)',
        source_code_url='https://example.com/"><script>',
    )
    page = render_home_page(make_home_page((card,)))
    assert "<script>" not in page
    assert "<b>kind" not in page
    assert "<img src=x" not in page
    assert '" onerror=' not in page
    assert "&lt;script&gt;alert(&#x27;t&#x27;)&lt;/script&gt;" in page
    assert "&lt;b&gt;kind&lt;/b&gt;" in page


def test_home_view_replaces_an_unsafe_source_code_url() -> None:
    card = make_card(source_code_url="javascript:alert(1)")
    page = render_home_page(make_home_page((card,)))
    assert "javascript:" not in page
    assert '<a class="card-link" href="#" rel="noopener noreferrer">' in page
