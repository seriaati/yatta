from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from .base import BaseModel

__all__ = ("Item", "ItemDetail", "ItemSource", "ItemType", "Recipe", "RecipeMaterial")


class RecipeMaterial(BaseModel):
    """Represent a material required for a recipe.

    Attributes:
        id: The ID of the material item.
        rarity: The rarity of the material item.
        icon: The URL to the material item's icon.
        amount: The amount of the material required.
    """

    id: int
    rarity: int = Field(alias="rank")
    icon: str
    amount: int = Field(alias="count")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/item/{v}.png"


class Recipe(BaseModel):
    """Represent a recipe to craft or obtain an item.

    Attributes:
        coin_cost: The amount of credits required.
        required_world_level: The Equilibrium Level required to use this recipe.
        materials: A list of standard materials required.
        special_materials: A list of special materials required (e.g., event currency).
    """

    coin_cost: int = Field(alias="coinCost")
    required_world_level: int = Field(alias="worldLevelRequire")
    materials: list[RecipeMaterial] = Field(alias="materialCost")
    special_materials: list[RecipeMaterial] = Field(alias="specialMaterialCost")

    @field_validator("coin_cost", mode="before")
    @classmethod
    def __convert_coin_cost(cls, v: int | None) -> int:
        return v or 0

    @field_validator("required_world_level", mode="before")
    @classmethod
    def __convert_required_world_level(cls, v: int | None) -> int:
        return v or 0

    @field_validator("materials", mode="before")
    @classmethod
    def __convert_materials(cls, v: dict[str, dict[str, Any]] | None) -> list[RecipeMaterial]:
        return [RecipeMaterial(id=int(id_), **m) for id_, m in v.items()] if v else []

    @field_validator("special_materials", mode="before")
    @classmethod
    def __convert_special_materials(
        cls, v: dict[str, dict[str, Any]] | None
    ) -> list[RecipeMaterial]:
        return [RecipeMaterial(id=int(id_), **m) for id_, m in v.items()] if v else []


class ItemSource(BaseModel):
    """Represent a source from which an item can be obtained.

    Attributes:
        description: A description of the source (e.g., "Omni-Synthesizer").
        recipes: A list of recipes associated with this source.
    """

    description: str
    recipes: list[Recipe] = Field(alias="recipe")

    @field_validator("recipes", mode="before")
    @classmethod
    def __convert_recipes(cls, v: list[dict[str, Any]] | None) -> list[Recipe]:
        return [Recipe(**r) for r in v] if v else []


class ItemType(BaseModel):
    """Represent the type of an item.

    Attributes:
        id: The numeric ID of the item type.
        name: The display name of the item type.
    """

    id: int
    name: str


class ItemDetail(BaseModel):
    """Represent detailed information about an item.

    Attributes:
        id: The unique identifier for the item.
        name: The name of the item.
        beta: Whether the item is currently in beta.
        rarity: The rarity (star rating) of the item.
        tags: A list of tags associated with the item.
        icon: The URL to the item's icon.
        route: The API route for this item.
        description: The functional description of the item.
        story: The lore or background story of the item (optional).
        sources: A list of sources where this item can be obtained.
    """

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

    @field_validator("tags", mode="before")
    @classmethod
    def _coerce_tags(cls, v):
        if v is None:
            return []
        return [str(tag) for tag in v]

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/item/{v}.png"

    @field_validator("sources", mode="before")
    @classmethod
    def __convert_sources(cls, v: list[dict[str, Any]]) -> list[ItemSource]:
        return [ItemSource(**s) for s in v] if v else []


class Item(BaseModel):
    """Represent basic information about an item.

    Attributes:
        id: The unique identifier for the item.
        name: The name of the item.
        beta: Whether the item is currently in beta.
        rarity: The rarity (star rating) of the item.
        type: The numeric ID representing the item type.
        tags: A list of tags associated with the item.
        icon: The URL to the item's icon.
        route: The API route for this item.
    """

    id: int
    name: str
    beta: bool = Field(False)
    rarity: int = Field(alias="rank")
    type: int
    tags: list[str]
    icon: str
    route: str

    @field_validator("tags", mode="before")
    @classmethod
    def _coerce_tags(cls, v):
        if v is None:
            return []
        return [str(tag) for tag in v]

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/item/{v}.png"
