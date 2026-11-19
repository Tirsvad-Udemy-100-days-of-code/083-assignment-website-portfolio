"""!
@file layout.py
@brief The layout every page shares: header, navigation and footer.
"""

from portfolio.constants import (
    ABOUT_PAGE_FILE_NAME,
    FOOTER_TEXT,
    HOME_PAGE_FILE_NAME,
    HTML_LANG,
    NAV_ABOUT_LABEL,
    NAV_ARIA_LABEL,
    NAV_HOME_LABEL,
    STYLESHEET_FILE_NAME,
)
from portfolio.presentation.views.html_safety import escape


def render_page(site_title: str, page_title: str, body: str, current_file: str) -> str:
    """!
    @brief Put the body of a page in the shared layout.
    @param site_title Title of the site, shown in the header and the tab.
    @param page_title Title of the page, shown in the tab.
    @param body HTML of the page content; the caller has already escaped it.
    @param current_file File name of the page, to mark its link in the navigation.
    @return The complete HTML document.
    """
    site = escape(site_title)
    return f"""<!DOCTYPE html>
<html lang="{escape(HTML_LANG)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(page_title)} | {site}</title>
  <link rel="stylesheet" href="{escape(STYLESHEET_FILE_NAME)}">
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a class="site-title" href="{escape(HOME_PAGE_FILE_NAME)}">{site}</a>
      {_navigation(current_file)}
    </div>
  </header>
  <main class="container">
{body}
  </main>
  <footer class="site-footer">
    <div class="container">{escape(FOOTER_TEXT)}</div>
  </footer>
</body>
</html>
"""


def _navigation(current_file: str) -> str:
    items = (
        (NAV_HOME_LABEL, HOME_PAGE_FILE_NAME),
        (NAV_ABOUT_LABEL, ABOUT_PAGE_FILE_NAME),
    )
    links = "".join(_nav_link(label, file, current_file) for label, file in items)
    return f'<nav aria-label="{escape(NAV_ARIA_LABEL)}">{links}</nav>'


def _nav_link(label: str, file_name: str, current_file: str) -> str:
    current = ' aria-current="page"' if file_name == current_file else ""
    return f'<a href="{escape(file_name)}"{current}>{escape(label)}</a>'
