"""!
@file project_card.py
@brief Data of one project as the home page shows it.
"""

from dataclasses import dataclass

from portfolio.domain.entities.project import Project


@dataclass(frozen=True, slots=True)
class ProjectCard:
    """!
    @brief One project on the home page.
    """

    ## @brief Name of the project.
    title: str
    ## @brief Kind of project.
    kind: str
    ## @brief Short description of the project.
    description: str
    ## @brief Address or relative path of the project image; empty when there is none.
    image_url: str
    ## @brief URL of the source code.
    source_code_url: str
    ## @brief Short labels such as the languages used.
    tags: tuple[str, ...]
    ## @brief Skills the project shows.
    skills: tuple[str, ...]


def to_project_card(project: Project) -> ProjectCard:
    """!
    @brief Copy a project into the data of a card.
    @param project The project.
    @return The card with the same values.
    """
    return ProjectCard(
        title=project.title,
        kind=project.kind,
        description=project.description,
        image_url=project.image_url,
        source_code_url=project.source_code_url,
        tags=project.tags,
        skills=project.skills,
    )
