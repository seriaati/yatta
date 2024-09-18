from typing import Any

from pydantic import Field, field_validator

from ..utils import replace_placeholders
from .base import BaseModel

__all__ = (
    "Relic",
    "RelicSet",
    "RelicSetDetail",
)


class Relic(BaseModel):
    pos: str
    name: str
    description: str
    story: str
    icon: str

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/relic/{v}.png"


class SetEffect(BaseModel):
    params: dict[str, list[int | float]] | None
    description: str

    @field_validator("description", mode="before")
    def _format_description(cls, v: str, values: Any) -> str:
        params = values.data.get("params")
        return replace_placeholders(v, params)


class SetEffects(BaseModel):
    two_piece: SetEffect = Field(alias="2")
    four_piece: SetEffect | None = Field(None, alias="4")


class RelicSetDetail(BaseModel):
    id: int
    name: str
    icon: str
    rarity_list: list[int] = Field(alias="levelList")
    is_planar_suit: bool = Field(alias="isPlanarSuit")
    route: str
    beta: bool = Field(False)

    set_effects: SetEffects = Field(alias="skillList")
    relics: list[Relic] = Field(alias="suite")

    @field_validator("icon", mode="before")
    def convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/relic/{v}.png"

    @field_validator("relics", mode="before")
    def convert_relics(cls, v: dict[str, dict[str, Any]]) -> list[Relic]:
        return [Relic(pos=pos, **v[pos]) for pos in v]


class RelicSet(BaseModel):
    id: int
    name: str
    beta: bool = Field(False)
    icon: str
    rarity_list: list[int] = Field(alias="levelList")
    is_planar_suit: bool = Field(alias="isPlanarSuit")
    route: str

    @field_validator("icon", mode="before")
    def convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/relic/{v}.png"
