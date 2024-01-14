from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags, replace_placeholders

__all__ = (
    "Character",
    "CharacterDetail",
    "CharacterEidolon",
    "CharacterScript",
    "CharacterStory",
    "CharacterTraces",
    "CharacterUpgrade",
    "CharacterVoice",
    "SkillAdd",
    "SkillListSkill",
    "SkillPoint",
    "SkillPromote",
    "SkillPromoteCostItem",
    "SkillTree",
    "SkillTreeSkill",
    "Status",
    "WeaknessBreak",
    "ExtraEffect",
    "CharacterAscensionItem",
    "BaseSkill",
    "BaseStat",
    "AddStat",
    "VoiceActor",
    "CharacterInfo",
    "CharacterType",
    "CharacterDetailTypes",
)


class CharacterStory(BaseModel):
    title: str
    text: str

    @field_validator("text", mode="before")
    def _format_text(cls, v: str) -> str:
        return remove_html_tags(v)


class CharacterVoice(BaseModel):
    title: str
    text: str
    audio: Optional[int]


class CharacterScript(BaseModel):
    story: List[CharacterStory]
    voice: List[CharacterVoice]

    @field_validator("story", mode="before")
    def _convert_story(cls, v: Optional[List[Dict[str, Any]]]) -> List[CharacterStory]:
        return [CharacterStory(**s) for s in v] if v else []

    @field_validator("voice", mode="before")
    def _convert_voice(cls, v: Optional[List[Dict[str, Any]]]) -> List[CharacterVoice]:
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

    params: Optional[List[Union[int, float]]]
    description: str
    skill_add_level_list: List[SkillAdd] = Field(alias="skillAddLevelList")
    """List of skills that increase their level because of this eidolon"""
    icon: str

    @field_validator("description", mode="before")
    def _format_description(cls, v: str, values) -> str:
        params = values.data.get("params")
        return replace_placeholders(remove_html_tags(v), params)

    @field_validator("skill_add_level_list", mode="before")
    def _convert_skill_add_level_list(
        cls, v: Optional[Dict[str, int]]
    ) -> List[SkillAdd]:
        return (
            [SkillAdd(id=int(id), level=level) for id, level in v.items()] if v else []
        )

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/skill/{v}.png"


class SkillPromoteCostItem(BaseModel):
    id: int
    amount: int


class SkillPromote(BaseModel):
    level: int
    cost_items: List[SkillPromoteCostItem] = Field(alias="costItems")

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(
        cls, v: Dict[str, Optional[Dict[str, int]]]
    ) -> List[SkillPromoteCostItem]:
        return (
            [
                SkillPromoteCostItem(id=int(id), amount=a)
                for id, a in v["costItems"].items()
            ]
            if v["costItems"]
            else []
        )


class Status(BaseModel):
    name: str
    value: Union[int, float]
    icon: str

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/status/{v}.png"


class ExtraEffect(BaseModel):
    name: str
    description: str
    icon: str


class WeaknessBreak(BaseModel):
    type: str
    value: int


class SkillPoint(BaseModel):
    type: str
    value: Optional[int]


class SkillListSkill(BaseModel):
    id: int
    name: str
    tag: Optional[str]
    type: str

    max_level: int = Field(alias="maxLevel")
    skill_points: List[SkillPoint] = Field(alias="skillPoints")
    weakness_break: List[WeaknessBreak] = Field(alias="weaknessBreak")
    description: str
    simplified_description: Optional[str] = Field(alias="descriptionSimple")

    traces: List[int]
    eidolons: List[int]
    extra_effects: List[ExtraEffect] = Field(alias="extraEffects")
    attack_type: Optional[str] = Field(alias="attackType")
    damage_type: Optional[str] = Field(alias="damageType")
    icon: str

    params: Optional[Dict[str, List[float]]]

    @field_validator("skill_points", mode="before")
    def _convert_skill_points(cls, v: Dict[str, Optional[int]]) -> List[SkillPoint]:
        return [SkillPoint(type=k, value=v) for k, v in v.items()]

    @field_validator("weakness_break", mode="before")
    def _convert_weakness_break(
        cls, v: Optional[Dict[str, int]]
    ) -> List[WeaknessBreak]:
        return [WeaknessBreak(type=k, value=v) for k, v in v.items()] if v else []

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("simplified_description", mode="before")
    def _format_simplified_description(cls, v: Optional[str]) -> Optional[str]:
        return remove_html_tags(v) if v else None

    @field_validator("traces", mode="before")
    def _convert_traces(cls, v: Optional[List[int]]) -> List[int]:
        return v if v else []

    @field_validator("eidolons", mode="before")
    def _convert_eidolons(cls, v: Optional[List[int]]) -> List[int]:
        return v if v else []

    @field_validator("extra_effects", mode="before")
    def _convert_extra_effects(
        cls, v: Optional[List[Dict[str, Any]]]
    ) -> List[ExtraEffect]:
        return [ExtraEffect(**e) for e in v] if v else []

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/skill/{v}.png"


class BaseSkill(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    point_type: str = Field(alias="pointType")
    point_position: str = Field(alias="pointPosition")
    max_level: int = Field(alias="maxLevel")
    is_default: bool = Field(alias="isDefault")

    avatar_level_limit: Optional[int] = Field(alias="avatarLevelLimit")
    avatar_promotion_limit: Optional[int] = Field(alias="avatarPromotionLimit")

    skill_list: List[SkillListSkill] = Field(alias="skillList")
    status_list: List[Status] = Field(alias="statusList")
    icon: str
    params: Optional[Dict[str, List[float]]]

    promote: List[SkillPromote]

    @field_validator("description", mode="before")
    def _format_description(cls, v: Optional[str]) -> Optional[str]:
        return remove_html_tags(v) if v else None

    @field_validator("skill_list", mode="before")
    def _convert_skill_list(
        cls, v: Optional[Dict[str, Dict[str, Any]]]
    ) -> List[SkillListSkill]:
        return [SkillListSkill(id=int(s), **v[s]) for s in v] if v else []

    @field_validator("status_list", mode="before")
    def _convert_status_list(cls, v: Optional[List[Dict[str, Any]]]) -> List[Status]:
        return [Status(**s) for s in v] if v else []

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/status/{v}.png"

    @field_validator("promote", mode="before")
    def _convert_promote(
        cls, v: Dict[str, Dict[str, Optional[Dict[str, int]]]]
    ) -> List[SkillPromote]:
        return [SkillPromote(level=int(p), costItems=v[p]) for p in v] if v else []  # type: ignore


class SkillTreeSkill(BaseModel):
    id: int
    points_direction: Optional[str] = Field(alias="pointsDirection")
    points: List[int]

    @field_validator("points", mode="before")
    def _convert_points(cls, v: Optional[List[int]]) -> List[int]:
        return v if v else []


class SkillTree(BaseModel):
    id: int
    type: str
    tree: List[SkillTreeSkill] = Field([])

    @field_validator("tree", mode="before")
    def _convert_tree(cls, v: Dict[str, Dict[str, Any]]) -> List[SkillTreeSkill]:
        return [SkillTreeSkill(**v[s]) for s in v]


class CharacterTraces(BaseModel):
    main_skills: List[BaseSkill] = Field(alias="mainSkills")
    sub_skills: List[BaseSkill] = Field(alias="subSkills")
    tree_skills: List[SkillTree] = Field(alias="skillsTree")

    @field_validator("main_skills", mode="before")
    def _convert_main_skills(cls, v: Dict[str, Dict[str, Any]]) -> List[BaseSkill]:
        return [BaseSkill(**v[s]) for s in v]

    @field_validator("sub_skills", mode="before")
    def _convert_sub_skills(cls, v: Dict[str, Dict[str, Any]]) -> List[BaseSkill]:
        return [BaseSkill(**v[s]) for s in v]

    @field_validator("tree_skills", mode="before")
    def _convert_tree_skills(cls, v: Dict[str, Dict[str, Any]]) -> List[SkillTree]:
        return [SkillTree(**v[s]) for s in v]


class AddStat(BaseModel):
    id: str
    value: Union[int, float]


class BaseStat(BaseModel):
    id: str
    value: Union[int, float]


class UpgradeItem(BaseModel):
    id: int
    amount: int


class CharacterUpgrade(BaseModel):
    level: int
    cost_items: List[UpgradeItem] = Field(alias="costItems")
    new_max_level: int = Field(alias="maxLevel")
    required_player_level: int = Field(alias="playerLevelRequire")
    required_world_level: int = Field(alias="worldLevelRequire")
    base_stats: List[BaseStat] = Field(alias="skillBase")
    add_stats: List[AddStat] = Field(alias="skillAdd")

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(cls, v: Optional[Dict[str, int]]) -> List[UpgradeItem]:
        return [UpgradeItem(id=int(k), amount=v) for k, v in v.items()] if v else []

    @field_validator("required_player_level", mode="before")
    def _convert_required_player_level(cls, v: Optional[int]) -> int:
        return v if v else 0

    @field_validator("required_world_level", mode="before")
    def _convert_required_world_level(cls, v: Optional[int]) -> int:
        return v if v else 0

    @field_validator("base_stats", mode="before")
    def _convert_base_stats(cls, v: Dict[str, Union[int, float]]) -> List[BaseStat]:
        return [BaseStat(id=k, value=v) for k, v in v.items()]

    @field_validator("add_stats", mode="before")
    def _convert_add_stats(cls, v: Dict[str, Union[int, float]]) -> List[AddStat]:
        return [AddStat(id=k, value=v) for k, v in v.items()]


class VoiceActor(BaseModel):
    lang: str
    name: str


class CharacterInfo(BaseModel):
    faction: Optional[str]
    description: str
    voice_actors: List[VoiceActor] = Field(alias="cv")

    @field_validator("voice_actors", mode="before")
    def _convert_voice_actors(cls, v: Optional[Dict[str, str]]) -> List[VoiceActor]:
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
    upgrades: List[CharacterUpgrade] = Field(alias="upgrade")
    traces: CharacterTraces
    eidolons: List[CharacterEidolon]
    ascension: List[CharacterAscensionItem]
    script: CharacterScript

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/avatar/{v}.png"

    @field_validator("eidolons", mode="before")
    def _convert_eidolons(cls, v: Dict[str, Dict[str, Any]]) -> List[CharacterEidolon]:
        return [CharacterEidolon(**v[s]) for s in v]

    @field_validator("ascension", mode="before")
    def _convert_ascension(cls, v: Dict[str, int]) -> List[CharacterAscensionItem]:
        return [CharacterAscensionItem(id=int(k), amount=v) for k, v in v.items()]

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
    path_type: str = Field(alias="pathType")
    combat_type: str = Field(alias="combatType")


class Character(BaseModel):
    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    types: CharacterType
    route: str
    beta: bool = Field(False)

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/avatar/{v}.png"

    @property
    def medium_icon(self) -> str:
        return self.icon.replace("avatar", "avatar/medium")

    @property
    def large_icon(self) -> str:
        return self.icon.replace("avatar", "avatar/large")

    @property
    def round_icon(self) -> str:
        return self.icon.replace("avatar", "avatar/round")
