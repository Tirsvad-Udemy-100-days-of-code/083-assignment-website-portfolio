"""!
@file guarded.py
@brief Runs a command action and turns the errors it may raise into an exit code.
"""

import logging
from collections.abc import Callable

from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.constants import EXIT_DATA_ERROR, EXIT_OK
from portfolio.domain.errors.domain_error import DomainError
from portfolio.presentation.shared.console import write_error
from portfolio.presentation.shared.usage_error import UsageError

_logger = logging.getLogger(__name__)


def run_guarded(action: Callable[[], None]) -> int:
    """!
    @brief Run an action; report a data, rule or usage error as one line.
    @param action The work of the command; it writes its own success message.
    @return 0 on success and 2 when the data, a rule or a value is wrong.
    """
    try:
        action()
    except (DomainError, DataSourceError, UsageError) as err:
        _logger.debug("The command failed", exc_info=True)
        write_error(str(err))
        return EXIT_DATA_ERROR
    return EXIT_OK
