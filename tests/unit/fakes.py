"""In-memory fakes of the application ports, for the unit tests."""

from collections.abc import Sequence

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
