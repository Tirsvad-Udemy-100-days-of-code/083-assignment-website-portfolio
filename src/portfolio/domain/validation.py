"""!
@file validation.py
@brief Text rules shared by the entities and value objects of the domain.
"""

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
