"""Unit tests of the build command."""

from pathlib import Path

import pytest

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.application.errors.site_write_error import SiteWriteError
from portfolio.constants import EXIT_DATA_ERROR, EXIT_OK, EXIT_OUTPUT_ERROR
from portfolio.presentation.commands.build_command import BuildCommand


def test_build_command_passes_the_folders_and_reports_the_count(
    capsys: pytest.CaptureFixture[str],
) -> None:
    calls: list[tuple[Path, Path]] = []

    def build(data_dir: Path, output_dir: Path) -> tuple[str, ...]:
        calls.append((data_dir, output_dir))
        return ("index.html", "about.html", "style.css")

    code = BuildCommand(build).run(Path("in"), Path("out"))

    captured = capsys.readouterr()
    assert code == EXIT_OK
    assert calls == [(Path("in"), Path("out"))]
    assert "Built 3 files into out" in captured.out
    assert captured.err == ""


def test_build_command_reports_a_data_error_on_one_line(
    capsys: pytest.CaptureFixture[str],
) -> None:
    def build(data_dir: Path, output_dir: Path) -> tuple[str, ...]:
        raise DataSourceError("data/projects.json: file not found")

    code = BuildCommand(build).run(Path("data"), Path("out"))

    captured = capsys.readouterr()
    assert code == EXIT_DATA_ERROR
    assert captured.out == ""
    assert captured.err == "error: data/projects.json: file not found\n"


def test_build_command_reports_a_write_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    def build(data_dir: Path, output_dir: Path) -> tuple[str, ...]:
        raise SiteWriteError("cannot write out/index.html: denied")

    code = BuildCommand(build).run(Path("data"), Path("out"))

    assert code == EXIT_OUTPUT_ERROR
    assert "cannot write out/index.html: denied" in capsys.readouterr().err
