"""!
@file site_writer.py
@brief Port through which the use cases write the files of the site.
"""

from typing import Protocol


class SiteWriter(Protocol):
    """!
    @brief Destination of the generated files; the use cases never know where it is.
    """

    def write_text(self, relative_path: str, content: str) -> None:
        """!
        @brief Write a text file inside the site, replacing an existing one.
        @param relative_path Path of the file inside the site, such as `index.html`.
        @param content The text to write.
        @throws SiteWriteError The path leaves the site or the file cannot be written.
        """
        ...

    def write_bytes(self, relative_path: str, content: bytes) -> None:
        """!
        @brief Write a binary file, such as an image, inside the site.
        @param relative_path Path of the file inside the site, such as `images/a.png`.
        @param content The bytes to write.
        @throws SiteWriteError The path leaves the site or the file cannot be written.
        """
        ...
