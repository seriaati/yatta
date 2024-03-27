from typing import Any, Self

from pydantic import BaseModel as _BaseModel
from pydantic import model_validator

from ..utils import format_str


class BaseModel(_BaseModel):
    @property
    def fields(self) -> dict[str, Any]:
        """Return all fields of the model as a dictionary."""
        schema = self.model_fields
        field_names = schema.keys()
        field_values = {name: getattr(self, name) for name in field_names}
        return field_values

    @model_validator(mode="after")
    def _format_fields(self) -> Self:
        fields_to_format = {"name", "description", "story", "text"}

        for field_name, field_value in self.fields.items():
            if field_name in fields_to_format and isinstance(field_value, str):
                setattr(self, field_name, format_str(field_value))

        return self
