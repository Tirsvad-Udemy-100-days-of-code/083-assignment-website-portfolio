"""!
@file import_portfolio.py
@brief Use case: copy the projects and the profile of one source into the storage.
"""

from collections.abc import Sequence

from portfolio.application.errors.database_not_empty_error import (
    DatabaseNotEmptyError,
)
from portfolio.application.errors.duplicate_project_error import DuplicateProjectError
from portfolio.application.ports.portfolio_import_target import PortfolioImportTarget
from portfolio.application.ports.profile_repository import ProfileRepository
from portfolio.application.ports.project_repository import ProjectRepository
from portfolio.domain.entities.project import Project


def import_portfolio(
    projects: ProjectRepository,
    profile: ProfileRepository,
    target: PortfolioImportTarget,
    replace: bool,
) -> int:
    """!
    @brief Read the whole source first, then store it in one all-or-nothing step.

    Nothing is written when the source cannot be read or holds a title twice.
    @param projects Source of the projects.
    @param profile Source of the profile.
    @param target Destination of the data.
    @param replace True to overwrite data that the target already holds.
    @return The number of imported projects.
    @throws DataSourceError The source cannot be read or the target cannot be used.
    @throws DuplicateProjectError Two projects of the source have the same title.
    @throws DatabaseNotEmptyError The target holds data and `replace` is False.
    """
    imported = tuple(projects.list_projects())
    imported_profile = profile.get_profile()
    _require_unique_titles(imported)
    if not replace and not target.is_empty():
        raise DatabaseNotEmptyError
    target.replace_all(imported, imported_profile)
    return len(imported)


def _require_unique_titles(projects: Sequence[Project]) -> None:
    titles: set[str] = set()
    for project in projects:
        if project.title in titles:
            raise DuplicateProjectError(project.title)
        titles.add(project.title)
