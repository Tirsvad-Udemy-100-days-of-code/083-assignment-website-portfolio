"""!
@file html_site_renderer.py
@brief SiteRenderer that produces HTML pages and a CSS stylesheet.
"""

# The project requires Python 3.13 or newer, so the 3.7 compatibility rule is moot.
from importlib import resources  # nosemgrep: python37-compatibility-importlib2

from portfolio.application.dto.about_page import AboutPage
from portfolio.application.dto.home_page import HomePage
from portfolio.constants import (
    ENCODING,
    PRESENTATION_PACKAGE,
    STATIC_DIR_NAME,
    STYLESHEET_FILE_NAME,
)
from portfolio.presentation.views.about_view import render_about_page
from portfolio.presentation.views.home_view import render_home_page


class HtmlSiteRenderer:
    """!
    @brief Implements the SiteRenderer port with HTML views.
    """

    def render_home(self, page: HomePage) -> str:
        """!
        @brief Render the home page as HTML.
        @param page The data of the home page.
        @return The HTML document.
        """
        return render_home_page(page)

    def render_about(self, page: AboutPage) -> str:
        """!
        @brief Render the about page as HTML.
        @param page The data of the about page.
        @return The HTML document.
        """
        return render_about_page(page)

    def stylesheet(self) -> str:
        """!
        @brief Read the stylesheet that ships with the package.
        @return The CSS text.
        """
        resource = (
            resources.files(PRESENTATION_PACKAGE)
            .joinpath(STATIC_DIR_NAME)
            .joinpath(STYLESHEET_FILE_NAME)
        )
        return resource.read_text(encoding=ENCODING)
