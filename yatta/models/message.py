from typing import Optional

from pydantic import BaseModel, Field, field_validator

__all__ = ("Contact", "Message")


class Contact(BaseModel):
    name: str
    signature: Optional[str] = Field(None)
    type: int
    icon: str

    @field_validator("icon", mode="before")
    def convert_icon(cls, v):
        return f"https://api.yatta.top/hsr/assets/UI/avatar/{v}.png"


class Message(BaseModel):
    id: int
    contact: Contact = Field(alias="contacts")
    section_count: int = Field(alias="sectionCount")
    route: str
