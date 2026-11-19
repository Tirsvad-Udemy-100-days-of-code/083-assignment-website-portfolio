"""Hostile text reaches SQL only as a value: it is stored and shown literally."""

import pytest

from portfolio.application.errors.project_not_found_error import ProjectNotFoundError
from portfolio.infrastructure.repositories.sqlite_profile_repository import (
    SqliteProfileRepository,
)
from portfolio.infrastructure.repositories.sqlite_project_repository import (
    SqliteProjectRepository,
)
from portfolio.infrastructure.sqlite_database import SqliteDatabase
from sample_data import make_link, make_profile, make_project

HOSTILE_TEXTS = [
    "x'); DROP TABLE project;--",
    "Robert'); --",
    "' OR '1'='1",
    '"; DROP TABLE profile; --',
    "a\\'; DELETE FROM project; --",
    "100% ? :name $1 {0} {title}",
]


def table_names(database: SqliteDatabase) -> set[str]:
    with database.read() as connection:
        rows = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    return {row[0] for row in rows}


@pytest.mark.parametrize("text", HOSTILE_TEXTS)
def test_hostile_project_text_is_stored_and_returned_literally(
    database: SqliteDatabase, text: str
) -> None:
    tables = table_names(database)
    repository = SqliteProjectRepository(database)
    project = make_project(
        title=text,
        kind=text,
        description=text,
        source_code_url=f"https://example.com/{text.replace(' ', '')}",
        tags=(text,),
        skills=(text,),
    )

    repository.add_project(project)

    assert repository.list_projects() == (project,)
    assert table_names(database) == tables


@pytest.mark.parametrize("text", HOSTILE_TEXTS)
def test_hostile_profile_text_is_stored_and_returned_literally(
    database: SqliteDatabase, text: str
) -> None:
    tables = table_names(database)
    repository = SqliteProfileRepository(database)
    profile = make_profile(
        name=text,
        headline=text,
        summary=text,
        skills=(text,),
        links=(make_link(text, text),),
    )

    repository.save_profile(profile)

    assert repository.get_profile() == profile
    assert table_names(database) == tables


@pytest.mark.parametrize("text", HOSTILE_TEXTS)
def test_a_hostile_title_in_a_lookup_matches_nothing_else(
    database: SqliteDatabase, text: str
) -> None:
    repository = SqliteProjectRepository(database)
    repository.add_project(make_project(title="Keep"))

    with pytest.raises(ProjectNotFoundError):
        repository.remove_project(text)
    with pytest.raises(ProjectNotFoundError):
        repository.replace_project(text, make_project(title="Other"))

    assert [p.title for p in repository.list_projects()] == ["Keep"]
    assert table_names(database) >= {"project", "profile"}


def test_a_hostile_title_can_be_changed_and_removed_by_its_own_text(
    database: SqliteDatabase,
) -> None:
    repository = SqliteProjectRepository(database)
    repository.add_project(make_project(title="x'); DROP TABLE project;--"))

    repository.replace_project(
        "x'); DROP TABLE project;--", make_project(title="Robert'); --")
    )
    assert [p.title for p in repository.list_projects()] == ["Robert'); --"]

    repository.remove_project("Robert'); --")
    assert repository.list_projects() == ()
