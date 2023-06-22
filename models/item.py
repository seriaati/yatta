from typing import List

from pydantic import BaseModel, Field, validator


class Item(BaseModel):
    id: int
    name: str
    rarity: int = Field(alias="rank")
    type: int
    tags: List[str]
    icon: str
    route: str

    @validator("icon", pre=True)
    def validate_icon(cls, v):
        return f"https://api.yatta.top/hsr/assets/UI/item/{v}.png"
