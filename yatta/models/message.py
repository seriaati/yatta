from pydantic import Field, field_validator

from .base import BaseModel

__all__ = ("Contact", "Message")


class Contact(BaseModel):
    name: str
    signature: str | None = Field(None)
    type: int
    icon: str

    @field_validator("icon", mode="before")
    def convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/avatar/{v}.png"


class Message(BaseModel):
    id: int
    contact: Contact = Field(alias="contacts")
    section_count: int = Field(alias="sectionCount")
    route: str | None = None
