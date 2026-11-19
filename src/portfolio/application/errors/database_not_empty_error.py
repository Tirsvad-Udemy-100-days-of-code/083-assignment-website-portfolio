"""!
@file database_not_empty_error.py
@brief Error raised when an import would overwrite stored data.
"""

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.constants import MESSAGE_DATABASE_NOT_EMPTY


class DatabaseNotEmptyError(DataSourceError):
    """!
    @brief The database already holds data and the import was not told to replace it.
    """

    def __init__(self) -> None:
        """!
        @brief Create the error.
        """
        super().__init__(MESSAGE_DATABASE_NOT_EMPTY)
