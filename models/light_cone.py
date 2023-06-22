from pydantic import BaseModel, Field, validator


class LightConeTypes(BaseModel):
    path_type: str = Field(alias="pathType")


class LightCone(BaseModel):
    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    types: LightConeTypes
    is_sellable: bool = Field(alias="isSellable")
    route: str

    @validator("icon", pre=True)
    def validate_icon(cls, v):
        return f"https://api.yatta.top/hsr/assets/UI/equipment/{v}.png"

    @validator("types", pre=True)
    def validate_types(cls, v):
        return LightConeTypes(**v)
