"""!
@file error_handlers.py
@brief The error pages: plain pages without a stack trace.
"""

import logging
from collections.abc import Mapping
from http import HTTPStatus
from types import MappingProxyType

from flask import Flask, Response, make_response, render_template
from werkzeug.exceptions import HTTPException, MethodNotAllowed

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.constants import (
    ERROR_TEMPLATE,
    ERROR_TEXT_METHOD_NOT_ALLOWED,
    ERROR_TEXT_NOT_FOUND,
    ERROR_TEXT_SERVER,
)

_logger = logging.getLogger(__name__)

_ALLOW = "Allow"

# What the page says for a status; any other status says its standard phrase.
_TEXTS: Mapping[HTTPStatus, str] = MappingProxyType(
    {
        HTTPStatus.NOT_FOUND: ERROR_TEXT_NOT_FOUND,
        HTTPStatus.METHOD_NOT_ALLOWED: ERROR_TEXT_METHOD_NOT_ALLOWED,
        HTTPStatus.INTERNAL_SERVER_ERROR: ERROR_TEXT_SERVER,
    }
)


def _error_page(status: HTTPStatus) -> Response:
    text = _TEXTS.get(status, status.phrase)
    page = render_template(
        ERROR_TEMPLATE, status=status.value, reason=status.phrase, message=text
    )
    return make_response(page, status.value)


def register_error_handlers(app: Flask) -> None:
    """!
    @brief Show a plain page for every HTTP error and for a failed read of the data.

    The page names the status and says what is wrong in one sentence; it never
    shows the exception, a path or a stack trace. The details go to the log.
    @param app The application.
    """

    @app.errorhandler(HTTPException)
    def show_http_error(error: HTTPException) -> Response:
        status = HTTPStatus(error.code or HTTPStatus.INTERNAL_SERVER_ERROR)
        response = _error_page(status)
        if isinstance(error, MethodNotAllowed) and error.valid_methods:
            response.headers[_ALLOW] = ", ".join(sorted(error.valid_methods))
        return response

    @app.errorhandler(DataSourceError)
    def show_data_error(error: DataSourceError) -> Response:
        _logger.error("The data cannot be read: %s", error)
        return _error_page(HTTPStatus.INTERNAL_SERVER_ERROR)
