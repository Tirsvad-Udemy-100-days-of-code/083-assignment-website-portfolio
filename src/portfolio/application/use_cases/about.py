"""!
@file about.py
@brief Use case: build the about page.
"""

from portfolio.application.dto.about_page import AboutPage
from portfolio.application.dto.link_item import LinkItem
from portfolio.application.ports.profile_repository import ProfileRepository
from portfolio.constants import SITE_TITLE


def about(repository: ProfileRepository) -> AboutPage:
    """!
    @brief Build the about page from the profile.
    @param repository Source of the profile.
    @return The about page.
    """
    profile = repository.get_profile()
    return AboutPage(
        site_title=SITE_TITLE,
        name=profile.name,
        headline=profile.headline,
        summary=profile.summary,
        skills=profile.skills,
        links=tuple(LinkItem(label=link.label, url=link.url) for link in profile.links),
        photo_url=profile.photo,
        initials=profile.initials,
    )
