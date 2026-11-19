"""!
@file profile_changes.py
@brief The fields of the profile that a change gives a new value.
"""

from dataclasses import dataclass

from portfolio.application.dto.link_item import LinkItem


@dataclass(frozen=True, slots=True)
class ProfileChanges:
    """!
    @brief New values for some fields of the profile.

    The field names are the ones of the Profile entity.
    """

    ## @brief New full name, or None.
    name: str | None = None
    ## @brief New headline, or None.
    headline: str | None = None
    ## @brief New summary, or None.
    summary: str | None = None
    ## @brief New photo path, or None.
    photo: str | None = None
    ## @brief New skills, which replace the old ones, or None.
    skills: tuple[str, ...] | None = None
    ## @brief New links, which replace the old ones, or None.
    links: tuple[LinkItem, ...] | None = None
