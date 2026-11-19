"""!
@file duplicate_project_error.py
@brief Error raised when a project title is already taken.
"""

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.constants import MESSAGE_PROJECT_EXISTS


class DuplicateProjectError(DataSourceError):
    """!
    @brief Another project already has the title.
    """

    def __init__(self, title: str) -> None:
        """!
        @brief Create the error.
        @param title The title that is already taken.
        """
        super().__init__(MESSAGE_PROJECT_EXISTS.format(title=title))
        self.title = title
