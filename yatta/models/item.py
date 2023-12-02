from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags


class RecipeMaterial(BaseModel):
    id: int
    rarity: int = Field(alias="rank")
    icon: str
    amount: int = Field(alias="count")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/item/{v}.png"


class Recipe(BaseModel):
    coin_cost: int = Field(alias="coinCost")
    required_world_level: int = Field(alias="worldLevelRequire")
    materials: List[RecipeMaterial] = Field(alias="materialCost")
    special_materials: List[RecipeMaterial] = Field(alias="specialMaterialCost")

    @field_validator("coin_cost", mode="before")
    def _convert_coin_cost(cls, v: Optional[int]) -> int:
        return v or 0

    @field_validator("required_world_level", mode="before")
    def _convert_required_world_level(cls, v: Optional[int]) -> int:
        return v or 0

    @field_validator("materials", mode="before")
    def _convert_materials(
        cls, v: Optional[Dict[str, Dict[str, Any]]]
    ) -> List[RecipeMaterial]:
        return [RecipeMaterial(id=int(id), **m) for id, m in v.items()] if v else []

    @field_validator("special_materials", mode="before")
    def _convert_special_materials(
        cls, v: Optional[Dict[str, Dict[str, Any]]]
    ) -> List[RecipeMaterial]:
        return [RecipeMaterial(id=int(id), **m) for id, m in v.items()] if v else []


class ItemSource(BaseModel):
    description: str
    recipes: List[Recipe] = Field(alias="recipe")

    @field_validator("recipes", mode="before")
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

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v):
        return f"https://api.yatta.top/hsr/assets/UI/item/{v}.png"

    @field_validator("story", mode="before")
    def _format_story(cls, v: Optional[str]) -> Optional[str]:
        return remove_html_tags(v) if v else None

    @field_validator("sources", mode="before")
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

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v):
        return f"https://api.yatta.top/hsr/assets/UI/item/{v}.png"
