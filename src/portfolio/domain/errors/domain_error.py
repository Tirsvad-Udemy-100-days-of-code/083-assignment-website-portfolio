"""!
@file domain_error.py
@brief Base class of every error the business rules raise.
"""


class DomainError(Exception):
    """!
    @brief A business rule was broken.
    """
