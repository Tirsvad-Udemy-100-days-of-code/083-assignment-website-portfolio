"""Integration tests of the file site writer."""

from pathlib import Path

import pytest

from portfolio.application.errors.site_write_error import SiteWriteError
from portfolio.infrastructure.site_writer import FileSiteWriter


def test_writer_writes_a_file_and_creates_the_output_folder(tmp_path: Path) -> None:
    output = tmp_path / "site" / "build"
    FileSiteWriter(output).write_text("index.html", "<p>hi</p>")
    assert (output / "index.html").read_text(encoding="utf-8") == "<p>hi</p>"


def test_writer_replaces_an_existing_file(tmp_path: Path) -> None:
    writer = FileSiteWriter(tmp_path)
    writer.write_text("a.txt", "old")
    writer.write_text("a.txt", "new")
    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "new"


def test_writer_creates_the_folders_of_a_nested_path(tmp_path: Path) -> None:
    FileSiteWriter(tmp_path).write_text("css/deep/style.css", "body {}")
    assert (tmp_path / "css" / "deep" / "style.css").is_file()


def test_writer_stores_unicode_as_utf8_with_lf_line_ends(tmp_path: Path) -> None:
    FileSiteWriter(tmp_path).write_text("a.html", "Blåbær 東京\nline two\n")
    assert (tmp_path / "a.html").read_bytes() == "Blåbær 東京\nline two\n".encode()


@pytest.mark.parametrize(
    "relative_path",
    ["../outside.txt", "a/../../outside.txt", "..", ".", ""],
)
def test_writer_refuses_a_path_that_leaves_the_output_folder(
    tmp_path: Path, relative_path: str
) -> None:
    output = tmp_path / "site"
    with pytest.raises(SiteWriteError, match="outside the output folder"):
        FileSiteWriter(output).write_text(relative_path, "x")
    assert not (tmp_path / "outside.txt").exists()


def test_writer_refuses_an_absolute_path(tmp_path: Path) -> None:
    target = tmp_path / "elsewhere.txt"
    with pytest.raises(SiteWriteError, match="outside the output folder"):
        FileSiteWriter(tmp_path / "site").write_text(str(target), "x")
    assert not target.exists()


def test_writer_reports_a_file_that_cannot_be_written(tmp_path: Path) -> None:
    blocker = tmp_path / "blocker"
    blocker.write_text("a file where a folder is needed", encoding="utf-8")
    with pytest.raises(SiteWriteError, match="cannot write") as error:
        FileSiteWriter(tmp_path).write_text("blocker/index.html", "x")
    assert isinstance(error.value.__cause__, OSError)
