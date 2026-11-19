"""!
@file app.py
@brief The application factory of the Flask site.
"""

from flask import Flask

from portfolio.application.ports.data_file_reader import DataFileReader
from portfolio.constants import PRESENTATION_PACKAGE
from portfolio.presentation.web.error_handlers import register_error_handlers
from portfolio.presentation.web.image_route import register_image_route
from portfolio.presentation.web.page_routes import (
    AboutPageProvider,
    HomePageProvider,
    register_page_routes,
)
from portfolio.presentation.web.security_headers import register_security_headers
from portfolio.presentation.web.template_support import register_template_support


def create_app(
    home_page: HomePageProvider,
    about_page: AboutPageProvider,
    images: DataFileReader,
) -> Flask:
    """!
    @brief Create the Flask application.

    The application only reads: it has no write route, no session and no secret
    key, and debug is off. The page providers and the image reader come from the
    composition root, so the application names no adapter.
    @param home_page Reads the home page from the database on each call.
    @param about_page Reads the about page from the database on each call.
    @param images Reads a file of the images folder of the data folder.
    @return The application, ready to be served.
    """
    app = Flask(PRESENTATION_PACKAGE, static_folder=None)
    # Cleaner HTML: no blank line for each block tag. This must come before the first
    # use of `app.jinja_env`, which the `debug` setter already makes.
    app.jinja_options = {"trim_blocks": True, "lstrip_blocks": True}
    app.debug = False
    register_template_support(app)
    register_page_routes(app, home_page, about_page)
    register_image_route(app, images)
    register_error_handlers(app)
    register_security_headers(app)
    return app
