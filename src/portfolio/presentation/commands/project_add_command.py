"""!
@file project_add_command.py
@brief Command `project add`: store a new project.
"""

from collections.abc import Callable
from pathlib import Path

from portfolio.application.dto.project_input import ProjectInput
from portfolio.constants import MESSAGE_PROJECT_ADDED
from portfolio.presentation.shared.console import write_info
from portfolio.presentation.shared.guarded import run_guarded

## @brief A function that adds a project to a database.
ProjectAdder = Callable[[Path, ProjectInput], None]


class ProjectAddCommand:
    """!
    @brief Runs the add_project use case and reports the result.
    """

    def __init__(self, add_project: ProjectAdder) -> None:
        """!
        @brief Create the command.
        @param add_project The add_project use case, with its adapters given.
        """
        self._add_project = add_project

    def run(self, database: Path, data: ProjectInput) -> int:
        """!
        @brief Add the project.
        @param database The database file.
        @param data The values of the project.
        @return The exit code: 0 on success and 2 when a value is invalid, the
            title is taken or the database cannot be used.
        """

        def action() -> None:
            self._add_project(database, data)
            write_info(MESSAGE_PROJECT_ADDED.format(title=data.title))

        return run_guarded(action)
