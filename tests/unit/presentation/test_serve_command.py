"""Unit tests of the serve command."""

from pathlib import Path

import pytest

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.constants import EXIT_DATA_ERROR, EXIT_OK, EXIT_SERVER_ERROR
from portfolio.presentation.commands.serve_command import ServeCommand

DATABASE = Path("data/portfolio.db")
DATA = Path("data")


class RecordingRunner:
    def __init__(self, error: Exception | None = None) -> None:
        self.calls: list[tuple[Path, Path, str, int]] = []
        self._error = error

    def __call__(self, database: Path, data: Path, host: str, port: int) -> None:
        self.calls.append((database, data, host, port))
        if self._error is not None:
            raise self._error


class RecordingCheck:
    def __init__(self, error: Exception | None = None) -> None:
        self.calls: list[Path] = []
        self._error = error

    def __call__(self, database: Path) -> None:
        self.calls.append(database)
        if self._error is not None:
            raise self._error


def test_serve_command_checks_the_database_then_runs_the_server() -> None:
    check, runner = RecordingCheck(), RecordingRunner()

    code = ServeCommand(check, runner).run(DATABASE, DATA, "127.0.0.1", 8123)

    assert code == EXIT_OK
    assert check.calls == [DATABASE]
    assert runner.calls == [(DATABASE, DATA, "127.0.0.1", 8123)]


def test_serve_command_names_init_and_import_when_the_database_is_missing(
    capsys: pytest.CaptureFixture[str],
) -> None:
    check = RecordingCheck(DataSourceError("database not found"))
    runner = RecordingRunner()

    code = ServeCommand(check, runner).run(DATABASE, DATA, "127.0.0.1", 8000)

    err = capsys.readouterr().err
    assert code == EXIT_DATA_ERROR
    assert runner.calls == []
    assert err.startswith("error: database ")
    assert str(DATABASE) in err
    assert "python -m portfolio init" in err
    assert "python -m portfolio import" in err
    assert err.count("\n") == 1
    assert "Traceback" not in err


def test_serve_command_reports_a_port_that_cannot_be_bound(
    capsys: pytest.CaptureFixture[str],
) -> None:
    runner = RecordingRunner(OSError("address already in use"))

    code = ServeCommand(RecordingCheck(), runner).run(DATABASE, DATA, "127.0.0.1", 8000)

    assert code == EXIT_SERVER_ERROR
    assert "127.0.0.1:8000: address already in use" in capsys.readouterr().err


def test_serve_command_reports_a_port_out_of_range(
    capsys: pytest.CaptureFixture[str],
) -> None:
    runner = RecordingRunner(OverflowError("bind(): port must be 0-65535."))

    code = ServeCommand(RecordingCheck(), runner).run(
        DATABASE, DATA, "127.0.0.1", 99999
    )

    assert code == EXIT_SERVER_ERROR
    assert "port must be 0-65535" in capsys.readouterr().err
