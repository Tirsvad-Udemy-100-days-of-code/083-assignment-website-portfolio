"""Unit tests of the SQLite import target, on an in-memory database."""

import pytest

from portfolio.infrastructure.errors.database_error import DatabaseError
from portfolio.infrastructure.repositories.sqlite_profile_repository import (
    SqliteProfileRepository,
)
from portfolio.infrastructure.repositories.sqlite_project_repository import (
    SqliteProjectRepository,
)
from portfolio.infrastructure.sqlite_database import SqliteDatabase
from portfolio.infrastructure.sqlite_portfolio_importer import SqlitePortfolioImporter
from sample_data import make_profile, make_project


def test_a_new_database_is_empty(database: SqliteDatabase) -> None:
    assert SqlitePortfolioImporter(database).is_empty() is True


def test_a_database_with_a_project_is_not_empty(database: SqliteDatabase) -> None:
    SqliteProjectRepository(database).add_project(make_project())

    assert SqlitePortfolioImporter(database).is_empty() is False


def test_a_database_with_a_profile_is_not_empty(database: SqliteDatabase) -> None:
    SqliteProfileRepository(database).save_profile(make_profile())

    assert SqlitePortfolioImporter(database).is_empty() is False


def test_replace_all_stores_the_projects_in_order_and_the_profile(
    database: SqliteDatabase,
) -> None:
    projects = [make_project(title="B"), make_project(title="A")]
    profile = make_profile()

    SqlitePortfolioImporter(database).replace_all(projects, profile)

    assert SqliteProjectRepository(database).list_projects() == tuple(projects)
    assert SqliteProfileRepository(database).get_profile() == profile


def test_replace_all_removes_what_was_stored_before(
    database: SqliteDatabase,
) -> None:
    SqliteProjectRepository(database).add_project(make_project(title="Old"))
    SqliteProfileRepository(database).save_profile(make_profile(name="Old Name"))
    new_profile = make_profile(name="New Name")

    SqlitePortfolioImporter(database).replace_all(
        [make_project(title="New")], new_profile
    )

    assert [p.title for p in SqliteProjectRepository(database).list_projects()] == [
        "New"
    ]
    assert SqliteProfileRepository(database).get_profile() == new_profile


def test_replace_all_rolls_back_when_a_title_occurs_twice(
    database: SqliteDatabase,
) -> None:
    SqliteProjectRepository(database).add_project(make_project(title="Keep"))
    projects = [make_project(title="Same"), make_project(title="Same")]

    with pytest.raises(DatabaseError, match="UNIQUE"):
        SqlitePortfolioImporter(database).replace_all(projects, make_profile())

    assert [p.title for p in SqliteProjectRepository(database).list_projects()] == [
        "Keep"
    ]
