from typing import Any

from pydantic import Field, field_validator

from .base import BaseModel

__all__ = (
    "Item",
    "ItemDetail",
    "ItemSource",
    "ItemType",
    "Recipe",
    "RecipeMaterial",
)


class RecipeMaterial(BaseModel):
    id: int
    rarity: int = Field(alias="rank")
    icon: str
    amount: int = Field(alias="count")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/item/{v}.png"


class Recipe(BaseModel):
    coin_cost: int = Field(alias="coinCost")
    required_world_level: int = Field(alias="worldLevelRequire")
    materials: list[RecipeMaterial] = Field(alias="materialCost")
    special_materials: list[RecipeMaterial] = Field(alias="specialMaterialCost")

    @field_validator("coin_cost", mode="before")
    def _convert_coin_cost(cls, v: int | None) -> int:
        return v or 0

    @field_validator("required_world_level", mode="before")
    def _convert_required_world_level(cls, v: int | None) -> int:
        return v or 0

    @field_validator("materials", mode="before")
    def _convert_materials(cls, v: dict[str, dict[str, Any]] | None) -> list[RecipeMaterial]:
        return [RecipeMaterial(id=int(id_), **m) for id_, m in v.items()] if v else []

    @field_validator("special_materials", mode="before")
    def _convert_special_materials(
        cls, v: dict[str, dict[str, Any]] | None
    ) -> list[RecipeMaterial]:
        return [RecipeMaterial(id=int(id_), **m) for id_, m in v.items()] if v else []


class ItemSource(BaseModel):
    description: str
    recipes: list[Recipe] = Field(alias="recipe")

    @field_validator("recipes", mode="before")
    def _convert_recipes(cls, v: list[dict[str, Any]] | None) -> list[Recipe]:
        return [Recipe(**r) for r in v] if v else []


class ItemType(BaseModel):
    id: int
    name: str


class ItemDetail(BaseModel):
    id: int
    name: str
    beta: bool = Field(False)
    rarity: int = Field(alias="rank")
    tags: list[str]
    icon: str
    route: str
    description: str
    story: str | None
    sources: list[ItemSource] = Field(alias="source")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/item/{v}.png"

    @field_validator("sources", mode="before")
    def _convert_sources(cls, v: list[dict[str, Any]]) -> list[ItemSource]:
        return [ItemSource(**s) for s in v] if v else []


class Item(BaseModel):
    id: int
    name: str
    beta: bool = Field(False)
    rarity: int = Field(alias="rank")
    type: int
    tags: list[str]
    icon: str
    route: str

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/item/{v}.png"
