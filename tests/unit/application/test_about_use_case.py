"""Unit tests of the about use case."""

from fakes import InMemoryProfileRepository
from portfolio.application.dto.link_item import LinkItem
from portfolio.application.use_cases.about import about
from portfolio.constants import SITE_TITLE
from sample_data import make_link, make_profile


def test_about_maps_the_profile_to_a_page() -> None:
    page = about(InMemoryProfileRepository(make_profile()))
    assert page.site_title == SITE_TITLE
    assert page.name == "Ada Lovelace"
    assert page.headline == "Software developer"
    assert page.summary == "Builds small, tested programs."
    assert page.skills == ("Python", "Testing")


def test_about_maps_links_to_link_items() -> None:
    profile = make_profile(links=(make_link(), make_link("Blog", "https://b.example")))
    page = about(InMemoryProfileRepository(profile))
    assert page.links == (
        LinkItem("GitHub", "https://example.com/me"),
        LinkItem("Blog", "https://b.example"),
    )


def test_about_returns_no_links_when_the_profile_has_none() -> None:
    page = about(InMemoryProfileRepository(make_profile(links=())))
    assert page.links == ()
