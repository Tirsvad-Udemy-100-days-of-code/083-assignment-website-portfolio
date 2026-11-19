"""!
@file template_support.py
@brief The filters and the texts the Jinja templates use.
"""

from flask import Flask

from portfolio.constants import (
    EMPTY_STATE_TEXT,
    ERROR_HOME_LINK_TEXT,
    FOOTER_TEXT,
    HOME_HEADING,
    HTML_LANG,
    LINKS_HEADING,
    NAV_ABOUT_LABEL,
    NAV_ARIA_LABEL,
    NAV_HOME_LABEL,
    PLACEHOLDER_COLOR_COUNT,
    SITE_TITLE,
    SKILLS_HEADING,
    SOURCE_CODE_LABEL,
    TAGS_LABEL,
)
from portfolio.presentation.web.safe_urls import image_src, safe_url


def placeholder_letter(title: str) -> str:
    """!
    @brief Give the letter a card without image shows in its place.
    @param title The title of the project.
    @return The first letter of the title in upper case; empty for a blank title.
    """
    return title.strip()[:1].upper()


def placeholder_color(title: str) -> int:
    """!
    @brief Give the colour number of the placeholder of a card, the same each time.
    @param title The title of the project.
    @return A number from 0 up to the number of placeholder colours.
    """
    return sum(ord(character) for character in title) % PLACEHOLDER_COLOR_COUNT


def register_template_support(app: Flask) -> None:
    """!
    @brief Add the filters and the texts to the templates of an application.

    There is no filter that marks text as safe: every value stays escaped.
    @param app The application.
    """
    app.jinja_env.filters.update(
        safe_url=safe_url,
        image_src=image_src,
        placeholder_letter=placeholder_letter,
        placeholder_color=placeholder_color,
    )
    app.jinja_env.globals.update(
        html_lang=HTML_LANG,
        site_title=SITE_TITLE,
        nav_aria_label=NAV_ARIA_LABEL,
        nav_home_label=NAV_HOME_LABEL,
        nav_about_label=NAV_ABOUT_LABEL,
        footer_text=FOOTER_TEXT,
        home_heading=HOME_HEADING,
        empty_state_text=EMPTY_STATE_TEXT,
        source_code_label=SOURCE_CODE_LABEL,
        skills_heading=SKILLS_HEADING,
        tags_label=TAGS_LABEL,
        links_heading=LINKS_HEADING,
        error_home_link_text=ERROR_HOME_LINK_TEXT,
    )
