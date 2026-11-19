"""!
@file schema_version_error.py
@brief Error raised when the schema of the database is not the one the program uses.
"""

from portfolio.application.errors.data_source_error import DataSourceError


class SchemaVersionError(DataSourceError):
    """!
    @brief The database has no schema, or a schema version this program cannot use.
    """
