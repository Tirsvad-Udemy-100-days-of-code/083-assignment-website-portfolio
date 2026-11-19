"""!
@file link.py
@brief The Link value object: a labelled address.
"""

from dataclasses import dataclass

from portfolio.domain.errors.invalid_profile_error import InvalidProfileError
from portfolio.domain.validation import require_non_blank


@dataclass(frozen=True, slots=True)
class Link:
    """!
    @brief An immutable labelled address, such as a profile on another site.
    """

    ## @brief Text shown for the link.
    label: str
    ## @brief Address the link points to.
    url: str

    def __post_init__(self) -> None:
        """!
        @brief Check the rules of a link.
        @throws InvalidProfileError The label or the url is blank.
        """
        require_non_blank(self.label, "label", InvalidProfileError)
        require_non_blank(self.url, "url", InvalidProfileError)
