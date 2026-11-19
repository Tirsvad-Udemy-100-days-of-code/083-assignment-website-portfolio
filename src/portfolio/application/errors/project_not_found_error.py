"""!
@file project_not_found_error.py
@brief Error raised when no stored project has a given title.
"""

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.constants import MESSAGE_PROJECT_NOT_FOUND


class ProjectNotFoundError(DataSourceError):
    """!
    @brief The project to change or remove is not stored.
    """

    def __init__(self, title: str) -> None:
        """!
        @brief Create the error.
        @param title The title that no project has.
        """
        super().__init__(MESSAGE_PROJECT_NOT_FOUND.format(title=title))
        self.title = title
