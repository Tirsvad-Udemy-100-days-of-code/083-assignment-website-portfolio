"""Unit tests of the SQLite profile repository, on an in-memory database."""

import pytest

from portfolio.application.errors.profile_not_found_error import ProfileNotFoundError
from portfolio.infrastructure.repositories.sqlite_profile_repository import (
    SqliteProfileRepository,
)
from portfolio.infrastructure.sqlite_database import SqliteDatabase
from sample_data import make_link, make_profile


@pytest.fixture
def repository(database: SqliteDatabase) -> SqliteProfileRepository:
    return SqliteProfileRepository(database)


def test_a_database_without_profile_raises_profile_not_found(
    repository: SqliteProfileRepository,
) -> None:
    with pytest.raises(ProfileNotFoundError):
        repository.get_profile()


def test_a_saved_profile_is_returned_with_every_field(
    repository: SqliteProfileRepository,
) -> None:
    profile = make_profile(
        skills=("C", "Python", "C"),
        links=(make_link("B", "https://b.com"), make_link("A", "https://a.com")),
        photo="images/me.png",
    )

    repository.save_profile(profile)

    assert repository.get_profile() == profile


def test_a_profile_without_photo_and_links_is_returned_unchanged(
    repository: SqliteProfileRepository,
) -> None:
    profile = make_profile(links=(), photo=None)

    repository.save_profile(profile)

    assert repository.get_profile() == profile


def test_saving_again_replaces_the_profile_and_its_lists(
    repository: SqliteProfileRepository, database: SqliteDatabase
) -> None:
    repository.save_profile(make_profile(skills=("A", "B", "C")))
    replacement = make_profile(
        name="Grace Hopper", skills=("COBOL",), links=(), photo=None
    )

    repository.save_profile(replacement)

    assert repository.get_profile() == replacement
    with database.read() as connection:
        rows = connection.execute("SELECT COUNT(*) FROM profile").fetchone()[0]
        skills = connection.execute("SELECT COUNT(*) FROM profile_skill").fetchone()[0]
        links = connection.execute("SELECT COUNT(*) FROM profile_link").fetchone()[0]
    assert (rows, skills, links) == (1, 1, 0)
