"""!
@file change_project.py
@brief Use case: change some fields of a stored project.
"""

from dataclasses import replace

from portfolio.application.dto.project_changes import ProjectChanges
from portfolio.application.errors.project_not_found_error import ProjectNotFoundError
from portfolio.application.ports.project_repository import ProjectRepository
from portfolio.application.ports.project_writer import ProjectWriter
from portfolio.application.use_cases.changed_fields import changed_fields
from portfolio.constants import MESSAGE_NOTHING_TO_CHANGE
from portfolio.domain.entities.project import Project
from portfolio.domain.errors.invalid_project_error import InvalidProjectError


def change_project(
    reader: ProjectRepository,
    writer: ProjectWriter,
    title: str,
    changes: ProjectChanges,
) -> str:
    """!
    @brief Give new values to a project; the Project entity checks the result.
    @param reader Source of the stored projects.
    @param writer Destination of the changed project.
    @param title The title of the stored project.
    @param changes The new values; a field that is None keeps its value.
    @return The title of the project after the change.
    @throws InvalidProjectError No value was given, or a value breaks a rule.
    @throws ProjectNotFoundError No project has the title.
    @throws DuplicateProjectError The new title belongs to another project.
    @throws DataSourceError The project cannot be read or stored.
    """
    new_values = changed_fields(changes)
    if not new_values:
        raise InvalidProjectError(MESSAGE_NOTHING_TO_CHANGE)
    changed = replace(_find(reader, title), **new_values)
    writer.replace_project(title, changed)
    return changed.title


def _find(reader: ProjectRepository, title: str) -> Project:
    for project in reader.list_projects():
        if project.title == title:
            return project
    raise ProjectNotFoundError(title)
