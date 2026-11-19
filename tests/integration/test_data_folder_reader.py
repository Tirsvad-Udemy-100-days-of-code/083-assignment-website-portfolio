"""Integration tests of the data folder reader."""

import os
from pathlib import Path

import pytest

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.infrastructure.data_folder_reader import FolderDataFileReader
from portfolio.infrastructure.errors.data_file_error import DataFileError


def test_reader_reads_the_bytes_of_a_file(tmp_path: Path) -> None:
    (tmp_path / "images").mkdir()
    (tmp_path / "images" / "a.png").write_bytes(b"\x89PNG\x00\xff")
    assert (
        FolderDataFileReader(tmp_path).read_bytes("images/a.png") == b"\x89PNG\x00\xff"
    )


def test_reader_reports_a_missing_file_with_its_path(tmp_path: Path) -> None:
    with pytest.raises(DataFileError, match="file not found") as error:
        FolderDataFileReader(tmp_path).read_bytes("images/none.png")
    assert "none.png" in str(error.value)
    assert isinstance(error.value, DataSourceError)


def test_reader_reports_a_folder_as_unreadable(tmp_path: Path) -> None:
    (tmp_path / "images").mkdir()
    with pytest.raises(DataFileError, match="cannot read"):
        FolderDataFileReader(tmp_path).read_bytes("images")


@pytest.mark.parametrize(
    "relative_path", ["../outside.png", "a/../../outside.png", "..", ".", ""]
)
def test_reader_refuses_a_path_that_leaves_the_data_folder(
    tmp_path: Path, relative_path: str
) -> None:
    (tmp_path / "outside.png").write_bytes(b"secret")
    data = tmp_path / "data"
    data.mkdir()
    with pytest.raises(DataFileError, match="outside the data folder"):
        FolderDataFileReader(data).read_bytes(relative_path)


def test_reader_refuses_an_absolute_path(tmp_path: Path) -> None:
    target = tmp_path / "elsewhere.png"
    target.write_bytes(b"secret")
    data = tmp_path / "data"
    data.mkdir()
    with pytest.raises(DataFileError, match="outside the data folder"):
        FolderDataFileReader(data).read_bytes(str(target))


def test_reader_refuses_a_symbolic_link_that_points_out_of_the_folder(
    tmp_path: Path,
) -> None:
    (tmp_path / "secret.png").write_bytes(b"secret")
    data = tmp_path / "data"
    data.mkdir()
    try:
        os.symlink(tmp_path / "secret.png", data / "link.png")
    except (OSError, NotImplementedError):
        pytest.skip("symbolic links are not available here")
    with pytest.raises(DataFileError, match="outside the data folder"):
        FolderDataFileReader(data).read_bytes("link.png")
