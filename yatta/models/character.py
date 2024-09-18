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
    "CharacterDetail",
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
    title: str
    text: str


class CharacterVoice(BaseModel):
    title: str
    text: str
    audio: int | None


class CharacterScript(BaseModel):
    stories: list[CharacterStory] = Field(alias="story")
    voices: list[CharacterVoice] = Field(alias="voice")

    @field_validator("stories", mode="before")
    def _convert_stories(cls, v: list[dict[str, Any]] | None) -> list[CharacterStory]:
        return [CharacterStory(**s) for s in v] if v else []

    @field_validator("voices", mode="before")
    def _convert_voices(cls, v: list[dict[str, Any]] | None) -> list[CharacterVoice]:
        return [CharacterVoice(**s) for s in v] if v else []


class CharacterAscensionItem(BaseModel):
    id: int
    amount: int


class SkillAdd(BaseModel):
    """Skill that inceases its level because of an eidolon"""

    id: int
    """ID of the skill"""
    level: int
    """Level added to the skill"""


class CharacterEidolon(BaseModel):
    id: int
    rank: int
    name: str

    params: list[int | float] | None
    description: str
    skill_add_level_list: list[SkillAdd] = Field(alias="skillAddLevelList")
    """List of skills that increase their level because of this eidolon"""
    icon: str

    @field_validator("description", mode="before")
    def _format_description(cls, v: str, values: Any) -> str:
        params = values.data.get("params")
        return replace_placeholders(format_str(v), params)

    @field_validator("skill_add_level_list", mode="before")
    def _convert_skill_add_level_list(cls, v: dict[str, int] | None) -> list[SkillAdd]:
        return [SkillAdd(id=int(id_), level=level) for id_, level in v.items()] if v else []

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/skill/{v}.png"


class SkillPromoteCostItem(BaseModel):
    id: int
    amount: int


class SkillPromote(BaseModel):
    level: int
    cost_items: list[SkillPromoteCostItem] = Field(alias="costItems")

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(cls, v: dict[str, dict[str, int] | None]) -> list[SkillPromoteCostItem]:
        return (
            [SkillPromoteCostItem(id=int(id_), amount=a) for id_, a in v["costItems"].items()]
            if v["costItems"]
            else []
        )


class Status(BaseModel):
    name: str
    value: int | float
    icon: str

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/status/{v}.png"


class ExtraEffect(BaseModel):
    name: str
    description: str
    icon: str


class WeaknessBreak(BaseModel):
    type: str
    value: int


class SkillPoint(BaseModel):
    type: str
    value: int | None


class SkillListSkill(BaseModel):
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

    @field_validator("skill_points", mode="before")
    def _convert_skill_points(cls, v: dict[str, int | None]) -> list[SkillPoint]:
        return [SkillPoint(type=k, value=v) for k, v in v.items()]

    @field_validator("weakness_break", mode="before")
    def _convert_weakness_break(cls, v: dict[str, int] | None) -> list[WeaknessBreak]:
        return [WeaknessBreak(type=k, value=v) for k, v in v.items()] if v else []

    @field_validator("simplified_description", mode="before")
    def _format_simplified_description(cls, v: str | None) -> str | None:
        return format_str(v) if v else None

    @field_validator("traces", mode="before")
    def _convert_traces(cls, v: list[int] | None) -> list[int]:
        return v if v else []

    @field_validator("eidolons", mode="before")
    def _convert_eidolons(cls, v: list[int] | None) -> list[int]:
        return v if v else []

    @field_validator("extra_effects", mode="before")
    def _convert_extra_effects(cls, v: list[dict[str, Any]] | None) -> list[ExtraEffect]:
        return [ExtraEffect(**e) for e in v] if v else []

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/skill/{v}.png"


class BaseSkill(BaseModel):
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
    def _convert_skill_list(cls, v: dict[str, dict[str, Any]] | None) -> list[SkillListSkill]:
        return [SkillListSkill(id=int(s), **v[s]) for s in v] if v else []

    @field_validator("status_list", mode="before")
    def _convert_status_list(cls, v: list[dict[str, Any]] | None) -> list[Status]:
        return [Status(**s) for s in v] if v else []

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        if "SkillIcon" in v:
            return f"https://sr.yatta.moe/hsr/assets/UI/skill/{v}.png"
        return f"https://sr.yatta.moe/hsr/assets/UI/status/{v}.png"

    @field_validator("promote", mode="before")
    def _convert_promote(cls, v: dict[str, dict[str, dict[str, int] | None]]) -> list[SkillPromote]:
        return [SkillPromote(level=int(p), costItems=v[p]) for p in v] if v else []  # type: ignore


class SkillTreeSkill(BaseModel):
    id: int
    points_direction: str | None = Field(alias="pointsDirection")
    points: list[int]

    @field_validator("points", mode="before")
    def _convert_points(cls, v: list[int] | None) -> list[int]:
        return v if v else []


class SkillTree(BaseModel):
    id: int
    type: str
    tree: list[SkillTreeSkill] = Field([])

    @field_validator("tree", mode="before")
    def _convert_tree(cls, v: dict[str, dict[str, Any]]) -> list[SkillTreeSkill]:
        return [SkillTreeSkill(**v[s]) for s in v]


class CharacterTraces(BaseModel):
    main_skills: list[BaseSkill] = Field(alias="mainSkills")
    sub_skills: list[BaseSkill] = Field(alias="subSkills")
    tree_skills: list[SkillTree] = Field(alias="skillsTree")

    @field_validator("main_skills", mode="before")
    def _convert_main_skills(cls, v: dict[str, dict[str, Any]]) -> list[BaseSkill]:
        return [BaseSkill(**v[s]) for s in v]

    @field_validator("sub_skills", mode="before")
    def _convert_sub_skills(cls, v: dict[str, dict[str, Any]]) -> list[BaseSkill]:
        return [BaseSkill(**v[s]) for s in v]

    @field_validator("tree_skills", mode="before")
    def _convert_tree_skills(cls, v: dict[str, dict[str, Any]]) -> list[SkillTree]:
        return [SkillTree(**v[s]) for s in v]


class CharacterCostItem(BaseModel):
    id: int
    amount: int


class CharacterUpgrade(BaseModel):
    level: int
    cost_items: list[CharacterCostItem] = Field(alias="costItems")
    max_level: int = Field(alias="maxLevel")
    required_player_level: int = Field(alias="playerLevelRequire")
    required_world_level: int = Field(alias="worldLevelRequire")
    skill_base: dict[str, int | float] = Field(alias="skillBase")
    skill_add: dict[str, int | float] = Field(alias="skillAdd")

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(cls, v: dict[str, int] | None) -> list[CharacterCostItem]:
        return [CharacterCostItem(id=int(k), amount=v) for k, v in v.items()] if v else []

    @field_validator("required_player_level", mode="before")
    def _convert_required_player_level(cls, v: int | None) -> int:
        return v if v else 0

    @field_validator("required_world_level", mode="before")
    def _convert_required_world_level(cls, v: int | None) -> int:
        return v if v else 0


class VoiceActor(BaseModel):
    lang: str
    name: str


class CharacterInfo(BaseModel):
    faction: str | None
    description: str
    voice_actors: list[VoiceActor] = Field(alias="cv")

    @field_validator("voice_actors", mode="before")
    def _convert_voice_actors(cls, v: dict[str, str] | None) -> list[VoiceActor]:
        return [VoiceActor(lang=k, name=v) for k, v in v.items()] if v else []


class CharacterDetailType(BaseModel):
    id: str
    name: str


class CharacterDetailTypes(BaseModel):
    path_type: CharacterDetailType = Field(alias="pathType")
    combat_type: CharacterDetailType = Field(alias="combatType")


class CharacterDetail(BaseModel):
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
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/avatar/{v}.png"

    @field_validator("eidolons", mode="before")
    def _convert_eidolons(cls, v: dict[str, dict[str, Any]]) -> list[CharacterEidolon]:
        return [CharacterEidolon(**v[s]) for s in v]

    @field_validator("ascension", mode="before")
    def _convert_ascension(cls, v: dict[str, int]) -> list[CharacterAscensionItem]:
        return [CharacterAscensionItem(id=int(k), amount=v) for k, v in v.items()]

    @field_validator("release_at", mode="before")
    def _convert_release_at(cls, v: int | None) -> datetime.datetime | None:
        return datetime.datetime.fromtimestamp(v) if v else None

    @property
    def medium_icon(self) -> str:
        return self.icon.replace("avatar", "avatar/medium")

    @property
    def large_icon(self) -> str:
        return self.icon.replace("avatar", "avatar/large")

    @property
    def round_icon(self) -> str:
        return self.icon.replace("avatar", "avatar/round")


class CharacterType(BaseModel):
    path_type: PathType = Field(alias="pathType")
    combat_type: CombatType = Field(alias="combatType")


class Character(BaseModel):
    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    types: CharacterType
    route: str
    beta: bool = Field(False)
    release_at: datetime.datetime | None = Field(None, alias="release")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/avatar/{v}.png"

    @field_validator("release_at", mode="before")
    def _convert_release_at(cls, v: int | None) -> datetime.datetime | None:
        return datetime.datetime.fromtimestamp(v) if v else None

    @property
    def medium_icon(self) -> str:
        return self.icon.replace("avatar", "avatar/medium")

    @property
    def large_icon(self) -> str:
        return self.icon.replace("avatar", "avatar/large")

    @property
    def round_icon(self) -> str:
        return self.icon.replace("avatar", "avatar/round")
