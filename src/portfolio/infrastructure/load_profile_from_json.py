"""!
@file load_profile_from_json.py
@brief Read the profile from a JSON file.
"""

from collections.abc import Mapping
from pathlib import Path

from portfolio.constants import (
    JSON_KEY_HEADLINE,
    JSON_KEY_LABEL,
    JSON_KEY_LINKS,
    JSON_KEY_NAME,
    JSON_KEY_PHOTO,
    JSON_KEY_SKILLS,
    JSON_KEY_SUMMARY,
    JSON_KEY_URL,
)
from portfolio.domain.entities.profile import Profile
from portfolio.domain.errors.domain_error import DomainError
from portfolio.domain.value_objects.link import Link
from portfolio.infrastructure.errors.data_file_error import DataFileError
from portfolio.infrastructure.json_document import (
    read_json_document,
    require_array,
    require_field,
    require_object,
    require_text,
    require_text_field,
    require_text_list,
)

_PROFILE = "the profile"


def load_profile_from_json(path: Path) -> Profile:
    """!
    @brief Read the profile from a JSON file.

    The file holds an object with the keys `name`, `headline`, `summary`, `skills`
    and `links`, and the optional key `photo`.
    @param path The JSON file.
    @return The profile.
    @throws DataFileError The file is missing, unreadable, not valid JSON, has the
        wrong shape, lacks a key or holds a value a profile does not accept.
    """
    fields = require_object(read_json_document(path), path, _PROFILE)
    try:
        return Profile(
            name=require_text_field(fields, JSON_KEY_NAME, path, _PROFILE),
            headline=require_text_field(fields, JSON_KEY_HEADLINE, path, _PROFILE),
            summary=require_text_field(fields, JSON_KEY_SUMMARY, path, _PROFILE),
            skills=_skills(fields, path),
            links=_links(fields, path),
            photo=_photo(fields, path),
        )
    except DomainError as err:
        raise DataFileError(path, str(err)) from err


def _skills(fields: Mapping[str, object], path: Path) -> tuple[str, ...]:
    value = require_field(fields, JSON_KEY_SKILLS, path, _PROFILE)
    return require_text_list(value, path, f"'{JSON_KEY_SKILLS}'", "skill")


def _photo(fields: Mapping[str, object], path: Path) -> str | None:
    value = fields.get(JSON_KEY_PHOTO)
    if value is None:
        return None
    return require_text(value, path, f"'{JSON_KEY_PHOTO}'").strip()


def _links(fields: Mapping[str, object], path: Path) -> tuple[Link, ...]:
    value = require_field(fields, JSON_KEY_LINKS, path, _PROFILE)
    values = require_array(value, path, f"'{JSON_KEY_LINKS}'")
    return tuple(
        _link(entry, path, f"link {number}")
        for number, entry in enumerate(values, start=1)
    )


def _link(value: object, path: Path, what: str) -> Link:
    fields = require_object(value, path, what)
    return Link(
        label=require_text_field(fields, JSON_KEY_LABEL, path, what),
        url=require_text_field(fields, JSON_KEY_URL, path, what),
    )
