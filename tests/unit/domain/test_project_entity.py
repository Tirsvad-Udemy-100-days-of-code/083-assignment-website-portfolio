"""Unit tests of the Project entity."""

import dataclasses

import pytest

from portfolio.constants import (
    MAX_DESCRIPTION_LENGTH,
    MAX_KIND_LENGTH,
    MAX_TITLE_LENGTH,
    MAX_URL_LENGTH,
)
from portfolio.domain.errors.domain_error import DomainError
from portfolio.domain.errors.invalid_project_error import InvalidProjectError
from sample_data import make_project


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
        image_url="i" * MAX_URL_LENGTH,
        source_code_url="s" * MAX_URL_LENGTH,
    )
    assert len(project.title) == MAX_TITLE_LENGTH


def test_project_is_immutable() -> None:
    project = make_project()
    with pytest.raises(dataclasses.FrozenInstanceError):
        project.title = "Other"  # type: ignore[misc]


@pytest.mark.parametrize("field", ["title", "kind", "description", "source_code_url"])
@pytest.mark.parametrize("blank", ["", "   ", "\t\n"])
def test_project_rejects_blank_field(field: str, blank: str) -> None:
    with pytest.raises(InvalidProjectError, match=field):
        make_project(**{field: blank})


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
        make_project(**{field: "x" * (limit + 1)})


def test_invalid_project_error_is_a_domain_error() -> None:
    with pytest.raises(DomainError):
        make_project(title="")
