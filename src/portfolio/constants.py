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
