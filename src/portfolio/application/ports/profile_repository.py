"""!
@file profile_repository.py
@brief Port through which the use cases read the profile.
"""

from typing import Protocol

from portfolio.domain.entities.profile import Profile


class ProfileRepository(Protocol):
    """!
    @brief Source of the profile; the use cases never know where it is kept.
    """

    def get_profile(self) -> Profile:
        """!
        @brief Read the profile of the owner of the portfolio.
        @return The profile.
        """
        ...
