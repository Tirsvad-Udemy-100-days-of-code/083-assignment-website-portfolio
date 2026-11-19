"""In-memory fakes of the application ports, for the unit tests."""

from collections.abc import Mapping, Sequence

from portfolio.application.dto.about_page import AboutPage
from portfolio.application.dto.home_page import HomePage
from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.application.errors.duplicate_project_error import DuplicateProjectError
from portfolio.application.errors.profile_not_found_error import ProfileNotFoundError
from portfolio.application.errors.project_not_found_error import ProjectNotFoundError
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


class InMemoryProjectStore:
    """Reads and writes projects in a list; stands in for the project database."""

    def __init__(self, projects: Sequence[Project] = ()) -> None:
        self.projects = list(projects)

    def list_projects(self) -> Sequence[Project]:
        return tuple(self.projects)

    def add_project(self, project: Project) -> None:
        if any(stored.title == project.title for stored in self.projects):
            raise DuplicateProjectError(project.title)
        self.projects.append(project)

    def replace_project(self, title: str, project: Project) -> None:
        for place, stored in enumerate(self.projects):
            if stored.title == title:
                self._require_free(project.title, except_place=place)
                self.projects[place] = project
                return
        raise ProjectNotFoundError(title)

    def _require_free(self, title: str, except_place: int) -> None:
        for place, stored in enumerate(self.projects):
            if place != except_place and stored.title == title:
                raise DuplicateProjectError(title)

    def remove_project(self, title: str) -> None:
        for place, stored in enumerate(self.projects):
            if stored.title == title:
                del self.projects[place]
                return
        raise ProjectNotFoundError(title)


class InMemoryProfileStore:
    """Reads and writes the profile in a field; stands in for the profile database."""

    def __init__(self, profile: Profile | None = None) -> None:
        self.profile = profile

    def get_profile(self) -> Profile:
        if self.profile is None:
            raise ProfileNotFoundError
        return self.profile

    def save_profile(self, profile: Profile) -> None:
        self.profile = profile


class FakeDatabaseInitializer:
    def __init__(self, created: bool) -> None:
        self._created = created
        self.calls = 0

    def initialize(self) -> bool:
        self.calls += 1
        return self._created


class FakeImportTarget:
    def __init__(self, empty: bool = True) -> None:
        self._empty = empty
        self.imported: tuple[Sequence[Project], Profile] | None = None

    def is_empty(self) -> bool:
        return self._empty

    def replace_all(self, projects: Sequence[Project], profile: Profile) -> None:
        self.imported = (projects, profile)
