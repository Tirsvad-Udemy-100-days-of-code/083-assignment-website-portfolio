"""!
@file data_file_error.py
@brief Error raised when a JSON data file cannot be used.
"""

from pathlib import Path

from portfolio.application.errors.data_source_error import DataSourceError


class DataFileError(DataSourceError):
    """!
    @brief A data file is missing, unreadable or does not hold valid data.
    """

    def __init__(self, path: Path, problem: str) -> None:
        """!
        @brief Create the error; the message names the file and the problem.
        @param path The data file.
        @param problem What is wrong with the file.
        """
        super().__init__(f"{path}: {problem}")
        self.path = path
        self.problem = problem
