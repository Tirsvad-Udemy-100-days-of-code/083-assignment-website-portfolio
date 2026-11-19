"""!
@file changed_fields.py
@brief Pick the fields of a change object that carry a new value.
"""

from dataclasses import fields
from typing import Any

from portfolio.application.dto.profile_changes import ProfileChanges
from portfolio.application.dto.project_changes import ProjectChanges


def changed_fields(changes: ProjectChanges | ProfileChanges) -> dict[str, Any]:
    """!
    @brief Collect the fields that are not None.
    @param changes The change object.
    @return The field names with their new values.
    """
    # Any: the values are handed to dataclasses.replace, which takes any field type.
    values = {field.name: getattr(changes, field.name) for field in fields(changes)}
    return {name: value for name, value in values.items() if value is not None}
