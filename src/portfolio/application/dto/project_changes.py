"""!
@file project_changes.py
@brief The fields of a project that a change gives a new value.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProjectChanges:
    """!
    @brief New values for some fields of a project.

    The field names are the ones of the Project entity.
    """

    ## @brief New title, or None.
    title: str | None = None
    ## @brief New kind, or None.
    kind: str | None = None
    ## @brief New description, or None.
    description: str | None = None
    ## @brief New image address or path, or None.
    image_url: str | None = None
    ## @brief New source code address, or None.
    source_code_url: str | None = None
    ## @brief New tags, which replace the old ones, or None.
    tags: tuple[str, ...] | None = None
    ## @brief New skills, which replace the old ones, or None.
    skills: tuple[str, ...] | None = None
