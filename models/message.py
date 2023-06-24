from typing import Optional

from pydantic import BaseModel, Field, validator


class Contact(BaseModel):
    name: str
    signature: Optional[str] = Field(None)
    type: int
    icon: str

    @validator("icon", pre=True)
    def validate_icon(cls, v):
        return f"https://api.yatta.top/hsr/assets/UI/avatar/{v}.png"


class Message(BaseModel):
    id: int
    contact: Contact = Field(alias="contacts")
    section_count: int = Field(alias="sectionCount")
    route: str

    @validator("contact", pre=True)
    def validate_contact(cls, v):
        return Contact(**v)
