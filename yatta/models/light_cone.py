from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = (
    "LightCone",
    "LightConeDetail",
    "LightConeSkill",
    "LightConeUpgrade",
    "LightConePathType",
    "LightConeAscensionMaterial",
    "LightConeCostItem",
)


class LightConeAscensionMaterial(BaseModel):
    id: int
    rarity: int


class LightConeSkill(BaseModel):
    name: str
    description: str
    params: Dict[str, List[Union[int, float]]]

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class LightConeCostItem(BaseModel):
    id: int
    amount: int


class LightConeUpgrade(BaseModel):
    level: int
    cost_items: List[LightConeCostItem] = Field(alias="costItems")
    max_level: int = Field(alias="maxLevel")
    level_require: int = Field(alias="playerLevelRequire")
    world_level_require: int = Field(alias="worldLevelRequire")
    skill_base: Dict[str, Union[int, float]] = Field(alias="skillBase")
    skill_add: Dict[str, Union[int, float]] = Field(alias="skillAdd")

    @field_validator("level_require", mode="before")
    def _convert_level_require(cls, v: Optional[int]) -> int:
        return v or 0

    @field_validator("world_level_require", mode="before")
    def _convert_world_level_require(cls, v: Optional[int]) -> int:
        return v or 0

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(
        cls, v: Optional[Dict[str, int]]
    ) -> List[LightConeCostItem]:
        return (
            [LightConeCostItem(id=int(id), amount=amount) for id, amount in v.items()]
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
    upgrades: List[LightConeUpgrade] = Field(alias="upgrade")
    skill: LightConeSkill
    ascension_materials: List[LightConeAscensionMaterial] = Field(alias="ascension")

    @field_validator("type", mode="before")
    def _convert_type(cls, v: Dict[str, Dict[str, Any]]) -> LightConePathType:
        return LightConePathType(**v["pathType"])

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/equipment/{v}.png"

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("upgrades", mode="before")
    def _convert_upgrades(cls, v: List[Dict[str, Any]]) -> List[LightConeUpgrade]:
        return [LightConeUpgrade(**upgrade) for upgrade in v]

    @field_validator("ascension_materials", mode="before")
    def _convert_ascension_materials(
        cls, v: Dict[str, int]
    ) -> List[LightConeAscensionMaterial]:
        return [
            LightConeAscensionMaterial(id=int(id), rarity=rarity)
            for id, rarity in v.items()
        ]

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
        return f"https://api.yatta.top/hsr/assets/UI/equipment/{v}.png"

    @field_validator("type", mode="before")
    def _convert_type(cls, v: Dict[str, str]) -> str:
        return v["pathType"]

    @property
    def medium_icon(self) -> str:
        return self.icon.replace("equipment", "equipment/medium")

    @property
    def large_icon(self) -> str:
        return self.icon.replace("equipment", "equipment/large")
