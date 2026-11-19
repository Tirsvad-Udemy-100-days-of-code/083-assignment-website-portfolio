"""Contract test: what the JSON files describe is what the SQLite repositories return.

A data folder is imported into a database; the repositories must return the
projects and the profile that the folder describes, in the same order, field by
field. The expected objects are built here from the raw JSON, not by the loaders.
"""

import json
from collections.abc import Callable
from pathlib import Path

import pytest

from data_files import profile_document, project_entry, write_json
from portfolio.application.ports.profile_repository import ProfileRepository
from portfolio.application.ports.project_repository import ProjectRepository
from portfolio.application.use_cases.import_portfolio import import_portfolio
from portfolio.constants import DEFAULT_DATA_DIR, PROFILE_FILE_NAME, PROJECTS_FILE_NAME
from portfolio.domain.entities.profile import Profile
from portfolio.domain.entities.project import Project
from portfolio.domain.value_objects.link import Link
from portfolio.infrastructure.load_from_json import load_from_json
from portfolio.infrastructure.load_profile_from_json import load_profile_from_json
from portfolio.infrastructure.repositories.sqlite_profile_repository import (
    SqliteProfileRepository,
)
from portfolio.infrastructure.repositories.sqlite_project_repository import (
    SqliteProjectRepository,
)
from portfolio.infrastructure.sqlite_database import SqliteDatabase
from portfolio.infrastructure.sqlite_database_initializer import (
    SqliteDatabaseInitializer,
)
from portfolio.infrastructure.sqlite_portfolio_importer import SqlitePortfolioImporter

SAMPLE_DATA = Path(__file__).resolve().parents[2] / DEFAULT_DATA_DIR

Repositories = tuple[ProjectRepository, ProfileRepository]


def sample_folder(tmp_path: Path) -> Path:
    """The sample data of the repository; nothing is written to `tmp_path`."""
    return SAMPLE_DATA


def unusual_folder(tmp_path: Path) -> Path:
    """Data with every optional value missing and text that needs care."""
    data = tmp_path / "unusual"
    data.mkdir()
    write_json(
        data / PROJECTS_FILE_NAME,
        [
            project_entry(
                title="Æble & <ø>",
                img_url="",
                tags=[],
                skills=[],
                description="Line one\nLine two, 日本語",
            ),
            project_entry(title="Duplicate tags", tags=["a", "a", "b"]),
            project_entry(title="A"),
        ],
    )
    write_json(
        data / PROFILE_FILE_NAME,
        profile_document(name="Zoë Ångström", skills=["C", "C", "Ada"], links=[]),
    )
    return data


FOLDERS: dict[str, Callable[[Path], Path]] = {
    "sample": sample_folder,
    "unusual": unusual_folder,
}


def sqlite_repositories(data: Path, tmp_path: Path) -> Repositories:
    database = SqliteDatabase(tmp_path / "portfolio.db")
    SqliteDatabaseInitializer(database).initialize()
    import_portfolio(
        load_from_json(data / PROJECTS_FILE_NAME),
        load_profile_from_json(data / PROFILE_FILE_NAME),
        SqlitePortfolioImporter(database),
        replace=False,
    )
    return SqliteProjectRepository(database), SqliteProfileRepository(database)


@pytest.fixture(params=sorted(FOLDERS))
def data_folder(request: pytest.FixtureRequest, tmp_path: Path) -> Path:
    return FOLDERS[request.param](tmp_path)


@pytest.fixture
def repositories(data_folder: Path, tmp_path: Path) -> Repositories:
    return sqlite_repositories(data_folder, tmp_path)


def expected_projects(data: Path) -> tuple[Project, ...]:
    entries = json.loads((data / PROJECTS_FILE_NAME).read_text(encoding="utf-8"))
    return tuple(
        Project(
            title=entry["title"],
            kind=entry["type"],
            description=entry["description"],
            image_url=entry["img_url"],
            source_code_url=entry["source_code_url"],
            tags=tuple(entry.get("tags", [])),
            skills=tuple(entry.get("skills", [])),
        )
        for entry in entries
    )


def expected_profile(data: Path) -> Profile:
    document = json.loads((data / PROFILE_FILE_NAME).read_text(encoding="utf-8"))
    return Profile(
        name=document["name"],
        headline=document["headline"],
        summary=document["summary"],
        skills=tuple(document["skills"]),
        links=tuple(Link(link["label"], link["url"]) for link in document["links"]),
        photo=document.get("photo"),
    )


def test_the_repository_returns_the_projects_of_the_data_in_order(
    repositories: Repositories, data_folder: Path
) -> None:
    projects, _ = repositories

    assert tuple(projects.list_projects()) == expected_projects(data_folder)


def test_the_repository_returns_every_field_of_every_project(
    repositories: Repositories, data_folder: Path
) -> None:
    projects, _ = repositories

    for actual, expected in zip(
        projects.list_projects(), expected_projects(data_folder), strict=True
    ):
        assert actual.title == expected.title
        assert actual.kind == expected.kind
        assert actual.description == expected.description
        assert actual.image_url == expected.image_url
        assert actual.source_code_url == expected.source_code_url
        assert actual.tags == expected.tags
        assert actual.skills == expected.skills


def test_the_repository_returns_the_profile_of_the_data(
    repositories: Repositories, data_folder: Path
) -> None:
    _, profile = repositories

    assert profile.get_profile() == expected_profile(data_folder)


def test_the_repository_returns_the_skills_links_and_photo_in_order(
    repositories: Repositories, data_folder: Path
) -> None:
    _, profile_repository = repositories
    expected = expected_profile(data_folder)

    profile = profile_repository.get_profile()

    assert profile.skills == expected.skills
    assert profile.links == expected.links
    assert profile.photo == expected.photo


def test_the_sample_data_has_the_content_the_contract_relies_on() -> None:
    projects = expected_projects(SAMPLE_DATA)
    profile = expected_profile(SAMPLE_DATA)

    assert len(projects) == 6
    assert all(project.tags and project.skills for project in projects)
    assert profile.photo == "images/profile.jpg"
    assert [link.label for link in profile.links] == ["GitHub", "LinkedIn"]
