"""!
@file json_document.py
@brief Read a JSON data file and check its shape, with errors that name the file.
"""

import json
from collections.abc import Mapping, Sequence
from pathlib import Path

from portfolio.constants import ENCODING
from portfolio.infrastructure.errors.data_file_error import DataFileError


def read_json_document(path: Path) -> object:
    """!
    @brief Read and parse a JSON file.
    @param path The file to read.
    @return The parsed document.
    @throws DataFileError The file is missing, unreadable or not valid JSON.
    """
    try:
        with path.open(encoding=ENCODING) as handle:
            document: object = json.load(handle)
    except FileNotFoundError as err:
        raise DataFileError(path, "file not found") from err
    except json.JSONDecodeError as err:
        problem = f"invalid JSON at line {err.lineno}, column {err.colno}: {err.msg}"
        raise DataFileError(path, problem) from err
    except (OSError, UnicodeDecodeError) as err:
        raise DataFileError(path, f"cannot read the file: {err}") from err
    return document


def require_object(value: object, path: Path, what: str) -> Mapping[str, object]:
    """!
    @brief Check that a value is a JSON object.
    @param value The value to check.
    @param path The data file, for the error message.
    @param what Name of the value, for the error message.
    @return The object.
    @throws DataFileError The value is not an object.
    """
    if not isinstance(value, dict):
        raise DataFileError(path, f"{what} must be a JSON object")
    return value


def require_array(value: object, path: Path, what: str) -> Sequence[object]:
    """!
    @brief Check that a value is a JSON array.
    @param value The value to check.
    @param path The data file, for the error message.
    @param what Name of the value, for the error message.
    @return The array.
    @throws DataFileError The value is not an array.
    """
    if not isinstance(value, list):
        raise DataFileError(path, f"{what} must be a JSON array")
    return value


def require_field(
    mapping: Mapping[str, object], key: str, path: Path, what: str
) -> object:
    """!
    @brief Take a value from an object and fail when the key is missing.
    @param mapping The object.
    @param key The key to take.
    @param path The data file, for the error message.
    @param what Name of the object, for the error message.
    @return The value of the key.
    @throws DataFileError The key is missing.
    """
    if key not in mapping:
        raise DataFileError(path, f"{what} is missing the key '{key}'")
    return mapping[key]


def require_text(value: object, path: Path, what: str) -> str:
    """!
    @brief Check that a value is text.
    @param value The value to check.
    @param path The data file, for the error message.
    @param what Name of the value, for the error message.
    @return The text.
    @throws DataFileError The value is not text.
    """
    if not isinstance(value, str):
        raise DataFileError(path, f"{what} must be text")
    return value


def require_text_field(
    mapping: Mapping[str, object], key: str, path: Path, what: str
) -> str:
    """!
    @brief Take a text value from an object and fail when it is missing or not text.
    @param mapping The object.
    @param key The key to take.
    @param path The data file, for the error message.
    @param what Name of the object, for the error message.
    @return The text.
    @throws DataFileError The key is missing or its value is not text.
    """
    value = require_field(mapping, key, path, what)
    return require_text(value, path, f"{what}: '{key}'")
