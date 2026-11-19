"""!
@file image_route.py
@brief The route that serves the images of the data folder.
"""

from http import HTTPStatus

from flask import Flask, Response, abort

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.application.ports.data_file_reader import DataFileReader
from portfolio.constants import ALLOWED_METHODS, IMAGE_CONTENT_TYPES, ROUTE_IMAGES
from portfolio.domain.validation import is_local_image_path

_ENDPOINT = "image"


def image_content_type(file: str) -> str | None:
    """!
    @brief Give the content type of an image file name from the whitelist.
    @param file The path in the images folder, as the request gave it.
    @return The content type, or None when the path is not a plain relative path
        to a file with a whitelisted ending.
    """
    if not is_local_image_path(file):
        return None
    lower = file.lower()
    for ending, content_type in IMAGE_CONTENT_TYPES.items():
        if lower.endswith(ending):
            return content_type
    return None


def register_image_route(app: Flask, images: DataFileReader) -> None:
    """!
    @brief Add the route that serves the files of the images folder.

    A path with `..`, a drive, a backslash or an ending outside the whitelist, and a
    link out of the folder, all give 404; the reader keeps every path inside.
    @param app The application.
    @param images Reads a file of the images folder, confined to it.
    """

    def show_image(file: str) -> Response:
        content_type = image_content_type(file)
        if content_type is None:
            abort(HTTPStatus.NOT_FOUND)
        try:
            content = images.read_bytes(file)
        except DataSourceError:
            abort(HTTPStatus.NOT_FOUND)
        return Response(content, content_type=content_type)

    app.add_url_rule(
        ROUTE_IMAGES,
        _ENDPOINT,
        show_image,
        methods=ALLOWED_METHODS,
        provide_automatic_options=False,
    )
