"""!
@file about_page.py
@brief Data of the about page.
"""

from dataclasses import dataclass

from portfolio.application.dto.link_item import LinkItem


@dataclass(frozen=True, slots=True)
class AboutPage:
    """!
    @brief What the about page shows.
    """

    ## @brief Title of the site.
    site_title: str
    ## @brief Full name.
    name: str
    ## @brief One-line professional headline.
    headline: str
    ## @brief Short text about the person.
    summary: str
    ## @brief Skills of the person.
    skills: tuple[str, ...]
    ## @brief Links to other sites.
    links: tuple[LinkItem, ...]
    ## @brief Relative path of the photo; None when the avatar shows the initials.
    photo_url: str | None
    ## @brief Initials of the name, shown in the avatar when there is no photo.
    initials: str
