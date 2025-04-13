from __future__ import annotations

from typing import Any, Self

from pydantic import BaseModel as _BaseModel
from pydantic import model_validator

from ..utils import format_str


class BaseModel(_BaseModel):
    """Base model for all data models, providing common functionality."""

    @property
    def fields(self) -> dict[str, Any]:
        """Return all fields of the model as a dictionary."""
        schema = BaseModel.model_fields
        field_names = schema.keys()
        return {name: getattr(self, name) for name in field_names}

    @model_validator(mode="after")
    def __format_fields(self) -> Self:
        fields_to_format = {"name", "description", "story", "text"}

        for field_name, field_value in self.model_dump().items():
            if field_name in fields_to_format and isinstance(field_value, str):
                setattr(self, field_name, format_str(field_value))

        return self
