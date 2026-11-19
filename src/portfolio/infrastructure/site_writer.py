"""!
@file site_writer.py
@brief SiteWriter that writes the files of the site to a folder.
"""

from pathlib import Path

from portfolio.application.errors.site_write_error import SiteWriteError
from portfolio.constants import ENCODING


class FileSiteWriter:
    """!
    @brief Implements the SiteWriter port with a folder on disk.
    """

    def __init__(self, output_dir: Path) -> None:
        """!
        @brief Create the writer.
        @param output_dir The folder of the site; created when it is missing.
        """
        self._root = output_dir.resolve()

    def write_text(self, relative_path: str, content: str) -> None:
        """!
        @brief Write a text file inside the folder, creating the folders it needs.
        @param relative_path Path of the file inside the folder.
        @param content The text to write, stored as UTF-8 with LF line ends.
        @throws SiteWriteError The path leaves the folder or the file cannot be written.
        """
        target = self._resolve(relative_path)
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding=ENCODING, newline="\n")
        except OSError as err:
            raise SiteWriteError(f"cannot write {target}: {err}") from err

    def _resolve(self, relative_path: str) -> Path:
        target = (self._root / relative_path).resolve()
        if target == self._root or not target.is_relative_to(self._root):
            raise SiteWriteError(f"{relative_path!r} is outside the output folder")
        return target
