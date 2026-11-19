"""!
@file home_view.py
@brief HTML view of the home page: a grid of project cards.
"""

from portfolio.application.dto.home_page import HomePage
from portfolio.application.dto.project_card import ProjectCard
from portfolio.constants import (
    EMPTY_STATE_TEXT,
    HOME_HEADING,
    HOME_PAGE_FILE_NAME,
    NAV_HOME_LABEL,
    SOURCE_CODE_LABEL,
)
from portfolio.presentation.views.html_safety import escape, is_safe_url, safe_url
from portfolio.presentation.views.layout import render_page


def render_home_page(page: HomePage) -> str:
    """!
    @brief Render the home page.
    @param page The data of the home page.
    @return The complete HTML document.
    """
    if page.projects:
        cards = "\n".join(_card(card) for card in page.projects)
        content = f'    <div class="card-grid">\n{cards}\n    </div>'
    else:
        content = f'    <p class="empty-state">{escape(EMPTY_STATE_TEXT)}</p>'
    body = f"    <h1>{escape(HOME_HEADING)}</h1>\n{content}"
    return render_page(page.site_title, NAV_HOME_LABEL, body, HOME_PAGE_FILE_NAME)


def _card(card: ProjectCard) -> str:
    return f"""      <article class="card">
{_image(card)}        <div class="card-body">
          <h2 class="card-title">{escape(card.title)}</h2>
          <span class="badge">{escape(card.kind)}</span>
          <p class="card-text">{escape(card.description)}</p>
          <a class="card-link" href="{escape(safe_url(card.source_code_url))}" \
rel="noopener noreferrer">{escape(SOURCE_CODE_LABEL)}</a>
        </div>
      </article>"""


def _image(card: ProjectCard) -> str:
    if not is_safe_url(card.image_url):
        return ""
    source = escape(safe_url(card.image_url))
    return (
        f'        <img class="card-image" src="{source}" '
        f'alt="{escape(card.title)}" loading="lazy">\n'
    )
