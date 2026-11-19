"""!
@file link_option.py
@brief Read the value of the `--link` option.
"""

from portfolio.application.dto.link_item import LinkItem
from portfolio.constants import LINK_SEPARATOR, MESSAGE_LINK_FORMAT
from portfolio.presentation.shared.usage_error import UsageError


def parse_link(text: str) -> LinkItem:
    """!
    @brief Split `LABEL=URL` at the first separator.
    @param text The value of the option.
    @return The link; the entity checks that both parts are filled.
    @throws UsageError The text holds no separator.
    """
    label, separator, url = text.partition(LINK_SEPARATOR)
    if not separator:
        raise UsageError(MESSAGE_LINK_FORMAT.format(value=text))
    return LinkItem(label=label, url=url)
