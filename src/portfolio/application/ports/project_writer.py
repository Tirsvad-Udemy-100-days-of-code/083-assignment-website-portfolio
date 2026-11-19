"""!
@file project_writer.py
@brief Port through which the use cases add, replace and remove projects.
"""

from typing import Protocol

from portfolio.domain.entities.project import Project


class ProjectWriter(Protocol):
    """!
    @brief Destination of project changes; each call is one all-or-nothing change.
    """

    def add_project(self, project: Project) -> None:
        """!
        @brief Store a new project after the last one.
        @param project The project to add.
        @throws DuplicateProjectError Another project has the title.
        """
        ...

    def replace_project(self, title: str, project: Project) -> None:
        """!
        @brief Replace the project with a title, keeping its place in the order.
        @param title The title of the stored project.
        @param project The new values; its title may differ from `title`.
        @throws ProjectNotFoundError No project has the title.
        @throws DuplicateProjectError The new title belongs to another project.
        """
        ...

    def remove_project(self, title: str) -> None:
        """!
        @brief Remove the project with a title.
        @param title The title of the stored project.
        @throws ProjectNotFoundError No project has the title.
        """
        ...
