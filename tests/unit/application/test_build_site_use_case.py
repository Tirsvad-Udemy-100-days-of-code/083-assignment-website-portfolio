"""Unit tests of the build_site use case."""

import pytest

from fakes import (
    InMemoryDataFileReader,
    InMemoryProfileRepository,
    InMemoryProjectRepository,
    InMemorySiteWriter,
    StubSiteRenderer,
)
from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.application.errors.site_write_error import SiteWriteError
from portfolio.application.use_cases.build_site import build_site
from portfolio.constants import (
    ABOUT_PAGE_FILE_NAME,
    HOME_PAGE_FILE_NAME,
    STYLESHEET_FILE_NAME,
)
from sample_data import make_profile, make_project, make_projects


class FailingSiteWriter:
    def write_text(self, relative_path: str, content: str) -> None:
        raise SiteWriteError("disk full")

    def write_bytes(self, relative_path: str, content: bytes) -> None:
        raise SiteWriteError("disk full")


def test_build_site_writes_the_three_files() -> None:
    writer = InMemorySiteWriter()
    build_site(
        InMemoryProjectRepository(make_projects(2)),
        InMemoryProfileRepository(make_profile()),
        InMemoryDataFileReader(),
        StubSiteRenderer(),
        writer,
    )
    assert writer.files == {
        HOME_PAGE_FILE_NAME: "home:2",
        ABOUT_PAGE_FILE_NAME: "about:Ada Lovelace",
        STYLESHEET_FILE_NAME: "css",
    }
    assert writer.binary_files == {}


def test_build_site_returns_the_written_paths_in_order() -> None:
    written = build_site(
        InMemoryProjectRepository([]),
        InMemoryProfileRepository(make_profile()),
        InMemoryDataFileReader(),
        StubSiteRenderer(),
        InMemorySiteWriter(),
    )
    assert written == (HOME_PAGE_FILE_NAME, ABOUT_PAGE_FILE_NAME, STYLESHEET_FILE_NAME)


def test_build_site_writes_an_empty_home_page_when_there_are_no_projects() -> None:
    writer = InMemorySiteWriter()
    build_site(
        InMemoryProjectRepository([]),
        InMemoryProfileRepository(make_profile()),
        InMemoryDataFileReader(),
        StubSiteRenderer(),
        writer,
    )
    assert writer.files[HOME_PAGE_FILE_NAME] == "home:0"


def test_build_site_propagates_a_write_failure() -> None:
    with pytest.raises(SiteWriteError, match="disk full"):
        build_site(
            InMemoryProjectRepository([]),
            InMemoryProfileRepository(make_profile()),
            InMemoryDataFileReader(),
            StubSiteRenderer(),
            FailingSiteWriter(),
        )


def test_build_site_copies_each_local_image_once_to_the_same_path() -> None:
    projects = [
        make_project(title="One", image_url="images/one.svg"),
        make_project(title="Two", image_url="images/one.svg"),
        make_project(title="Three", image_url="images/three.png"),
    ]
    reader = InMemoryDataFileReader(
        {"images/one.svg": b"<svg/>", "images/three.png": b"PNG"}
    )
    writer = InMemorySiteWriter()
    written = build_site(
        InMemoryProjectRepository(projects),
        InMemoryProfileRepository(make_profile()),
        reader,
        StubSiteRenderer(),
        writer,
    )
    assert writer.binary_files == {
        "images/one.svg": b"<svg/>",
        "images/three.png": b"PNG",
    }
    assert reader.reads == ["images/one.svg", "images/three.png"]
    assert written[-2:] == ("images/one.svg", "images/three.png")


def test_build_site_copies_the_profile_photo() -> None:
    writer = InMemorySiteWriter()
    written = build_site(
        InMemoryProjectRepository([]),
        InMemoryProfileRepository(make_profile(photo="images/me.jpg")),
        InMemoryDataFileReader({"images/me.jpg": b"JPEG"}),
        StubSiteRenderer(),
        writer,
    )
    assert writer.binary_files == {"images/me.jpg": b"JPEG"}
    assert written[-1] == "images/me.jpg"


def test_build_site_does_not_read_remote_images() -> None:
    reader = InMemoryDataFileReader()
    build_site(
        InMemoryProjectRepository([make_project()]),
        InMemoryProfileRepository(make_profile()),
        reader,
        StubSiteRenderer(),
        InMemorySiteWriter(),
    )
    assert reader.reads == []


def test_build_site_writes_nothing_when_an_image_is_missing() -> None:
    writer = InMemorySiteWriter()
    with pytest.raises(DataSourceError, match=r"missing\.svg"):
        build_site(
            InMemoryProjectRepository([make_project(image_url="images/missing.svg")]),
            InMemoryProfileRepository(make_profile()),
            InMemoryDataFileReader(),
            StubSiteRenderer(),
            writer,
        )
    assert writer.files == {}
    assert writer.binary_files == {}
