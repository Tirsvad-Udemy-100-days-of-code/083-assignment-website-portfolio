"""Unit tests of the command line parser of the composition root."""

from pathlib import Path

import pytest

from portfolio import __main__ as entry_point
from portfolio import constants


def test_build_defaults_come_from_the_constants() -> None:
    arguments = entry_point.build_parser().parse_args(["build"])
    assert arguments.data == Path(constants.DEFAULT_DATA_DIR)
    assert arguments.out == Path(constants.DEFAULT_OUTPUT_DIR)


def test_build_takes_data_and_out() -> None:
    arguments = entry_point.build_parser().parse_args(
        ["build", "--data", "d", "--out", "o"]
    )
    assert (arguments.data, arguments.out) == (Path("d"), Path("o"))


def test_serve_defaults_come_from_the_constants() -> None:
    arguments = entry_point.build_parser().parse_args(["serve"])
    assert arguments.out == Path(constants.DEFAULT_OUTPUT_DIR)
    assert arguments.host == constants.DEFAULT_HOST
    assert arguments.port == constants.DEFAULT_PORT


def test_serve_takes_out_host_and_port() -> None:
    arguments = entry_point.build_parser().parse_args(
        ["serve", "--out", "o", "--host", "localhost", "--port", "9000"]
    )
    assert (arguments.out, arguments.host, arguments.port) == (
        Path("o"),
        "localhost",
        9000,
    )


def test_main_prints_the_help_without_a_command(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert entry_point.main([]) == constants.EXIT_OK
    out = capsys.readouterr().out
    assert constants.COMMAND_BUILD in out
    assert constants.COMMAND_SERVE in out


def test_main_rejects_an_unknown_command() -> None:
    with pytest.raises(SystemExit) as exit_info:
        entry_point.main(["publish"])
    assert exit_info.value.code == constants.EXIT_DATA_ERROR
