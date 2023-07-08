from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator

from ..utils import remove_html_tags


class RecipeMaterial(BaseModel):
    id: int
    rarity: int = Field(alias="rank")
    icon: str
    amount: int = Field(alias="count")

    @validator("icon", pre=True)
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/item/{v}.png"


class Recipe(BaseModel):
    coin_cost: int = Field(alias="coinCost")
    required_world_level: int = Field(alias="worldLevelRequire")
    materials: List[RecipeMaterial] = Field(alias="materialCost")
    special_materials: List[RecipeMaterial] = Field(alias="specialMaterialCost")

    @validator("coin_cost", pre=True)
    def _convert_coin_cost(cls, v: Optional[int]) -> int:
        return v or 0

    @validator("required_world_level", pre=True)
    def _convert_required_world_level(cls, v: Optional[int]) -> int:
        return v or 0

    @validator("materials", pre=True)
    def _convert_materials(
        cls, v: Optional[Dict[str, Dict[str, Any]]]
    ) -> List[RecipeMaterial]:
        return [RecipeMaterial(id=int(id), **m) for id, m in v.items()] if v else []

    @validator("special_materials", pre=True)
    def _convert_special_materials(
        cls, v: Optional[Dict[str, Dict[str, Any]]]
    ) -> List[RecipeMaterial]:
        return [RecipeMaterial(id=int(id), **m) for id, m in v.items()] if v else []


class ItemSource(BaseModel):
    description: str
    recipes: List[Recipe] = Field(alias="recipe")

    @validator("recipes", pre=True)
    def _convert_recipes(cls, v: Optional[List[Dict[str, Any]]]) -> List[Recipe]:
        return [Recipe(**r) for r in v] if v else []


class ItemType(BaseModel):
    id: int
    name: str


class ItemDetail(BaseModel):
    id: int
    name: str
    beta: bool = Field(False)
    rarity: int = Field(alias="rank")
    tags: List[str]
    icon: str
    route: str
    description: str
    story: Optional[str]
    sources: List[ItemSource] = Field(alias="source")

    @validator("icon", pre=True)
    def _convert_icon(cls, v):
        return f"https://api.yatta.top/hsr/assets/UI/item/{v}.png"

    @validator("story", pre=True)
    def _format_story(cls, v: Optional[str]) -> Optional[str]:
        return remove_html_tags(v) if v else None

    @validator("sources", pre=True)
    def _convert_sources(cls, v: List[Dict[str, Any]]) -> List[ItemSource]:
        return [ItemSource(**s) for s in v] if v else []


class Item(BaseModel):
    id: int
    name: str
    beta: bool = Field(False)
    rarity: int = Field(alias="rank")
    type: int
    tags: List[str]
    icon: str
    route: str

    @validator("icon", pre=True)
    def _convert_icon(cls, v):
        return f"https://api.yatta.top/hsr/assets/UI/item/{v}.png"
