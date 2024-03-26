from pydantic import Field, field_validator

from .base import BaseModel

__all__ = ("Changelog", "ChangelogCategory")


class ChangelogCategory(BaseModel):
    category: str
    item_ids: list[int]

    @field_validator("item_ids", mode="before")
    def _intify_ids(cls, v: list[str]) -> list[int]:
        return [int(i) for i in v]


class Changelog(BaseModel):
    id: int
    version: str
    categories: list[ChangelogCategory] = Field(alias="items")
    beta: bool = Field(False)

    @field_validator("categories", mode="before")
    def _convert_categories(cls, v: dict[str, list[int]]) -> list[ChangelogCategory]:
        return [ChangelogCategory(category=k, item_ids=v) for k, v in v.items()]
