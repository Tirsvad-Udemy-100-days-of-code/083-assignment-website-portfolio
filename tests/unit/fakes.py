"""In-memory fakes of the application ports, for the unit tests."""

from collections.abc import Mapping, Sequence

from portfolio.application.dto.about_page import AboutPage
from portfolio.application.dto.home_page import HomePage
from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.domain.entities.profile import Profile
from portfolio.domain.entities.project import Project


class InMemoryProjectRepository:
    def __init__(self, projects: Sequence[Project]) -> None:
        self._projects = projects

    def list_projects(self) -> Sequence[Project]:
        return self._projects


class InMemoryProfileRepository:
    def __init__(self, profile: Profile) -> None:
        self._profile = profile

    def get_profile(self) -> Profile:
        return self._profile


class InMemorySiteWriter:
    def __init__(self) -> None:
        self.files: dict[str, str] = {}
        self.binary_files: dict[str, bytes] = {}

    def write_text(self, relative_path: str, content: str) -> None:
        self.files[relative_path] = content

    def write_bytes(self, relative_path: str, content: bytes) -> None:
        self.binary_files[relative_path] = content


class InMemoryDataFileReader:
    def __init__(self, files: Mapping[str, bytes] | None = None) -> None:
        self._files = files or {}
        self.reads: list[str] = []

    def read_bytes(self, relative_path: str) -> bytes:
        self.reads.append(relative_path)
        if relative_path not in self._files:
            raise DataSourceError(f"{relative_path}: file not found")
        return self._files[relative_path]


class StubSiteRenderer:
    """Returns short markers, so a test sees which page data was rendered."""

    def render_home(self, page: HomePage) -> str:
        return f"home:{len(page.projects)}"

    def render_about(self, page: AboutPage) -> str:
        return f"about:{page.name}"

    def stylesheet(self) -> str:
        return "css"
