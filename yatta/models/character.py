from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator

from ..utils import remove_html_tags, replace_placeholders


class CharacterStory(BaseModel):
    title: str
    text: str

    @validator("text", pre=True)
    def _format_text(cls, v: str) -> str:
        return remove_html_tags(v)


class CharacterVoice(BaseModel):
    title: str
    text: str
    audio: Optional[int]


class CharacterScript(BaseModel):
    story: List[CharacterStory]
    voice: List[CharacterVoice]

    @validator("story", pre=True)
    def _convert_story(cls, v: Optional[List[Dict[str, Any]]]) -> List[CharacterStory]:
        return [CharacterStory(**s) for s in v] if v else []

    @validator("voice", pre=True)
    def _convert_voice(cls, v: Optional[List[Dict[str, Any]]]) -> List[CharacterVoice]:
        return [CharacterVoice(**s) for s in v] if v else []


class AscensionItem(BaseModel):
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

    @validator("description", pre=True)
    def _format_description(cls, v: str, values: Dict[str, Any]) -> str:
        params = values.get("params")
        return replace_placeholders(remove_html_tags(v), params)

    @validator("skill_add_level_list", pre=True)
    def _convert_skill_add_level_list(
        cls, v: Optional[Dict[str, int]]
    ) -> List[SkillAdd]:
        return [SkillAdd(id=int(id), level=l) for id, l in v.items()] if v else []

    @validator("icon", pre=True)
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/skill/{v}.png"


class SkillPromoteCostItem(BaseModel):
    id: int
    amount: int


class SkillPromote(BaseModel):
    level: int
    cost_items: List[SkillPromoteCostItem] = Field(alias="costItems")

    @validator("cost_items", pre=True)
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

    @validator("icon", pre=True)
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

    params: Optional[Dict[str, List[int]]]

    @validator("skill_points", pre=True)
    def _convert_skill_points(cls, v: Dict[str, Optional[int]]) -> List[SkillPoint]:
        return [SkillPoint(type=k, value=v) for k, v in v.items()]

    @validator("weakness_break", pre=True)
    def _convert_weakness_break(
        cls, v: Optional[Dict[str, int]]
    ) -> List[WeaknessBreak]:
        return [WeaknessBreak(type=k, value=v) for k, v in v.items()] if v else []

    @validator("description", pre=True)
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @validator("simplified_description", pre=True)
    def _format_simplified_description(cls, v: Optional[str]) -> Optional[str]:
        return remove_html_tags(v) if v else None

    @validator("traces", pre=True)
    def _convert_traces(cls, v: Optional[List[int]]) -> List[int]:
        return v if v else []

    @validator("eidolons", pre=True)
    def _convert_eidolons(cls, v: Optional[List[int]]) -> List[int]:
        return v if v else []

    @validator("extra_effects", pre=True)
    def _convert_extra_effects(
        cls, v: Optional[List[Dict[str, Any]]]
    ) -> List[ExtraEffect]:
        return [ExtraEffect(**e) for e in v] if v else []

    @validator("icon", pre=True)
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
    params: Optional[Dict[str, List[int]]]

    promote: List[SkillPromote]

    @validator("skill_list", pre=True)
    def _convert_skill_list(
        cls, v: Optional[Dict[str, Dict[str, Any]]]
    ) -> List[SkillListSkill]:
        return [SkillListSkill(id=int(s), **v[s]) for s in v] if v else []

    @validator("status_list", pre=True)
    def _convert_status_list(cls, v: Optional[List[Dict[str, Any]]]) -> List[Status]:
        return [Status(**s) for s in v] if v else []

    @validator("icon", pre=True)
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/status/{v}.png"

    @validator("promote", pre=True)
    def _convert_promote(
        cls, v: Dict[str, Dict[str, Optional[Dict[str, int]]]]
    ) -> List[SkillPromote]:
        return [SkillPromote(level=int(p), costItems=v[p]) for p in v] if v else []  # type: ignore


class SkillTreeSkill(BaseModel):
    id: int
    points_direction: Optional[str] = Field(alias="pointsDirection")
    points: List[int]

    @validator("points", pre=True)
    def _convert_points(cls, v: Optional[List[int]]) -> List[int]:
        return v if v else []


class SkillTree(BaseModel):
    id: int
    type: str
    tree: List[SkillTreeSkill] = Field([])

    @validator("tree", pre=True)
    def _convert_tree(cls, v: Dict[str, Dict[str, Any]]) -> List[SkillTreeSkill]:
        return [SkillTreeSkill(**v[s]) for s in v]


class CharacterTraces(BaseModel):
    main_skills: List[BaseSkill] = Field(alias="mainSkills")
    sub_skills: List[BaseSkill] = Field(alias="subSkills")
    tree_skills: List[SkillTree] = Field(alias="skillsTree")

    @validator("main_skills", pre=True)
    def _convert_main_skills(cls, v: Dict[str, Dict[str, Any]]) -> List[BaseSkill]:
        return [BaseSkill(**v[s]) for s in v]

    @validator("sub_skills", pre=True)
    def _convert_sub_skills(cls, v: Dict[str, Dict[str, Any]]) -> List[BaseSkill]:
        return [BaseSkill(**v[s]) for s in v]

    @validator("tree_skills", pre=True)
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

    @validator("cost_items", pre=True)
    def _convert_cost_items(cls, v: Optional[Dict[str, int]]) -> List[UpgradeItem]:
        return [UpgradeItem(id=int(k), amount=v) for k, v in v.items()] if v else []

    @validator("required_player_level", pre=True)
    def _convert_required_player_level(cls, v: Optional[int]) -> int:
        return v if v else 0

    @validator("required_world_level", pre=True)
    def _convert_required_world_level(cls, v: Optional[int]) -> int:
        return v if v else 0

    @validator("base_stats", pre=True)
    def _convert_base_stats(cls, v: Dict[str, Union[int, float]]) -> List[BaseStat]:
        return [BaseStat(id=k, value=v) for k, v in v.items()]

    @validator("add_stats", pre=True)
    def _convert_add_stats(cls, v: Dict[str, Union[int, float]]) -> List[AddStat]:
        return [AddStat(id=k, value=v) for k, v in v.items()]


class CharacterCV(BaseModel):
    lang: str
    name: str


class CharacterInfo(BaseModel):
    faction: Optional[str]
    description: str
    cv: List[CharacterCV]

    @validator("cv", pre=True)
    def _convert_cv(cls, v: Optional[Dict[str, str]]) -> List[CharacterCV]:
        return [CharacterCV(lang=k, name=v) for k, v in v.items()] if v else []


class Type(BaseModel):
    id: str
    name: str


class CharacterDetailTypes(BaseModel):
    path_type: Type = Field(alias="pathType")
    combat_type: Type = Field(alias="combatType")


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
    ascension: List[AscensionItem]
    script: CharacterScript

    @validator("icon", pre=True)
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/avatar/{v}.png"

    @validator("eidolons", pre=True)
    def _convert_eidolons(cls, v: Dict[str, Dict[str, Any]]) -> List[CharacterEidolon]:
        return [CharacterEidolon(**v[s]) for s in v]

    @validator("ascension", pre=True)
    def _convert_ascension(cls, v: Dict[str, int]) -> List[AscensionItem]:
        return [AscensionItem(id=int(k), amount=v) for k, v in v.items()]


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

    @validator("icon", pre=True)
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/avatar/{v}.png"
