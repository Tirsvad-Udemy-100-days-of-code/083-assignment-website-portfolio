"""!
@file profile.py
@brief The Profile entity: who the portfolio is about.
"""

from dataclasses import dataclass

from portfolio.domain.errors.invalid_profile_error import InvalidProfileError
from portfolio.domain.validation import require_non_blank
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

    def __post_init__(self) -> None:
        """!
        @brief Check the rules of a profile.
        @throws InvalidProfileError A text is blank or there is no skill.
        """
        require_non_blank(self.name, "name", InvalidProfileError)
        require_non_blank(self.headline, "headline", InvalidProfileError)
        require_non_blank(self.summary, "summary", InvalidProfileError)
        if not self.skills:
            raise InvalidProfileError("skills must not be empty")
        for skill in self.skills:
            require_non_blank(skill, "skill", InvalidProfileError)
