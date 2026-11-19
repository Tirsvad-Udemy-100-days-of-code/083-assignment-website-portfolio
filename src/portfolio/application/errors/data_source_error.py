"""!
@file data_source_error.py
@brief Error raised when a source of data cannot be read.
"""


class DataSourceError(Exception):
    """!
    @brief A repository could not read its data: missing, unreadable or invalid.
    """
