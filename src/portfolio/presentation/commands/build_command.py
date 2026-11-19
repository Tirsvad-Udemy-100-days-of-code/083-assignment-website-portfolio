"""!
@file build_command.py
@brief Command `build`: write the site from the data files.
"""

import logging
from collections.abc import Callable
from pathlib import Path

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.application.errors.site_write_error import SiteWriteError
from portfolio.constants import (
    EXIT_DATA_ERROR,
    EXIT_OK,
    EXIT_OUTPUT_ERROR,
    MESSAGE_BUILT,
)
from portfolio.presentation.shared.console import write_error, write_info

## @brief A function that builds the site from a data folder into an output folder
## and returns the relative paths of the files it wrote.
SiteBuilder = Callable[[Path, Path], tuple[str, ...]]

_logger = logging.getLogger(__name__)


class BuildCommand:
    """!
    @brief Runs the build_site use case and reports the result to the user.
    """

    def __init__(self, build: SiteBuilder) -> None:
        """!
        @brief Create the command.
        @param build The build_site use case, with its adapters already given.
        """
        self._build = build

    def run(self, data_dir: Path, output_dir: Path) -> int:
        """!
        @brief Build the site.
        @param data_dir Folder with the JSON data files.
        @param output_dir Folder to write the site to.
        @return The exit code: 0 on success, 2 for a data file problem and 3 when
            the output cannot be written.
        """
        try:
            written = self._build(data_dir, output_dir)
        except DataSourceError as err:
            _logger.debug("The data cannot be read", exc_info=True)
            write_error(str(err))
            return EXIT_DATA_ERROR
        except SiteWriteError as err:
            _logger.debug("The site cannot be written", exc_info=True)
            write_error(str(err))
            return EXIT_OUTPUT_ERROR
        write_info(MESSAGE_BUILT.format(count=len(written), folder=output_dir))
        return EXIT_OK
