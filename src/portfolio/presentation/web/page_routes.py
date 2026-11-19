"""!
@file page_routes.py
@brief The routes of the home page, the about page and the stylesheet.
"""

from collections.abc import Callable
from pathlib import Path

from flask import Flask, Response, render_template, send_from_directory

from portfolio.application.dto.about_page import AboutPage
from portfolio.application.dto.home_page import HomePage
from portfolio.constants import (
    ABOUT_TEMPLATE,
    ALLOWED_METHODS,
    CSS_CONTENT_TYPE,
    HOME_TEMPLATE,
    ROUTE_ABOUT,
    ROUTE_HOME,
    ROUTE_STYLESHEET,
    STATIC_DIR_NAME,
    STYLESHEET_FILE_NAME,
)

## @brief A function that reads the home page from the data; called on each request.
HomePageProvider = Callable[[], HomePage]

## @brief A function that reads the about page from the data; called on each request.
AboutPageProvider = Callable[[], AboutPage]


def register_page_routes(
    app: Flask, home_page: HomePageProvider, about_page: AboutPageProvider
) -> None:
    """!
    @brief Add the routes of the pages and the stylesheet.

    The routes answer GET and HEAD only, and no OPTIONS.
    @param app The application.
    @param home_page Reads the home page; it opens the database on every call.
    @param about_page Reads the about page; it opens the database on every call.
    """
    static_folder = Path(app.root_path) / STATIC_DIR_NAME

    def show_home() -> str:
        page = home_page()
        return render_template(HOME_TEMPLATE, page=page, site_title=page.site_title)

    def show_about() -> str:
        page = about_page()
        return render_template(ABOUT_TEMPLATE, page=page, site_title=page.site_title)

    def show_stylesheet() -> Response:
        return send_from_directory(
            static_folder, STYLESHEET_FILE_NAME, mimetype=CSS_CONTENT_TYPE
        )

    routes = (
        (ROUTE_HOME, "home", show_home),
        (ROUTE_ABOUT, "about", show_about),
        (ROUTE_STYLESHEET, "stylesheet", show_stylesheet),
    )
    for rule, endpoint, view in routes:
        app.add_url_rule(
            rule,
            endpoint,
            view,
            methods=ALLOWED_METHODS,
            provide_automatic_options=False,
        )
