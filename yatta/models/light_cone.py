from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator

from ..utils import remove_html_tags


class AcensionMaterial(BaseModel):
    id: int
    rarity: int


class LightConeSkill(BaseModel):
    name: str
    description: str
    params: Dict[str, List[Union[int, float]]]

    @validator("description", pre=True)
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class CostItem(BaseModel):
    id: int
    amount: int


class LightConeUpgrade(BaseModel):
    level: int
    cost_items: List[CostItem] = Field(alias="costItems")
    max_level: int = Field(alias="maxLevel")
    level_require: int = Field(alias="playerLevelRequire")
    world_level_require: int = Field(alias="worldLevelRequire")
    skill_base: Dict[str, Union[int, float]] = Field(alias="skillBase")
    skill_add: Dict[str, Union[int, float]] = Field(alias="skillAdd")

    @validator("level_require", pre=True)
    def _convert_level_require(cls, v: Optional[int]) -> int:
        return v or 0

    @validator("world_level_require", pre=True)
    def _convert_world_level_require(cls, v: Optional[int]) -> int:
        return v or 0

    @validator("cost_items", pre=True)
    def _convert_cost_items(cls, v: Optional[Dict[str, int]]) -> List[CostItem]:
        return (
            [CostItem(id=int(id), amount=amount) for id, amount in v.items()]
            if v
            else []
        )


class PathType(BaseModel):
    id: str
    name: str


class LightConeDetail(BaseModel):
    id: int
    name: str
    beta: bool = Field(False)
    rarity: int = Field(alias="rank")
    type: PathType = Field(alias="types")
    icon: str
    is_sellable: bool = Field(alias="isSellable")
    route: str
    description: str
    upgrades: List[LightConeUpgrade] = Field(alias="upgrade")
    skill: LightConeSkill
    ascension_materials: List[AcensionMaterial] = Field(alias="ascension")

    @validator("type", pre=True)
    def _convert_type(cls, v: Dict[str, Dict[str, Any]]) -> PathType:
        return PathType(**v["pathType"])

    @validator("icon", pre=True)
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/equipment/{v}.png"

    @validator("description", pre=True)
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @validator("upgrades", pre=True)
    def _convert_upgrades(cls, v: List[Dict[str, Any]]) -> List[LightConeUpgrade]:
        return [LightConeUpgrade(**upgrade) for upgrade in v]

    @validator("ascension_materials", pre=True)
    def _convert_ascension_materials(cls, v: Dict[str, int]) -> List[AcensionMaterial]:
        return [AcensionMaterial(id=int(id), rarity=rarity) for id, rarity in v.items()]


class LightCone(BaseModel):
    id: int
    name: str
    beta: bool = Field(False)
    rarity: int = Field(alias="rank")
    icon: str
    type: str = Field(alias="types")
    is_sellable: bool = Field(alias="isSellable")
    route: str

    @validator("icon", pre=True)
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/equipment/{v}.png"

    @validator("type", pre=True)
    def _convert_type(cls, v: Dict[str, str]) -> str:
        return v["pathType"]
