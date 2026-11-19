"""!
@file project.py
@brief The Project entity: one piece of work shown in the portfolio.
"""

from dataclasses import dataclass

from portfolio.constants import (
    MAX_DESCRIPTION_LENGTH,
    MAX_KIND_LENGTH,
    MAX_PROJECT_SKILLS,
    MAX_SKILL_LENGTH,
    MAX_TAG_LENGTH,
    MAX_TAGS,
    MAX_TITLE_LENGTH,
    MAX_URL_LENGTH,
)
from portfolio.domain.errors.invalid_project_error import InvalidProjectError
from portfolio.domain.validation import (
    is_local_image_path,
    is_remote_url,
    require_max_length,
    require_non_blank,
    require_text_list,
)

_IMAGE_RULE = (
    "image_url must be empty, an http or https address, or a relative path to an "
    "image file in the data folder"
)


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
    ## @brief Image of the project: an http or https address, a relative path to an
    ## image file in the data folder, or empty when there is none.
    image_url: str
    ## @brief URL of the source code.
    source_code_url: str
    ## @brief Short labels such as the languages used; may be empty.
    tags: tuple[str, ...] = ()
    ## @brief Skills the project shows; may be empty.
    skills: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """!
        @brief Check the rules of a project.
        @throws InvalidProjectError A field is blank, too long or not allowed.
        """
        self._check_text("title", self.title, MAX_TITLE_LENGTH)
        self._check_text("kind", self.kind, MAX_KIND_LENGTH)
        self._check_text("description", self.description, MAX_DESCRIPTION_LENGTH)
        require_max_length(
            self.image_url, "image_url", MAX_URL_LENGTH, InvalidProjectError
        )
        self._check_image(self.image_url)
        self._check_text("source_code_url", self.source_code_url, MAX_URL_LENGTH)
        require_text_list(
            self.tags, "tag", MAX_TAGS, MAX_TAG_LENGTH, InvalidProjectError
        )
        require_text_list(
            self.skills,
            "skill",
            MAX_PROJECT_SKILLS,
            MAX_SKILL_LENGTH,
            InvalidProjectError,
        )

    @staticmethod
    def _check_text(field: str, value: str, max_length: int) -> None:
        require_non_blank(value, field, InvalidProjectError)
        require_max_length(value, field, max_length, InvalidProjectError)

    @staticmethod
    def _check_image(image_url: str) -> None:
        if image_url and not (
            is_remote_url(image_url) or is_local_image_path(image_url)
        ):
            raise InvalidProjectError(_IMAGE_RULE)
