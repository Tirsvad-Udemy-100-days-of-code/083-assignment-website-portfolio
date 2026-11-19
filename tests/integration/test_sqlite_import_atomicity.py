"""An import that fails in the middle leaves the database as it was."""

from collections.abc import Iterator
from pathlib import Path

import pytest

from portfolio.domain.entities.project import Project
from portfolio.infrastructure.errors.database_error import DatabaseError
from portfolio.infrastructure.repositories.sqlite_profile_repository import (
    SqliteProfileRepository,
)
from portfolio.infrastructure.repositories.sqlite_project_repository import (
    SqliteProjectRepository,
)
from portfolio.infrastructure.sqlite_database import SqliteDatabase
from portfolio.infrastructure.sqlite_database_initializer import (
    SqliteDatabaseInitializer,
)
from portfolio.infrastructure.sqlite_portfolio_importer import SqlitePortfolioImporter
from sample_data import make_profile, make_project


class ProjectsThatFailAfter(list[Project]):
    """Gives `good` projects when iterated, then raises while the import writes."""

    def __init__(self, good: int) -> None:
        super().__init__()
        self._good = good

    def __iter__(self) -> Iterator[Project]:
        for number in range(self._good):
            yield make_project(title=f"Project {number}")
        raise RuntimeError("the import failed in the middle")


@pytest.fixture
def database(tmp_path: Path) -> SqliteDatabase:
    created = SqliteDatabase(tmp_path / "portfolio.db")
    SqliteDatabaseInitializer(created).initialize()
    return created


def test_a_failure_in_the_middle_leaves_an_empty_database_empty(
    database: SqliteDatabase,
) -> None:
    importer = SqlitePortfolioImporter(database)

    with pytest.raises(RuntimeError, match="in the middle"):
        importer.replace_all(ProjectsThatFailAfter(3), make_profile())

    assert importer.is_empty() is True
    assert SqliteProjectRepository(database).list_projects() == ()


def test_a_failure_in_the_middle_keeps_the_data_that_was_stored(
    database: SqliteDatabase,
) -> None:
    kept_project = make_project(title="Kept")
    kept_profile = make_profile(name="Kept Name")
    SqliteProjectRepository(database).add_project(kept_project)
    SqliteProfileRepository(database).save_profile(kept_profile)

    with pytest.raises(RuntimeError, match="in the middle"):
        SqlitePortfolioImporter(database).replace_all(
            ProjectsThatFailAfter(2), make_profile(name="New Name")
        )

    assert SqliteProjectRepository(database).list_projects() == (kept_project,)
    assert SqliteProfileRepository(database).get_profile() == kept_profile


def test_a_database_error_in_the_middle_leaves_nothing_behind(
    database: SqliteDatabase,
) -> None:
    projects = [make_project(title="One"), make_project(title="Two")]
    projects.append(make_project(title="One"))
    importer = SqlitePortfolioImporter(database)

    with pytest.raises(DatabaseError, match="UNIQUE"):
        importer.replace_all(projects, make_profile())

    assert importer.is_empty() is True
