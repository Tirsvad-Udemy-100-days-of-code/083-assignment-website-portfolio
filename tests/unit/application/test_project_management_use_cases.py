"""Unit tests of the use cases that list, add, change and remove projects."""

import pytest

from fakes import InMemoryProjectStore
from portfolio.application.dto.project_changes import ProjectChanges
from portfolio.application.dto.project_input import ProjectInput
from portfolio.application.errors.duplicate_project_error import DuplicateProjectError
from portfolio.application.errors.project_not_found_error import ProjectNotFoundError
from portfolio.application.use_cases.add_project import add_project
from portfolio.application.use_cases.change_project import change_project
from portfolio.application.use_cases.list_projects import list_projects
from portfolio.application.use_cases.remove_project import remove_project
from portfolio.constants import MAX_TAGS, MAX_TITLE_LENGTH
from portfolio.domain.errors.invalid_project_error import InvalidProjectError
from sample_data import make_project


def new_input(
    title: str = "Weather app",
    description: str = "Shows the weather.",
    image_url: str = "",
    tags: tuple[str, ...] = (),
    skills: tuple[str, ...] = (),
) -> ProjectInput:
    return ProjectInput(
        title=title,
        kind="Web app",
        description=description,
        source_code_url="https://example.com/weather",
        image_url=image_url,
        tags=tags,
        skills=skills,
    )


def test_list_projects_returns_the_cards_in_the_order_of_the_store() -> None:
    store = InMemoryProjectStore([make_project(title="B"), make_project(title="A")])

    cards = list_projects(store)

    assert [card.title for card in cards] == ["B", "A"]
    assert cards[0].tags == ("Python", "API")


def test_list_projects_of_an_empty_store_is_empty() -> None:
    assert list_projects(InMemoryProjectStore()) == ()


def test_add_project_stores_the_values() -> None:
    store = InMemoryProjectStore()

    add_project(store, new_input(tags=("Python",), skills=("Testing",)))

    stored = store.projects[0]
    assert (stored.title, stored.tags, stored.skills, stored.image_url) == (
        "Weather app",
        ("Python",),
        ("Testing",),
        "",
    )


def test_add_project_rejects_a_title_that_is_too_long() -> None:
    store = InMemoryProjectStore()

    with pytest.raises(InvalidProjectError):
        add_project(store, new_input(title="x" * (MAX_TITLE_LENGTH + 1)))

    assert store.projects == []


def test_add_project_accepts_the_longest_title() -> None:
    store = InMemoryProjectStore()

    add_project(store, new_input(title="x" * MAX_TITLE_LENGTH))

    assert len(store.projects) == 1


def test_add_project_rejects_too_many_tags() -> None:
    tags = tuple(f"tag{number}" for number in range(MAX_TAGS + 1))

    with pytest.raises(InvalidProjectError):
        add_project(InMemoryProjectStore(), new_input(tags=tags))


@pytest.mark.parametrize(
    "image_url", ["javascript:alert(1)", "../secret.png", "images/doc.txt"]
)
def test_add_project_rejects_an_unsafe_image(image_url: str) -> None:
    with pytest.raises(InvalidProjectError):
        add_project(InMemoryProjectStore(), new_input(image_url=image_url))


def test_add_project_rejects_a_blank_description() -> None:
    with pytest.raises(InvalidProjectError):
        add_project(InMemoryProjectStore(), new_input(description="   "))


def test_add_project_rejects_a_title_that_is_taken() -> None:
    store = InMemoryProjectStore([make_project(title="Weather app")])

    with pytest.raises(DuplicateProjectError):
        add_project(store, new_input())


def test_change_project_changes_only_the_given_fields() -> None:
    original = make_project(title="A", kind="Web app")
    store = InMemoryProjectStore([original])

    title = change_project(store, store, "A", ProjectChanges(kind="CLI"))

    assert title == "A"
    assert store.projects == [make_project(title="A", kind="CLI")]


def test_change_project_renames_a_project_and_keeps_its_place() -> None:
    store = InMemoryProjectStore([make_project(title="A"), make_project(title="B")])

    title = change_project(store, store, "A", ProjectChanges(title="C"))

    assert title == "C"
    assert [project.title for project in store.projects] == ["C", "B"]


def test_change_project_replaces_the_tags() -> None:
    store = InMemoryProjectStore([make_project(title="A")])

    change_project(store, store, "A", ProjectChanges(tags=("Rust",)))

    assert store.projects[0].tags == ("Rust",)


def test_change_project_rejects_an_invalid_value_and_keeps_the_project() -> None:
    store = InMemoryProjectStore([make_project(title="A")])

    with pytest.raises(InvalidProjectError):
        change_project(store, store, "A", ProjectChanges(image_url="javascript:x"))

    assert store.projects == [make_project(title="A")]


def test_change_project_without_a_value_is_refused() -> None:
    store = InMemoryProjectStore([make_project(title="A")])

    with pytest.raises(InvalidProjectError, match="nothing to change"):
        change_project(store, store, "A", ProjectChanges())


def test_change_project_of_an_unknown_title_is_refused() -> None:
    store = InMemoryProjectStore([make_project(title="A")])

    with pytest.raises(ProjectNotFoundError):
        change_project(store, store, "Z", ProjectChanges(kind="CLI"))


def test_change_project_to_a_taken_title_is_refused() -> None:
    store = InMemoryProjectStore([make_project(title="A"), make_project(title="B")])

    with pytest.raises(DuplicateProjectError):
        change_project(store, store, "A", ProjectChanges(title="B"))


def test_remove_project_removes_the_project() -> None:
    store = InMemoryProjectStore([make_project(title="A"), make_project(title="B")])

    remove_project(store, "A")

    assert [project.title for project in store.projects] == ["B"]


def test_remove_project_of_an_unknown_title_is_refused() -> None:
    with pytest.raises(ProjectNotFoundError):
        remove_project(InMemoryProjectStore(), "A")
