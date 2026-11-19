"""!
@file invalid_profile_error.py
@brief Error raised when profile data breaks a rule.
"""

from portfolio.domain.errors.domain_error import DomainError


class InvalidProfileError(DomainError):
    """!
    @brief The data of a profile, or of one of its links, is not valid.
    """
