"""The sample data files shipped in data/ load and fit the rules of the domain."""

from pathlib import Path

from portfolio.constants import DEFAULT_DATA_DIR, PROFILE_FILE_NAME, PROJECTS_FILE_NAME
from portfolio.infrastructure.load_from_json import load_from_json
from portfolio.infrastructure.load_profile_from_json import load_profile_from_json

DATA_DIR = Path(__file__).resolve().parents[2] / DEFAULT_DATA_DIR


def test_sample_projects_load() -> None:
    projects = load_from_json(DATA_DIR / PROJECTS_FILE_NAME)
    assert len(projects) == 6
    assert len({project.title for project in projects}) == len(projects)
    for project in projects:
        assert project.tags
        assert project.skills
        assert (DATA_DIR / project.image_url).is_file()


def test_sample_profile_loads() -> None:
    profile = load_profile_from_json(DATA_DIR / PROFILE_FILE_NAME)
    assert profile.name == "Jens Tirsvad Nielsen"
    assert len(profile.skills) >= 1
    assert profile.links


def test_sample_profile_links_to_linkedin_and_github() -> None:
    profile = load_profile_from_json(DATA_DIR / PROFILE_FILE_NAME)
    urls = {link.label: link.url for link in profile.links}
    assert urls["LinkedIn"] == "https://www.linkedin.com/in/tirsvad74/"
    assert "GitHub" in urls


def test_sample_profile_has_a_photo_file_that_exists() -> None:
    profile = load_profile_from_json(DATA_DIR / PROFILE_FILE_NAME)
    assert profile.photo == "images/profile.jpg"
    assert (DATA_DIR / profile.photo).is_file()
    assert profile.initials == "JN"
