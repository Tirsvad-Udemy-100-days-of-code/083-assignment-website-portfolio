"""!
@file database_error.py
@brief Error raised when the SQLite database cannot be used.
"""

from portfolio.application.errors.data_source_error import DataSourceError


class DatabaseError(DataSourceError):
    """!
    @brief The database file is missing, unreadable, locked or not a SQLite database.
    """

    def __init__(self, location: str, problem: str) -> None:
        """!
        @brief Create the error; the message names the database and the problem.
        @param location The path of the database file.
        @param problem What is wrong with the database.
        """
        super().__init__(f"{location}: {problem}")
        self.location = location
        self.problem = problem
