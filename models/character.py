from pydantic import BaseModel, Field, validator


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

    @validator("icon", pre=True)
    def validate_icon(cls, v):
        return f"https://api.yatta.top/hsr/assets/UI/avatar/{v}.png"

    @validator("types", pre=True)
    def validate_types(cls, v):
        return CharacterType(**v)
