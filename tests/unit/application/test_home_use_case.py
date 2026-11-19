"""Unit tests of the home use case."""

import random

import pytest

from fakes import InMemoryProjectRepository
from portfolio.application.use_cases.home import home
from portfolio.constants import HOME_PROJECT_LIMIT, SITE_TITLE
from sample_data import make_project, make_projects


def test_home_maps_a_project_to_a_card() -> None:
    page = home(InMemoryProjectRepository([make_project()]))
    card = page.projects[0]
    assert page.site_title == SITE_TITLE
    assert (card.title, card.kind) == ("Weather app", "Web app")
    assert card.description == "Shows the weather of a city."
    assert card.image_url == "https://example.com/weather.png"
    assert card.source_code_url == "https://example.com/weather"


def test_home_maps_tags_and_skills_to_the_card() -> None:
    project = make_project(tags=("C", "Rust"), skills=("SIMD", "Threads"))
    card = home(InMemoryProjectRepository([project])).projects[0]
    assert card.tags == ("C", "Rust")
    assert card.skills == ("SIMD", "Threads")


def test_home_maps_a_relative_image_path_unchanged() -> None:
    project = make_project(image_url="images/a.svg")
    card = home(InMemoryProjectRepository([project])).projects[0]
    assert card.image_url == "images/a.svg"


def test_home_returns_no_cards_when_repository_is_empty() -> None:
    assert home(InMemoryProjectRepository([])).projects == ()


def test_home_returns_no_cards_when_repository_is_empty_and_random() -> None:
    page = home(InMemoryProjectRepository([]), rng=random.Random(1))
    assert page.projects == ()


def test_home_keeps_file_order_without_rng() -> None:
    repository = InMemoryProjectRepository(make_projects(3))
    titles = [card.title for card in home(repository).projects]
    assert titles == ["Project 0", "Project 1", "Project 2"]


def test_home_takes_the_first_projects_up_to_the_default_limit() -> None:
    repository = InMemoryProjectRepository(make_projects(HOME_PROJECT_LIMIT + 1))
    titles = [card.title for card in home(repository).projects]
    assert len(titles) == HOME_PROJECT_LIMIT
    assert titles[-1] == f"Project {HOME_PROJECT_LIMIT - 1}"


def test_home_takes_exactly_the_limit_when_there_are_that_many() -> None:
    repository = InMemoryProjectRepository(make_projects(HOME_PROJECT_LIMIT))
    assert len(home(repository).projects) == HOME_PROJECT_LIMIT


def test_home_honours_a_custom_limit() -> None:
    repository = InMemoryProjectRepository(make_projects(5))
    assert len(home(repository, limit=2).projects) == 2


@pytest.mark.parametrize("limit", [0, -1])
def test_home_rejects_limit_below_one(limit: int) -> None:
    with pytest.raises(ValueError, match="limit"):
        home(InMemoryProjectRepository([]), limit=limit)


def test_home_sample_is_reproducible_with_a_seeded_rng() -> None:
    repository = InMemoryProjectRepository(make_projects(20))
    first = home(repository, limit=5, rng=random.Random(1))
    second = home(repository, limit=5, rng=random.Random(1))
    assert first == second
    assert len(first.projects) == 5
    assert len({card.title for card in first.projects}) == 5


def test_home_sample_matches_the_rng_pick() -> None:
    projects = make_projects(20)
    expected = random.Random(1).sample(projects, k=5)
    page = home(InMemoryProjectRepository(projects), limit=5, rng=random.Random(1))
    assert [card.title for card in page.projects] == [p.title for p in expected]


def test_home_sample_returns_all_when_fewer_than_limit() -> None:
    repository = InMemoryProjectRepository(make_projects(3))
    page = home(repository, rng=random.Random(1))
    assert sorted(card.title for card in page.projects) == [
        "Project 0",
        "Project 1",
        "Project 2",
    ]
