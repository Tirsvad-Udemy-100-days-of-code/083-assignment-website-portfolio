"""!
@file home.py
@brief Use case: build the home page.
"""

import random

from portfolio.application.dto.home_page import HomePage
from portfolio.application.dto.project_card import ProjectCard
from portfolio.application.ports.project_repository import ProjectRepository
from portfolio.constants import HOME_PROJECT_LIMIT, SITE_TITLE
from portfolio.domain.entities.project import Project


def home(
    repository: ProjectRepository,
    limit: int = HOME_PROJECT_LIMIT,
    rng: random.Random | None = None,
) -> HomePage:
    """!
    @brief Build the home page from at most `limit` projects.
    @param repository Source of the projects.
    @param limit Largest number of projects shown; at least 1.
    @param rng Random source for a random pick; None keeps the source order.
    @return The home page.
    @throws ValueError The limit is smaller than 1.
    """
    if limit < 1:
        raise ValueError("limit must be at least 1")
    projects = repository.list_projects()
    if rng is None:
        chosen = projects[:limit]
    else:
        chosen = rng.sample(projects, k=min(limit, len(projects)))
    return HomePage(
        site_title=SITE_TITLE,
        projects=tuple(_to_card(project) for project in chosen),
    )


def _to_card(project: Project) -> ProjectCard:
    return ProjectCard(
        title=project.title,
        kind=project.kind,
        description=project.description,
        image_url=project.image_url,
        source_code_url=project.source_code_url,
    )
