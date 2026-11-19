"""!
@file profile_set_command.py
@brief Command `profile set`: create the profile or change some of its fields.
"""

from collections.abc import Callable, Sequence
from dataclasses import replace
from pathlib import Path

from portfolio.application.dto.profile_changes import ProfileChanges
from portfolio.constants import MESSAGE_PROFILE_CHANGED, MESSAGE_PROFILE_CREATED
from portfolio.presentation.shared.console import write_info
from portfolio.presentation.shared.guarded import run_guarded
from portfolio.presentation.shared.link_option import parse_link

## @brief A function that sets the profile of a database; True when it was created.
ProfileSetter = Callable[[Path, ProfileChanges], bool]


class ProfileSetCommand:
    """!
    @brief Runs the set_profile use case and reports the result.
    """

    def __init__(self, set_profile: ProfileSetter) -> None:
        """!
        @brief Create the command.
        @param set_profile The set_profile use case, with its adapters given.
        """
        self._set_profile = set_profile

    def run(
        self,
        database: Path,
        changes: ProfileChanges,
        links: Sequence[str] | None,
    ) -> int:
        """!
        @brief Create or change the profile.
        @param database The database file.
        @param changes The new values, without the links.
        @param links The new links as `LABEL=URL`, or None to keep the stored ones.
        @return The exit code: 0 on success and 2 when no value is given, a value
            is invalid, a new profile is incomplete or the database cannot be used.
        """

        def action() -> None:
            parsed = (
                None if links is None else tuple(parse_link(text) for text in links)
            )
            created = self._set_profile(database, replace(changes, links=parsed))
            write_info(MESSAGE_PROFILE_CREATED if created else MESSAGE_PROFILE_CHANGED)

        return run_guarded(action)
