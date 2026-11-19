"""!
@file profile_writer.py
@brief Port through which the use cases store the profile.
"""

from typing import Protocol

from portfolio.domain.entities.profile import Profile


class ProfileWriter(Protocol):
    """!
    @brief Destination of the profile; a save is one all-or-nothing change.
    """

    def save_profile(self, profile: Profile) -> None:
        """!
        @brief Store the profile, replacing the one that is stored.
        @param profile The profile to keep.
        """
        ...
