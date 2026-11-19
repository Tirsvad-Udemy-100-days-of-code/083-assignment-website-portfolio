"""Valid sample entities for the unit tests; a test overrides the field it probes."""

from portfolio.domain.entities.profile import Profile
from portfolio.domain.entities.project import Project
from portfolio.domain.value_objects.link import Link


def make_project(
    title: str = "Weather app",
    kind: str = "Web app",
    description: str = "Shows the weather of a city.",
    image_url: str = "https://example.com/weather.png",
    source_code_url: str = "https://example.com/weather",
) -> Project:
    return Project(title, kind, description, image_url, source_code_url)


def make_projects(count: int) -> list[Project]:
    return [make_project(title=f"Project {number}") for number in range(count)]


def make_link(label: str = "GitHub", url: str = "https://example.com/me") -> Link:
    return Link(label, url)


def make_profile(
    name: str = "Ada Lovelace",
    headline: str = "Software developer",
    summary: str = "Builds small, tested programs.",
    skills: tuple[str, ...] = ("Python", "Testing"),
    links: tuple[Link, ...] = (make_link(),),
) -> Profile:
    return Profile(name, headline, summary, skills, links)
