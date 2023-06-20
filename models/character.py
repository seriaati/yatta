from pydantic import BaseModel, Field, validator


class CharacterType(BaseModel):
    path_type: str = Field(alias="pathType")
    combat_type: str = Field(alias="combatType")


class Character(BaseModel):
    id: int
    name: str
    rarity: int = Field(alias="rank")
    types: CharacterType

    @validator("types", pre=True)
    def validate_types(cls, v):
        return CharacterType(**v)
