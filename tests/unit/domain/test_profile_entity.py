"""Unit tests of the Profile entity."""

from collections.abc import Callable

import pytest

from portfolio.domain.entities.profile import Profile
from portfolio.domain.errors.invalid_profile_error import InvalidProfileError
from sample_data import make_profile


def test_profile_keeps_its_data_when_valid() -> None:
    profile = make_profile()
    assert profile.name == "Ada Lovelace"
    assert profile.skills == ("Python", "Testing")
    assert len(profile.links) == 1


def test_profile_accepts_no_links() -> None:
    assert make_profile(links=()).links == ()


@pytest.mark.parametrize(
    ("field", "build"),
    [
        ("name", lambda blank: make_profile(name=blank)),
        ("headline", lambda blank: make_profile(headline=blank)),
        ("summary", lambda blank: make_profile(summary=blank)),
    ],
)
@pytest.mark.parametrize("blank", ["", "   "])
def test_profile_rejects_blank_field(
    field: str, build: Callable[[str], Profile], blank: str
) -> None:
    with pytest.raises(InvalidProfileError, match=field):
        build(blank)


def test_profile_rejects_empty_skills() -> None:
    with pytest.raises(InvalidProfileError, match="skills"):
        make_profile(skills=())


def test_profile_rejects_blank_skill() -> None:
    with pytest.raises(InvalidProfileError, match="skill"):
        make_profile(skills=("Python", "  "))
