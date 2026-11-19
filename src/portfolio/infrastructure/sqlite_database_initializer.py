"""!
@file sqlite_database_initializer.py
@brief DatabaseInitializer that creates the SQLite schema.
"""

from portfolio.infrastructure.sqlite_database import SqliteDatabase
from portfolio.infrastructure.sqlite_schema import initialize_schema


class SqliteDatabaseInitializer:
    """!
    @brief Implements the DatabaseInitializer port with SQLite.
    """

    def __init__(self, database: SqliteDatabase) -> None:
        """!
        @brief Create the initializer.
        @param database The database to prepare.
        """
        self._database = database

    def initialize(self) -> bool:
        """!
        @brief Create the file and the schema when they are missing.
        @return True when the schema was created, False when it was already current.
        @throws SchemaVersionError The schema is newer than this program knows.
        @throws DatabaseError The file is not a SQLite database or cannot be used.
        """
        with self._database.create() as connection:
            return initialize_schema(connection)
