"""!
@file validation.py
@brief Text rules shared by the entities and value objects of the domain.
"""

from urllib.parse import urlsplit

from portfolio.constants import IMAGE_EXTENSIONS, SAFE_URL_SCHEMES
from portfolio.domain.errors.domain_error import DomainError


def require_non_blank(value: str, field: str, error_type: type[DomainError]) -> None:
    """!
    @brief Check that a text holds something other than white space.
    @param value The text to check.
    @param field The name of the field, used in the error message.
    @param error_type The error to raise when the rule is broken.
    @throws DomainError The given error type, when the text is blank.
    """
    if not value.strip():
        raise error_type(f"{field} must not be blank")


def require_max_length(
    value: str, field: str, max_length: int, error_type: type[DomainError]
) -> None:
    """!
    @brief Check that a text is not longer than a limit.
    @param value The text to check.
    @param field The name of the field, used in the error message.
    @param max_length The longest accepted length, in characters.
    @param error_type The error to raise when the rule is broken.
    @throws DomainError The given error type, when the text is too long.
    """
    if len(value) > max_length:
        raise error_type(f"{field} must be at most {max_length} characters")


def require_text_list(
    values: tuple[str, ...],
    field: str,
    max_items: int,
    max_length: int,
    error_type: type[DomainError],
) -> None:
    """!
    @brief Check a list of short texts: not too many, none blank, none too long.
    @param values The texts to check.
    @param field The singular name of an item, used in the error message.
    @param max_items The largest accepted number of items.
    @param max_length The longest accepted item, in characters.
    @param error_type The error to raise when a rule is broken.
    @throws DomainError The given error type, when a rule is broken.
    """
    if len(values) > max_items:
        raise error_type(f"{field}s must hold at most {max_items} entries")
    for value in values:
        require_non_blank(value, field, error_type)
        require_max_length(value, field, max_length, error_type)


def is_remote_url(value: str) -> bool:
    """!
    @brief Tell whether a text is an http or https address.
    @param value The text to check.
    @return True for an address with a safe scheme and a host, without space.
    """
    if not value.isprintable() or " " in value or "\\" in value:
        return False
    try:
        parts = urlsplit(value)
    except ValueError:
        return False
    return parts.scheme.lower() in SAFE_URL_SCHEMES and bool(parts.netloc)


def is_local_image_path(value: str) -> bool:
    """!
    @brief Tell whether a text is a relative path to an image file in the data folder.

    The path has no scheme, no host, no query, no fragment, no drive, no `..`, no
    surrounding space and ends with a known image extension.
    @param value The text to check.
    @return True when the path can be read from the data folder and copied.
    """
    if not value or value != value.strip() or not value.isprintable():
        return False
    if any(mark in value for mark in ("\\", "?", "#", ":")):
        return False
    segments = value.split("/")
    if ".." in segments or "" in segments:
        return False
    return value.lower().endswith(IMAGE_EXTENSIONS)
