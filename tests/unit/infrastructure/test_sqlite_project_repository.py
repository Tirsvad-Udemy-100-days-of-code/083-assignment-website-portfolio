"""Unit tests of the SQLite project repository, on an in-memory database."""

import pytest

from portfolio.application.errors.duplicate_project_error import DuplicateProjectError
from portfolio.application.errors.project_not_found_error import ProjectNotFoundError
from portfolio.infrastructure.repositories.sqlite_project_repository import (
    SqliteProjectRepository,
)
from portfolio.infrastructure.sqlite_database import SqliteDatabase
from sample_data import make_project


@pytest.fixture
def repository(database: SqliteDatabase) -> SqliteProjectRepository:
    return SqliteProjectRepository(database)


def titles(repository: SqliteProjectRepository) -> list[str]:
    return [project.title for project in repository.list_projects()]


def test_an_empty_database_lists_no_project(
    repository: SqliteProjectRepository,
) -> None:
    assert repository.list_projects() == ()


def test_an_added_project_is_returned_with_every_field(
    repository: SqliteProjectRepository,
) -> None:
    project = make_project(tags=("b", "a", "b"), skills=("z", "y"))

    repository.add_project(project)

    assert repository.list_projects() == (project,)


def test_a_project_without_tags_skills_and_image_is_returned_unchanged(
    repository: SqliteProjectRepository,
) -> None:
    project = make_project(image_url="", tags=(), skills=())

    repository.add_project(project)

    assert repository.list_projects() == (project,)


def test_projects_come_back_in_the_order_they_were_added(
    repository: SqliteProjectRepository,
) -> None:
    for title in ("C", "A", "B"):
        repository.add_project(make_project(title=title))

    assert titles(repository) == ["C", "A", "B"]


def test_unicode_text_is_stored_unchanged(
    repository: SqliteProjectRepository,
) -> None:
    project = make_project(title="Blå bær ✓", description="Æble, ø og å: 日本語")

    repository.add_project(project)

    assert repository.list_projects() == (project,)


def test_adding_a_title_that_is_taken_is_refused_and_changes_nothing(
    repository: SqliteProjectRepository,
) -> None:
    repository.add_project(make_project(title="A"))

    with pytest.raises(DuplicateProjectError):
        repository.add_project(make_project(title="A", kind="Other"))

    assert repository.list_projects() == (make_project(title="A"),)


def test_replacing_a_project_keeps_its_place_and_swaps_its_lists(
    repository: SqliteProjectRepository,
) -> None:
    for title in ("A", "B", "C"):
        repository.add_project(make_project(title=title))
    changed = make_project(title="B2", kind="CLI", tags=("x",), skills=())

    repository.replace_project("B", changed)

    assert titles(repository) == ["A", "B2", "C"]
    assert repository.list_projects()[1] == changed


def test_replacing_a_project_with_its_own_title_is_allowed(
    repository: SqliteProjectRepository,
) -> None:
    repository.add_project(make_project(title="A"))

    repository.replace_project("A", make_project(title="A", kind="CLI"))

    assert repository.list_projects() == (make_project(title="A", kind="CLI"),)


def test_replacing_an_unknown_project_is_refused(
    repository: SqliteProjectRepository,
) -> None:
    with pytest.raises(ProjectNotFoundError):
        repository.replace_project("A", make_project(title="A"))


def test_replacing_with_a_title_that_is_taken_is_refused(
    repository: SqliteProjectRepository,
) -> None:
    repository.add_project(make_project(title="A"))
    repository.add_project(make_project(title="B"))

    with pytest.raises(DuplicateProjectError):
        repository.replace_project("A", make_project(title="B"))

    assert titles(repository) == ["A", "B"]


def test_removing_a_project_removes_its_tags_and_skills(
    repository: SqliteProjectRepository, database: SqliteDatabase
) -> None:
    repository.add_project(make_project(title="A"))
    repository.add_project(make_project(title="B"))

    repository.remove_project("A")

    assert titles(repository) == ["B"]
    with database.read() as connection:
        tags = connection.execute("SELECT COUNT(*) FROM project_tag").fetchone()[0]
        skills = connection.execute("SELECT COUNT(*) FROM project_skill").fetchone()[0]
    assert (tags, skills) == (2, 1)


def test_removing_an_unknown_project_is_refused(
    repository: SqliteProjectRepository,
) -> None:
    with pytest.raises(ProjectNotFoundError):
        repository.remove_project("A")


def test_a_project_added_after_a_removal_comes_last(
    repository: SqliteProjectRepository,
) -> None:
    for title in ("A", "B", "C"):
        repository.add_project(make_project(title=title))
    repository.remove_project("B")

    repository.add_project(make_project(title="D"))

    assert titles(repository) == ["A", "C", "D"]
