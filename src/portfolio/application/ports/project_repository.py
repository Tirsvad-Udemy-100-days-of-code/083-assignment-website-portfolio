"""!
@file project_repository.py
@brief Port through which the use cases read projects.
"""

from collections.abc import Sequence
from typing import Protocol

from portfolio.domain.entities.project import Project


class ProjectRepository(Protocol):
    """!
    @brief Source of the projects; the use cases never know where they are kept.
    """

    def list_projects(self) -> Sequence[Project]:
        """!
        @brief Read every project, in the order of the source.
        @return The projects.
        """
        ...
