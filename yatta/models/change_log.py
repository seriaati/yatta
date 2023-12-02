from typing import Dict, List

from pydantic import BaseModel, Field, field_validator

__all__ = ("ChangeLog", "ChangeLogItem")


class ChangeLogItem(BaseModel):
    category: str
    ids: List[int]

    @field_validator("ids", mode="before")
    def _intify_ids(cls, v: List[str]) -> List[int]:
        return [int(i) for i in v]


class ChangeLog(BaseModel):
    id: int
    version: str
    items: List[ChangeLogItem]
    beta: bool = Field(False)

    @field_validator("items", mode="before")
    def _convert_items(cls, v: Dict[str, List[int]]) -> List[ChangeLogItem]:
        return [ChangeLogItem(category=k, ids=v) for k, v in v.items()]
