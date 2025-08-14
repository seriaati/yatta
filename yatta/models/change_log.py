from __future__ import annotations

from pydantic import Field, field_validator

from .base import BaseModel

__all__ = ("Changelog", "ChangelogCategory")


class ChangelogCategory(BaseModel):
    """Represent a category of changes within a changelog entry.

    Attributes:
        category: The name of the category (e.g., "avatar", "equipment").
        item_ids: A list of item IDs that were changed within this category.
    """

    category: str
    item_ids: list[int]

    @field_validator("item_ids", mode="before")
    @classmethod
    def __intify_ids(cls, v: list[str]) -> list[int]:
        return [int(i) for i in v]


class Changelog(BaseModel):
    """Represent a changelog entry for a specific version.

    Attributes:
        id: The unique identifier for the changelog entry.
        version: The version string associated with these changes.
        categories: A list of categories detailing the changes.
        beta: Whether this changelog pertains to a beta version.
    """

    id: int
    version: str
    categories: list[ChangelogCategory] = Field(alias="items")
    beta: bool = Field(False)

    @field_validator("version", mode="before")
    @classmethod
    def _coerce_version(cls, v):
        return str(v) if v is not None else ""

    @field_validator("categories", mode="before")
    @classmethod
    def __convert_categories(cls, v: dict[str, list[int]]) -> list[ChangelogCategory]:
        return [ChangelogCategory(category=k, item_ids=v) for k, v in v.items()]
