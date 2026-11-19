"""!
@file data_folder_reader.py
@brief DataFileReader that reads the files of the data folder.
"""

from pathlib import Path

from portfolio.infrastructure.confined_path import resolve_inside
from portfolio.infrastructure.errors.data_file_error import DataFileError


class FolderDataFileReader:
    """!
    @brief Implements the DataFileReader port with a folder on disk.
    """

    def __init__(self, data_dir: Path) -> None:
        """!
        @brief Create the reader.
        @param data_dir The data folder.
        """
        self._root = data_dir.resolve()

    def read_bytes(self, relative_path: str) -> bytes:
        """!
        @brief Read a file inside the data folder.
        @param relative_path Path of the file inside the data folder.
        @return The content of the file.
        @throws DataFileError The path leaves the folder, or the file is missing or
            cannot be read.
        """
        target = resolve_inside(self._root, relative_path)
        if target is None:
            raise DataFileError(
                self._root / relative_path,
                f"{relative_path!r} is outside the data folder",
            )
        try:
            return target.read_bytes()
        except FileNotFoundError as err:
            raise DataFileError(target, "file not found") from err
        except OSError as err:
            raise DataFileError(target, f"cannot read the file: {err}") from err
