"""!
@file sqlite_profile_repository.py
@brief ProfileRepository and ProfileWriter that keep the profile in SQLite.

Every statement is static text; values reach SQL only through `?` placeholders.
"""

import sqlite3

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.application.errors.profile_not_found_error import ProfileNotFoundError
from portfolio.domain.entities.profile import Profile
from portfolio.domain.errors.domain_error import DomainError
from portfolio.domain.value_objects.link import Link
from portfolio.infrastructure.sqlite_database import SqliteDatabase

# The profile is one row, and its id is always 1.
_SELECT_PROFILE = "SELECT name, headline, summary, photo FROM profile WHERE id = 1"
_SELECT_SKILLS = "SELECT skill FROM profile_skill ORDER BY position"
_SELECT_LINKS = "SELECT label, url FROM profile_link ORDER BY position"
_INSERT_PROFILE = (
    "INSERT INTO profile (id, name, headline, summary, photo) VALUES (1, ?, ?, ?, ?)"
)
_INSERT_SKILL = "INSERT INTO profile_skill (position, skill) VALUES (?, ?)"
_INSERT_LINK = "INSERT INTO profile_link (position, label, url) VALUES (?, ?, ?)"
_DELETE_PROFILE = "DELETE FROM profile"
_DELETE_SKILLS = "DELETE FROM profile_skill"
_DELETE_LINKS = "DELETE FROM profile_link"


def replace_profile(connection: sqlite3.Connection, profile: Profile) -> None:
    """!
    @brief Store the profile in place of the stored one, inside the open transaction.
    @param connection An open connection with a transaction.
    @param profile The profile to store.
    @throws sqlite3.Error The profile cannot be stored.
    """
    delete_profile(connection)
    connection.execute(
        _INSERT_PROFILE,
        (profile.name, profile.headline, profile.summary, profile.photo),
    )
    connection.executemany(
        _INSERT_SKILL, [(place, skill) for place, skill in enumerate(profile.skills)]
    )
    connection.executemany(
        _INSERT_LINK,
        [(place, link.label, link.url) for place, link in enumerate(profile.links)],
    )


def delete_profile(connection: sqlite3.Connection) -> None:
    """!
    @brief Delete the profile with its skills and links.
    @param connection An open connection with a transaction.
    @throws sqlite3.Error The profile cannot be deleted.
    """
    connection.execute(_DELETE_SKILLS)
    connection.execute(_DELETE_LINKS)
    connection.execute(_DELETE_PROFILE)


class SqliteProfileRepository:
    """!
    @brief Implements the ProfileRepository and ProfileWriter ports with SQLite.
    """

    def __init__(self, database: SqliteDatabase) -> None:
        """!
        @brief Create the repository.
        @param database The database to read and write.
        """
        self._database = database

    def get_profile(self) -> Profile:
        """!
        @brief Read the profile.
        @return The profile.
        @throws ProfileNotFoundError The database holds no profile.
        @throws DataSourceError The database cannot be used or holds an invalid profile.
        """
        with self._database.read() as connection:
            row = connection.execute(_SELECT_PROFILE).fetchone()
            if row is None:
                raise ProfileNotFoundError
            skills = tuple(item[0] for item in connection.execute(_SELECT_SKILLS))
            links = tuple(
                _to_link(label, url) for label, url in connection.execute(_SELECT_LINKS)
            )
        name, headline, summary, photo = row
        try:
            return Profile(name, headline, summary, skills, links, photo)
        except DomainError as err:
            raise DataSourceError(
                f"the database holds an invalid profile: {err}"
            ) from err

    def save_profile(self, profile: Profile) -> None:
        """!
        @brief Store the profile, replacing the one that is stored.
        @param profile The profile to keep.
        @throws DataSourceError The database cannot be used.
        """
        with self._database.write() as connection:
            replace_profile(connection, profile)


def _to_link(label: str, url: str) -> Link:
    try:
        return Link(label, url)
    except DomainError as err:
        raise DataSourceError(f"the database holds an invalid link: {err}") from err
