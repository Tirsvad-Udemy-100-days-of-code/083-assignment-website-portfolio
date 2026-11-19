"""The sample data files shipped in data/ load and fit the rules of the domain."""

from pathlib import Path

from portfolio.constants import DEFAULT_DATA_DIR, PROFILE_FILE_NAME, PROJECTS_FILE_NAME
from portfolio.infrastructure.repositories.json_profile_repository import (
    JsonProfileRepository,
)
from portfolio.infrastructure.repositories.json_project_repository import (
    JsonProjectRepository,
)

DATA_DIR = Path(__file__).resolve().parents[2] / DEFAULT_DATA_DIR


def test_sample_projects_load() -> None:
    projects = JsonProjectRepository(DATA_DIR / PROJECTS_FILE_NAME).list_projects()
    assert len(projects) >= 6
    assert len({project.title for project in projects}) == len(projects)


def test_sample_profile_loads() -> None:
    profile = JsonProfileRepository(DATA_DIR / PROFILE_FILE_NAME).get_profile()
    assert profile.name == "Jens Tirsvad Nielsen"
    assert len(profile.skills) >= 1
    assert profile.links
