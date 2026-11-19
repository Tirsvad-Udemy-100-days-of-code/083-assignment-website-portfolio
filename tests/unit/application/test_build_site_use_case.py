"""Unit tests of the build_site use case."""

import pytest

from fakes import (
    InMemoryProfileRepository,
    InMemoryProjectRepository,
    InMemorySiteWriter,
    StubSiteRenderer,
)
from portfolio.application.errors.site_write_error import SiteWriteError
from portfolio.application.use_cases.build_site import build_site
from portfolio.constants import (
    ABOUT_PAGE_FILE_NAME,
    HOME_PAGE_FILE_NAME,
    STYLESHEET_FILE_NAME,
)
from sample_data import make_profile, make_projects


class FailingSiteWriter:
    def write_text(self, relative_path: str, content: str) -> None:
        raise SiteWriteError("disk full")


def test_build_site_writes_the_three_files() -> None:
    writer = InMemorySiteWriter()
    build_site(
        InMemoryProjectRepository(make_projects(2)),
        InMemoryProfileRepository(make_profile()),
        StubSiteRenderer(),
        writer,
    )
    assert writer.files == {
        HOME_PAGE_FILE_NAME: "home:2",
        ABOUT_PAGE_FILE_NAME: "about:Ada Lovelace",
        STYLESHEET_FILE_NAME: "css",
    }


def test_build_site_returns_the_written_paths_in_order() -> None:
    written = build_site(
        InMemoryProjectRepository([]),
        InMemoryProfileRepository(make_profile()),
        StubSiteRenderer(),
        InMemorySiteWriter(),
    )
    assert written == (HOME_PAGE_FILE_NAME, ABOUT_PAGE_FILE_NAME, STYLESHEET_FILE_NAME)


def test_build_site_writes_an_empty_home_page_when_there_are_no_projects() -> None:
    writer = InMemorySiteWriter()
    build_site(
        InMemoryProjectRepository([]),
        InMemoryProfileRepository(make_profile()),
        StubSiteRenderer(),
        writer,
    )
    assert writer.files[HOME_PAGE_FILE_NAME] == "home:0"


def test_build_site_propagates_a_write_failure() -> None:
    with pytest.raises(SiteWriteError, match="disk full"):
        build_site(
            InMemoryProjectRepository([]),
            InMemoryProfileRepository(make_profile()),
            StubSiteRenderer(),
            FailingSiteWriter(),
        )
