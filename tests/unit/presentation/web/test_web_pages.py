"""Tests of the routes, methods and templates of the Flask site (test client)."""

import re
from typing import NoReturn

import pytest
from werkzeug.exceptions import BadRequest
from werkzeug.test import TestResponse

from fakes import InMemoryDataFileReader
from portfolio.application.dto.home_page import HomePage
from portfolio.application.dto.link_item import LinkItem
from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.constants import (
    EMPTY_STATE_TEXT,
    PLACEHOLDER_COLOR_COUNT,
    ROUTE_ABOUT,
    ROUTE_HOME,
    ROUTE_STYLESHEET,
)
from sample_data import make_about_page, make_card, make_home_page
from web_app import make_client, make_test_app

IMAGE_FILES = {"a.svg": b"<svg/>"}
READABLE_PATHS = [ROUTE_HOME, ROUTE_ABOUT, ROUTE_STYLESHEET, "/images/a.svg"]


@pytest.mark.parametrize("path", [ROUTE_HOME, ROUTE_ABOUT])
def test_a_page_is_html(path: str) -> None:
    response = make_client().get(path)

    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"
    assert response.text.startswith("<!DOCTYPE html>")
    assert '<html lang="en">' in response.text


def test_home_page_shows_one_card_per_project_with_both_faces() -> None:
    page = make_home_page(
        (
            make_card(title="First", image_url="images/a.svg", tags=("C", "Rust")),
            make_card(title="Second", skills=("Testing", "Design")),
        )
    )

    html = make_client(home_page=page).get(ROUTE_HOME).text

    cards = html.split('<article class="flip-card" tabindex="0">')[1:]
    assert len(cards) == 2
    front, back = cards[0].split('<div class="flip-card-face flip-card-back">')
    assert '<h2 class="card-title">First</h2>' in front
    assert '<span class="badge">Web app</span>' in front
    assert '<p class="card-text">Shows the weather of a city.</p>' in front
    assert (
        '<img class="card-image" src="/images/a.svg" alt="First" loading="lazy">'
        in front
    )
    assert (
        '<a class="card-link" href="https://example.com/weather" '
        'rel="noopener noreferrer">Source code</a>'
    ) in back
    assert '<ul class="tags" aria-label="Tags">' in back
    assert '<li class="tag">C</li><li class="tag">Rust</li>' in back
    assert '<ul class="skill-list"><li>Working with web APIs</li></ul>' in back
    assert "<li>Testing</li><li>Design</li>" in cards[1]


def test_home_page_keeps_the_order_of_the_projects() -> None:
    page = make_home_page(tuple(make_card(title=f"Project {n}") for n in range(4)))

    html = make_client(home_page=page).get(ROUTE_HOME).text

    positions = [html.index(f"Project {n}</h2>") for n in range(4)]
    assert positions == sorted(positions)


def test_a_card_without_image_shows_a_placeholder_with_the_first_letter() -> None:
    page = make_home_page((make_card(title="zebra app", image_url=""),))

    html = make_client(home_page=page).get(ROUTE_HOME).text

    color = sum(ord(character) for character in "zebra app") % PLACEHOLDER_COLOR_COUNT
    assert (
        f'<div class="card-image card-placeholder placeholder-{color}" '
        'aria-hidden="true">Z</div>'
    ) in html
    assert "<img" not in html


def test_the_placeholder_colour_is_the_same_on_every_request() -> None:
    client = make_client(home_page=make_home_page((make_card(image_url=""),)))

    colours = {
        re.search(r"placeholder-(\d)", client.get(ROUTE_HOME).text) for _ in range(3)
    }

    assert len({match.group(1) for match in colours if match}) == 1


def test_a_card_without_tags_and_skills_has_no_empty_lists() -> None:
    page = make_home_page((make_card(tags=(), skills=()),))

    html = make_client(home_page=page).get(ROUTE_HOME).text

    assert 'class="tags"' not in html
    assert 'class="skill-list"' not in html
    assert 'class="skills-title"' not in html


def test_home_page_without_projects_shows_the_empty_state() -> None:
    html = make_client(home_page=make_home_page(())).get(ROUTE_HOME).text

    assert f'<p class="empty-state">{EMPTY_STATE_TEXT}</p>' in html
    assert "flip-card" not in html


def test_the_navigation_marks_the_home_page_as_current() -> None:
    html = make_client().get(ROUTE_HOME).text

    assert '<a href="/" aria-current="page">Home</a>' in html
    assert '<a href="/about">About</a>' in html
    assert html.count('aria-current="page"') == 1


def test_the_navigation_marks_the_about_page_as_current() -> None:
    html = make_client().get(ROUTE_ABOUT).text

    assert '<a href="/about" aria-current="page">About</a>' in html
    assert '<a href="/">Home</a>' in html
    assert html.count('aria-current="page"') == 1


def test_the_layout_links_the_stylesheet_and_has_a_title_and_a_footer() -> None:
    html = make_client().get(ROUTE_HOME).text

    assert '<link rel="stylesheet" href="/static/style.css">' in html
    assert "<title>Home | Portfolio</title>" in html
    assert '<a class="site-title" href="/">Portfolio</a>' in html
    assert '<footer class="site-footer">' in html


def test_about_page_shows_the_photo_as_avatar() -> None:
    page = make_about_page(photo_url="images/me.jpg")

    html = make_client(about_page=page).get(ROUTE_ABOUT).text

    assert '<img class="avatar" src="/images/me.jpg" alt="Ada Lovelace">' in html
    assert "avatar-initials" not in html


def test_about_page_shows_the_initials_without_a_photo() -> None:
    html = make_client(about_page=make_about_page(photo_url=None)).get(ROUTE_ABOUT).text

    assert '<div class="avatar avatar-initials" aria-hidden="true">AL</div>' in html
    assert "<img" not in html


def test_about_page_shows_headline_summary_skills_and_links() -> None:
    page = make_about_page(
        links=(
            LinkItem("GitHub", "https://github.com/ada"),
            LinkItem("LinkedIn", "https://www.linkedin.com/in/ada/"),
        )
    )

    html = make_client(about_page=page).get(ROUTE_ABOUT).text

    assert "<h1>Ada Lovelace</h1>" in html
    assert '<p class="headline">Software developer</p>' in html
    assert "<p>Builds small, tested programs.</p>" in html
    assert '<ul class="skills">' in html
    assert "<li>Python</li>" in html
    assert (
        '<li><a href="https://www.linkedin.com/in/ada/" '
        'rel="noopener noreferrer">LinkedIn</a></li>'
    ) in html


def test_stylesheet_is_served_as_css() -> None:
    response = make_client().get(ROUTE_STYLESHEET, buffered=True)

    assert response.status_code == 200
    assert response.content_type.startswith("text/css")
    assert "grid-template-columns" in response.text


def test_image_is_served_with_its_content_type() -> None:
    client = make_client(images=InMemoryDataFileReader(IMAGE_FILES))

    response = client.get("/images/a.svg")

    assert response.status_code == 200
    assert response.content_type.startswith("image/svg+xml")
    assert response.data == b"<svg/>"


@pytest.mark.parametrize("path", READABLE_PATHS)
def test_head_answers_like_get_without_a_body(path: str) -> None:
    client = make_client(images=InMemoryDataFileReader(IMAGE_FILES))

    response = client.head(path, buffered=True)

    assert response.status_code == 200
    assert response.data == b""
    assert client.get(path, buffered=True).status_code == 200


@pytest.mark.parametrize(
    "path",
    [
        "/index.html",
        "/about.html",
        "/about/",
        "/nothing",
        "/static/other.css",
        "/static/",
        "/static",
        "/images",
        "/images/",
        "/admin",
    ],
)
def test_any_other_address_is_404_with_a_plain_page(path: str) -> None:
    response = make_client().get(path, buffered=True)

    assert response.status_code == 404
    assert "<h1>404 Not Found</h1>" in response.text
    assert "This page does not exist." in response.text
    assert '<a href="/">Back to the home page</a>' in response.text
    assert "Traceback" not in response.text


@pytest.mark.parametrize("method", ["POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@pytest.mark.parametrize("path", READABLE_PATHS)
def test_any_other_method_is_405_with_a_plain_page(path: str, method: str) -> None:
    client = make_client(images=InMemoryDataFileReader(IMAGE_FILES))

    response = client.open(path, method=method)

    assert response.status_code == 405
    assert response.headers["Allow"] == "GET, HEAD"
    assert "<h1>405 Method Not Allowed</h1>" in response.text
    assert "Traceback" not in response.text


def test_a_method_on_an_unknown_address_is_404() -> None:
    assert make_client().post("/nothing").status_code == 404


def test_every_request_reads_the_data_again() -> None:
    cards = [make_card(title="Before")]
    client = make_client(home_page=lambda: make_home_page(tuple(cards)))

    assert "Before" in client.get(ROUTE_HOME).text
    cards[:] = [make_card(title="After")]
    html = client.get(ROUTE_HOME).text

    assert "After" in html
    assert "Before" not in html


def test_every_request_reads_the_profile_again() -> None:
    names = ["Ada Lovelace"]
    client = make_client(about_page=lambda: make_about_page(name=names[0]))

    assert "Ada Lovelace" in client.get(ROUTE_ABOUT).text
    names[0] = "Grace Hopper"

    assert "Grace Hopper" in client.get(ROUTE_ABOUT).text


def failing_read() -> NoReturn:
    raise DataSourceError("/secret/place/portfolio.db: disk on fire")


def assert_plain_500_page(response: TestResponse) -> None:
    assert response.status_code == 500
    assert "<h1>500 Internal Server Error</h1>" in response.text
    assert "The site cannot read its data right now." in response.text
    assert "disk on fire" not in response.text
    assert "/secret/place" not in response.text


def test_a_failing_read_of_the_projects_gives_a_plain_500_page() -> None:
    assert_plain_500_page(make_client(home_page=failing_read).get(ROUTE_HOME))


def test_a_failing_read_of_the_profile_gives_a_plain_500_page() -> None:
    assert_plain_500_page(make_client(about_page=failing_read).get(ROUTE_ABOUT))


def test_an_unexpected_error_gives_a_plain_500_page_without_a_stack_trace() -> None:
    def broken() -> HomePage:
        raise RuntimeError("secret detail")

    response = make_client(home_page=broken).get(ROUTE_HOME)

    assert response.status_code == 500
    assert "secret detail" not in response.text
    assert "Traceback" not in response.text


def test_any_other_http_error_gives_a_plain_page_with_its_standard_phrase() -> None:
    app = make_test_app()

    with app.test_request_context("/"):
        response = app.make_response(app.handle_user_exception(BadRequest()))

    assert response.status_code == 400
    assert "<h1>400 Bad Request</h1>" in response.get_data(as_text=True)
    assert "Traceback" not in response.get_data(as_text=True)
