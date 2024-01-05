from typing import Dict, List

from pydantic import BaseModel, Field, field_validator

__all__ = ("Changelog", "ChangelogCategory")


class ChangelogCategory(BaseModel):
    category: str
    item_ids: List[int]

    @field_validator("item_ids", mode="before")
    def _intify_ids(cls, v: List[str]) -> List[int]:
        return [int(i) for i in v]


class Changelog(BaseModel):
    id: int
    version: str
    categories: List[ChangelogCategory] = Field(alias="items")
    beta: bool = Field(False)

    @field_validator("items", mode="before")
    def _convert_categories(cls, v: Dict[str, List[int]]) -> List[ChangelogCategory]:
        return [ChangelogCategory(category=k, item_ids=v) for k, v in v.items()]
