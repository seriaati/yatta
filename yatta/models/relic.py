from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from ..utils import replace_placeholders
from .base import BaseModel

__all__ = ("Relic", "RelicSet", "RelicSetDetail", "SetEffect", "SetEffects")


class Relic(BaseModel):
    """Represent a single relic piece.

    Attributes:
        pos: The position/slot of the relic (e.g., "HEAD", "HAND").
        name: The name of the relic piece.
        description: The description of the relic piece.
        story: The lore or story associated with the relic piece.
        icon: The URL to the relic piece's icon.
    """

    pos: str
    name: str
    description: str
    story: str
    icon: str

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/relic/{v}.png"


class SetEffect(BaseModel):
    """Represent a set effect for a relic set.

    Attributes:
        params: Parameters used in the description placeholder replacement.
        description: The formatted description of the set effect.
    """

    params: dict[str, list[int | float]] | None
    description: str

    @field_validator("description", mode="before")
    @classmethod
    def __format_description(cls, v: str, values: Any) -> str:
        params = values.data.get("params")
        return replace_placeholders(v, params)


class SetEffects(BaseModel):
    """Contain the 2-piece and 4-piece set effects.

    Attributes:
        two_piece: The effect activated when 2 pieces of the set are equipped.
        four_piece: The effect activated when 4 pieces of the set are equipped (optional).
    """

    two_piece: SetEffect = Field(alias="2")  # pyright: ignore[reportGeneralTypeIssues]
    four_piece: SetEffect | None = Field(None, alias="4")  # pyright: ignore[reportGeneralTypeIssues]


class RelicSetDetail(BaseModel):
    """Represent detailed information about a relic set.

    Attributes:
        id: The unique identifier for the relic set.
        name: The name of the relic set.
        icon: The URL to the relic set's icon.
        rarity_list: A list of rarities this set is available in.
        is_planar_suit: Whether the set is a Planar Ornament set.
        route: The API route for this relic set.
        beta: Whether the relic set is currently in beta.
        set_effects: The 2-piece and 4-piece effects of the set.
        relics: A list of individual relic pieces belonging to this set.
    """

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
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/relic/{v}.png"

    @field_validator("relics", mode="before")
    @classmethod
    def __convert_relics(cls, v: dict[str, dict[str, Any]]) -> list[Relic]:
        return [Relic(pos=pos, **v[pos]) for pos in v]


class RelicSet(BaseModel):
    """Represent basic information about a relic set.

    Attributes:
        id: The unique identifier for the relic set.
        name: The name of the relic set.
        beta: Whether the relic set is currently in beta.
        icon: The URL to the relic set's icon.
        rarity_list: A list of rarities this set is available in.
        is_planar_suit: Whether the set is a Planar Ornament set.
        route: The API route for this relic set.
    """

    id: int
    name: str
    beta: bool = Field(False)
    icon: str
    rarity_list: list[int] = Field(alias="levelList")
    is_planar_suit: bool = Field(alias="isPlanarSuit")
    route: str

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/relic/{v}.png"
