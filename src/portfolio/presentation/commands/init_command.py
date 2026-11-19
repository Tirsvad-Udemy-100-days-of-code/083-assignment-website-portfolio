"""!
@file init_command.py
@brief Command `init`: create the database or confirm that it is ready.
"""

from collections.abc import Callable
from pathlib import Path

from portfolio.constants import (
    MESSAGE_DATABASE_CREATED,
    MESSAGE_DATABASE_READY,
    SCHEMA_VERSION,
)
from portfolio.presentation.shared.console import write_info
from portfolio.presentation.shared.guarded import run_guarded

## @brief A function that prepares the database at a path; True when it was created.
DatabaseInitialization = Callable[[Path], bool]


class InitCommand:
    """!
    @brief Runs the initialize_database use case and reports the result.
    """

    def __init__(self, initialize: DatabaseInitialization) -> None:
        """!
        @brief Create the command.
        @param initialize The initialize_database use case, with its adapters given.
        """
        self._initialize = initialize

    def run(self, database: Path) -> int:
        """!
        @brief Create the database or confirm that it is ready.
        @param database The database file.
        @return The exit code: 0 on success and 2 when the database cannot be used,
            for example when its schema is newer than the program.
        """

        def action() -> None:
            created = self._initialize(database)
            message = MESSAGE_DATABASE_CREATED if created else MESSAGE_DATABASE_READY
            write_info(message.format(path=database, version=SCHEMA_VERSION))

        return run_guarded(action)
