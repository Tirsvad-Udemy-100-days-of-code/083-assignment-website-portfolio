"""!
@file set_profile.py
@brief Use case: create the profile or change some of its fields.
"""

from dataclasses import replace

from portfolio.application.dto.link_item import LinkItem
from portfolio.application.dto.profile_changes import ProfileChanges
from portfolio.application.errors.profile_not_found_error import ProfileNotFoundError
from portfolio.application.ports.profile_repository import ProfileRepository
from portfolio.application.ports.profile_writer import ProfileWriter
from portfolio.application.use_cases.changed_fields import changed_fields
from portfolio.constants import (
    MESSAGE_NEW_PROFILE_INCOMPLETE,
    MESSAGE_NOTHING_TO_CHANGE,
)
from portfolio.domain.entities.profile import Profile
from portfolio.domain.errors.invalid_profile_error import InvalidProfileError
from portfolio.domain.value_objects.link import Link


def set_profile(
    reader: ProfileRepository, writer: ProfileWriter, changes: ProfileChanges
) -> bool:
    """!
    @brief Create the profile, or give new values to the stored one.

    The Profile entity checks the result. A new profile needs a name, a headline,
    a summary and at least one skill.
    @param reader Source of the stored profile.
    @param writer Destination of the profile.
    @param changes The new values; a field that is None keeps its value.
    @return True when the profile was created, False when it was changed.
    @throws InvalidProfileError No value was given, a new profile is incomplete or
        a value breaks a rule.
    @throws DataSourceError The profile cannot be read or stored.
    """
    new_values = changed_fields(changes)
    if not new_values:
        raise InvalidProfileError(MESSAGE_NOTHING_TO_CHANGE)
    try:
        stored = reader.get_profile()
    except ProfileNotFoundError:
        writer.save_profile(_new_profile(changes))
        return True
    if changes.links is not None:
        new_values["links"] = _to_links(changes.links)
    writer.save_profile(replace(stored, **new_values))
    return False


def _new_profile(changes: ProfileChanges) -> Profile:
    if (
        changes.name is None
        or changes.headline is None
        or changes.summary is None
        or not changes.skills
    ):
        raise InvalidProfileError(MESSAGE_NEW_PROFILE_INCOMPLETE)
    return Profile(
        name=changes.name,
        headline=changes.headline,
        summary=changes.summary,
        skills=changes.skills,
        links=_to_links(changes.links or ()),
        photo=changes.photo,
    )


def _to_links(items: tuple[LinkItem, ...]) -> tuple[Link, ...]:
    return tuple(Link(label=item.label, url=item.url) for item in items)
