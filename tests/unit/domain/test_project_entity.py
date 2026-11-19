"""Unit tests of the Project entity."""

import dataclasses
from collections.abc import Callable

import pytest

from portfolio.constants import (
    MAX_DESCRIPTION_LENGTH,
    MAX_KIND_LENGTH,
    MAX_PROJECT_SKILLS,
    MAX_SKILL_LENGTH,
    MAX_TAG_LENGTH,
    MAX_TAGS,
    MAX_TITLE_LENGTH,
    MAX_URL_LENGTH,
)
from portfolio.domain.entities.project import Project
from portfolio.domain.errors.domain_error import DomainError
from portfolio.domain.errors.invalid_project_error import InvalidProjectError
from sample_data import make_project


def project_with(field: str, value: str) -> Project:
    """Build a valid project in which one text field has the given value."""
    return Project(**(dataclasses.asdict(make_project()) | {field: value}))


def test_project_keeps_its_data_when_valid() -> None:
    project = make_project()
    assert project.title == "Weather app"
    assert project.kind == "Web app"


def test_project_accepts_empty_image_url() -> None:
    assert make_project(image_url="").image_url == ""


def test_project_accepts_values_at_the_limits() -> None:
    project = make_project(
        title="t" * MAX_TITLE_LENGTH,
        kind="k" * MAX_KIND_LENGTH,
        description="d" * MAX_DESCRIPTION_LENGTH,
        image_url="i" * (MAX_URL_LENGTH - len(".png")) + ".png",
        source_code_url="s" * MAX_URL_LENGTH,
        tags=("t" * MAX_TAG_LENGTH,) * MAX_TAGS,
        skills=("s" * MAX_SKILL_LENGTH,) * MAX_PROJECT_SKILLS,
    )
    assert len(project.title) == MAX_TITLE_LENGTH
    assert len(project.tags) == MAX_TAGS
    assert len(project.skills) == MAX_PROJECT_SKILLS


def test_project_has_no_tags_and_no_skills_by_default() -> None:
    project = Project("t", "k", "d", "", "https://example.com")
    assert project.tags == ()
    assert project.skills == ()


@pytest.mark.parametrize(
    "image_url",
    [
        "https://example.com/a.png",
        "http://example.com/image",
        "images/a.svg",
        "a.JPG",
        "deep/er/photo.webp",
    ],
)
def test_project_accepts_an_address_or_a_relative_image_path(image_url: str) -> None:
    assert make_project(image_url=image_url).image_url == image_url


@pytest.mark.parametrize(
    "image_url",
    [
        "javascript:alert(1)",
        "data:image/png;base64,AAAA",
        "file:///etc/passwd",
        "ftp://example.com/a.png",
        "https://",
        "//evil.example.com/a.png",
        "/etc/passwd.png",
        "../a.png",
        "images/../../a.png",
        "images//a.png",
        "C:/a.png",
        r"images\a.png",
        "images/a.png?x=1",
        "images/a.png#top",
        " images/a.png",
        "images/notes.txt",
        "images/profile",
        "https://exa mple.com/a.png",
    ],
)
def test_project_rejects_an_unsafe_image(image_url: str) -> None:
    with pytest.raises(InvalidProjectError, match="image_url must be"):
        make_project(image_url=image_url)


@pytest.mark.parametrize(
    "build",
    [
        lambda: make_project(tags=("Python", "  ")),
        lambda: make_project(skills=("Python", "  ")),
    ],
    ids=["tags", "skills"],
)
def test_project_rejects_a_blank_tag_or_skill(build: Callable[[], Project]) -> None:
    with pytest.raises(InvalidProjectError, match="must not be blank"):
        build()


@pytest.mark.parametrize(
    ("build", "match"),
    [
        (
            lambda: make_project(tags=("x" * (MAX_TAG_LENGTH + 1),)),
            "tag must be at most",
        ),
        (
            lambda: make_project(skills=("x" * (MAX_SKILL_LENGTH + 1),)),
            "skill must be at most",
        ),
    ],
    ids=["tag", "skill"],
)
def test_project_rejects_a_tag_or_skill_one_over_the_limit(
    build: Callable[[], Project], match: str
) -> None:
    with pytest.raises(InvalidProjectError, match=match):
        build()


@pytest.mark.parametrize(
    "build",
    [
        lambda: make_project(tags=("x",) * (MAX_TAGS + 1)),
        lambda: make_project(skills=("x",) * (MAX_PROJECT_SKILLS + 1)),
    ],
    ids=["tags", "skills"],
)
def test_project_rejects_one_entry_too_many(build: Callable[[], Project]) -> None:
    with pytest.raises(InvalidProjectError, match="at most"):
        build()


def test_project_is_immutable() -> None:
    project = make_project()
    with pytest.raises(dataclasses.FrozenInstanceError):
        project.title = "Other"  # type: ignore[misc]


@pytest.mark.parametrize("field", ["title", "kind", "description", "source_code_url"])
@pytest.mark.parametrize("blank", ["", "   ", "\t\n"])
def test_project_rejects_blank_field(field: str, blank: str) -> None:
    with pytest.raises(InvalidProjectError, match=field):
        project_with(field, blank)


@pytest.mark.parametrize(
    ("field", "limit"),
    [
        ("title", MAX_TITLE_LENGTH),
        ("kind", MAX_KIND_LENGTH),
        ("description", MAX_DESCRIPTION_LENGTH),
        ("image_url", MAX_URL_LENGTH),
        ("source_code_url", MAX_URL_LENGTH),
    ],
)
def test_project_rejects_field_one_over_the_limit(field: str, limit: int) -> None:
    with pytest.raises(InvalidProjectError, match=field):
        project_with(field, "x" * (limit + 1))


def test_invalid_project_error_is_a_domain_error() -> None:
    with pytest.raises(DomainError):
        make_project(title="")
