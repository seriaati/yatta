from __future__ import annotations

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
    """Represent a material required for light cone ascension.

    Attributes:
        id: The ID of the ascension material item.
        rarity: The rarity of the ascension material item.
    """

    id: int
    rarity: int


class LightConeSkill(BaseModel):
    """Represent the skill of a light cone.

    Attributes:
        name: The name of the light cone skill.
        description: The description of the light cone skill.
        params: Parameters associated with the skill's effects, often scaling with superimposition.
    """

    name: str
    description: str
    params: dict[str, list[int | float]]


class LightConeCostItem(BaseModel):
    """Represent an item and its amount required for upgrading a light cone.

    Attributes:
        id: The ID of the required item.
        amount: The amount of the item required.
    """

    id: int
    amount: int


class LightConeUpgrade(BaseModel):
    """Represent the details for a specific ascension level of a light cone.

    Attributes:
        level: The ascension level (0-indexed).
        cost_items: A list of items required for this ascension.
        max_level: The maximum character level achievable after this ascension.
        required_player_level: The Trailblaze Level required for this ascension.
        required_world_level: The Equilibrium Level required for this ascension.
        skill_base: Base stats provided by the light cone at this ascension.
        skill_add: Additional stats gained per level within this ascension rank.
    """

    level: int
    cost_items: list[LightConeCostItem] = Field(alias="costItems")
    max_level: int = Field(alias="maxLevel")
    required_player_level: int = Field(alias="playerLevelRequire")
    required_world_level: int = Field(alias="worldLevelRequire")
    skill_base: dict[str, int | float] = Field(alias="skillBase")
    skill_add: dict[str, int | float] = Field(alias="skillAdd")

    @field_validator("required_player_level", mode="before")
    @classmethod
    def __convert_required_player_level(cls, v: int | None) -> int:
        return v or 0

    @field_validator("required_world_level", mode="before")
    @classmethod
    def __convert_world_level_require(cls, v: int | None) -> int:
        return v or 0

    @field_validator("cost_items", mode="before")
    @classmethod
    def __convert_cost_items(cls, v: dict[str, int] | None) -> list[LightConeCostItem]:
        return (
            [LightConeCostItem(id=int(id_), amount=amount) for id_, amount in v.items()]
            if v
            else []
        )


class LightConePathType(BaseModel):
    """Represent the path type of a light cone.

    Attributes:
        id: The identifier string for the path type (e.g., "Warrior").
        name: The display name of the path type (e.g., "Destruction").
    """

    id: str
    name: str


class LightConeDetail(BaseModel):
    """Represent detailed information about a light cone.

    Attributes:
        id: The unique identifier for the light cone.
        name: The name of the light cone.
        beta: Whether the light cone is currently in beta.
        rarity: The rarity (star rating) of the light cone.
        type: The path type of the light cone.
        icon: The URL to the light cone's standard icon.
        is_sellable: Whether the light cone can be sold.
        route: The API route for this light cone.
        description: The lore or background description of the light cone.
        upgrades: A list of ascension details for each rank.
        skill: The skill details of the light cone.
        ascension_materials: A list of materials required for ascension across all ranks.
    """

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
    @classmethod
    def __convert_type(cls, v: dict[str, dict[str, Any]]) -> LightConePathType:
        return LightConePathType(**v["pathType"])

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/equipment/{v}.png"

    @field_validator("upgrades", mode="before")
    @classmethod
    def __convert_upgrades(cls, v: list[dict[str, Any]]) -> list[LightConeUpgrade]:
        return [LightConeUpgrade(**upgrade) for upgrade in v]

    @field_validator("ascension_materials", mode="before")
    @classmethod
    def __convert_ascension_materials(cls, v: dict[str, int]) -> list[LightConeAscensionMaterial]:
        return [LightConeAscensionMaterial(id=int(id_), rarity=rarity) for id_, rarity in v.items()]

    @property
    def medium_icon(self) -> str:
        """Return the URL to the medium-sized icon."""
        return self.icon.replace("equipment", "equipment/medium")

    @property
    def large_icon(self) -> str:
        """Return the URL to the large-sized icon."""
        return self.icon.replace("equipment", "equipment/large")


class LightCone(BaseModel):
    """Represent basic information about a light cone.

    Attributes:
        id: The unique identifier for the light cone.
        name: The name of the light cone.
        beta: Whether the light cone is currently in beta.
        rarity: The rarity (star rating) of the light cone.
        icon: The URL to the light cone's standard icon.
        type: The identifier string for the path type (e.g., "Warrior").
        is_sellable: Whether the light cone can be sold.
        route: The API route for this light cone.
    """

    id: int
    name: str
    beta: bool = Field(False)
    rarity: int = Field(alias="rank")
    icon: str
    type: str = Field(alias="types")
    is_sellable: bool = Field(alias="isSellable")
    route: str

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/equipment/{v}.png"

    @field_validator("type", mode="before")
    @classmethod
    def __convert_type(cls, v: dict[str, str]) -> str:
        return v["pathType"]

    @property
    def medium_icon(self) -> str:
        """Return the URL to the medium-sized icon."""
        return self.icon.replace("equipment", "equipment/medium")

    @property
    def large_icon(self) -> str:
        """Return the URL to the large-sized icon."""
        return self.icon.replace("equipment", "equipment/large")
