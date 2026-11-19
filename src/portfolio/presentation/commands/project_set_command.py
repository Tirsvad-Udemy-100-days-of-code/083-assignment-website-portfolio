"""!
@file project_set_command.py
@brief Command `project set`: change some fields of a stored project.
"""

from collections.abc import Callable
from pathlib import Path

from portfolio.application.dto.project_changes import ProjectChanges
from portfolio.constants import MESSAGE_PROJECT_CHANGED
from portfolio.presentation.shared.console import write_info
from portfolio.presentation.shared.guarded import run_guarded

## @brief A function that changes a project of a database and returns its new title.
ProjectChanger = Callable[[Path, str, ProjectChanges], str]


class ProjectSetCommand:
    """!
    @brief Runs the change_project use case and reports the result.
    """

    def __init__(self, change_project: ProjectChanger) -> None:
        """!
        @brief Create the command.
        @param change_project The change_project use case, with its adapters given.
        """
        self._change_project = change_project

    def run(self, database: Path, title: str, changes: ProjectChanges) -> int:
        """!
        @brief Change the project.
        @param database The database file.
        @param title The title of the stored project.
        @param changes The new values.
        @return The exit code: 0 on success and 2 when no value is given, a value
            is invalid, the project is missing or the database cannot be used.
        """

        def action() -> None:
            new_title = self._change_project(database, title, changes)
            write_info(MESSAGE_PROJECT_CHANGED.format(title=new_title))

        return run_guarded(action)
