"""!
@file data_file_reader.py
@brief Port through which the use cases read a file of the data folder.
"""

from typing import Protocol


class DataFileReader(Protocol):
    """!
    @brief Source of the files the data refers to, such as images.
    """

    def read_bytes(self, relative_path: str) -> bytes:
        """!
        @brief Read a file of the data folder.
        @param relative_path Path of the file inside the data folder.
        @return The content of the file.
        @throws DataSourceError The path leaves the data folder, or the file is
            missing or cannot be read.
        """
        ...
