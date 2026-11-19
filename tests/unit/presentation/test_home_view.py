"""Unit tests of the home view."""

from portfolio.constants import (
    EMPTY_STATE_TEXT,
    HOME_HEADING,
    SKILLS_HEADING,
    SOURCE_CODE_LABEL,
)
from portfolio.presentation.views.home_view import render_home_page
from sample_data import make_card, make_home_page


def _faces(page: str) -> tuple[str, str]:
    """Split a rendered card into its front and its back."""
    front, back = page.split('<div class="flip-card-face flip-card-back">')
    return front, back


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
    assert page.count('<article class="flip-card" tabindex="0">') == 3
    assert EMPTY_STATE_TEXT not in page


def test_home_view_puts_the_image_title_description_and_kind_on_the_front() -> None:
    front, back = _faces(render_home_page(make_home_page()))
    for text in ("<img", "Weather app", "Shows the weather of a city.", "Web app"):
        assert text in front
        assert text not in back


def test_home_view_puts_the_link_the_tags_and_the_skills_on_the_back() -> None:
    card = make_card(tags=("C", "Rust"), skills=("SIMD", "Threads"))
    front, back = _faces(render_home_page(make_home_page((card,))))
    assert f'rel="noopener noreferrer">{SOURCE_CODE_LABEL}</a>' in back
    assert '<li class="tag">C</li><li class="tag">Rust</li>' in back
    assert f'<h3 class="skills-title">{SKILLS_HEADING}</h3>' in back
    assert "<li>SIMD</li><li>Threads</li>" in back
    assert "SIMD" not in front
    assert SOURCE_CODE_LABEL not in front


def test_home_view_makes_the_card_focusable() -> None:
    assert 'class="flip-card" tabindex="0"' in render_home_page(make_home_page())


def test_home_view_shows_a_local_image_by_its_relative_path() -> None:
    card = make_card(image_url="images/weather.svg")
    page = render_home_page(make_home_page((card,)))
    assert 'src="images/weather.svg"' in page
    assert 'alt="Weather app"' in page


def test_home_view_omits_the_back_lists_when_there_are_none() -> None:
    card = make_card(tags=(), skills=())
    page = render_home_page(make_home_page((card,)))
    assert 'class="tags"' not in page
    assert SKILLS_HEADING not in page
    assert SOURCE_CODE_LABEL in page


def test_home_view_shows_a_placeholder_with_the_first_letter_without_an_image() -> None:
    page = render_home_page(make_home_page((make_card(title="prime", image_url=""),)))
    assert "<img" not in page
    assert 'aria-hidden="true">P</div>' in page
    assert "card-placeholder placeholder-" in page


def test_home_view_shows_a_placeholder_for_an_unsafe_image() -> None:
    card = make_card(image_url="javascript:alert(1)")
    page = render_home_page(make_home_page((card,)))
    assert "<img" not in page
    assert "card-placeholder" in page
    assert "javascript:" not in page


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
        tags=("<i>tag</i>",),
        skills=("<u>skill</u>",),
    )
    page = render_home_page(make_home_page((card,)))
    assert "<script>" not in page
    assert "<b>kind" not in page
    assert "<img src=x" not in page
    assert '" onerror=' not in page
    assert "&lt;script&gt;alert(&#x27;t&#x27;)&lt;/script&gt;" in page
    assert "&lt;b&gt;kind&lt;/b&gt;" in page
    assert "<i>tag" not in page
    assert "<u>skill" not in page
    assert "&lt;i&gt;tag&lt;/i&gt;" in page
    assert "&lt;u&gt;skill&lt;/u&gt;" in page


def test_home_view_replaces_an_unsafe_source_code_url() -> None:
    card = make_card(source_code_url="javascript:alert(1)")
    page = render_home_page(make_home_page((card,)))
    assert "javascript:" not in page
    assert '<a class="card-link" href="#" rel="noopener noreferrer">' in page
