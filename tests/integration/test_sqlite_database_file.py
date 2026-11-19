"""The SQLite database as a file: creation, persistence, versions and bad files."""

import sqlite3
from pathlib import Path

import pytest

from portfolio.application.errors.schema_version_error import SchemaVersionError
from portfolio.constants import SCHEMA_VERSION
from portfolio.infrastructure.errors.database_error import DatabaseError
from portfolio.infrastructure.repositories.sqlite_profile_repository import (
    SqliteProfileRepository,
)
from portfolio.infrastructure.repositories.sqlite_project_repository import (
    SqliteProjectRepository,
)
from portfolio.infrastructure.sqlite_database import SqliteDatabase
from portfolio.infrastructure.sqlite_database_initializer import (
    SqliteDatabaseInitializer,
)
from sample_data import make_profile, make_project

NOT_A_DATABASE = "This is a text file, not a SQLite database. " * 20


def initialize(path: Path) -> bool:
    return SqliteDatabaseInitializer(SqliteDatabase(path)).initialize()


def stored_version(path: Path) -> int:
    connection = sqlite3.connect(path)
    try:
        return int(connection.execute("PRAGMA user_version").fetchone()[0])
    finally:
        connection.close()


def test_init_creates_the_file_with_the_current_schema_version(
    tmp_path: Path,
) -> None:
    path = tmp_path / "portfolio.db"

    assert initialize(path) is True

    assert path.is_file()
    assert stored_version(path) == SCHEMA_VERSION


def test_init_creates_the_missing_folders_of_the_path(tmp_path: Path) -> None:
    path = tmp_path / "a" / "b" / "portfolio.db"

    assert initialize(path) is True

    assert path.is_file()


def test_init_on_a_current_database_keeps_its_data(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.db"
    initialize(path)
    SqliteProjectRepository(SqliteDatabase(path)).add_project(make_project())

    assert initialize(path) is False

    assert len(SqliteProjectRepository(SqliteDatabase(path)).list_projects()) == 1


def test_data_survives_opening_the_file_again(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.db"
    initialize(path)
    project = make_project(title="Kept", tags=("a", "b"), skills=("s",))
    profile = make_profile(photo="images/me.png")
    SqliteProjectRepository(SqliteDatabase(path)).add_project(project)
    SqliteProfileRepository(SqliteDatabase(path)).save_profile(profile)

    assert SqliteProjectRepository(SqliteDatabase(path)).list_projects() == (project,)
    assert SqliteProfileRepository(SqliteDatabase(path)).get_profile() == profile


def test_init_stops_on_a_schema_newer_than_the_program(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.db"
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA user_version = 99")
    connection.close()

    with pytest.raises(SchemaVersionError) as error:
        initialize(path)

    assert "99" in str(error.value)
    assert str(SCHEMA_VERSION) in str(error.value)
    assert "newer" in str(error.value)
    assert stored_version(path) == 99


def test_reading_a_database_with_a_newer_schema_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.db"
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA user_version = 99")
    connection.close()

    with pytest.raises(SchemaVersionError, match="newer"):
        SqliteProjectRepository(SqliteDatabase(path)).list_projects()


def test_init_refuses_a_file_that_is_not_a_sqlite_database(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.db"
    path.write_text(NOT_A_DATABASE, encoding="utf-8")

    with pytest.raises(DatabaseError, match="not a database") as error:
        initialize(path)

    assert str(path) in str(error.value)
    assert path.read_text(encoding="utf-8") == NOT_A_DATABASE


def test_reading_a_file_that_is_not_a_sqlite_database_is_refused(
    tmp_path: Path,
) -> None:
    path = tmp_path / "portfolio.db"
    path.write_text(NOT_A_DATABASE, encoding="utf-8")

    with pytest.raises(DatabaseError, match="not a database"):
        SqliteProjectRepository(SqliteDatabase(path)).list_projects()


def test_reading_a_missing_file_is_refused_and_does_not_create_it(
    tmp_path: Path,
) -> None:
    path = tmp_path / "portfolio.db"

    with pytest.raises(DatabaseError, match="init"):
        SqliteProjectRepository(SqliteDatabase(path)).list_projects()

    assert not path.exists()


def test_reading_a_database_without_schema_asks_for_init(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.db"
    sqlite3.connect(path).close()

    with pytest.raises(SchemaVersionError, match="init"):
        SqliteProjectRepository(SqliteDatabase(path)).list_projects()


def test_init_on_a_database_with_foreign_tables_and_no_version_is_refused(
    tmp_path: Path,
) -> None:
    path = tmp_path / "portfolio.db"
    connection = sqlite3.connect(path)
    connection.execute("CREATE TABLE project (id INTEGER)")
    connection.commit()
    connection.close()

    with pytest.raises(DatabaseError, match="already exists"):
        initialize(path)

    assert stored_version(path) == 0


def test_a_path_that_is_a_folder_is_refused(tmp_path: Path) -> None:
    with pytest.raises(DatabaseError):
        initialize(tmp_path)


def test_no_connection_stays_open_after_an_operation(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.db"
    initialize(path)
    repository = SqliteProjectRepository(SqliteDatabase(path))
    repository.add_project(make_project())
    repository.list_projects()

    # Windows refuses to delete a file that a connection still holds open.
    path.unlink()

    assert not path.exists()


def test_foreign_keys_are_on_in_every_connection(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.db"
    initialize(path)

    with SqliteDatabase(path).read() as connection:
        assert connection.execute("PRAGMA foreign_keys").fetchone() == (1,)


def test_a_failed_write_is_rolled_back(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.db"
    initialize(path)
    database = SqliteDatabase(path)

    def fail_after_a_write() -> None:
        with database.write() as connection:
            connection.execute(
                "INSERT INTO profile (id, name, headline, summary)"
                " VALUES (1, 'n', 'h', 's')"
            )
            raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        fail_after_a_write()

    with database.read() as connection:
        assert connection.execute("SELECT COUNT(*) FROM profile").fetchone() == (0,)
