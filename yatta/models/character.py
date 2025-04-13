from __future__ import annotations

import datetime
from typing import Any

from pydantic import Field, field_validator

from ..enums import CombatType, PathType
from ..utils import format_str, replace_placeholders
from .base import BaseModel

__all__ = (
    "BaseSkill",
    "Character",
    "CharacterAscensionItem",
    "CharacterCostItem",
    "CharacterDetail",
    "CharacterDetailType",
    "CharacterDetailTypes",
    "CharacterEidolon",
    "CharacterInfo",
    "CharacterScript",
    "CharacterStory",
    "CharacterTraces",
    "CharacterType",
    "CharacterUpgrade",
    "CharacterVoice",
    "ExtraEffect",
    "SkillAdd",
    "SkillListSkill",
    "SkillPoint",
    "SkillPromote",
    "SkillPromoteCostItem",
    "SkillTree",
    "SkillTreeSkill",
    "Status",
    "VoiceActor",
    "WeaknessBreak",
)


class CharacterStory(BaseModel):
    """Represent a piece of character story/lore.

    Attributes:
        title: The title of the story section.
        text: The content of the story section.
    """

    title: str
    text: str


class CharacterVoice(BaseModel):
    """Represent a character voice line.

    Attributes:
        title: The title or trigger condition of the voice line.
        text: The transcribed text of the voice line.
        audio: The ID or reference to the audio file (optional).
    """

    title: str
    text: str
    audio: int | None


class CharacterScript(BaseModel):
    """Contain character stories and voice lines.

    Attributes:
        stories: A list of character story sections.
        voices: A list of character voice lines.
    """

    stories: list[CharacterStory] = Field(alias="story")
    voices: list[CharacterVoice] = Field(alias="voice")

    @field_validator("stories", mode="before")
    @classmethod
    def __convert_stories(cls, v: list[dict[str, Any]] | None) -> list[CharacterStory]:
        return [CharacterStory(**s) for s in v] if v else []

    @field_validator("voices", mode="before")
    @classmethod
    def __convert_voices(cls, v: list[dict[str, Any]] | None) -> list[CharacterVoice]:
        return [CharacterVoice(**s) for s in v] if v else []


class CharacterAscensionItem(BaseModel):
    """Represent an item and amount required for character ascension.

    Attributes:
        id: The ID of the required item.
        amount: The amount of the item required.
    """

    id: int
    amount: int


class SkillAdd(BaseModel):
    """Represent a skill level increase granted by an Eidolon.

    Attributes:
        id: ID of the skill whose level is increased.
        level: The number of levels added to the skill.
    """

    id: int
    """ID of the skill"""
    level: int
    """Level added to the skill"""


class CharacterEidolon(BaseModel):
    """Represent a character Eidolon.

    Attributes:
        id: The unique identifier for the Eidolon.
        rank: The rank of the Eidolon (1-6).
        name: The name of the Eidolon.
        params: Parameters used for placeholder replacement in the description.
        description: The formatted description of the Eidolon's effect.
        skill_add_level_list: List of skills whose levels are increased by this Eidolon.
        icon: The URL to the Eidolon's icon.
    """

    id: int
    rank: int
    name: str

    params: list[int | float] | None
    description: str
    skill_add_level_list: list[SkillAdd] = Field(alias="skillAddLevelList")
    """List of skills that increase their level because of this eidolon"""
    icon: str

    @field_validator("description", mode="before")
    @classmethod
    def __format_description(cls, v: str, values: Any) -> str:
        params = values.data.get("params")
        return replace_placeholders(format_str(v), params)

    @field_validator("skill_add_level_list", mode="before")
    @classmethod
    def __convert_skill_add_level_list(cls, v: dict[str, int] | None) -> list[SkillAdd]:
        return [SkillAdd(id=int(id_), level=level) for id_, level in v.items()] if v else []

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/skill/{v}.png"


class SkillPromoteCostItem(BaseModel):
    """Represent an item and amount required for promoting (leveling up) a skill/trace.

    Attributes:
        id: The ID of the required item.
        amount: The amount of the item required.
    """

    id: int
    amount: int


class SkillPromote(BaseModel):
    """Represent the cost to promote (level up) a skill/trace to a specific level.

    Attributes:
        level: The target level for the promotion.
        cost_items: A list of items required for this promotion.
    """

    level: int
    cost_items: list[SkillPromoteCostItem] = Field(alias="costItems")

    @field_validator("cost_items", mode="before")
    @classmethod
    def __convert_cost_items(
        cls, v: dict[str, dict[str, int] | None]
    ) -> list[SkillPromoteCostItem]:
        return (
            [SkillPromoteCostItem(id=int(id_), amount=a) for id_, a in v["costItems"].items()]
            if v["costItems"]
            else []
        )


class Status(BaseModel):
    """Represent a status effect or stat bonus granted by a trace node.

    Attributes:
        name: The name of the status or stat (e.g., "HPAddedRatio").
        value: The value of the status or stat bonus.
        icon: The URL to the icon representing the status or stat.
    """

    name: str
    value: int | float
    icon: str

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/status/{v}.png"


class ExtraEffect(BaseModel):
    """Represent an extra effect associated with a skill.

    Attributes:
        name: The name of the extra effect.
        description: The description of the extra effect.
        icon: The URL to the icon for the extra effect.
    """

    name: str
    description: str
    icon: str


class WeaknessBreak(BaseModel):
    """Represent the toughness damage dealt by a skill.

    Attributes:
        type: The type of weakness break (e.g., "Skill").
        value: The amount of toughness damage dealt.
    """

    type: str
    value: int


class SkillPoint(BaseModel):
    """Represent skill point generation or consumption by a skill.

    Attributes:
        type: The type of skill point interaction (e.g., "SkillPoint", "EnergyGenerate").
        value: The amount of skill points generated (positive) or consumed (negative), or energy generated.
    """

    type: str
    value: int | None


class SkillListSkill(BaseModel):
    """Represent detailed information about a specific character skill (Basic ATK, Skill, Ultimate, Talent).

    Attributes:
        id: The unique identifier for the skill.
        name: The name of the skill.
        tag: A tag associated with the skill (e.g., "Single Target").
        type: The type of the skill (e.g., "Basic ATK", "Skill", "Ultimate", "Talent").
        max_level: The maximum level this skill can reach.
        skill_points: Information about skill point generation/consumption.
        weakness_break: Information about toughness damage dealt.
        description: The detailed description of the skill (may contain placeholders).
        simplified_description: A simplified description of the skill.
        traces: List of trace IDs related to this skill.
        eidolons: List of Eidolon IDs related to this skill.
        extra_effects: List of extra effects associated with this skill.
        attack_type: The attack type (e.g., "Normal", "AoE").
        damage_type: The damage type (e.g., "Physical", "Fire").
        icon: The URL to the skill's icon.
        params: Parameters used for scaling and placeholder replacement in descriptions.
    """

    id: int
    name: str
    tag: str | None
    type: str

    max_level: int = Field(alias="maxLevel")
    skill_points: list[SkillPoint] = Field(alias="skillPoints")
    weakness_break: list[WeaknessBreak] = Field(alias="weaknessBreak")
    description: str | None
    simplified_description: str | None = Field(alias="descriptionSimple")

    traces: list[int]
    eidolons: list[int]
    extra_effects: list[ExtraEffect] = Field(alias="extraEffects")
    attack_type: str | None = Field(alias="attackType")
    damage_type: str | None = Field(alias="damageType")
    icon: str

    params: dict[str, list[float]] | None

    @field_validator("type", mode="before")
    @classmethod
    def __convert_type(cls, v: Any) -> str:
        return str(v)

    @field_validator("skill_points", mode="before")
    @classmethod
    def __convert_skill_points(cls, v: dict[str, int | None]) -> list[SkillPoint]:
        return [SkillPoint(type=k, value=v) for k, v in v.items()]

    @field_validator("weakness_break", mode="before")
    @classmethod
    def __convert_weakness_break(cls, v: dict[str, int] | None) -> list[WeaknessBreak]:
        return [WeaknessBreak(type=k, value=v) for k, v in v.items()] if v else []

    @field_validator("simplified_description", mode="before")
    @classmethod
    def __format_simplified_description(cls, v: str | None) -> str | None:
        return format_str(v) if v else None

    @field_validator("traces", mode="before")
    @classmethod
    def __convert_traces(cls, v: list[int] | None) -> list[int]:
        return v or []

    @field_validator("eidolons", mode="before")
    @classmethod
    def __convert_eidolons(cls, v: list[int] | None) -> list[int]:
        return v or []

    @field_validator("extra_effects", mode="before")
    @classmethod
    def __convert_extra_effects(cls, v: list[dict[str, Any]] | None) -> list[ExtraEffect]:
        return [ExtraEffect(**e) for e in v] if v else []

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/skill/{v}.png"


class BaseSkill(BaseModel):
    """Represent a base skill or a trace node in the character's skill tree.

    Attributes:
        id: The unique identifier for the skill or trace node.
        name: The name of the skill or trace node (optional for some traces).
        description: The description of the skill or trace node (optional for some traces).
        point_type: The type of point in the skill tree.
        point_position: The position identifier within the skill tree.
        max_level: The maximum level this skill or trace can reach.
        is_default: Whether this skill/trace is unlocked by default.
        avatar_level_limit: The character level required to unlock this trace (optional).
        avatar_promotion_limit: The character ascension rank required to unlock this trace (optional).
        skill_list: Detailed information if this node represents a main skill (Basic ATK, Skill, etc.).
        status_list: List of status effects or stat bonuses granted by this trace node.
        icon: The URL to the icon for this skill or trace node.
        params: Parameters used for scaling (optional).
        promote: List of promotion costs for leveling up this skill or trace.
    """

    id: int
    name: str | None
    description: str | None

    point_type: str = Field(alias="pointType")
    point_position: str = Field(alias="pointPosition")
    max_level: int = Field(alias="maxLevel")
    is_default: bool = Field(alias="isDefault")

    avatar_level_limit: int | None = Field(alias="avatarLevelLimit")
    avatar_promotion_limit: int | None = Field(alias="avatarPromotionLimit")

    skill_list: list[SkillListSkill] = Field(alias="skillList")
    status_list: list[Status] = Field(alias="statusList")
    icon: str
    params: dict[str, list[float]] | None

    promote: list[SkillPromote]

    @field_validator("skill_list", mode="before")
    @classmethod
    def __convert_skill_list(cls, v: dict[str, dict[str, Any]] | None) -> list[SkillListSkill]:
        return [SkillListSkill(id=int(s), **v[s]) for s in v] if v else []

    @field_validator("status_list", mode="before")
    @classmethod
    def __convert_status_list(cls, v: list[dict[str, Any]] | None) -> list[Status]:
        return [Status(**s) for s in v] if v else []

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        if "SkillIcon" in v:
            return f"https://sr.yatta.moe/hsr/assets/UI/skill/{v}.png"
        return f"https://sr.yatta.moe/hsr/assets/UI/status/{v}.png"

    @field_validator("promote", mode="before")
    @classmethod
    def __convert_promote(
        cls, v: dict[str, dict[str, dict[str, int] | None]]
    ) -> list[SkillPromote]:
        return [SkillPromote(level=int(p), costItems=v[p]) for p in v] if v else []  # type: ignore


class SkillTreeSkill(BaseModel):
    """Represent a connection or node within a skill tree structure.

    Attributes:
        id: The ID of the skill/trace node this connection points to or represents.
        points_direction: The direction of the connection (optional).
        points: A list of connected skill/trace node IDs.
    """

    id: int
    points_direction: str | None = Field(alias="pointsDirection")
    points: list[int]

    @field_validator("points", mode="before")
    @classmethod
    def __convert_points(cls, v: list[int] | None) -> list[int]:
        return v or []


class SkillTree(BaseModel):
    """Represent a skill tree structure for a character.

    Attributes:
        id: The identifier for this skill tree.
        type: The type of skill tree.
        tree: A list of skills/connections within the tree.
    """

    id: int
    type: str
    tree: list[SkillTreeSkill] = Field([])

    @field_validator("tree", mode="before")
    @classmethod
    def __convert_tree(cls, v: dict[str, dict[str, Any]]) -> list[SkillTreeSkill]:
        return [SkillTreeSkill(**v[s]) for s in v]


class CharacterTraces(BaseModel):
    """Contain all character traces (skills and passive abilities).

    Attributes:
        main_skills: List of main skills (Basic ATK, Skill, Ultimate, Talent).
        sub_skills: List of passive trace nodes (stat bonuses, extra abilities).
        tree_skills: List representing the structure and connections of the skill trees.
    """

    main_skills: list[BaseSkill] = Field(alias="mainSkills")
    sub_skills: list[BaseSkill] = Field(alias="subSkills")
    tree_skills: list[SkillTree] = Field(alias="skillsTree")

    @field_validator("main_skills", mode="before")
    @classmethod
    def __convert_main_skills(cls, v: dict[str, dict[str, Any]]) -> list[BaseSkill]:
        return [BaseSkill(**v[s]) for s in v]

    @field_validator("sub_skills", mode="before")
    @classmethod
    def __convert_sub_skills(cls, v: dict[str, dict[str, Any]]) -> list[BaseSkill]:
        return [BaseSkill(**v[s]) for s in v]

    @field_validator("tree_skills", mode="before")
    @classmethod
    def __convert_tree_skills(cls, v: dict[str, dict[str, Any]]) -> list[SkillTree]:
        return [SkillTree(**v[s]) for s in v]


class CharacterCostItem(BaseModel):
    """Represent an item and amount required for character level upgrades.

    Attributes:
        id: The ID of the required item.
        amount: The amount of the item required.
    """

    id: int
    amount: int


class CharacterUpgrade(BaseModel):
    """Represent the details for a specific character ascension rank.

    Attributes:
        level: The ascension rank (0-indexed).
        cost_items: A list of items required for this ascension.
        max_level: The maximum character level achievable after this ascension.
        required_player_level: The Trailblaze Level required for this ascension.
        required_world_level: The Equilibrium Level required for this ascension.
        skill_base: Base stats of the character at this ascension rank (level 1 of the rank).
        skill_add: Additional stats gained per level within this ascension rank.
    """

    level: int
    cost_items: list[CharacterCostItem] = Field(alias="costItems")
    max_level: int = Field(alias="maxLevel")
    required_player_level: int = Field(alias="playerLevelRequire")
    required_world_level: int = Field(alias="worldLevelRequire")
    skill_base: dict[str, int | float] = Field(alias="skillBase")
    skill_add: dict[str, int | float] = Field(alias="skillAdd")

    @field_validator("cost_items", mode="before")
    @classmethod
    def __convert_cost_items(cls, v: dict[str, int] | None) -> list[CharacterCostItem]:
        return [CharacterCostItem(id=int(k), amount=v) for k, v in v.items()] if v else []

    @field_validator("required_player_level", mode="before")
    @classmethod
    def __convert_required_player_level(cls, v: int | None) -> int:
        return v or 0

    @field_validator("required_world_level", mode="before")
    @classmethod
    def __convert_required_world_level(cls, v: int | None) -> int:
        return v or 0


class VoiceActor(BaseModel):
    """Represent a voice actor for a specific language.

    Attributes:
        lang: The language code (e.g., "en", "jp").
        name: The name of the voice actor.
    """

    lang: str
    name: str


class CharacterInfo(BaseModel):
    """Represent additional information about a character (fetter info).

    Attributes:
        faction: The faction or affiliation of the character (optional).
        description: A general description or profile of the character.
        voice_actors: A list of voice actors for different languages.
    """

    faction: str | None
    description: str
    voice_actors: list[VoiceActor] = Field(alias="cv")

    @field_validator("voice_actors", mode="before")
    @classmethod
    def __convert_voice_actors(cls, v: dict[str, str] | None) -> list[VoiceActor]:
        return [VoiceActor(lang=k, name=v) for k, v in v.items()] if v else []


class CharacterDetailType(BaseModel):
    """Represent either the Path or Combat Type with its ID and name.

    Attributes:
        id: The identifier string (e.g., "Warrior", "Ice").
        name: The display name (e.g., "Destruction", "Ice").
    """

    id: str
    name: str


class CharacterDetailTypes(BaseModel):
    """Contain the character's Path and Combat Type details.

    Attributes:
        path_type: The character's Path details.
        combat_type: The character's Combat Type details.
    """

    path_type: CharacterDetailType = Field(alias="pathType")
    combat_type: CharacterDetailType = Field(alias="combatType")


class CharacterDetail(BaseModel):
    """Represent detailed information about a character.

    Attributes:
        id: The unique identifier for the character.
        name: The name of the character.
        beta: Whether the character is currently in beta.
        rarity: The rarity (star rating) of the character.
        types: The Path and Combat Type details of the character.
        icon: The URL to the character's standard avatar icon.
        release: Timestamp of the character's release (may be 0 if unreleased or unknown).
        route: The API route for this character.
        info: Additional fetter information (description, faction, VAs).
        upgrades: A list of ascension details for each rank.
        traces: Container for all skill and trace information.
        eidolons: A list of the character's Eidolons.
        ascension: A list of materials required for ascension across all ranks.
        script: Container for character stories and voice lines.
        release_at: Datetime object representing the release timestamp (optional).
    """

    id: int
    name: str
    beta: bool = Field(False)
    rarity: int = Field(alias="rank")
    types: CharacterDetailTypes
    icon: str
    release: int
    route: str
    info: CharacterInfo = Field(alias="fetter")
    upgrades: list[CharacterUpgrade] = Field(alias="upgrade")
    traces: CharacterTraces
    eidolons: list[CharacterEidolon]
    ascension: list[CharacterAscensionItem]
    script: CharacterScript
    release_at: datetime.datetime | None = Field(None, alias="release")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/avatar/{v}.png"

    @field_validator("eidolons", mode="before")
    @classmethod
    def __convert_eidolons(cls, v: dict[str, dict[str, Any]]) -> list[CharacterEidolon]:
        return [CharacterEidolon(**v[s]) for s in v]

    @field_validator("ascension", mode="before")
    @classmethod
    def __convert_ascension(cls, v: dict[str, int]) -> list[CharacterAscensionItem]:
        return [CharacterAscensionItem(id=int(k), amount=v) for k, v in v.items()]

    @field_validator("release_at", mode="before")
    @classmethod
    def __convert_release_at(cls, v: int | None) -> datetime.datetime | None:
        return datetime.datetime.fromtimestamp(v) if v else None

    @property
    def medium_icon(self) -> str:
        """Return the URL to the medium-sized avatar icon."""
        return self.icon.replace("avatar", "avatar/medium")

    @property
    def large_icon(self) -> str:
        """Return the URL to the large-sized avatar icon (full splash art)."""
        return self.icon.replace("avatar", "avatar/large")

    @property
    def round_icon(self) -> str:
        """Return the URL to the round avatar icon."""
        return self.icon.replace("avatar", "avatar/round")


class CharacterType(BaseModel):
    """Contain the character's Path and Combat Type enums.

    Attributes:
        path_type: The character's Path enum.
        combat_type: The character's Combat Type enum.
    """

    path_type: PathType = Field(alias="pathType")
    combat_type: CombatType = Field(alias="combatType")


class Character(BaseModel):
    """Represent basic information about a character.

    Attributes:
        id: The unique identifier for the character.
        name: The name of the character.
        rarity: The rarity (star rating) of the character.
        icon: The URL to the character's standard avatar icon.
        types: Container for the character's Path and Combat Type enums.
        route: The API route for this character.
        beta: Whether the character is currently in beta.
        release_at: Datetime object representing the release timestamp (optional).
    """

    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    types: CharacterType
    route: str
    beta: bool = Field(False)
    release_at: datetime.datetime | None = Field(None, alias="release")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/avatar/{v}.png"

    @field_validator("release_at", mode="before")
    @classmethod
    def __convert_release_at(cls, v: int | None) -> datetime.datetime | None:
        return datetime.datetime.fromtimestamp(v) if v else None

    @property
    def medium_icon(self) -> str:
        """Return the URL to the medium-sized avatar icon."""
        return self.icon.replace("avatar", "avatar/medium")

    @property
    def large_icon(self) -> str:
        """Return the URL to the large-sized avatar icon (full splash art)."""
        return self.icon.replace("avatar", "avatar/large")

    @property
    def round_icon(self) -> str:
        """Return the URL to the round avatar icon."""
        return self.icon.replace("avatar", "avatar/round")
