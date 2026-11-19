"""!
@file project_remove_command.py
@brief Command `project remove`: delete a stored project.
"""

from collections.abc import Callable
from pathlib import Path

from portfolio.constants import MESSAGE_PROJECT_REMOVED
from portfolio.presentation.shared.console import write_info
from portfolio.presentation.shared.guarded import run_guarded

## @brief A function that removes the project with a title from a database.
ProjectRemover = Callable[[Path, str], None]


class ProjectRemoveCommand:
    """!
    @brief Runs the remove_project use case and reports the result.
    """

    def __init__(self, remove_project: ProjectRemover) -> None:
        """!
        @brief Create the command.
        @param remove_project The remove_project use case, with its adapters given.
        """
        self._remove_project = remove_project

    def run(self, database: Path, title: str) -> int:
        """!
        @brief Remove the project.
        @param database The database file.
        @param title The title of the stored project.
        @return The exit code: 0 on success and 2 when the project is missing or
            the database cannot be used.
        """

        def action() -> None:
            self._remove_project(database, title)
            write_info(MESSAGE_PROJECT_REMOVED.format(title=title))

        return run_guarded(action)
