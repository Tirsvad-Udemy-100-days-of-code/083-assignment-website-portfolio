"""!
@file invalid_project_error.py
@brief Error raised when project data breaks a rule.
"""

from portfolio.domain.errors.domain_error import DomainError


class InvalidProjectError(DomainError):
    """!
    @brief The data of a project is not valid.
    """
