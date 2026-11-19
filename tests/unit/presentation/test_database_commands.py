"""Unit tests of the commands that create, fill and manage the database."""

from pathlib import Path

import pytest

from portfolio.application.dto.link_item import LinkItem
from portfolio.application.dto.profile_changes import ProfileChanges
from portfolio.application.dto.project_card import ProjectCard
from portfolio.application.dto.project_changes import ProjectChanges
from portfolio.application.dto.project_input import ProjectInput
from portfolio.application.errors.database_not_empty_error import (
    DatabaseNotEmptyError,
)
from portfolio.application.errors.project_not_found_error import ProjectNotFoundError
from portfolio.application.errors.schema_version_error import SchemaVersionError
from portfolio.constants import EXIT_DATA_ERROR, EXIT_OK, SCHEMA_VERSION
from portfolio.domain.errors.invalid_project_error import InvalidProjectError
from portfolio.presentation.commands.import_command import ImportCommand
from portfolio.presentation.commands.init_command import InitCommand
from portfolio.presentation.commands.profile_set_command import ProfileSetCommand
from portfolio.presentation.commands.project_add_command import ProjectAddCommand
from portfolio.presentation.commands.project_list_command import ProjectListCommand
from portfolio.presentation.commands.project_remove_command import (
    ProjectRemoveCommand,
)
from portfolio.presentation.commands.project_set_command import ProjectSetCommand
from portfolio.presentation.shared.link_option import parse_link
from portfolio.presentation.shared.usage_error import UsageError

DATABASE = Path("portfolio.db")


def test_init_command_reports_a_created_database(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = InitCommand(lambda path: True).run(DATABASE)

    captured = capsys.readouterr()
    assert code == EXIT_OK
    assert f"Created the database {DATABASE}" in captured.out
    assert f"schema version {SCHEMA_VERSION}" in captured.out
    assert captured.err == ""


def test_init_command_reports_a_database_that_is_up_to_date(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = InitCommand(lambda path: False).run(DATABASE)

    assert code == EXIT_OK
    assert "is up to date" in capsys.readouterr().out


def test_init_command_reports_a_newer_schema_on_one_line(
    capsys: pytest.CaptureFixture[str],
) -> None:
    def initialize(path: Path) -> bool:
        raise SchemaVersionError("the database has schema version 9, too new")

    code = InitCommand(initialize).run(DATABASE)

    captured = capsys.readouterr()
    assert code == EXIT_DATA_ERROR
    assert captured.out == ""
    assert captured.err == "error: the database has schema version 9, too new\n"


def test_import_command_passes_its_arguments_and_reports_the_count(
    capsys: pytest.CaptureFixture[str],
) -> None:
    calls: list[tuple[Path, Path, bool]] = []

    def import_data(database: Path, data_dir: Path, replace: bool) -> int:
        calls.append((database, data_dir, replace))
        return 6

    code = ImportCommand(import_data).run(DATABASE, Path("data"), True)

    assert code == EXIT_OK
    assert calls == [(DATABASE, Path("data"), True)]
    assert "Imported 6 projects" in capsys.readouterr().out


def test_import_command_reports_a_database_that_holds_data(
    capsys: pytest.CaptureFixture[str],
) -> None:
    def import_data(database: Path, data_dir: Path, replace: bool) -> int:
        raise DatabaseNotEmptyError

    code = ImportCommand(import_data).run(DATABASE, Path("data"), False)

    assert code == EXIT_DATA_ERROR
    assert "--replace" in capsys.readouterr().err


def test_project_list_command_prints_one_line_per_project(
    capsys: pytest.CaptureFixture[str],
) -> None:
    card = ProjectCard("A", "Web", "d", "", "https://e.com", (), ())

    code = ProjectListCommand(lambda path: (card,)).run(DATABASE)

    assert code == EXIT_OK
    assert capsys.readouterr().out == "A | Web | https://e.com\n"


def test_project_list_command_says_so_when_there_is_no_project(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = ProjectListCommand(lambda path: ()).run(DATABASE)

    assert code == EXIT_OK
    assert capsys.readouterr().out == "No projects.\n"


def test_project_add_command_reports_an_invalid_value_on_one_line(
    capsys: pytest.CaptureFixture[str],
) -> None:
    def add(database: Path, data: ProjectInput) -> None:
        raise InvalidProjectError("title must not be blank")

    data = ProjectInput("", "k", "d", "https://e.com")
    code = ProjectAddCommand(add).run(DATABASE, data)

    captured = capsys.readouterr()
    assert code == EXIT_DATA_ERROR
    assert captured.err == "error: title must not be blank\n"
    assert captured.out == ""


def test_project_add_command_reports_the_added_title(
    capsys: pytest.CaptureFixture[str],
) -> None:
    added: list[ProjectInput] = []
    data = ProjectInput("A", "k", "d", "https://e.com")

    code = ProjectAddCommand(lambda path, value: added.append(value)).run(
        DATABASE, data
    )

    assert code == EXIT_OK
    assert added == [data]
    assert "Added the project 'A'" in capsys.readouterr().out


def test_project_set_command_reports_the_new_title(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = ProjectSetCommand(lambda path, title, changes: "New").run(
        DATABASE, "Old", ProjectChanges(title="New")
    )

    assert code == EXIT_OK
    assert "Changed the project 'New'" in capsys.readouterr().out


def test_project_set_command_reports_a_missing_project(
    capsys: pytest.CaptureFixture[str],
) -> None:
    def change(database: Path, title: str, changes: ProjectChanges) -> str:
        raise ProjectNotFoundError(title)

    code = ProjectSetCommand(change).run(DATABASE, "Old", ProjectChanges(kind="k"))

    assert code == EXIT_DATA_ERROR
    assert capsys.readouterr().err == "error: no project has the title 'Old'\n"


def test_project_remove_command_reports_the_removed_title(
    capsys: pytest.CaptureFixture[str],
) -> None:
    removed: list[str] = []

    code = ProjectRemoveCommand(lambda path, title: removed.append(title)).run(
        DATABASE, "A"
    )

    assert code == EXIT_OK
    assert removed == ["A"]
    assert "Removed the project 'A'" in capsys.readouterr().out


def test_profile_set_command_parses_the_links_and_reports_a_new_profile(
    capsys: pytest.CaptureFixture[str],
) -> None:
    received: list[ProfileChanges] = []

    def set_profile(database: Path, changes: ProfileChanges) -> bool:
        received.append(changes)
        return True

    code = ProfileSetCommand(set_profile).run(
        DATABASE, ProfileChanges(name="Ada"), ["Site=https://e.com/?a=b"]
    )

    assert code == EXIT_OK
    assert received == [
        ProfileChanges(name="Ada", links=(LinkItem("Site", "https://e.com/?a=b"),))
    ]
    assert capsys.readouterr().out == "Created the profile\n"


def test_profile_set_command_keeps_the_links_when_none_are_given(
    capsys: pytest.CaptureFixture[str],
) -> None:
    received: list[ProfileChanges] = []

    def set_profile(database: Path, changes: ProfileChanges) -> bool:
        received.append(changes)
        return False

    code = ProfileSetCommand(set_profile).run(
        DATABASE, ProfileChanges(headline="h"), None
    )

    assert code == EXIT_OK
    assert received[0].links is None
    assert capsys.readouterr().out == "Changed the profile\n"


def test_profile_set_command_reports_a_link_without_separator(
    capsys: pytest.CaptureFixture[str],
) -> None:
    calls: list[ProfileChanges] = []

    def set_profile(database: Path, changes: ProfileChanges) -> bool:
        calls.append(changes)
        return True

    code = ProfileSetCommand(set_profile).run(DATABASE, ProfileChanges(), ["nolink"])

    assert code == EXIT_DATA_ERROR
    assert calls == []
    assert capsys.readouterr().err == "error: link 'nolink' must look like LABEL=URL\n"


def test_parse_link_splits_at_the_first_separator() -> None:
    assert parse_link("A=b=c") == LinkItem("A", "b=c")


def test_parse_link_without_a_separator_is_refused() -> None:
    with pytest.raises(UsageError):
        parse_link("abc")
