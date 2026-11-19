"""!
@file sqlite_project_repository.py
@brief ProjectRepository and ProjectWriter that keep the projects in SQLite.

Every statement is static text; values reach SQL only through `?` placeholders.
"""

import sqlite3
from collections.abc import Iterable, Sequence

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.application.errors.duplicate_project_error import DuplicateProjectError
from portfolio.application.errors.project_not_found_error import ProjectNotFoundError
from portfolio.domain.entities.project import Project
from portfolio.domain.errors.domain_error import DomainError
from portfolio.infrastructure.sqlite_database import SqliteDatabase

_SELECT_PROJECTS = """
    SELECT id, title, kind, description, image_url, source_code_url
    FROM project ORDER BY position
"""
_SELECT_TAGS = "SELECT project_id, value FROM project_tag ORDER BY position"
_SELECT_SKILLS = "SELECT project_id, value FROM project_skill ORDER BY position"
_SELECT_ID_OF_TITLE = "SELECT id FROM project WHERE title = ?"
_SELECT_LAST_POSITION = "SELECT COALESCE(MAX(position), 0) FROM project"
_INSERT_PROJECT = """
    INSERT INTO project
        (position, title, kind, description, image_url, source_code_url)
    VALUES (?, ?, ?, ?, ?, ?)
"""
_INSERT_TAG = "INSERT INTO project_tag (project_id, position, value) VALUES (?, ?, ?)"
_INSERT_SKILL = (
    "INSERT INTO project_skill (project_id, position, value) VALUES (?, ?, ?)"
)
_UPDATE_PROJECT = """
    UPDATE project
    SET title = ?, kind = ?, description = ?, image_url = ?, source_code_url = ?
    WHERE id = ?
"""
_DELETE_TAGS = "DELETE FROM project_tag WHERE project_id = ?"
_DELETE_SKILLS = "DELETE FROM project_skill WHERE project_id = ?"
_DELETE_PROJECT = "DELETE FROM project WHERE title = ?"
_DELETE_ALL_PROJECTS = "DELETE FROM project"


def insert_project(
    connection: sqlite3.Connection, position: int, project: Project
) -> None:
    """!
    @brief Insert a project with its tags and skills, inside the open transaction.
    @param connection An open connection with a transaction.
    @param position The place of the project in the display order.
    @param project The project to store.
    @throws sqlite3.Error The project cannot be stored, for example its title is taken.
    """
    cursor = connection.execute(
        _INSERT_PROJECT,
        (
            position,
            project.title,
            project.kind,
            project.description,
            project.image_url,
            project.source_code_url,
        ),
    )
    _insert_lists(connection, _row_id(cursor), project)


def delete_all_projects(connection: sqlite3.Connection) -> None:
    """!
    @brief Delete every project; its tags and skills go with it.
    @param connection An open connection with a transaction.
    @throws sqlite3.Error The projects cannot be deleted.
    """
    connection.execute(_DELETE_ALL_PROJECTS)


def _row_id(cursor: sqlite3.Cursor) -> int:
    if cursor.lastrowid is None:
        raise DataSourceError("the database gave no id to the new row")
    return cursor.lastrowid


def _insert_lists(
    connection: sqlite3.Connection, project_id: int, project: Project
) -> None:
    connection.executemany(
        _INSERT_TAG,
        [(project_id, place, tag) for place, tag in enumerate(project.tags)],
    )
    connection.executemany(
        _INSERT_SKILL,
        [(project_id, place, skill) for place, skill in enumerate(project.skills)],
    )


def _group(rows: Iterable[tuple[int, str]]) -> dict[int, tuple[str, ...]]:
    grouped: dict[int, list[str]] = {}
    for project_id, value in rows:
        grouped.setdefault(project_id, []).append(value)
    return {project_id: tuple(values) for project_id, values in grouped.items()}


def _to_project(
    row: tuple[int, str, str, str, str, str],
    tags: dict[int, tuple[str, ...]],
    skills: dict[int, tuple[str, ...]],
) -> Project:
    project_id, title, kind, description, image_url, source_code_url = row
    return Project(
        title=title,
        kind=kind,
        description=description,
        image_url=image_url,
        source_code_url=source_code_url,
        tags=tags.get(project_id, ()),
        skills=skills.get(project_id, ()),
    )


class SqliteProjectRepository:
    """!
    @brief Implements the ProjectRepository and ProjectWriter ports with SQLite.
    """

    def __init__(self, database: SqliteDatabase) -> None:
        """!
        @brief Create the repository.
        @param database The database to read and write.
        """
        self._database = database

    def list_projects(self) -> Sequence[Project]:
        """!
        @brief Read every project, in the order they were added.
        @return The projects.
        @throws DataSourceError The database cannot be used or holds an invalid project.
        """
        with self._database.read() as connection:
            rows = connection.execute(_SELECT_PROJECTS).fetchall()
            tags = _group(connection.execute(_SELECT_TAGS))
            skills = _group(connection.execute(_SELECT_SKILLS))
        try:
            return tuple(_to_project(row, tags, skills) for row in rows)
        except DomainError as err:
            raise DataSourceError(
                f"the database holds an invalid project: {err}"
            ) from err

    def add_project(self, project: Project) -> None:
        """!
        @brief Store a new project after the last one.
        @param project The project to add.
        @throws DuplicateProjectError Another project has the title.
        @throws DataSourceError The database cannot be used.
        """
        with self._database.write() as connection:
            if _find_id(connection, project.title) is not None:
                raise DuplicateProjectError(project.title)
            last = int(connection.execute(_SELECT_LAST_POSITION).fetchone()[0])
            insert_project(connection, last + 1, project)

    def replace_project(self, title: str, project: Project) -> None:
        """!
        @brief Replace the project with a title, keeping its place in the order.
        @param title The title of the stored project.
        @param project The new values; its title may differ from `title`.
        @throws ProjectNotFoundError No project has the title.
        @throws DuplicateProjectError The new title belongs to another project.
        @throws DataSourceError The database cannot be used.
        """
        with self._database.write() as connection:
            project_id = _find_id(connection, title)
            if project_id is None:
                raise ProjectNotFoundError(title)
            other_id = _find_id(connection, project.title)
            if other_id is not None and other_id != project_id:
                raise DuplicateProjectError(project.title)
            connection.execute(
                _UPDATE_PROJECT,
                (
                    project.title,
                    project.kind,
                    project.description,
                    project.image_url,
                    project.source_code_url,
                    project_id,
                ),
            )
            connection.execute(_DELETE_TAGS, (project_id,))
            connection.execute(_DELETE_SKILLS, (project_id,))
            _insert_lists(connection, project_id, project)

    def remove_project(self, title: str) -> None:
        """!
        @brief Remove the project with a title.
        @param title The title of the stored project.
        @throws ProjectNotFoundError No project has the title.
        @throws DataSourceError The database cannot be used.
        """
        with self._database.write() as connection:
            if connection.execute(_DELETE_PROJECT, (title,)).rowcount == 0:
                raise ProjectNotFoundError(title)


def _find_id(connection: sqlite3.Connection, title: str) -> int | None:
    row = connection.execute(_SELECT_ID_OF_TITLE, (title,)).fetchone()
    return None if row is None else int(row[0])
