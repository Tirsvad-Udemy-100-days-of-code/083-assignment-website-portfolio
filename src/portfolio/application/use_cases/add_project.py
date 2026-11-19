"""!
@file add_project.py
@brief Use case: add a project.
"""

from portfolio.application.dto.project_input import ProjectInput
from portfolio.application.ports.project_writer import ProjectWriter
from portfolio.domain.entities.project import Project


def add_project(writer: ProjectWriter, data: ProjectInput) -> None:
    """!
    @brief Check the values through the Project entity and store the project.
    @param writer Destination of the project.
    @param data The values of the new project.
    @throws InvalidProjectError A value breaks a rule of a project.
    @throws DuplicateProjectError Another project has the title.
    @throws DataSourceError The project cannot be stored.
    """
    writer.add_project(
        Project(
            title=data.title,
            kind=data.kind,
            description=data.description,
            image_url=data.image_url,
            source_code_url=data.source_code_url,
            tags=data.tags,
            skills=data.skills,
        )
    )
