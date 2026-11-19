"""!
@file project_list_command.py
@brief Command `project list`: show the stored projects.
"""

from collections.abc import Callable
from pathlib import Path

from portfolio.application.dto.project_card import ProjectCard
from portfolio.constants import MESSAGE_NO_PROJECTS, MESSAGE_PROJECT_LINE
from portfolio.presentation.shared.console import write_info
from portfolio.presentation.shared.guarded import run_guarded

## @brief A function that reads the projects of a database.
ProjectLister = Callable[[Path], tuple[ProjectCard, ...]]


class ProjectListCommand:
    """!
    @brief Runs the list_projects use case and prints one line per project.
    """

    def __init__(self, list_projects: ProjectLister) -> None:
        """!
        @brief Create the command.
        @param list_projects The list_projects use case, with its adapters given.
        """
        self._list_projects = list_projects

    def run(self, database: Path) -> int:
        """!
        @brief Print the projects.
        @param database The database file.
        @return The exit code: 0 on success and 2 when the database cannot be used.
        """

        def action() -> None:
            projects = self._list_projects(database)
            if not projects:
                write_info(MESSAGE_NO_PROJECTS)
            for project in projects:
                write_info(
                    MESSAGE_PROJECT_LINE.format(
                        title=project.title,
                        kind=project.kind,
                        source_code_url=project.source_code_url,
                    )
                )

        return run_guarded(action)
