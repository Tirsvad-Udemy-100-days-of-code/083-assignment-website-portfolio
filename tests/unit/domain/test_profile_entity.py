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


def test_profile_has_no_photo_by_default() -> None:
    assert make_profile().photo is None


def test_profile_accepts_a_relative_photo_path() -> None:
    assert make_profile(photo="images/profile.jpg").photo == "images/profile.jpg"


@pytest.mark.parametrize(
    "photo",
    [
        "",
        "https://example.com/me.jpg",
        "javascript:alert(1)",
        "data:image/png;base64,AAAA",
        "/etc/me.jpg",
        "../me.jpg",
        "images/me.txt",
    ],
)
def test_profile_rejects_a_photo_that_is_not_a_relative_image_path(photo: str) -> None:
    with pytest.raises(InvalidProfileError, match="photo"):
        make_profile(photo=photo)


@pytest.mark.parametrize(
    ("name", "initials"),
    [
        ("Ada Lovelace", "AL"),
        ("Jens Tirsvad Nielsen", "JN"),
        ("  grace   hopper ", "GH"),
        ("Plato", "P"),
        ("Åse Østergård", "ÅØ"),
    ],
)
def test_profile_initials_are_the_first_and_the_last_letter_of_the_name(
    name: str, initials: str
) -> None:
    assert make_profile(name=name).initials == initials
