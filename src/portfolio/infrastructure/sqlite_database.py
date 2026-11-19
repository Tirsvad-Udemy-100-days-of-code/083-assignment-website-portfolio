"""!
@file sqlite_database.py
@brief Opens and closes the connections to the SQLite database.
"""

import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from pathlib import Path

from portfolio.constants import (
    IN_MEMORY_DATABASE,
    MESSAGE_DATABASE_NOT_FOUND,
    MESSAGE_DATABASE_READ_ONLY,
    SQLITE_READ_ONLY_QUERY,
)
from portfolio.infrastructure.errors.database_error import DatabaseError
from portfolio.infrastructure.sqlite_schema import require_current_schema

_FOREIGN_KEYS_ON = "PRAGMA foreign_keys = ON"
_BEGIN_READ = "BEGIN"
_BEGIN_WRITE = "BEGIN IMMEDIATE"


class SqliteDatabase:
    """!
    @brief A SQLite database file; every operation opens a connection and closes it.

    A read or a write runs in one transaction: a write is committed when it ends
    and rolled back when it fails. The location `:memory:` keeps one connection
    open for the life of the object, because every new connection to it would be
    a new, empty database; call `close` when the object is no longer needed.

    A read-only database opens its file with the SQLite option `mode=ro`, so the
    engine itself refuses every change and the file is never created.
    """

    def __init__(self, location: Path | str, read_only: bool = False) -> None:
        """!
        @brief Create the object; nothing is opened yet.
        @param location The database file, or `:memory:`.
        @param read_only True to open the file read-only; `write` and `create` then
            fail with a DatabaseError.
        @throws ValueError The database is `:memory:`, which cannot be read-only.
        """
        if read_only and str(location) == IN_MEMORY_DATABASE:
            raise ValueError("an in-memory database cannot be read-only")
        self._location = str(location)
        self._read_only = read_only
        self._shared: sqlite3.Connection | None = None

    def close(self) -> None:
        """!
        @brief Close the connection that an in-memory database keeps.
        """
        if self._shared is not None:
            self._shared.close()
            self._shared = None

    @contextmanager
    def read(self) -> Iterator[sqlite3.Connection]:
        """!
        @brief Open the existing database for reading, in one transaction.
        @return A context manager that gives the connection.
        @throws SchemaVersionError The schema is missing, newer or unknown.
        @throws DatabaseError The file is missing or cannot be used.
        """
        with self._transaction(_BEGIN_READ, create=False) as connection:
            require_current_schema(connection)
            yield connection

    @contextmanager
    def write(self) -> Iterator[sqlite3.Connection]:
        """!
        @brief Open the existing database for writing, in one transaction.

        The changes are committed when the block ends and rolled back when it
        raises.
        @return A context manager that gives the connection.
        @throws SchemaVersionError The schema is missing, newer or unknown.
        @throws DatabaseError The file is missing or cannot be used.
        """
        with self._transaction(_BEGIN_WRITE, create=False) as connection:
            require_current_schema(connection)
            yield connection

    @contextmanager
    def create(self) -> Iterator[sqlite3.Connection]:
        """!
        @brief Open the database for writing and create its file when it is missing.

        The schema is not checked; the caller prepares it. The changes are
        committed when the block ends and rolled back when it raises.
        @return A context manager that gives the connection.
        @throws DatabaseError The file cannot be created or used.
        """
        with self._transaction(_BEGIN_WRITE, create=True) as connection:
            yield connection

    @contextmanager
    def _transaction(self, begin: str, create: bool) -> Iterator[sqlite3.Connection]:
        with self._connection(create) as connection, connection:
            connection.execute(begin)
            yield connection

    @contextmanager
    def _connection(self, create: bool) -> Iterator[sqlite3.Connection]:
        """Give a connection and turn a SQLite or file error into a DatabaseError."""
        try:
            if self._read_only and create:
                raise DatabaseError(self._location, MESSAGE_DATABASE_READ_ONLY)
            if self._location == IN_MEMORY_DATABASE:
                yield self._shared_connection()
            else:
                path = Path(self._location)
                if create:
                    path.parent.mkdir(parents=True, exist_ok=True)
                elif not path.is_file():
                    raise DatabaseError(self._location, MESSAGE_DATABASE_NOT_FOUND)
                with closing(self._new_connection()) as connection:
                    yield connection
        except (sqlite3.Error, OSError) as err:
            raise DatabaseError(self._location, str(err)) from err

    def _shared_connection(self) -> sqlite3.Connection:
        if self._shared is None:
            self._shared = self._new_connection()
        return self._shared

    def _new_connection(self) -> sqlite3.Connection:
        if self._read_only:
            # A URI, so that SQLite takes the option; as_uri quotes `?` and `#`.
            uri = Path(self._location).resolve().as_uri() + SQLITE_READ_ONLY_QUERY
            connection = sqlite3.connect(uri, uri=True)
        else:
            connection = sqlite3.connect(self._location)
        try:
            connection.execute(_FOREIGN_KEYS_ON)
        except sqlite3.Error:
            connection.close()
            raise
        return connection
