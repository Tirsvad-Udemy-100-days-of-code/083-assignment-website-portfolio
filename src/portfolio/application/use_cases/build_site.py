"""!
@file build_site.py
@brief Use case: build every file of the site.
"""

from portfolio.application.dto.about_page import AboutPage
from portfolio.application.dto.home_page import HomePage
from portfolio.application.ports.data_file_reader import DataFileReader
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
from portfolio.domain.validation import is_local_image_path


def build_site(
    project_repository: ProjectRepository,
    profile_repository: ProfileRepository,
    data_files: DataFileReader,
    renderer: SiteRenderer,
    writer: SiteWriter,
) -> tuple[str, ...]:
    """!
    @brief Render the pages and the stylesheet, copy the images, and write them.

    Every file is rendered and every image is read before the first file is
    written, so a failure while reading or rendering leaves the site untouched.
    An image is written to the same relative path it has in the data folder.
    @param project_repository Source of the projects.
    @param profile_repository Source of the profile.
    @param data_files Source of the image files the data refers to.
    @param renderer Turns the page data into text.
    @param writer Destination of the files.
    @return The relative paths of the written files, in the order of writing: the
        pages and the stylesheet, then the images.
    @throws DataSourceError A repository cannot read its data or an image cannot be
        read.
    @throws SiteWriteError A file cannot be written.
    """
    home_page = home(project_repository)
    about_page = about(profile_repository)
    images = {
        path: data_files.read_bytes(path)
        for path in _local_images(home_page, about_page)
    }
    texts = (
        (HOME_PAGE_FILE_NAME, renderer.render_home(home_page)),
        (ABOUT_PAGE_FILE_NAME, renderer.render_about(about_page)),
        (STYLESHEET_FILE_NAME, renderer.stylesheet()),
    )
    for relative_path, content in texts:
        writer.write_text(relative_path, content)
    for relative_path, data in images.items():
        writer.write_bytes(relative_path, data)
    return tuple(relative_path for relative_path, _ in texts) + tuple(images)


def _local_images(home_page: HomePage, about_page: AboutPage) -> tuple[str, ...]:
    """Give each image file of the pages once, in the order the pages show them."""
    candidates = [
        about_page.photo_url,
        *(card.image_url for card in home_page.projects),
    ]
    return tuple(
        dict.fromkeys(
            path
            for path in candidates
            if path is not None and is_local_image_path(path)
        )
    )
