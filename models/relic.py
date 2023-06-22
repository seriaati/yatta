from typing import List

from pydantic import BaseModel, Field, validator


class Relic(BaseModel):
    id: int
    name: str
    icon: str
    level_list: List[int] = Field(alias="levelList")
    is_planar_suit: bool = Field(alias="isPlanarSuit")
    route: str

    @validator("icon", pre=True)
    def validate_icon(cls, v):
        return f"https://api.yatta.top/hsr/assets/UI/relic/{v}.png"
