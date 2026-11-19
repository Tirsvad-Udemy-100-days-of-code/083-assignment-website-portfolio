"""!
@file json_project_repository.py
@brief ProjectRepository that reads a JSON file.
"""

from collections.abc import Sequence
from pathlib import Path

from portfolio.domain.entities.project import Project
from portfolio.infrastructure.load_from_json import load_from_json


class JsonProjectRepository:
    """!
    @brief Implements the ProjectRepository port with a JSON file.
    """

    def __init__(self, path: Path) -> None:
        """!
        @brief Create the repository.
        @param path The JSON file with the projects.
        """
        self._path = path

    def list_projects(self) -> Sequence[Project]:
        """!
        @brief Read every project, in the order of the file.
        @return The projects.
        @throws DataFileError The file cannot be used.
        """
        return load_from_json(self._path)
