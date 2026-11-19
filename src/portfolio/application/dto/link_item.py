"""!
@file link_item.py
@brief Data of one link as the about page shows it.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LinkItem:
    """!
    @brief One link on the about page.
    """

    ## @brief Text shown for the link.
    label: str
    ## @brief Address the link points to.
    url: str
