"""!
@file profile_not_found_error.py
@brief Error raised when the database holds no profile.
"""

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.constants import MESSAGE_PROFILE_MISSING


class ProfileNotFoundError(DataSourceError):
    """!
    @brief The profile has not been created yet.
    """

    def __init__(self) -> None:
        """!
        @brief Create the error.
        """
        super().__init__(MESSAGE_PROFILE_MISSING)
