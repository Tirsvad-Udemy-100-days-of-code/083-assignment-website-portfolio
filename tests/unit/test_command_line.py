"""Unit tests of the command line parser of the composition root."""

from pathlib import Path

import pytest

from portfolio import __main__ as entry_point
from portfolio import constants


def test_serve_defaults_come_from_the_constants() -> None:
    arguments = entry_point.build_parser().parse_args(["serve"])
    assert arguments.db == Path(constants.DEFAULT_DATABASE_PATH)
    assert arguments.data == Path(constants.DEFAULT_DATA_DIR)
    assert arguments.host == constants.DEFAULT_HOST
    assert arguments.port == constants.DEFAULT_PORT


def test_serve_takes_db_data_host_and_port() -> None:
    arguments = entry_point.build_parser().parse_args(
        [
            "serve",
            "--db",
            "x.db",
            "--data",
            "d",
            "--host",
            "localhost",
            "--port",
            "9000",
        ]
    )
    assert (arguments.db, arguments.data, arguments.host, arguments.port) == (
        Path("x.db"),
        Path("d"),
        "localhost",
        9000,
    )


@pytest.mark.parametrize("port", ["0", "1", "8000", "65535"])
def test_serve_accepts_a_port_number(port: str) -> None:
    arguments = entry_point.build_parser().parse_args(["serve", "--port", port])
    assert arguments.port == int(port)


@pytest.mark.parametrize("port", ["-1", "65536", "99999", "http", "", "80.5"])
def test_serve_rejects_a_value_that_is_not_a_port_number(
    port: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        entry_point.build_parser().parse_args(["serve", "--port", port])
    assert exit_info.value.code == constants.EXIT_DATA_ERROR
    assert "is not a port number from 0 to 65535" in capsys.readouterr().err


def test_build_is_no_longer_a_command() -> None:
    with pytest.raises(SystemExit) as exit_info:
        entry_point.main(["build"])
    assert exit_info.value.code == constants.EXIT_DATA_ERROR


def test_main_prints_the_help_without_a_command(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert entry_point.main([]) == constants.EXIT_OK
    out = capsys.readouterr().out
    assert "{init,import,project,profile,serve}" in out


def test_main_rejects_an_unknown_command() -> None:
    with pytest.raises(SystemExit) as exit_info:
        entry_point.main(["publish"])
    assert exit_info.value.code == constants.EXIT_DATA_ERROR


def test_database_commands_default_to_the_database_of_the_constants() -> None:
    parser = entry_point.build_parser()
    for command in (
        ["init"],
        ["import"],
        ["project", "list"],
        ["project", "remove", "A"],
        ["profile", "set"],
    ):
        arguments = parser.parse_args(command)
        assert arguments.db == Path(constants.DEFAULT_DATABASE_PATH)


def test_import_takes_db_data_and_replace() -> None:
    arguments = entry_point.build_parser().parse_args(
        ["import", "--db", "x.db", "--data", "d", "--replace"]
    )
    assert (arguments.db, arguments.data, arguments.replace) == (
        Path("x.db"),
        Path("d"),
        True,
    )


def test_import_defaults_to_the_data_folder_and_no_replace() -> None:
    arguments = entry_point.build_parser().parse_args(["import"])
    assert arguments.data == Path(constants.DEFAULT_DATA_DIR)
    assert arguments.replace is False


def test_project_add_collects_the_repeated_tags_and_skills() -> None:
    arguments = entry_point.build_parser().parse_args(
        [
            "project",
            "add",
            "--title",
            "T",
            "--kind",
            "K",
            "--description",
            "D",
            "--source-code-url",
            "https://e.com",
            "--tag",
            "a",
            "--tag",
            "b",
            "--skill",
            "s",
        ]
    )
    assert arguments.tag == ["a", "b"]
    assert arguments.skill == ["s"]
    assert arguments.image_url == ""


def test_project_add_requires_the_title() -> None:
    with pytest.raises(SystemExit) as exit_info:
        entry_point.build_parser().parse_args(["project", "add"])
    assert exit_info.value.code == constants.EXIT_DATA_ERROR


def test_project_set_leaves_unnamed_options_unset() -> None:
    arguments = entry_point.build_parser().parse_args(
        ["project", "set", "Old", "--new-title", "New"]
    )
    assert arguments.title == "Old"
    assert arguments.new_title == "New"
    assert arguments.tag is None
    assert arguments.kind is None


def test_profile_set_collects_the_repeated_links() -> None:
    arguments = entry_point.build_parser().parse_args(
        ["profile", "set", "--link", "A=https://a.com", "--link", "B=https://b.com"]
    )
    assert arguments.link == ["A=https://a.com", "B=https://b.com"]
    assert arguments.name is None


def test_main_lists_the_database_commands_in_the_help(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert entry_point.main([]) == constants.EXIT_OK
    out = capsys.readouterr().out
    for name in (
        constants.COMMAND_INIT,
        constants.COMMAND_IMPORT,
        constants.COMMAND_PROJECT,
        constants.COMMAND_PROFILE,
    ):
        assert name in out
