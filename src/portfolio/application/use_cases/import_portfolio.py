"""!
@file import_portfolio.py
@brief Use case: store the projects and the profile of one source in the storage.
"""

from collections.abc import Sequence

from portfolio.application.errors.database_not_empty_error import (
    DatabaseNotEmptyError,
)
from portfolio.application.errors.duplicate_project_error import DuplicateProjectError
from portfolio.application.ports.portfolio_import_target import PortfolioImportTarget
from portfolio.domain.entities.profile import Profile
from portfolio.domain.entities.project import Project


def import_portfolio(
    projects: Sequence[Project],
    profile: Profile,
    target: PortfolioImportTarget,
    replace: bool,
) -> int:
    """!
    @brief Store the whole source in one all-or-nothing step.

    The caller has read the source completely, so nothing is written when the source
    cannot be read; nothing is written either when it holds a title twice.
    @param projects The projects of the source, in order.
    @param profile The profile of the source.
    @param target Destination of the data.
    @param replace True to overwrite data that the target already holds.
    @return The number of imported projects.
    @throws DataSourceError The target cannot be used.
    @throws DuplicateProjectError Two projects of the source have the same title.
    @throws DatabaseNotEmptyError The target holds data and `replace` is False.
    """
    imported = tuple(projects)
    _require_unique_titles(imported)
    if not replace and not target.is_empty():
        raise DatabaseNotEmptyError
    target.replace_all(imported, profile)
    return len(imported)


def _require_unique_titles(projects: Sequence[Project]) -> None:
    titles: set[str] = set()
    for project in projects:
        if project.title in titles:
            raise DuplicateProjectError(project.title)
        titles.add(project.title)
