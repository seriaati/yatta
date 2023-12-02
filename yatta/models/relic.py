from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags, replace_placeholders


class Relic(BaseModel):
    pos: str
    name: str
    description: str
    story: str
    icon: str

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/relic/{v}.png"


class SetEffect(BaseModel):
    params: Optional[Dict[str, List[Union[int, float]]]]
    description: str

    @field_validator("description", mode="before")
    def _format_description(cls, v: str, values) -> str:
        params = values.get("params")
        return replace_placeholders(remove_html_tags(v), params)


class SetEffects(BaseModel):
    two_piece: SetEffect = Field(alias="2")
    four_piece: Optional[SetEffect] = Field(None, alias="4")


class RelicSetDetail(BaseModel):
    id: int
    name: str
    icon: str
    rarity_list: List[int] = Field(alias="levelList")
    is_planar_suit: bool = Field(alias="isPlanarSuit")
    route: str
    beta: bool = Field(False)

    set_effects: SetEffects = Field(alias="skillList")
    relics: List[Relic] = Field(alias="suite")

    @field_validator("icon", mode="before")
    def convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/relic/{v}.png"

    @field_validator("relics", mode="before")
    def convert_relics(cls, v: Dict[str, Dict[str, Any]]) -> List[Relic]:
        return [Relic(pos=pos, **v[pos]) for pos in v]


class RelicSet(BaseModel):
    id: int
    name: str
    beta: bool = Field(False)
    icon: str
    rarity_list: List[int] = Field(alias="levelList")
    is_planar_suit: bool = Field(alias="isPlanarSuit")
    route: str

    @field_validator("icon", mode="before")
    def convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/relic/{v}.png"
