from typing import Any

from pydantic import Field, field_validator

from .base import BaseModel

__all__ = (
    "LightCone",
    "LightConeAscensionMaterial",
    "LightConeCostItem",
    "LightConeDetail",
    "LightConePathType",
    "LightConeSkill",
    "LightConeUpgrade",
)


class LightConeAscensionMaterial(BaseModel):
    id: int
    rarity: int


class LightConeSkill(BaseModel):
    name: str
    description: str
    params: dict[str, list[int | float]]


class LightConeCostItem(BaseModel):
    id: int
    amount: int


class LightConeUpgrade(BaseModel):
    level: int
    cost_items: list[LightConeCostItem] = Field(alias="costItems")
    max_level: int = Field(alias="maxLevel")
    required_player_level: int = Field(alias="playerLevelRequire")
    required_world_level: int = Field(alias="worldLevelRequire")
    skill_base: dict[str, int | float] = Field(alias="skillBase")
    skill_add: dict[str, int | float] = Field(alias="skillAdd")

    @field_validator("required_player_level", mode="before")
    def _convert_required_player_level(cls, v: int | None) -> int:
        return v or 0

    @field_validator("required_world_level", mode="before")
    def _convert_world_level_require(cls, v: int | None) -> int:
        return v or 0

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(cls, v: dict[str, int] | None) -> list[LightConeCostItem]:
        return (
            [LightConeCostItem(id=int(id_), amount=amount) for id_, amount in v.items()]
            if v
            else []
        )


class LightConePathType(BaseModel):
    id: str
    name: str


class LightConeDetail(BaseModel):
    id: int
    name: str
    beta: bool = Field(False)
    rarity: int = Field(alias="rank")
    type: LightConePathType = Field(alias="types")
    icon: str
    is_sellable: bool = Field(alias="isSellable")
    route: str
    description: str
    upgrades: list[LightConeUpgrade] = Field(alias="upgrade")
    skill: LightConeSkill
    ascension_materials: list[LightConeAscensionMaterial] = Field(alias="ascension")

    @field_validator("type", mode="before")
    def _convert_type(cls, v: dict[str, dict[str, Any]]) -> LightConePathType:
        return LightConePathType(**v["pathType"])

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/equipment/{v}.png"

    @field_validator("upgrades", mode="before")
    def _convert_upgrades(cls, v: list[dict[str, Any]]) -> list[LightConeUpgrade]:
        return [LightConeUpgrade(**upgrade) for upgrade in v]

    @field_validator("ascension_materials", mode="before")
    def _convert_ascension_materials(cls, v: dict[str, int]) -> list[LightConeAscensionMaterial]:
        return [LightConeAscensionMaterial(id=int(id_), rarity=rarity) for id_, rarity in v.items()]

    @property
    def medium_icon(self) -> str:
        return self.icon.replace("equipment", "equipment/medium")

    @property
    def large_icon(self) -> str:
        return self.icon.replace("equipment", "equipment/large")


class LightCone(BaseModel):
    id: int
    name: str
    beta: bool = Field(False)
    rarity: int = Field(alias="rank")
    icon: str
    type: str = Field(alias="types")
    is_sellable: bool = Field(alias="isSellable")
    route: str

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/equipment/{v}.png"

    @field_validator("type", mode="before")
    def _convert_type(cls, v: dict[str, str]) -> str:
        return v["pathType"]

    @property
    def medium_icon(self) -> str:
        return self.icon.replace("equipment", "equipment/medium")

    @property
    def large_icon(self) -> str:
        return self.icon.replace("equipment", "equipment/large")
