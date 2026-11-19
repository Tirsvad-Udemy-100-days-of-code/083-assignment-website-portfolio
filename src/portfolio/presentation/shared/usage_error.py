"""!
@file usage_error.py
@brief Error raised when a command line value cannot be understood.
"""


class UsageError(Exception):
    """!
    @brief A value on the command line has the wrong form.
    """
