"""!
@file about_view.py
@brief HTML view of the about page: name, headline, summary, skills and links.
"""

from portfolio.application.dto.about_page import AboutPage
from portfolio.application.dto.link_item import LinkItem
from portfolio.constants import (
    ABOUT_PAGE_FILE_NAME,
    LINKS_HEADING,
    NAV_ABOUT_LABEL,
    SKILLS_HEADING,
)
from portfolio.presentation.views.html_safety import escape, safe_url
from portfolio.presentation.views.layout import render_page


def render_about_page(page: AboutPage) -> str:
    """!
    @brief Render the about page.
    @param page The data of the about page.
    @return The complete HTML document.
    """
    skills = "\n".join(f"        <li>{escape(skill)}</li>" for skill in page.skills)
    links = "\n".join(_link(link) for link in page.links)
    body = f"""    <section class="about">
      <h1>{escape(page.name)}</h1>
      <p class="headline">{escape(page.headline)}</p>
      <p>{escape(page.summary)}</p>
      <h2>{escape(SKILLS_HEADING)}</h2>
      <ul class="skills">
{skills}
      </ul>
      <h2>{escape(LINKS_HEADING)}</h2>
      <ul class="links">
{links}
      </ul>
    </section>"""
    return render_page(page.site_title, NAV_ABOUT_LABEL, body, ABOUT_PAGE_FILE_NAME)


def _link(link: LinkItem) -> str:
    return (
        f'        <li><a href="{escape(safe_url(link.url))}" '
        f'rel="noopener noreferrer">{escape(link.label)}</a></li>'
    )
