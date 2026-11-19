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

## @brief Longest accepted URL (image or source code), in characters.
MAX_URL_LENGTH: Final[int] = 200

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

## @brief JSON key of the full name in the profile.
JSON_KEY_NAME: Final[str] = "name"

## @brief JSON key of the headline in the profile.
JSON_KEY_HEADLINE: Final[str] = "headline"

## @brief JSON key of the summary in the profile.
JSON_KEY_SUMMARY: Final[str] = "summary"

## @brief JSON key of the skills list in the profile.
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
