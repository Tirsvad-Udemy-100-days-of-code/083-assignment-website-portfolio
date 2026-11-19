"""Fixtures of the unit tests."""

from collections.abc import Iterator

import pytest

from portfolio.constants import IN_MEMORY_DATABASE
from portfolio.infrastructure.sqlite_database import SqliteDatabase
from portfolio.infrastructure.sqlite_database_initializer import (
    SqliteDatabaseInitializer,
)


@pytest.fixture
def database() -> Iterator[SqliteDatabase]:
    """An initialised SQLite database that lives in memory."""
    in_memory = SqliteDatabase(IN_MEMORY_DATABASE)
    SqliteDatabaseInitializer(in_memory).initialize()
    try:
        yield in_memory
    finally:
        in_memory.close()
