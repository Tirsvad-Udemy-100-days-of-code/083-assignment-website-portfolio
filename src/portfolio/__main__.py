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

from portfolio.application.dto.profile_changes import ProfileChanges
from portfolio.application.dto.project_card import ProjectCard
from portfolio.application.dto.project_changes import ProjectChanges
from portfolio.application.dto.project_input import ProjectInput
from portfolio.application.use_cases.add_project import add_project
from portfolio.application.use_cases.build_site import build_site
from portfolio.application.use_cases.change_project import change_project
from portfolio.application.use_cases.import_portfolio import import_portfolio
from portfolio.application.use_cases.initialize_database import initialize_database
from portfolio.application.use_cases.list_projects import list_projects
from portfolio.application.use_cases.remove_project import remove_project
from portfolio.application.use_cases.set_profile import set_profile
from portfolio.constants import (
    APP_DESCRIPTION,
    APP_NAME,
    COMMAND_BUILD,
    COMMAND_IMPORT,
    COMMAND_INIT,
    COMMAND_PROFILE,
    COMMAND_PROJECT,
    COMMAND_SERVE,
    DEFAULT_DATA_DIR,
    DEFAULT_DATABASE_PATH,
    DEFAULT_HOST,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PORT,
    EXIT_OK,
    HELP_BUILD,
    HELP_DATA_DIR,
    HELP_DATABASE,
    HELP_DESCRIPTION,
    HELP_HEADLINE,
    HELP_HOST,
    HELP_IMAGE_URL,
    HELP_IMPORT,
    HELP_INIT,
    HELP_KIND,
    HELP_LINK,
    HELP_NAME,
    HELP_NEW_TITLE,
    HELP_OUTPUT_DIR,
    HELP_PHOTO,
    HELP_PORT,
    HELP_PROFILE,
    HELP_PROFILE_SET,
    HELP_PROFILE_SKILL,
    HELP_PROJECT,
    HELP_PROJECT_ADD,
    HELP_PROJECT_LIST,
    HELP_PROJECT_REMOVE,
    HELP_PROJECT_SET,
    HELP_PROJECT_SKILL,
    HELP_PROJECT_TITLE,
    HELP_REPLACE,
    HELP_SERVE,
    HELP_SOURCE_CODE_URL,
    HELP_SUMMARY,
    HELP_TAG,
    HELP_TITLE,
    LOG_FORMAT,
    PROFILE_FILE_NAME,
    PROJECTS_FILE_NAME,
    SUBCOMMAND_ADD,
    SUBCOMMAND_LIST,
    SUBCOMMAND_REMOVE,
    SUBCOMMAND_SET,
)
from portfolio.infrastructure.data_folder_reader import FolderDataFileReader
from portfolio.infrastructure.repositories.json_profile_repository import (
    JsonProfileRepository,
)
from portfolio.infrastructure.repositories.json_project_repository import (
    JsonProjectRepository,
)
from portfolio.infrastructure.repositories.sqlite_profile_repository import (
    SqliteProfileRepository,
)
from portfolio.infrastructure.repositories.sqlite_project_repository import (
    SqliteProjectRepository,
)
from portfolio.infrastructure.site_writer import FileSiteWriter
from portfolio.infrastructure.sqlite_database import SqliteDatabase
from portfolio.infrastructure.sqlite_database_initializer import (
    SqliteDatabaseInitializer,
)
from portfolio.infrastructure.sqlite_portfolio_importer import SqlitePortfolioImporter
from portfolio.presentation.commands.build_command import BuildCommand
from portfolio.presentation.commands.import_command import ImportCommand
from portfolio.presentation.commands.init_command import InitCommand
from portfolio.presentation.commands.profile_set_command import ProfileSetCommand
from portfolio.presentation.commands.project_add_command import ProjectAddCommand
from portfolio.presentation.commands.project_list_command import ProjectListCommand
from portfolio.presentation.commands.project_remove_command import (
    ProjectRemoveCommand,
)
from portfolio.presentation.commands.project_set_command import ProjectSetCommand
from portfolio.presentation.commands.serve_command import (
    ServeCommand,
    serve_directory,
)
from portfolio.presentation.html_site_renderer import HtmlSiteRenderer

_Handler = Callable[[argparse.Namespace], int]

# The parsers of one level of commands; the class is private in the standard
# library, and the lazy `type` statement never evaluates the subscription.
type _Commands = argparse._SubParsersAction[argparse.ArgumentParser]


def build_parser() -> argparse.ArgumentParser:
    """!
    @brief Create the command line parser with every command of the program.
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

    _add_database_commands(commands)
    return parser


def _add_database_commands(commands: _Commands) -> None:
    database = argparse.ArgumentParser(add_help=False)
    database.add_argument(
        "--db", type=Path, default=Path(DEFAULT_DATABASE_PATH), help=HELP_DATABASE
    )

    init = commands.add_parser(
        COMMAND_INIT, parents=[database], help=HELP_INIT, description=HELP_INIT
    )
    init.set_defaults(handler=_run_init)

    import_data = commands.add_parser(
        COMMAND_IMPORT, parents=[database], help=HELP_IMPORT, description=HELP_IMPORT
    )
    import_data.add_argument(
        "--data", type=Path, default=Path(DEFAULT_DATA_DIR), help=HELP_DATA_DIR
    )
    import_data.add_argument("--replace", action="store_true", help=HELP_REPLACE)
    import_data.set_defaults(handler=_run_import)

    _add_project_commands(commands, database)
    _add_profile_commands(commands, database)


def _add_project_commands(
    commands: _Commands, database: argparse.ArgumentParser
) -> None:
    project = commands.add_parser(
        COMMAND_PROJECT, help=HELP_PROJECT, description=HELP_PROJECT
    )
    actions = project.add_subparsers(
        title="commands", dest="project_command", required=True
    )

    show = actions.add_parser(
        SUBCOMMAND_LIST,
        parents=[database],
        help=HELP_PROJECT_LIST,
        description=HELP_PROJECT_LIST,
    )
    show.set_defaults(handler=_run_project_list)

    add = actions.add_parser(
        SUBCOMMAND_ADD,
        parents=[database],
        help=HELP_PROJECT_ADD,
        description=HELP_PROJECT_ADD,
    )
    add.add_argument("--title", required=True, help=HELP_TITLE)
    add.add_argument("--kind", required=True, help=HELP_KIND)
    add.add_argument("--description", required=True, help=HELP_DESCRIPTION)
    add.add_argument("--source-code-url", required=True, help=HELP_SOURCE_CODE_URL)
    add.add_argument("--image-url", default="", help=HELP_IMAGE_URL)
    add.add_argument("--tag", action="append", default=[], help=HELP_TAG)
    add.add_argument("--skill", action="append", default=[], help=HELP_PROJECT_SKILL)
    add.set_defaults(handler=_run_project_add)

    change = actions.add_parser(
        SUBCOMMAND_SET,
        parents=[database],
        help=HELP_PROJECT_SET,
        description=HELP_PROJECT_SET,
    )
    change.add_argument("title", help=HELP_PROJECT_TITLE)
    change.add_argument("--new-title", help=HELP_NEW_TITLE)
    change.add_argument("--kind", help=HELP_KIND)
    change.add_argument("--description", help=HELP_DESCRIPTION)
    change.add_argument("--source-code-url", help=HELP_SOURCE_CODE_URL)
    change.add_argument("--image-url", help=HELP_IMAGE_URL)
    change.add_argument("--tag", action="append", help=HELP_TAG)
    change.add_argument("--skill", action="append", help=HELP_PROJECT_SKILL)
    change.set_defaults(handler=_run_project_set)

    remove = actions.add_parser(
        SUBCOMMAND_REMOVE,
        parents=[database],
        help=HELP_PROJECT_REMOVE,
        description=HELP_PROJECT_REMOVE,
    )
    remove.add_argument("title", help=HELP_PROJECT_TITLE)
    remove.set_defaults(handler=_run_project_remove)


def _add_profile_commands(
    commands: _Commands, database: argparse.ArgumentParser
) -> None:
    profile = commands.add_parser(
        COMMAND_PROFILE, help=HELP_PROFILE, description=HELP_PROFILE
    )
    actions = profile.add_subparsers(
        title="commands", dest="profile_command", required=True
    )
    change = actions.add_parser(
        SUBCOMMAND_SET,
        parents=[database],
        help=HELP_PROFILE_SET,
        description=HELP_PROFILE_SET,
    )
    change.add_argument("--name", help=HELP_NAME)
    change.add_argument("--headline", help=HELP_HEADLINE)
    change.add_argument("--summary", help=HELP_SUMMARY)
    change.add_argument("--photo", help=HELP_PHOTO)
    change.add_argument("--skill", action="append", help=HELP_PROFILE_SKILL)
    change.add_argument("--link", action="append", help=HELP_LINK)
    change.set_defaults(handler=_run_profile_set)


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


def _run_init(arguments: argparse.Namespace) -> int:
    return InitCommand(_prepare_database).run(arguments.db)


def _run_import(arguments: argparse.Namespace) -> int:
    return ImportCommand(_import_data).run(
        arguments.db, arguments.data, arguments.replace
    )


def _run_project_list(arguments: argparse.Namespace) -> int:
    return ProjectListCommand(_read_projects).run(arguments.db)


def _run_project_add(arguments: argparse.Namespace) -> int:
    data = ProjectInput(
        title=arguments.title,
        kind=arguments.kind,
        description=arguments.description,
        source_code_url=arguments.source_code_url,
        image_url=arguments.image_url,
        tags=tuple(arguments.tag),
        skills=tuple(arguments.skill),
    )
    return ProjectAddCommand(_store_project).run(arguments.db, data)


def _run_project_set(arguments: argparse.Namespace) -> int:
    changes = ProjectChanges(
        title=arguments.new_title,
        kind=arguments.kind,
        description=arguments.description,
        image_url=arguments.image_url,
        source_code_url=arguments.source_code_url,
        tags=_optional_tuple(arguments.tag),
        skills=_optional_tuple(arguments.skill),
    )
    return ProjectSetCommand(_update_project).run(
        arguments.db, arguments.title, changes
    )


def _run_project_remove(arguments: argparse.Namespace) -> int:
    return ProjectRemoveCommand(_delete_project).run(arguments.db, arguments.title)


def _run_profile_set(arguments: argparse.Namespace) -> int:
    changes = ProfileChanges(
        name=arguments.name,
        headline=arguments.headline,
        summary=arguments.summary,
        photo=arguments.photo,
        skills=_optional_tuple(arguments.skill),
    )
    return ProfileSetCommand(_store_profile).run(arguments.db, changes, arguments.link)


def _optional_tuple(values: list[str] | None) -> tuple[str, ...] | None:
    return None if values is None else tuple(values)


def _prepare_database(path: Path) -> bool:
    return initialize_database(SqliteDatabaseInitializer(SqliteDatabase(path)))


def _import_data(path: Path, data_dir: Path, replace: bool) -> int:
    return import_portfolio(
        JsonProjectRepository(data_dir / PROJECTS_FILE_NAME),
        JsonProfileRepository(data_dir / PROFILE_FILE_NAME),
        SqlitePortfolioImporter(SqliteDatabase(path)),
        replace,
    )


def _read_projects(path: Path) -> tuple[ProjectCard, ...]:
    return list_projects(SqliteProjectRepository(SqliteDatabase(path)))


def _store_project(path: Path, data: ProjectInput) -> None:
    add_project(SqliteProjectRepository(SqliteDatabase(path)), data)


def _update_project(path: Path, title: str, changes: ProjectChanges) -> str:
    repository = SqliteProjectRepository(SqliteDatabase(path))
    return change_project(repository, repository, title, changes)


def _delete_project(path: Path, title: str) -> None:
    remove_project(SqliteProjectRepository(SqliteDatabase(path)), title)


def _store_profile(path: Path, changes: ProfileChanges) -> bool:
    repository = SqliteProfileRepository(SqliteDatabase(path))
    return set_profile(repository, repository, changes)


def _build_site(data_dir: Path, output_dir: Path) -> tuple[str, ...]:
    return build_site(
        JsonProjectRepository(data_dir / PROJECTS_FILE_NAME),
        JsonProfileRepository(data_dir / PROFILE_FILE_NAME),
        FolderDataFileReader(data_dir),
        HtmlSiteRenderer(),
        FileSiteWriter(output_dir),
    )


if __name__ == "__main__":
    raise SystemExit(main())
