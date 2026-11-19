"""Valid sample entities for the unit tests; a test overrides the field it probes."""

from portfolio.application.dto.about_page import AboutPage
from portfolio.application.dto.home_page import HomePage
from portfolio.application.dto.link_item import LinkItem
from portfolio.application.dto.project_card import ProjectCard
from portfolio.domain.entities.profile import Profile
from portfolio.domain.entities.project import Project
from portfolio.domain.value_objects.link import Link


def make_project(
    title: str = "Weather app",
    kind: str = "Web app",
    description: str = "Shows the weather of a city.",
    image_url: str = "https://example.com/weather.png",
    source_code_url: str = "https://example.com/weather",
    tags: tuple[str, ...] = ("Python", "API"),
    skills: tuple[str, ...] = ("Working with web APIs",),
) -> Project:
    return Project(title, kind, description, image_url, source_code_url, tags, skills)


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
    photo: str | None = None,
) -> Profile:
    return Profile(name, headline, summary, skills, links, photo)


def make_card(
    title: str = "Weather app",
    kind: str = "Web app",
    description: str = "Shows the weather of a city.",
    image_url: str = "https://example.com/weather.png",
    source_code_url: str = "https://example.com/weather",
    tags: tuple[str, ...] = ("Python", "API"),
    skills: tuple[str, ...] = ("Working with web APIs",),
) -> ProjectCard:
    return ProjectCard(
        title, kind, description, image_url, source_code_url, tags, skills
    )


def make_home_page(projects: tuple[ProjectCard, ...] = (make_card(),)) -> HomePage:
    return HomePage(site_title="Portfolio", projects=projects)


def make_about_page(
    name: str = "Ada Lovelace",
    headline: str = "Software developer",
    summary: str = "Builds small, tested programs.",
    skills: tuple[str, ...] = ("Python", "Testing"),
    links: tuple[LinkItem, ...] = (LinkItem("GitHub", "https://example.com/me"),),
    photo_url: str | None = None,
    initials: str = "AL",
) -> AboutPage:
    return AboutPage(
        "Portfolio", name, headline, summary, skills, links, photo_url, initials
    )
