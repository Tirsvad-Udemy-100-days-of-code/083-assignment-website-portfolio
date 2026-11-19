"""!
@file serve_command.py
@brief Command `serve`: show the built site on a local web server.
"""

import functools
import logging
from collections.abc import Callable
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from portfolio.constants import (
    EXIT_OK,
    EXIT_OUTPUT_ERROR,
    EXIT_SERVER_ERROR,
    MESSAGE_MISSING_OUTPUT,
    MESSAGE_SERVER_FAILED,
    MESSAGE_SERVING,
    MESSAGE_STOPPED,
)
from portfolio.presentation.shared.console import write_error, write_info

## @brief A function that serves a folder on a host and port until it is stopped.
ServerRunner = Callable[[Path, str, int], None]

_logger = logging.getLogger(__name__)


class _LoggingRequestHandler(SimpleHTTPRequestHandler):
    """!
    @brief Serves files and sends the access log to `logging`, not to the stream.
    """

    # The signature is the one of the base class, whose arguments are untyped.
    def log_message(self, format: str, *args: object) -> None:
        _logger.info("%s - %s", self.address_string(), format % args)


def create_server(directory: Path, host: str, port: int) -> ThreadingHTTPServer:
    """!
    @brief Create a web server for a folder; it is bound but does not run yet.
    @param directory The folder to serve.
    @param host Address to bind to.
    @param port Port to bind to; 0 lets the system choose a free one.
    @return The server; read the chosen port from `server_port`.
    @throws OSError The address cannot be bound.
    """
    handler = functools.partial(_LoggingRequestHandler, directory=str(directory))
    return ThreadingHTTPServer((host, port), handler)


def serve(server: ThreadingHTTPServer) -> None:
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


def serve_directory(directory: Path, host: str, port: int) -> None:
    """!
    @brief Create a server for a folder and run it until it is interrupted.
    @param directory The folder to serve.
    @param host Address to bind to.
    @param port Port to bind to.
    @throws OSError The address cannot be bound.
    """
    server = create_server(directory, host, port)
    write_info(
        MESSAGE_SERVING.format(folder=directory, host=host, port=server.server_port)
    )
    serve(server)


class ServeCommand:
    """!
    @brief Checks the folder to serve, starts the server and reports problems.
    """

    def __init__(self, runner: ServerRunner) -> None:
        """!
        @brief Create the command.
        @param runner Serves a folder; `serve_directory` in the program.
        """
        self._runner = runner

    def run(self, output_dir: Path, host: str, port: int) -> int:
        """!
        @brief Serve the built site.
        @param output_dir Folder of the built site.
        @param host Address to bind to.
        @param port Port to bind to.
        @return The exit code: 0 after a clean stop, 3 when the folder is missing
            and 4 when the server cannot start.
        """
        if not output_dir.is_dir():
            write_error(MESSAGE_MISSING_OUTPUT.format(folder=output_dir))
            return EXIT_OUTPUT_ERROR
        try:
            self._runner(output_dir, host, port)
        except (OSError, OverflowError) as err:
            _logger.debug("The server cannot start", exc_info=True)
            write_error(MESSAGE_SERVER_FAILED.format(host=host, port=port, reason=err))
            return EXIT_SERVER_ERROR
        return EXIT_OK
