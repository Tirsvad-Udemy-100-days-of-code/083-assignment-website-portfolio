"""!
@file load_from_json.py
@brief Read the projects from a JSON file.
"""

from pathlib import Path

from portfolio.constants import (
    JSON_KEY_DESCRIPTION,
    JSON_KEY_IMAGE_URL,
    JSON_KEY_KIND,
    JSON_KEY_SOURCE_CODE_URL,
    JSON_KEY_TITLE,
)
from portfolio.domain.entities.project import Project
from portfolio.domain.errors.domain_error import DomainError
from portfolio.infrastructure.errors.data_file_error import DataFileError
from portfolio.infrastructure.json_document import (
    read_json_document,
    require_array,
    require_object,
    require_text_field,
)


def load_from_json(path: Path) -> tuple[Project, ...]:
    """!
    @brief Read the projects from a JSON file.

    The file holds a list of objects with the keys `title`, `type`,
    `description`, `img_url` and `source_code_url`.
    @param path The JSON file.
    @return The projects, in the order of the file.
    @throws DataFileError The file is missing, unreadable, not valid JSON, has the
        wrong shape, lacks a key or holds a value a project does not accept.
    """
    entries = require_array(read_json_document(path), path, "the document")
    return tuple(
        _to_project(entry, path, f"project {number}")
        for number, entry in enumerate(entries, start=1)
    )


def _to_project(entry: object, path: Path, what: str) -> Project:
    fields = require_object(entry, path, what)
    try:
        return Project(
            title=require_text_field(fields, JSON_KEY_TITLE, path, what),
            kind=require_text_field(fields, JSON_KEY_KIND, path, what),
            description=require_text_field(fields, JSON_KEY_DESCRIPTION, path, what),
            image_url=require_text_field(fields, JSON_KEY_IMAGE_URL, path, what),
            source_code_url=require_text_field(
                fields, JSON_KEY_SOURCE_CODE_URL, path, what
            ),
        )
    except DomainError as err:
        raise DataFileError(path, f"{what}: {err}") from err
