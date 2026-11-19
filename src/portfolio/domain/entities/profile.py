"""!
@file profile.py
@brief The Profile entity: who the portfolio is about.
"""

from dataclasses import dataclass

from portfolio.constants import MAX_URL_LENGTH
from portfolio.domain.errors.invalid_profile_error import InvalidProfileError
from portfolio.domain.validation import (
    is_local_image_path,
    require_max_length,
    require_non_blank,
)
from portfolio.domain.value_objects.link import Link


@dataclass(frozen=True, slots=True)
class Profile:
    """!
    @brief An immutable profile of the owner of the portfolio.
    """

    ## @brief Full name.
    name: str
    ## @brief One-line professional headline.
    headline: str
    ## @brief Short text about the person.
    summary: str
    ## @brief Skills, at least one.
    skills: tuple[str, ...]
    ## @brief Links to other sites.
    links: tuple[Link, ...]
    ## @brief Relative path to the photo in the data folder; None when there is none.
    photo: str | None = None

    def __post_init__(self) -> None:
        """!
        @brief Check the rules of a profile.
        @throws InvalidProfileError A text is blank, there is no skill or the photo
            is not a relative path to an image file.
        """
        require_non_blank(self.name, "name", InvalidProfileError)
        require_non_blank(self.headline, "headline", InvalidProfileError)
        require_non_blank(self.summary, "summary", InvalidProfileError)
        if not self.skills:
            raise InvalidProfileError("skills must not be empty")
        for skill in self.skills:
            require_non_blank(skill, "skill", InvalidProfileError)
        self._check_photo()

    @property
    def initials(self) -> str:
        """!
        @brief The first letters of the first and the last word of the name.
        @return Upper-case letters; one letter for a name of one word.
        """
        words = self.name.split()
        letters = words[0][0] if len(words) == 1 else words[0][0] + words[-1][0]
        return letters.upper()

    def _check_photo(self) -> None:
        if self.photo is None:
            return
        require_max_length(self.photo, "photo", MAX_URL_LENGTH, InvalidProfileError)
        if not is_local_image_path(self.photo):
            raise InvalidProfileError(
                "photo must be a relative path to an image file in the data folder"
            )
