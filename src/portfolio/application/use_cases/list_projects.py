"""!
@file list_projects.py
@brief Use case: list every stored project.
"""

from portfolio.application.dto.project_card import ProjectCard, to_project_card
from portfolio.application.ports.project_repository import ProjectRepository


def list_projects(repository: ProjectRepository) -> tuple[ProjectCard, ...]:
    """!
    @brief Read every project, in the order they are shown.
    @param repository Source of the projects.
    @return The projects as plain data.
    @throws DataSourceError The projects cannot be read.
    """
    return tuple(to_project_card(project) for project in repository.list_projects())
