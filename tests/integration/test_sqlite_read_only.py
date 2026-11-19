"""The read-only SQLite database, and the site that opens the database that way."""

import sqlite3
import sys
from pathlib import Path

import pytest

from portfolio import __main__ as entry_point
from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.application.errors.schema_version_error import SchemaVersionError
from portfolio.constants import (
    DEFAULT_DATA_DIR,
    PROFILE_FILE_NAME,
    PROJECTS_FILE_NAME,
    ROUTE_ABOUT,
    ROUTE_HOME,
)
from portfolio.infrastructure.errors.database_error import DatabaseError
from portfolio.infrastructure.repositories.sqlite_project_repository import (
    SqliteProjectRepository,
)
from portfolio.infrastructure.sqlite_database import SqliteDatabase
from portfolio.infrastructure.sqlite_database_initializer import (
    SqliteDatabaseInitializer,
)
from sample_data import make_project

SAMPLE_DATA = Path(__file__).resolve().parents[2] / DEFAULT_DATA_DIR
COUNT_PROJECTS = "SELECT COUNT(*) FROM project"


def prepare(path: Path) -> Path:
    """An initialised database with one project."""
    SqliteDatabaseInitializer(SqliteDatabase(path)).initialize()
    SqliteProjectRepository(SqliteDatabase(path)).add_project(make_project())
    return path


def count_projects(path: Path) -> int:
    connection = sqlite3.connect(path)
    try:
        return int(connection.execute(COUNT_PROJECTS).fetchone()[0])
    finally:
        connection.close()


def test_a_read_only_database_reads(tmp_path: Path) -> None:
    path = prepare(tmp_path / "portfolio.db")

    projects = SqliteProjectRepository(
        SqliteDatabase(path, read_only=True)
    ).list_projects()

    assert [project.title for project in projects] == ["Weather app"]


def test_a_read_only_database_refuses_a_write(tmp_path: Path) -> None:
    path = prepare(tmp_path / "portfolio.db")

    with (
        pytest.raises(DatabaseError, match="readonly"),
        SqliteDatabase(path, read_only=True).write() as connection,
    ):
        connection.execute("DELETE FROM project")

    assert count_projects(path) == 1


def test_a_connection_to_read_only_database_refuses_a_write_in_a_read(
    tmp_path: Path,
) -> None:
    path = prepare(tmp_path / "portfolio.db")

    with (
        pytest.raises(DatabaseError, match="readonly"),
        SqliteDatabase(path, read_only=True).read() as connection,
    ):
        connection.execute("DELETE FROM project")

    assert count_projects(path) == 1


def test_a_read_only_repository_refuses_to_add_a_project(tmp_path: Path) -> None:
    path = prepare(tmp_path / "portfolio.db")
    repository = SqliteProjectRepository(SqliteDatabase(path, read_only=True))

    with pytest.raises(DataSourceError):
        repository.add_project(make_project(title="Other"))

    assert count_projects(path) == 1


def test_a_read_only_database_never_creates_the_file(tmp_path: Path) -> None:
    path = tmp_path / "missing" / "portfolio.db"
    database = SqliteDatabase(path, read_only=True)

    with pytest.raises(DatabaseError, match="not found"), database.read():
        pass
    with pytest.raises(DatabaseError, match="read-only"), database.create():
        pass

    assert not path.exists()
    assert not path.parent.exists()


def test_a_read_only_database_still_checks_the_schema(tmp_path: Path) -> None:
    path = tmp_path / "empty.db"
    sqlite3.connect(path).close()

    with (
        pytest.raises(SchemaVersionError),
        SqliteDatabase(path, read_only=True).read(),
    ):
        pass


QUESTION_MARK_NAME = pytest.param(
    "what?.db",
    marks=pytest.mark.skipif(
        sys.platform == "win32", reason="Windows file names cannot hold a ?"
    ),
)


@pytest.mark.parametrize(
    "name", ["my data", QUESTION_MARK_NAME, "a#b.db", "100%.db", "æøå.db"]
)
def test_a_path_with_special_characters_opens_read_only(
    tmp_path: Path, name: str
) -> None:
    path = prepare(tmp_path / name)

    with SqliteDatabase(path, read_only=True).read() as connection:
        assert connection.execute(COUNT_PROJECTS).fetchone() == (1,)


def test_a_relative_path_opens_read_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    prepare(tmp_path / "portfolio.db")
    monkeypatch.chdir(tmp_path)

    with SqliteDatabase(Path("portfolio.db"), read_only=True).read() as connection:
        assert connection.execute(COUNT_PROJECTS).fetchone() == (1,)


def test_an_in_memory_database_cannot_be_read_only() -> None:
    with pytest.raises(ValueError, match="in-memory"):
        SqliteDatabase(":memory:", read_only=True)


def import_sample(path: Path) -> None:
    assert entry_point.main(["init", "--db", str(path)]) == 0
    assert (
        entry_point.main(["import", "--db", str(path), "--data", str(SAMPLE_DATA)]) == 0
    )


class ConnectionSpy:
    """Records the location of every SQLite connection and passes the call on."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch) -> None:
        self.locations: list[str] = []
        self._connect = sqlite3.connect
        monkeypatch.setattr(sqlite3, "connect", self)

    def __call__(self, location: str, *args: object, **kwargs: object) -> object:
        self.locations.append(location)
        return self._connect(location, *args, **kwargs)  # type: ignore[call-overload]


def test_the_site_opens_the_database_read_only_on_every_request(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "portfolio.db"
    import_sample(path)
    client = entry_point.create_site(path, SAMPLE_DATA).test_client()
    spy = ConnectionSpy(monkeypatch)

    assert client.get(ROUTE_HOME).status_code == 200
    assert client.get(ROUTE_ABOUT).status_code == 200
    assert client.get(ROUTE_HOME).status_code == 200

    assert len(spy.locations) == 3
    assert all(location.startswith("file:///") for location in spy.locations)
    assert all(location.endswith("?mode=ro") for location in spy.locations)


def test_a_write_through_the_connection_of_the_site_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "portfolio.db"
    import_sample(path)
    client = entry_point.create_site(path, SAMPLE_DATA).test_client()
    spy = ConnectionSpy(monkeypatch)
    client.get(ROUTE_HOME)
    before = count_projects(path)

    site_connection = sqlite3.connect(spy.locations[0], uri=True)
    try:
        with pytest.raises(sqlite3.OperationalError, match="readonly"):
            site_connection.execute("DELETE FROM project")
    finally:
        site_connection.close()

    assert count_projects(path) == before


def test_serving_does_not_change_the_database_file(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.db"
    import_sample(path)
    before = path.read_bytes()
    client = entry_point.create_site(path, SAMPLE_DATA).test_client()

    for target in (ROUTE_HOME, ROUTE_ABOUT, "/images/profile.jpg", "/nope"):
        client.get(target)

    assert path.read_bytes() == before
    assert not list(tmp_path.glob("portfolio.db-*"))


def test_the_site_gives_a_500_page_when_the_database_is_gone(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.db"
    import_sample(path)
    client = entry_point.create_site(path, SAMPLE_DATA).test_client()
    path.unlink()

    response = client.get(ROUTE_HOME)

    assert response.status_code == 500
    assert str(tmp_path) not in response.text
    assert "Traceback" not in response.text
    assert not path.exists()


def test_the_sample_files_are_where_the_site_tests_expect_them() -> None:
    assert (SAMPLE_DATA / PROJECTS_FILE_NAME).is_file()
    assert (SAMPLE_DATA / PROFILE_FILE_NAME).is_file()
    assert (SAMPLE_DATA / "images" / "profile.jpg").is_file()
