"""!
@file import_command.py
@brief Command `import`: copy the JSON data files into the database.
"""

from collections.abc import Callable
from pathlib import Path

from portfolio.constants import MESSAGE_IMPORTED
from portfolio.presentation.shared.console import write_info
from portfolio.presentation.shared.guarded import run_guarded

## @brief A function that imports a data folder into a database and returns the
## number of imported projects; its arguments are the database, the data folder
## and whether existing data may be replaced.
PortfolioImport = Callable[[Path, Path, bool], int]


class ImportCommand:
    """!
    @brief Runs the import_portfolio use case and reports the result.
    """

    def __init__(self, import_data: PortfolioImport) -> None:
        """!
        @brief Create the command.
        @param import_data The import_portfolio use case, with its adapters given.
        """
        self._import_data = import_data

    def run(self, database: Path, data_dir: Path, replace: bool) -> int:
        """!
        @brief Import the data files.
        @param database The database file.
        @param data_dir Folder with the JSON data files.
        @param replace True to overwrite data that the database already holds.
        @return The exit code: 0 on success and 2 when the data or the database
            cannot be used, or the database holds data and `replace` is False.
        """

        def action() -> None:
            count = self._import_data(database, data_dir, replace)
            write_info(MESSAGE_IMPORTED.format(count=count, path=database))

        return run_guarded(action)
