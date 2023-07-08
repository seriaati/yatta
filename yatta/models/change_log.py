from typing import Dict, List

from pydantic import BaseModel, Field, validator


class Item(BaseModel):
    category: str
    ids: List[int]

    @validator("ids", pre=True)
    def _intify_ids(cls, v: List[str]) -> List[int]:
        return [int(i) for i in v]


class ChangeLog(BaseModel):
    id: int
    version: str
    items: List[Item]
    beta: bool = Field(False)

    @validator("items", pre=True)
    def _convert_items(cls, v: Dict[str, List[str]]) -> List[Item]:
        return [Item(category=k, ids=v) for k, v in v.items()]  # type: ignore
