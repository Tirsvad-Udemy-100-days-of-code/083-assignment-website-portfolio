"""Unit tests of the set_profile use case."""

import pytest

from fakes import InMemoryProfileStore
from portfolio.application.dto.link_item import LinkItem
from portfolio.application.dto.profile_changes import ProfileChanges
from portfolio.application.use_cases.set_profile import set_profile
from portfolio.domain.errors.invalid_profile_error import InvalidProfileError
from portfolio.domain.value_objects.link import Link
from sample_data import make_profile


def complete_changes(
    name: str | None = "Grace Hopper",
    headline: str | None = "Compiler pioneer",
    summary: str | None = "Wrote the first compiler.",
    skills: tuple[str, ...] | None = ("COBOL",),
    links: tuple[LinkItem, ...] | None = None,
) -> ProfileChanges:
    return ProfileChanges(
        name=name, headline=headline, summary=summary, skills=skills, links=links
    )


def test_set_profile_creates_the_profile_when_there_is_none() -> None:
    store = InMemoryProfileStore()
    links = (LinkItem("Site", "https://example.com"),)

    created = set_profile(store, store, complete_changes(links=links))

    assert created is True
    assert store.profile is not None
    assert store.profile.name == "Grace Hopper"
    assert store.profile.links == (Link("Site", "https://example.com"),)
    assert store.profile.photo is None


@pytest.mark.parametrize(
    "changes",
    [
        complete_changes(name=None),
        complete_changes(headline=None),
        complete_changes(summary=None),
        complete_changes(skills=None),
        complete_changes(skills=()),
    ],
)
def test_set_profile_refuses_a_new_profile_without_a_required_field(
    changes: ProfileChanges,
) -> None:
    store = InMemoryProfileStore()

    with pytest.raises(InvalidProfileError, match="new profile needs"):
        set_profile(store, store, changes)

    assert store.profile is None


def test_set_profile_changes_only_the_given_fields() -> None:
    store = InMemoryProfileStore(make_profile())

    created = set_profile(store, store, ProfileChanges(headline="New headline"))

    assert created is False
    assert store.profile == make_profile(headline="New headline")


def test_set_profile_replaces_the_skills_and_the_links() -> None:
    store = InMemoryProfileStore(make_profile())

    set_profile(
        store,
        store,
        ProfileChanges(
            skills=("Rust",), links=(LinkItem("Blog", "https://example.com/blog"),)
        ),
    )

    assert store.profile is not None
    assert store.profile.skills == ("Rust",)
    assert store.profile.links == (Link("Blog", "https://example.com/blog"),)


def test_set_profile_sets_a_photo() -> None:
    store = InMemoryProfileStore(make_profile())

    set_profile(store, store, ProfileChanges(photo="images/me.png"))

    assert store.profile is not None
    assert store.profile.photo == "images/me.png"


def test_set_profile_rejects_an_invalid_photo_and_keeps_the_profile() -> None:
    store = InMemoryProfileStore(make_profile())

    with pytest.raises(InvalidProfileError):
        set_profile(store, store, ProfileChanges(photo="../me.png"))

    assert store.profile == make_profile()


def test_set_profile_rejects_a_blank_name() -> None:
    store = InMemoryProfileStore(make_profile())

    with pytest.raises(InvalidProfileError):
        set_profile(store, store, ProfileChanges(name="  "))


def test_set_profile_without_a_value_is_refused() -> None:
    store = InMemoryProfileStore(make_profile())

    with pytest.raises(InvalidProfileError, match="nothing to change"):
        set_profile(store, store, ProfileChanges())
