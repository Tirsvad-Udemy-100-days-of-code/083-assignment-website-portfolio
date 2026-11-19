"""!
@file sqlite_portfolio_importer.py
@brief PortfolioImportTarget that loads a whole portfolio into SQLite.

Every statement is static text; values reach SQL only through `?` placeholders.
"""

from collections.abc import Sequence

from portfolio.domain.entities.profile import Profile
from portfolio.domain.entities.project import Project
from portfolio.infrastructure.repositories.sqlite_profile_repository import (
    replace_profile,
)
from portfolio.infrastructure.repositories.sqlite_project_repository import (
    delete_all_projects,
    insert_project,
)
from portfolio.infrastructure.sqlite_database import SqliteDatabase

_SELECT_HOLDS_DATA = (
    "SELECT EXISTS (SELECT 1 FROM project) OR EXISTS (SELECT 1 FROM profile)"
)


class SqlitePortfolioImporter:
    """!
    @brief Implements the PortfolioImportTarget port with SQLite.
    """

    def __init__(self, database: SqliteDatabase) -> None:
        """!
        @brief Create the importer.
        @param database The database to fill.
        """
        self._database = database

    def is_empty(self) -> bool:
        """!
        @brief Tell whether the database holds no project and no profile.
        @return True when it holds nothing.
        @throws DataSourceError The database cannot be used.
        """
        with self._database.read() as connection:
            return not connection.execute(_SELECT_HOLDS_DATA).fetchone()[0]

    def replace_all(self, projects: Sequence[Project], profile: Profile) -> None:
        """!
        @brief Replace everything stored by the given data, in one transaction.

        When anything fails, the transaction is rolled back and the database keeps
        what it held before.
        @param projects The projects, in the order to show them.
        @param profile The profile.
        @throws DataSourceError The database cannot be used.
        """
        with self._database.write() as connection:
            delete_all_projects(connection)
            for place, project in enumerate(projects, start=1):
                insert_project(connection, place, project)
            replace_profile(connection, profile)
