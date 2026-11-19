"""!
@file site_renderer.py
@brief Port through which the use cases turn page data into files.
"""

from typing import Protocol

from portfolio.application.dto.about_page import AboutPage
from portfolio.application.dto.home_page import HomePage


class SiteRenderer(Protocol):
    """!
    @brief Turns page data into text; the use cases never know the format.
    """

    def render_home(self, page: HomePage) -> str:
        """!
        @brief Render the home page.
        @param page The data of the home page.
        @return The text of the page.
        """
        ...

    def render_about(self, page: AboutPage) -> str:
        """!
        @brief Render the about page.
        @param page The data of the about page.
        @return The text of the page.
        """
        ...

    def stylesheet(self) -> str:
        """!
        @brief Give the stylesheet the pages refer to.
        @return The text of the stylesheet.
        """
        ...
