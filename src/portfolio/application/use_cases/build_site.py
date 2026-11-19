"""!
@file build_site.py
@brief Use case: build every file of the site.
"""

from portfolio.application.ports.profile_repository import ProfileRepository
from portfolio.application.ports.project_repository import ProjectRepository
from portfolio.application.ports.site_renderer import SiteRenderer
from portfolio.application.ports.site_writer import SiteWriter
from portfolio.application.use_cases.about import about
from portfolio.application.use_cases.home import home
from portfolio.constants import (
    ABOUT_PAGE_FILE_NAME,
    HOME_PAGE_FILE_NAME,
    STYLESHEET_FILE_NAME,
)


def build_site(
    project_repository: ProjectRepository,
    profile_repository: ProfileRepository,
    renderer: SiteRenderer,
    writer: SiteWriter,
) -> tuple[str, ...]:
    """!
    @brief Render the home page, the about page and the stylesheet, and write them.

    Every file is rendered before the first one is written, so a failure while
    reading or rendering leaves the site untouched.
    @param project_repository Source of the projects.
    @param profile_repository Source of the profile.
    @param renderer Turns the page data into text.
    @param writer Destination of the files.
    @return The relative paths of the written files, in the order of writing.
    @throws DataSourceError A repository cannot read its data.
    @throws SiteWriteError A file cannot be written.
    """
    files = (
        (HOME_PAGE_FILE_NAME, renderer.render_home(home(project_repository))),
        (ABOUT_PAGE_FILE_NAME, renderer.render_about(about(profile_repository))),
        (STYLESHEET_FILE_NAME, renderer.stylesheet()),
    )
    for relative_path, content in files:
        writer.write_text(relative_path, content)
    return tuple(relative_path for relative_path, _ in files)
