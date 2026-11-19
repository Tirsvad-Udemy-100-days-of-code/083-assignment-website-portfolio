"""!
@file sqlite_schema.py
@brief The schema of the SQLite database and the check of its version.

Every statement is static text; values reach SQL only through `?` placeholders.
"""

import sqlite3

from portfolio.application.errors.schema_version_error import SchemaVersionError
from portfolio.constants import (
    MESSAGE_SCHEMA_MISSING,
    MESSAGE_SCHEMA_NEWER,
    MESSAGE_SCHEMA_UNKNOWN,
    SCHEMA_VERSION,
)

## @brief Schema version of a database that was never initialised.
_NO_SCHEMA = 0

_READ_VERSION = "PRAGMA user_version"

# The position columns keep the insertion order, which is the display order. The
# CHECK rules mirror the "not blank" rules of the entities; the entities stay the
# authority and the limits on length and count are checked there only.
_SCHEMA_STATEMENTS = (
    """
    CREATE TABLE project (
        id INTEGER PRIMARY KEY,
        position INTEGER NOT NULL UNIQUE,
        title TEXT NOT NULL UNIQUE CHECK (length(trim(title)) > 0),
        kind TEXT NOT NULL CHECK (length(trim(kind)) > 0),
        description TEXT NOT NULL CHECK (length(trim(description)) > 0),
        image_url TEXT NOT NULL,
        source_code_url TEXT NOT NULL CHECK (length(trim(source_code_url)) > 0)
    )
    """,
    """
    CREATE TABLE project_tag (
        project_id INTEGER NOT NULL REFERENCES project (id) ON DELETE CASCADE,
        position INTEGER NOT NULL,
        value TEXT NOT NULL CHECK (length(trim(value)) > 0),
        PRIMARY KEY (project_id, position)
    )
    """,
    """
    CREATE TABLE project_skill (
        project_id INTEGER NOT NULL REFERENCES project (id) ON DELETE CASCADE,
        position INTEGER NOT NULL,
        value TEXT NOT NULL CHECK (length(trim(value)) > 0),
        PRIMARY KEY (project_id, position)
    )
    """,
    # The profile is a single row: its id can only be 1.
    """
    CREATE TABLE profile (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        name TEXT NOT NULL CHECK (length(trim(name)) > 0),
        headline TEXT NOT NULL CHECK (length(trim(headline)) > 0),
        summary TEXT NOT NULL CHECK (length(trim(summary)) > 0),
        photo TEXT CHECK (photo IS NULL OR length(trim(photo)) > 0)
    )
    """,
    """
    CREATE TABLE profile_skill (
        position INTEGER PRIMARY KEY,
        skill TEXT NOT NULL CHECK (length(trim(skill)) > 0)
    )
    """,
    """
    CREATE TABLE profile_link (
        position INTEGER PRIMARY KEY,
        label TEXT NOT NULL CHECK (length(trim(label)) > 0),
        url TEXT NOT NULL CHECK (length(trim(url)) > 0)
    )
    """,
    # PRAGMA cannot take a placeholder, so the number is written here; a test
    # checks that it equals SCHEMA_VERSION.
    "PRAGMA user_version = 1",
)


def read_schema_version(connection: sqlite3.Connection) -> int:
    """!
    @brief Read the schema version stored in the database file.
    @param connection An open connection.
    @return The version; 0 for a database that was never initialised.
    @throws sqlite3.Error The file is not a SQLite database.
    """
    return int(connection.execute(_READ_VERSION).fetchone()[0])


def create_schema(connection: sqlite3.Connection) -> None:
    """!
    @brief Create every table and set the schema version, inside the open transaction.
    @param connection An open connection with a transaction.
    @throws sqlite3.Error A table cannot be created, for example it already exists.
    """
    for statement in _SCHEMA_STATEMENTS:
        connection.execute(statement)


def require_current_schema(connection: sqlite3.Connection) -> None:
    """!
    @brief Check that the database has the schema version this program uses.
    @param connection An open connection.
    @throws SchemaVersionError The schema is missing, newer or unknown.
    @throws sqlite3.Error The file is not a SQLite database.
    """
    version = read_schema_version(connection)
    if version != SCHEMA_VERSION:
        raise _version_error(version)


def _version_error(version: int) -> SchemaVersionError:
    if version == _NO_SCHEMA:
        return SchemaVersionError(MESSAGE_SCHEMA_MISSING)
    if version > SCHEMA_VERSION:
        return SchemaVersionError(
            MESSAGE_SCHEMA_NEWER.format(found=version, known=SCHEMA_VERSION)
        )
    return SchemaVersionError(MESSAGE_SCHEMA_UNKNOWN.format(found=version))


def initialize_schema(connection: sqlite3.Connection) -> bool:
    """!
    @brief Create the schema when the database has none, inside the open transaction.
    @param connection An open connection with a transaction.
    @return True when the schema was created, False when it was already current.
    @throws SchemaVersionError The schema is newer or unknown.
    @throws sqlite3.Error The file is not a SQLite database or a table cannot be made.
    """
    version = read_schema_version(connection)
    if version == _NO_SCHEMA:
        create_schema(connection)
        return True
    if version != SCHEMA_VERSION:
        raise _version_error(version)
    return False
