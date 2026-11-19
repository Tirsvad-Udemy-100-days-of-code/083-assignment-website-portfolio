"""!
@file constants.py
@brief Every constant of the portfolio project, defined once.

Other modules import their constants from here; no module repeats a literal
that is defined in this file.
"""

from typing import Final

## @brief Name of the package and of the command line program.
APP_NAME: Final[str] = "portfolio"

## @brief One-line description of the program, shown in the command line help.
APP_DESCRIPTION: Final[str] = "Build and preview a portfolio website."

## @brief Folder that holds the JSON data files, relative to the working directory.
DEFAULT_DATA_DIR: Final[str] = "data"

## @brief Folder the generated site is written to, relative to the working directory.
DEFAULT_OUTPUT_DIR: Final[str] = "build"

## @brief Host the preview server binds to; loopback only, so nothing is exposed.
DEFAULT_HOST: Final[str] = "127.0.0.1"

## @brief Port of the preview server.
DEFAULT_PORT: Final[int] = 8000

## @brief Title of the site, shown on every page.
SITE_TITLE: Final[str] = "Portfolio"

## @brief Largest number of projects the home page shows.
HOME_PROJECT_LIMIT: Final[int] = 10

## @brief Longest accepted project title, in characters.
MAX_TITLE_LENGTH: Final[int] = 30

## @brief Longest accepted project kind (the JSON key `type`), in characters.
MAX_KIND_LENGTH: Final[int] = 30

## @brief Longest accepted project description, in characters.
MAX_DESCRIPTION_LENGTH: Final[int] = 250

## @brief Longest accepted URL, image path or photo path, in characters.
MAX_URL_LENGTH: Final[int] = 200

## @brief Longest accepted project tag, in characters.
MAX_TAG_LENGTH: Final[int] = 30

## @brief Largest number of tags on one project.
MAX_TAGS: Final[int] = 10

## @brief Longest accepted project skill, in characters.
MAX_SKILL_LENGTH: Final[int] = 60

## @brief Largest number of skills on one project.
MAX_PROJECT_SKILLS: Final[int] = 10

## @brief File name endings an image of the data folder may have, in lower case.
IMAGE_EXTENSIONS: Final[tuple[str, ...]] = (
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".avif",
)

## @brief Number of colours the placeholder of a card without image can have.
PLACEHOLDER_COLOR_COUNT: Final[int] = 6

## @brief Character encoding of every text file the program reads or writes.
ENCODING: Final[str] = "utf-8"

## @brief Name of the JSON file that lists the projects, inside the data folder.
PROJECTS_FILE_NAME: Final[str] = "projects.json"

## @brief Name of the JSON file that holds the profile, inside the data folder.
PROFILE_FILE_NAME: Final[str] = "profile.json"

## @brief File name of the home page in the generated site.
HOME_PAGE_FILE_NAME: Final[str] = "index.html"

## @brief File name of the about page in the generated site.
ABOUT_PAGE_FILE_NAME: Final[str] = "about.html"

## @brief File name of the stylesheet, in the package and in the generated site.
STYLESHEET_FILE_NAME: Final[str] = "style.css"

## @brief Folder of the presentation package that holds the stylesheet.
STATIC_DIR_NAME: Final[str] = "static"

## @brief Package that holds the static files, as importlib.resources names it.
PRESENTATION_PACKAGE: Final[str] = "portfolio.presentation"

## @brief Name of the command that builds the site.
COMMAND_BUILD: Final[str] = "build"

## @brief Name of the command that serves the built site.
COMMAND_SERVE: Final[str] = "serve"

## @brief Exit code of a run that succeeded.
EXIT_OK: Final[int] = 0

## @brief Exit code when a data file is missing or invalid.
EXIT_DATA_ERROR: Final[int] = 2

## @brief Exit code when the output folder is missing or cannot be written.
EXIT_OUTPUT_ERROR: Final[int] = 3

## @brief Exit code when the preview server cannot start.
EXIT_SERVER_ERROR: Final[int] = 4

## @brief Format of the log lines written by the `logging` module.
LOG_FORMAT: Final[str] = "%(message)s"

## @brief JSON key of the project title.
JSON_KEY_TITLE: Final[str] = "title"

## @brief JSON key of the project kind.
JSON_KEY_KIND: Final[str] = "type"

## @brief JSON key of the project description.
JSON_KEY_DESCRIPTION: Final[str] = "description"

## @brief JSON key of the project image URL.
JSON_KEY_IMAGE_URL: Final[str] = "img_url"

## @brief JSON key of the project source code URL.
JSON_KEY_SOURCE_CODE_URL: Final[str] = "source_code_url"

## @brief JSON key of the tag list of a project.
JSON_KEY_TAGS: Final[str] = "tags"

## @brief JSON key of the profile photo, a path inside the data folder.
JSON_KEY_PHOTO: Final[str] = "photo"

## @brief JSON key of the full name in the profile.
JSON_KEY_NAME: Final[str] = "name"

## @brief JSON key of the headline in the profile.
JSON_KEY_HEADLINE: Final[str] = "headline"

## @brief JSON key of the summary in the profile.
JSON_KEY_SUMMARY: Final[str] = "summary"

## @brief JSON key of the skills list, in the profile and in a project.
JSON_KEY_SKILLS: Final[str] = "skills"

## @brief JSON key of the links list in the profile.
JSON_KEY_LINKS: Final[str] = "links"

## @brief JSON key of the text of a link.
JSON_KEY_LABEL: Final[str] = "label"

## @brief JSON key of the address of a link.
JSON_KEY_URL: Final[str] = "url"

## @brief URL schemes a link or image may use; anything else is replaced.
SAFE_URL_SCHEMES: Final[tuple[str, ...]] = ("http", "https")

## @brief URL put in place of an unsafe one, so the page still renders.
FALLBACK_URL: Final[str] = "#"

## @brief Language of the generated pages.
HTML_LANG: Final[str] = "en"

## @brief Label of the link to the home page.
NAV_HOME_LABEL: Final[str] = "Home"

## @brief Label of the link to the about page.
NAV_ABOUT_LABEL: Final[str] = "About"

## @brief Accessible name of the navigation.
NAV_ARIA_LABEL: Final[str] = "Main"

## @brief Footer text of every page; it holds no year, so the output is stable.
FOOTER_TEXT: Final[str] = "Built with the Python standard library."

## @brief Heading of the project list on the home page.
HOME_HEADING: Final[str] = "My projects"

## @brief Text shown on the home page when there is no project.
EMPTY_STATE_TEXT: Final[str] = (
    "No projects yet. Add some to the projects data file and build the site again."
)

## @brief Text of the link to the source code of a project.
SOURCE_CODE_LABEL: Final[str] = "Source code"

## @brief Heading of the skills list on the about page.
SKILLS_HEADING: Final[str] = "Skills"

## @brief Accessible name of the list of tags on the back of a project card.
TAGS_LABEL: Final[str] = "Tags"

## @brief Heading of the links list on the about page.
LINKS_HEADING: Final[str] = "Links"

## @brief Help text of the build command.
HELP_BUILD: Final[str] = "Write the site (HTML and CSS) from the data files."

## @brief Help text of the serve command.
HELP_SERVE: Final[str] = "Serve the built site on a local web server."

## @brief Help text of the option that names the data folder.
HELP_DATA_DIR: Final[str] = "Folder with the JSON data files (default: %(default)s)."

## @brief Help text of the option that names the output folder.
HELP_OUTPUT_DIR: Final[str] = "Folder of the generated site (default: %(default)s)."

## @brief Help text of the option that names the host.
HELP_HOST: Final[str] = "Address to bind the server to (default: %(default)s)."

## @brief Help text of the option that names the port.
HELP_PORT: Final[str] = "Port of the server (default: %(default)s)."

## @brief Message after a build; fields: count, folder.
MESSAGE_BUILT: Final[str] = "Built {count} files into {folder}\n"

## @brief Message when the server starts; fields: folder, host, port.
MESSAGE_SERVING: Final[str] = (
    "Serving {folder} at http://{host}:{port}/ (press Ctrl+C to stop)\n"
)

## @brief Message after the server stopped.
MESSAGE_STOPPED: Final[str] = "Server stopped.\n"

## @brief Format of an error message on the error stream; field: message.
MESSAGE_ERROR: Final[str] = "error: {message}\n"

## @brief Error when the folder to serve is missing; field: folder.
MESSAGE_MISSING_OUTPUT: Final[str] = (
    "output folder {folder} does not exist; run the build command first"
)

## @brief Error when the server cannot start; fields: host, port, reason.
MESSAGE_SERVER_FAILED: Final[str] = "cannot start the server on {host}:{port}: {reason}"

## @brief Database file, relative to the working directory; ignored by git.
DEFAULT_DATABASE_PATH: Final[str] = "data/portfolio.db"

## @brief Location that SQLite keeps in memory only; used by the tests.
IN_MEMORY_DATABASE: Final[str] = ":memory:"

## @brief Version of the database schema, stored in `PRAGMA user_version`.
##
## The schema script in `sqlite_schema.py` sets the same number; PRAGMA cannot take
## a parameter, so a test checks that the two agree.
SCHEMA_VERSION: Final[int] = 1

## @brief Name of the command that creates the database.
COMMAND_INIT: Final[str] = "init"

## @brief Name of the command that imports the JSON data files.
COMMAND_IMPORT: Final[str] = "import"

## @brief Name of the command group that manages the projects.
COMMAND_PROJECT: Final[str] = "project"

## @brief Name of the command group that manages the profile.
COMMAND_PROFILE: Final[str] = "profile"

## @brief Name of the sub-command that lists the projects.
SUBCOMMAND_LIST: Final[str] = "list"

## @brief Name of the sub-command that adds a project.
SUBCOMMAND_ADD: Final[str] = "add"

## @brief Name of the sub-command that changes a project or the profile.
SUBCOMMAND_SET: Final[str] = "set"

## @brief Name of the sub-command that removes a project.
SUBCOMMAND_REMOVE: Final[str] = "remove"

## @brief Separator between the label and the address in the option `--link`.
LINK_SEPARATOR: Final[str] = "="

## @brief Help text of the init command.
HELP_INIT: Final[str] = "Create the database, or check that it is up to date."

## @brief Help text of the import command.
HELP_IMPORT: Final[str] = "Copy the JSON data files into the database."

## @brief Help text of the project command group.
HELP_PROJECT: Final[str] = "Manage the projects in the database."

## @brief Help text of the profile command group.
HELP_PROFILE: Final[str] = "Manage the profile in the database."

## @brief Help text of the project list command.
HELP_PROJECT_LIST: Final[str] = "List the projects."

## @brief Help text of the project add command.
HELP_PROJECT_ADD: Final[str] = "Add a project."

## @brief Help text of the project set command.
HELP_PROJECT_SET: Final[str] = "Change the given fields of a project."

## @brief Help text of the project remove command.
HELP_PROJECT_REMOVE: Final[str] = "Remove a project."

## @brief Help text of the profile set command.
HELP_PROFILE_SET: Final[str] = "Create the profile or change the given fields."

## @brief Help text of the option that names the database.
HELP_DATABASE: Final[str] = "Database file (default: %(default)s)."

## @brief Help text of the option that replaces existing data on import.
HELP_REPLACE: Final[str] = "Replace the data of a database that already holds some."

## @brief Help text of the argument that names a project.
HELP_PROJECT_TITLE: Final[str] = "Title of the project."

## @brief Help text of the option that gives the title of a new project.
HELP_TITLE: Final[str] = "Title of the new project."

## @brief Help text of the option that gives a new title to a project.
HELP_NEW_TITLE: Final[str] = "New title of the project."

## @brief Help text of the option that gives the kind of a project.
HELP_KIND: Final[str] = "Kind of project, for example Website."

## @brief Help text of the option that gives the description of a project.
HELP_DESCRIPTION: Final[str] = "Short description of the project."

## @brief Help text of the option that gives the image of a project.
HELP_IMAGE_URL: Final[str] = (
    "http or https address, or relative path of an image in the data folder."
)

## @brief Help text of the option that gives the source code address of a project.
HELP_SOURCE_CODE_URL: Final[str] = "Address of the source code."

## @brief Help text of the option that gives one tag; repeat it for more.
HELP_TAG: Final[str] = "A tag of the project; repeat the option. Replaces the tags."

## @brief Help text of the option that gives one project skill; repeat it for more.
HELP_PROJECT_SKILL: Final[str] = (
    "A skill of the project; repeat the option. Replaces the skills."
)

## @brief Help text of the option that gives the name of the profile.
HELP_NAME: Final[str] = "Full name."

## @brief Help text of the option that gives the headline of the profile.
HELP_HEADLINE: Final[str] = "One-line professional headline."

## @brief Help text of the option that gives the summary of the profile.
HELP_SUMMARY: Final[str] = "Short text about the person."

## @brief Help text of the option that gives the photo of the profile.
HELP_PHOTO: Final[str] = "Relative path of the photo in the data folder."

## @brief Help text of the option that gives one profile skill.
HELP_PROFILE_SKILL: Final[str] = (
    "A skill of the profile; repeat the option. Replaces the skills."
)

## @brief Help text of the option that gives one profile link.
HELP_LINK: Final[str] = "A link as LABEL=URL; repeat the option. Replaces the links."

## @brief Message after init created the database; fields: path, version.
MESSAGE_DATABASE_CREATED: Final[str] = (
    "Created the database {path} (schema version {version})\n"
)

## @brief Message after init found a current database; fields: path, version.
MESSAGE_DATABASE_READY: Final[str] = (
    "The database {path} is up to date (schema version {version})\n"
)

## @brief Message after an import; fields: count, path.
MESSAGE_IMPORTED: Final[str] = "Imported {count} projects and the profile into {path}\n"

## @brief Message after a project was added; field: title.
MESSAGE_PROJECT_ADDED: Final[str] = "Added the project {title!r}\n"

## @brief Message after a project was changed; field: title.
MESSAGE_PROJECT_CHANGED: Final[str] = "Changed the project {title!r}\n"

## @brief Message after a project was removed; field: title.
MESSAGE_PROJECT_REMOVED: Final[str] = "Removed the project {title!r}\n"

## @brief Message after the profile was created.
MESSAGE_PROFILE_CREATED: Final[str] = "Created the profile\n"

## @brief Message after the profile was changed.
MESSAGE_PROFILE_CHANGED: Final[str] = "Changed the profile\n"

## @brief Message of the project list when there is no project.
MESSAGE_NO_PROJECTS: Final[str] = "No projects.\n"

## @brief One line of the project list; fields: title, kind, source_code_url.
MESSAGE_PROJECT_LINE: Final[str] = "{title} | {kind} | {source_code_url}\n"

## @brief Error when no project has the title; field: title.
MESSAGE_PROJECT_NOT_FOUND: Final[str] = "no project has the title {title!r}"

## @brief Error when a project already has the title; field: title.
MESSAGE_PROJECT_EXISTS: Final[str] = "a project with the title {title!r} already exists"

## @brief Error when the database holds no profile.
MESSAGE_PROFILE_MISSING: Final[str] = (
    "the database holds no profile yet; create it with the profile set command"
)

## @brief Error when an import would overwrite data.
MESSAGE_DATABASE_NOT_EMPTY: Final[str] = (
    "the database already holds data; use --replace to overwrite it"
)

## @brief Error when the database file does not exist.
MESSAGE_DATABASE_NOT_FOUND: Final[str] = (
    "database not found; run the init command first"
)

## @brief Error when the schema is missing; the database is not initialised.
MESSAGE_SCHEMA_MISSING: Final[str] = (
    "the database has no schema; run the init command first"
)

## @brief Error when the schema is newer than the program; fields: found, known.
MESSAGE_SCHEMA_NEWER: Final[str] = (
    "the database has schema version {found}, newer than version {known} "
    "that this program knows; update the program"
)

## @brief Error when the schema version is not one this program can use.
MESSAGE_SCHEMA_UNKNOWN: Final[str] = (
    "the database has the unknown schema version {found}"
)

## @brief Error when a change has no new value.
MESSAGE_NOTHING_TO_CHANGE: Final[str] = "nothing to change: no new value was given"

## @brief Error when the profile does not exist and the data to create it is short.
MESSAGE_NEW_PROFILE_INCOMPLETE: Final[str] = (
    "a new profile needs a name, a headline, a summary and at least one skill"
)

## @brief Error when a link option is not LABEL=URL; field: value.
MESSAGE_LINK_FORMAT: Final[str] = "link {value!r} must look like LABEL=URL"
