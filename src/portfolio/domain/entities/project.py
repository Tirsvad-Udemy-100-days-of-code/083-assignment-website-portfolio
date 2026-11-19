"""!
@file project.py
@brief The Project entity: one piece of work shown in the portfolio.
"""

from dataclasses import dataclass

from portfolio.constants import (
    MAX_DESCRIPTION_LENGTH,
    MAX_KIND_LENGTH,
    MAX_TITLE_LENGTH,
    MAX_URL_LENGTH,
)
from portfolio.domain.errors.invalid_project_error import InvalidProjectError
from portfolio.domain.validation import require_max_length, require_non_blank


@dataclass(frozen=True, slots=True)
class Project:
    """!
    @brief An immutable project of the portfolio; invalid data cannot exist.
    """

    ## @brief Name of the project.
    title: str
    ## @brief Kind of project (the JSON key `type`).
    kind: str
    ## @brief Short description of the project.
    description: str
    ## @brief URL of the project image; empty when there is none.
    image_url: str
    ## @brief URL of the source code.
    source_code_url: str

    def __post_init__(self) -> None:
        """!
        @brief Check the rules of a project.
        @throws InvalidProjectError A field is blank or too long.
        """
        self._check_text("title", self.title, MAX_TITLE_LENGTH)
        self._check_text("kind", self.kind, MAX_KIND_LENGTH)
        self._check_text("description", self.description, MAX_DESCRIPTION_LENGTH)
        require_max_length(
            self.image_url, "image_url", MAX_URL_LENGTH, InvalidProjectError
        )
        self._check_text("source_code_url", self.source_code_url, MAX_URL_LENGTH)

    @staticmethod
    def _check_text(field: str, value: str, max_length: int) -> None:
        require_non_blank(value, field, InvalidProjectError)
        require_max_length(value, field, max_length, InvalidProjectError)
