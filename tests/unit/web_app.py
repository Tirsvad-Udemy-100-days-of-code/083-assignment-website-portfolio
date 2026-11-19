"""Builders of the Flask application for the tests, with in-memory data."""

from collections.abc import Callable

from flask import Flask
from flask.testing import FlaskClient

from fakes import InMemoryDataFileReader
from portfolio.application.dto.about_page import AboutPage
from portfolio.application.dto.home_page import HomePage
from portfolio.application.ports.data_file_reader import DataFileReader
from portfolio.presentation.web.app import create_app
from sample_data import make_about_page, make_home_page


def make_test_app(
    home_page: HomePage | Callable[[], HomePage] | None = None,
    about_page: AboutPage | Callable[[], AboutPage] | None = None,
    images: DataFileReader | None = None,
) -> Flask:
    """An application whose pages come from the given data, or from the samples."""
    home = home_page if home_page is not None else make_home_page()
    about = about_page if about_page is not None else make_about_page()
    return create_app(
        home_page=home if callable(home) else lambda: home,
        about_page=about if callable(about) else lambda: about,
        images=images if images is not None else InMemoryDataFileReader(),
    )


def make_client(
    home_page: HomePage | Callable[[], HomePage] | None = None,
    about_page: AboutPage | Callable[[], AboutPage] | None = None,
    images: DataFileReader | None = None,
) -> FlaskClient:
    """A test client of an application built by `make_test_app`."""
    return make_test_app(home_page, about_page, images).test_client()
