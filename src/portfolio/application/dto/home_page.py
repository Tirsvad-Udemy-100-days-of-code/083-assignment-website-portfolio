"""!
@file home_page.py
@brief Data of the home page.
"""

from dataclasses import dataclass

from portfolio.application.dto.project_card import ProjectCard


@dataclass(frozen=True, slots=True)
class HomePage:
    """!
    @brief What the home page shows.
    """

    ## @brief Title of the site.
    site_title: str
    ## @brief The featured projects.
    projects: tuple[ProjectCard, ...]
