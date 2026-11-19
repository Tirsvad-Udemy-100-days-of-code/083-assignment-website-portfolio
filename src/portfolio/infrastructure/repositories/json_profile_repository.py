"""!
@file json_profile_repository.py
@brief ProfileRepository that reads a JSON file.
"""

from collections.abc import Mapping, Sequence
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


class JsonProfileRepository:
    """!
    @brief Implements the ProfileRepository port with a JSON file.
    """

    def __init__(self, path: Path) -> None:
        """!
        @brief Create the repository.
        @param path The JSON file with the profile.
        """
        self._path = path

    def get_profile(self) -> Profile:
        """!
        @brief Read the profile.
        @return The profile.
        @throws DataFileError The file cannot be used.
        """
        fields = require_object(read_json_document(self._path), self._path, _PROFILE)
        try:
            return Profile(
                name=self._text(fields, JSON_KEY_NAME),
                headline=self._text(fields, JSON_KEY_HEADLINE),
                summary=self._text(fields, JSON_KEY_SUMMARY),
                skills=self._skills(fields),
                links=self._links(fields),
                photo=self._photo(fields),
            )
        except DomainError as err:
            raise DataFileError(self._path, str(err)) from err

    def _text(self, fields: Mapping[str, object], key: str) -> str:
        return require_text_field(fields, key, self._path, _PROFILE)

    def _skills(self, fields: Mapping[str, object]) -> tuple[str, ...]:
        value = require_field(fields, JSON_KEY_SKILLS, self._path, _PROFILE)
        return require_text_list(value, self._path, f"'{JSON_KEY_SKILLS}'", "skill")

    def _photo(self, fields: Mapping[str, object]) -> str | None:
        value = fields.get(JSON_KEY_PHOTO)
        if value is None:
            return None
        return require_text(value, self._path, f"'{JSON_KEY_PHOTO}'").strip()

    def _links(self, fields: Mapping[str, object]) -> tuple[Link, ...]:
        values = self._array(fields, JSON_KEY_LINKS)
        return tuple(
            self._link(value, f"link {number}")
            for number, value in enumerate(values, start=1)
        )

    def _link(self, value: object, what: str) -> Link:
        fields = require_object(value, self._path, what)
        return Link(
            label=require_text_field(fields, JSON_KEY_LABEL, self._path, what),
            url=require_text_field(fields, JSON_KEY_URL, self._path, what),
        )

    def _array(self, fields: Mapping[str, object], key: str) -> Sequence[object]:
        value = require_field(fields, key, self._path, _PROFILE)
        return require_array(value, self._path, f"'{key}'")
