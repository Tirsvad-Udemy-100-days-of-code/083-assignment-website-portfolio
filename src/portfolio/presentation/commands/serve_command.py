"""!
@file serve_command.py
@brief Command `serve`: show the site from the database on a local web server.
"""

import logging
from collections.abc import Callable
from pathlib import Path

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.constants import (
    EXIT_DATA_ERROR,
    EXIT_OK,
    EXIT_SERVER_ERROR,
    MESSAGE_DATABASE_UNAVAILABLE,
    MESSAGE_SERVER_FAILED,
)
from portfolio.presentation.shared.console import write_error

## @brief A function that checks that a database can feed the site; it raises a
## DataSourceError when the file is missing, is not a database or holds no profile.
DatabaseCheck = Callable[[Path], None]

## @brief A function that serves the site of a database and a data folder on a host
## and port until it is stopped; its arguments are the database, the data folder,
## the host and the port.
ServerRunner = Callable[[Path, Path, str, int], None]

_logger = logging.getLogger(__name__)


class ServeCommand:
    """!
    @brief Checks the database, starts the server and reports problems.
    """

    def __init__(self, check_database: DatabaseCheck, runner: ServerRunner) -> None:
        """!
        @brief Create the command.
        @param check_database Checks the database before the server starts.
        @param runner Serves the site; `serve_app` with the application in the program.
        """
        self._check_database = check_database
        self._runner = runner

    def run(self, database: Path, data_dir: Path, host: str, port: int) -> int:
        """!
        @brief Serve the site.
        @param database The database file.
        @param data_dir The data folder; its `images` folder holds the images.
        @param host Address to bind to.
        @param port Port to bind to.
        @return The exit code: 0 after a clean stop, 2 when the database is missing
            or cannot be used, and 4 when the server cannot start.
        """
        try:
            self._check_database(database)
        except DataSourceError:
            _logger.debug("The database cannot feed the site", exc_info=True)
            write_error(MESSAGE_DATABASE_UNAVAILABLE.format(path=database))
            return EXIT_DATA_ERROR
        try:
            self._runner(database, data_dir, host, port)
        except (OSError, OverflowError) as err:
            _logger.debug("The server cannot start", exc_info=True)
            write_error(MESSAGE_SERVER_FAILED.format(host=host, port=port, reason=err))
            return EXIT_SERVER_ERROR
        return EXIT_OK
