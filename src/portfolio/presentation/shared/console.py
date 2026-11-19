"""!
@file console.py
@brief Messages to the user on the standard streams.
"""

import sys

from portfolio.constants import MESSAGE_ERROR


def write_info(message: str) -> None:
    """!
    @brief Write a message to the standard output.
    @param message The text, with its line end.
    """
    sys.stdout.write(message)


def write_error(message: str) -> None:
    """!
    @brief Write one error line to the standard error.
    @param message The problem, without prefix and line end.
    """
    sys.stderr.write(MESSAGE_ERROR.format(message=message))
