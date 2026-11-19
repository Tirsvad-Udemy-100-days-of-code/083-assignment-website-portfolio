"""!
@file home_view.py
@brief HTML view of the home page: a grid of flip cards, one per project.
"""

from portfolio.application.dto.home_page import HomePage
from portfolio.application.dto.project_card import ProjectCard
from portfolio.constants import (
    EMPTY_STATE_TEXT,
    HOME_HEADING,
    HOME_PAGE_FILE_NAME,
    NAV_HOME_LABEL,
    PLACEHOLDER_COLOR_COUNT,
    SKILLS_HEADING,
    SOURCE_CODE_LABEL,
    TAGS_LABEL,
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
    return f"""      <article class="flip-card" tabindex="0">
        <div class="flip-card-inner">
          <div class="flip-card-face flip-card-front">
{_image(card)}            <div class="card-body">
              <h2 class="card-title">{escape(card.title)}</h2>
              <span class="badge">{escape(card.kind)}</span>
              <p class="card-text">{escape(card.description)}</p>
            </div>
          </div>
          <div class="flip-card-face flip-card-back">
            <a class="card-link" href="{escape(safe_url(card.source_code_url))}" \
rel="noopener noreferrer">{escape(SOURCE_CODE_LABEL)}</a>
{_tags(card)}{_skills(card)}          </div>
        </div>
      </article>"""


def _image(card: ProjectCard) -> str:
    if not is_safe_url(card.image_url):
        return _placeholder(card.title)
    source = escape(safe_url(card.image_url))
    return (
        f'            <img class="card-image" src="{source}" '
        f'alt="{escape(card.title)}" loading="lazy">\n'
    )


def _placeholder(title: str) -> str:
    letter = title.strip()[:1].upper()
    color = sum(ord(character) for character in title) % PLACEHOLDER_COLOR_COUNT
    return (
        f'            <div class="card-image card-placeholder placeholder-{color}" '
        f'aria-hidden="true">{escape(letter)}</div>\n'
    )


def _tags(card: ProjectCard) -> str:
    if not card.tags:
        return ""
    items = "".join(f'<li class="tag">{escape(tag)}</li>' for tag in card.tags)
    return (
        f'            <ul class="tags" aria-label="{escape(TAGS_LABEL)}">{items}</ul>\n'
    )


def _skills(card: ProjectCard) -> str:
    if not card.skills:
        return ""
    items = "".join(f"<li>{escape(skill)}</li>" for skill in card.skills)
    return (
        f'            <h3 class="skills-title">{escape(SKILLS_HEADING)}</h3>\n'
        f'            <ul class="skill-list">{items}</ul>\n'
    )
