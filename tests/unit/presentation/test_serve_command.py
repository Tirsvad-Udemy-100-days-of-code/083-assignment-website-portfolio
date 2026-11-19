"""Unit tests of the serve command."""

from pathlib import Path

import pytest

from portfolio.constants import EXIT_OK, EXIT_OUTPUT_ERROR, EXIT_SERVER_ERROR
from portfolio.presentation.commands.serve_command import ServeCommand


class RecordingRunner:
    def __init__(self, error: Exception | None = None) -> None:
        self.calls: list[tuple[Path, str, int]] = []
        self._error = error

    def __call__(self, directory: Path, host: str, port: int) -> None:
        self.calls.append((directory, host, port))
        if self._error is not None:
            raise self._error


def test_serve_command_runs_the_server_on_the_folder(tmp_path: Path) -> None:
    runner = RecordingRunner()
    code = ServeCommand(runner).run(tmp_path, "127.0.0.1", 8123)
    assert code == EXIT_OK
    assert runner.calls == [(tmp_path, "127.0.0.1", 8123)]


def test_serve_command_refuses_a_missing_folder(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    runner = RecordingRunner()
    missing = tmp_path / "nothing"
    code = ServeCommand(runner).run(missing, "127.0.0.1", 8000)
    err = capsys.readouterr().err
    assert code == EXIT_OUTPUT_ERROR
    assert runner.calls == []
    assert f"output folder {missing} does not exist" in err
    assert err.count("\n") == 1


def test_serve_command_refuses_a_file_in_place_of_the_folder(tmp_path: Path) -> None:
    a_file = tmp_path / "file.txt"
    a_file.write_text("x", encoding="utf-8")
    runner = RecordingRunner()
    assert ServeCommand(runner).run(a_file, "127.0.0.1", 8000) == EXIT_OUTPUT_ERROR
    assert runner.calls == []


def test_serve_command_reports_a_port_that_cannot_be_bound(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    runner = RecordingRunner(OSError("address already in use"))
    code = ServeCommand(runner).run(tmp_path, "127.0.0.1", 8000)
    assert code == EXIT_SERVER_ERROR
    assert "127.0.0.1:8000: address already in use" in capsys.readouterr().err
