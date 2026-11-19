"""!
@file project_input.py
@brief Data of a project to add, as the management commands give it.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProjectInput:
    """!
    @brief The values of a new project; the Project entity checks them.
    """

    ## @brief Name of the project.
    title: str
    ## @brief Kind of project.
    kind: str
    ## @brief Short description of the project.
    description: str
    ## @brief Source code address.
    source_code_url: str
    ## @brief Image address or relative path; empty when there is none.
    image_url: str = ""
    ## @brief Short labels such as the languages used.
    tags: tuple[str, ...] = ()
    ## @brief Skills the project shows.
    skills: tuple[str, ...] = ()
