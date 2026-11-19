"""!
@file __main__.py
@brief Entry point of `python -m portfolio` and composition root of the program.

This is the only module that names the concrete adapters; it creates them and
hands them to the commands.
"""

import argparse
import logging
from collections.abc import Callable, Sequence
from pathlib import Path

from portfolio.application.use_cases.build_site import build_site
from portfolio.constants import (
    APP_DESCRIPTION,
    APP_NAME,
    COMMAND_BUILD,
    COMMAND_SERVE,
    DEFAULT_DATA_DIR,
    DEFAULT_HOST,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PORT,
    EXIT_OK,
    HELP_BUILD,
    HELP_DATA_DIR,
    HELP_HOST,
    HELP_OUTPUT_DIR,
    HELP_PORT,
    HELP_SERVE,
    LOG_FORMAT,
    PROFILE_FILE_NAME,
    PROJECTS_FILE_NAME,
)
from portfolio.infrastructure.repositories.json_profile_repository import (
    JsonProfileRepository,
)
from portfolio.infrastructure.repositories.json_project_repository import (
    JsonProjectRepository,
)
from portfolio.infrastructure.site_writer import FileSiteWriter
from portfolio.presentation.commands.build_command import BuildCommand
from portfolio.presentation.commands.serve_command import (
    ServeCommand,
    serve_directory,
)
from portfolio.presentation.html_site_renderer import HtmlSiteRenderer

_Handler = Callable[[argparse.Namespace], int]


def build_parser() -> argparse.ArgumentParser:
    """!
    @brief Create the command line parser with the commands build and serve.
    @return The parser of the program.
    """
    parser = argparse.ArgumentParser(
        prog=f"python -m {APP_NAME}",
        description=APP_DESCRIPTION,
    )
    commands = parser.add_subparsers(title="commands", dest="command")

    build = commands.add_parser(COMMAND_BUILD, help=HELP_BUILD, description=HELP_BUILD)
    build.add_argument(
        "--data", type=Path, default=Path(DEFAULT_DATA_DIR), help=HELP_DATA_DIR
    )
    build.add_argument(
        "--out", type=Path, default=Path(DEFAULT_OUTPUT_DIR), help=HELP_OUTPUT_DIR
    )
    build.set_defaults(handler=_run_build)

    serve = commands.add_parser(COMMAND_SERVE, help=HELP_SERVE, description=HELP_SERVE)
    serve.add_argument(
        "--out", type=Path, default=Path(DEFAULT_OUTPUT_DIR), help=HELP_OUTPUT_DIR
    )
    serve.add_argument("--host", default=DEFAULT_HOST, help=HELP_HOST)
    serve.add_argument("--port", type=int, default=DEFAULT_PORT, help=HELP_PORT)
    serve.set_defaults(handler=_run_serve)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """!
    @brief Run the program.
    @param argv The command line arguments; `sys.argv` when None.
    @return The process exit code; 0 and the help text when no command is given.
    """
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    parser = build_parser()
    arguments = parser.parse_args(argv)
    handler: _Handler | None = getattr(arguments, "handler", None)
    if handler is None:
        parser.print_help()
        return EXIT_OK
    return handler(arguments)


def _run_build(arguments: argparse.Namespace) -> int:
    return BuildCommand(_build_site).run(arguments.data, arguments.out)


def _run_serve(arguments: argparse.Namespace) -> int:
    return ServeCommand(serve_directory).run(
        arguments.out, arguments.host, arguments.port
    )


def _build_site(data_dir: Path, output_dir: Path) -> tuple[str, ...]:
    return build_site(
        JsonProjectRepository(data_dir / PROJECTS_FILE_NAME),
        JsonProfileRepository(data_dir / PROFILE_FILE_NAME),
        HtmlSiteRenderer(),
        FileSiteWriter(output_dir),
    )


if __name__ == "__main__":
    raise SystemExit(main())
