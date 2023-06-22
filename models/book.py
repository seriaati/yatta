from pydantic import BaseModel, Field, validator


class Book(BaseModel):
    id: int
    name: str
    world_type: int = Field(alias="worldType")
    chapter_count: int = Field(alias="chapterCount")
    icon: str
    route: str

    @validator("icon", pre=True)
    def validate_icon(cls, v):
        return f"https://api.yatta.top/hsr/assets/UI/book/{v}.png"
