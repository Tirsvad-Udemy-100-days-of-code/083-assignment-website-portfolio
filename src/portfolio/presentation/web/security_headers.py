"""!
@file security_headers.py
@brief The security headers every response carries.
"""

from flask import Flask, Response

from portfolio.constants import SECURITY_HEADERS


def register_security_headers(app: Flask) -> None:
    """!
    @brief Add the security headers to every response, error pages included.
    @param app The application.
    """

    @app.after_request
    def add_headers(response: Response) -> Response:
        for name, value in SECURITY_HEADERS:
            response.headers[name] = value
        return response
