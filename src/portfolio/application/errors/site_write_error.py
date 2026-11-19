"""!
@file site_write_error.py
@brief Error raised when a page of the site cannot be written.
"""


class SiteWriteError(Exception):
    """!
    @brief A site writer refused or failed to write a file.
    """
