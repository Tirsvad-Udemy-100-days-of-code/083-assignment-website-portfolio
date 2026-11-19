"""!
@file server.py
@brief Create and run the web server that serves the Flask application.
"""

from typing import Protocol

from flask import Flask
from werkzeug.serving import BaseWSGIServer, make_server

from portfolio.constants import MESSAGE_SERVING, MESSAGE_STOPPED
from portfolio.presentation.shared.console import write_info


class RunnableServer(Protocol):
    """!
    @brief A bound web server that can run and be closed.
    """

    @property
    def server_port(self) -> int:
        """!
        @brief The port the server is bound to.
        @return The port; the one the system chose when port 0 was asked.
        """
        ...

    def serve_forever(self) -> None:
        """!
        @brief Handle requests until `shutdown` is called.
        """
        ...

    def server_close(self) -> None:
        """!
        @brief Release the port.
        """
        ...


def create_server(app: Flask, host: str, port: int) -> BaseWSGIServer:
    """!
    @brief Create a threaded web server for an application; it is bound but not running.
    @param app The application to serve.
    @param host Address to bind to.
    @param port Port to bind to; 0 lets the system choose a free one.
    @return The server; read the chosen port from `server_port`.
    @throws OSError The address cannot be bound.
    """
    return make_server(host, port, app, threaded=True)


def serve(server: RunnableServer) -> None:
    """!
    @brief Serve requests until the user interrupts with Ctrl+C, then close.
    @param server The server to run.
    """
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        write_info(MESSAGE_STOPPED)
    finally:
        server.server_close()


def serve_app(app: Flask, host: str, port: int) -> None:
    """!
    @brief Create a server for an application and run it until it is interrupted.
    @param app The application to serve.
    @param host Address to bind to.
    @param port Port to bind to.
    @throws OSError The address cannot be bound.
    """
    server = create_server(app, host, port)
    write_info(MESSAGE_SERVING.format(host=host, port=server.server_port))
    serve(server)
