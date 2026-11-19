"""Unit tests of the Link value object."""

import pytest

from portfolio.domain.errors.invalid_profile_error import InvalidProfileError
from sample_data import make_link


def test_link_keeps_its_data_when_valid() -> None:
    link = make_link()
    assert (link.label, link.url) == ("GitHub", "https://example.com/me")


@pytest.mark.parametrize("field", ["label", "url"])
@pytest.mark.parametrize("blank", ["", "  "])
def test_link_rejects_blank_field(field: str, blank: str) -> None:
    with pytest.raises(InvalidProfileError, match=field):
        make_link(**{field: blank})


def test_links_with_equal_data_are_equal() -> None:
    assert make_link() == make_link()
