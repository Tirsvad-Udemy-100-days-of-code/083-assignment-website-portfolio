"""!
@file portfolio_import_target.py
@brief Port through which the use cases load a whole portfolio into the storage.
"""

from collections.abc import Sequence
from typing import Protocol

from portfolio.domain.entities.profile import Profile
from portfolio.domain.entities.project import Project


class PortfolioImportTarget(Protocol):
    """!
    @brief Destination of an import of the projects and the profile.
    """

    def is_empty(self) -> bool:
        """!
        @brief Tell whether the storage holds no project and no profile.
        @return True when it holds nothing.
        """
        ...

    def replace_all(self, projects: Sequence[Project], profile: Profile) -> None:
        """!
        @brief Replace everything stored by the given data, all or nothing.
        @param projects The projects, in the order to show them.
        @param profile The profile.
        """
        ...
