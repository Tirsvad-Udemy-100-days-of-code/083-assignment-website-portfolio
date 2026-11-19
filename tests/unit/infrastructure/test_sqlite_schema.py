"""Unit tests of the SQLite schema, on an in-memory database."""

import sqlite3

import pytest

from portfolio.application.errors.schema_version_error import SchemaVersionError
from portfolio.constants import IN_MEMORY_DATABASE, SCHEMA_VERSION
from portfolio.infrastructure.errors.database_error import DatabaseError
from portfolio.infrastructure.sqlite_database import SqliteDatabase
from portfolio.infrastructure.sqlite_database_initializer import (
    SqliteDatabaseInitializer,
)
from portfolio.infrastructure.sqlite_schema import read_schema_version

EXPECTED_TABLES = {
    "project",
    "project_tag",
    "project_skill",
    "profile",
    "profile_skill",
    "profile_link",
}


def table_names(database: SqliteDatabase) -> set[str]:
    with database.read() as connection:
        rows = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    return {row[0] for row in rows}


def test_initialize_creates_every_table(database: SqliteDatabase) -> None:
    assert table_names(database) == EXPECTED_TABLES


def test_the_schema_script_sets_the_version_of_the_constant(
    database: SqliteDatabase,
) -> None:
    with database.read() as connection:
        assert read_schema_version(connection) == SCHEMA_VERSION


def test_initialize_reports_true_once_and_then_false() -> None:
    in_memory = SqliteDatabase(IN_MEMORY_DATABASE)
    initializer = SqliteDatabaseInitializer(in_memory)
    try:
        assert initializer.initialize() is True
        assert initializer.initialize() is False
        assert table_names(in_memory) == EXPECTED_TABLES
    finally:
        in_memory.close()


def test_initialize_refuses_a_schema_that_is_newer_than_the_program() -> None:
    assert SCHEMA_VERSION < 99
    in_memory = SqliteDatabase(IN_MEMORY_DATABASE)
    try:
        with in_memory.create() as connection:
            connection.execute("PRAGMA user_version = 99")
        with pytest.raises(SchemaVersionError, match="newer"):
            SqliteDatabaseInitializer(in_memory).initialize()
    finally:
        in_memory.close()


def test_read_refuses_a_database_without_schema() -> None:
    in_memory = SqliteDatabase(IN_MEMORY_DATABASE)
    try:
        with pytest.raises(SchemaVersionError, match="init"), in_memory.read():
            pass
    finally:
        in_memory.close()


def test_foreign_keys_are_switched_on(database: SqliteDatabase) -> None:
    with database.read() as connection:
        assert connection.execute("PRAGMA foreign_keys").fetchone() == (1,)


def test_a_tag_of_an_unknown_project_is_refused(database: SqliteDatabase) -> None:
    with (
        pytest.raises(DatabaseError, match="FOREIGN KEY"),
        database.write() as connection,
    ):
        connection.execute(
            "INSERT INTO project_tag (project_id, position, value) VALUES (1, 0, 'x')"
        )


def test_a_blank_title_is_refused_by_the_schema(database: SqliteDatabase) -> None:
    with pytest.raises(DatabaseError, match="CHECK"), database.write() as connection:
        connection.execute(
            "INSERT INTO project (position, title, kind, description, image_url,"
            " source_code_url) VALUES (1, '  ', 'k', 'd', '', 'u')"
        )


def test_a_second_profile_row_is_refused_by_the_schema(
    database: SqliteDatabase,
) -> None:
    with pytest.raises(DatabaseError, match="CHECK"), database.write() as connection:
        connection.execute(
            "INSERT INTO profile (id, name, headline, summary)"
            " VALUES (2, 'n', 'h', 's')"
        )


def test_sqlite_errors_are_the_cause_of_the_data_source_error(
    database: SqliteDatabase,
) -> None:
    with pytest.raises(DatabaseError) as error, database.write() as connection:
        connection.execute("SELECT * FROM missing_table")
    assert isinstance(error.value.__cause__, sqlite3.Error)
