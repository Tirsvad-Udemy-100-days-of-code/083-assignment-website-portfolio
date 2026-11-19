"""!
@file remove_project.py
@brief Use case: remove a project.
"""

from portfolio.application.ports.project_writer import ProjectWriter


def remove_project(writer: ProjectWriter, title: str) -> None:
    """!
    @brief Remove the project with a title.
    @param writer Destination of the change.
    @param title The title of the stored project.
    @throws ProjectNotFoundError No project has the title.
    @throws DataSourceError The project cannot be removed.
    """
    writer.remove_project(title)
