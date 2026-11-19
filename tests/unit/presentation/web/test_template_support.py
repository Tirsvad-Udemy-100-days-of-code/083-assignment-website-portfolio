"""Unit tests of the template filters and the texts of the templates."""

import pytest

from portfolio.constants import PLACEHOLDER_COLOR_COUNT
from portfolio.presentation.web.template_support import (
    placeholder_color,
    placeholder_letter,
)
from web_app import make_test_app


@pytest.mark.parametrize(
    ("title", "letter"),
    [("weather", "W"), ("  spaced", "S"), ("Éclair", "É"), ("", ""), ("   ", "")],
)
def test_placeholder_letter_is_the_first_letter_in_upper_case(
    title: str, letter: str
) -> None:
    assert placeholder_letter(title) == letter


def test_placeholder_color_is_stable_and_within_the_colour_count() -> None:
    for title in ("", "a", "Prime Number Benchmark", "日本語"):
        assert placeholder_color(title) == placeholder_color(title)
        assert 0 <= placeholder_color(title) < PLACEHOLDER_COLOR_COUNT


def test_placeholder_color_depends_on_the_title() -> None:
    assert placeholder_color("a") != placeholder_color("b")


def test_the_application_registers_the_filters_of_the_templates() -> None:
    filters = make_test_app().jinja_env.filters

    for name in ("safe_url", "image_src", "placeholder_letter", "placeholder_color"):
        assert name in filters
