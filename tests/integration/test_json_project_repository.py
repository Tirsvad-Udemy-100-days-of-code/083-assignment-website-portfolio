"""Integration tests of the JSON project repository."""

from pathlib import Path

import pytest

from data_files import project_entry, write_json
from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.infrastructure.repositories.json_project_repository import (
    JsonProjectRepository,
)


def test_repository_lists_the_projects_of_the_file(tmp_path: Path) -> None:
    path = write_json(tmp_path / "projects.json", [project_entry(title="One")])
    projects = JsonProjectRepository(path).list_projects()
    assert [project.title for project in projects] == ["One"]


def test_repository_reads_the_file_again_on_each_call(tmp_path: Path) -> None:
    path = write_json(tmp_path / "projects.json", [])
    repository = JsonProjectRepository(path)
    assert repository.list_projects() == ()
    write_json(path, [project_entry()])
    assert len(repository.list_projects()) == 1


def test_repository_reports_a_missing_file_as_a_data_source_error(
    tmp_path: Path,
) -> None:
    with pytest.raises(DataSourceError, match=r"projects\.json: file not found"):
        JsonProjectRepository(tmp_path / "projects.json").list_projects()
