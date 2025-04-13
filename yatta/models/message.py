from __future__ import annotations

from pydantic import Field, field_validator

from .base import BaseModel

__all__ = ("Contact", "Message")


class Contact(BaseModel):
    """Represent a message contact.

    Attributes:
        name: The name of the contact.
        signature: The signature of the contact (optional).
        type: The type identifier of the contact.
        icon: The URL to the contact's avatar icon.
    """

    name: str
    signature: str | None = Field(None)
    type: int
    icon: str

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/avatar/{v}.png"


class Message(BaseModel):
    """Represent a message thread or conversation.

    Attributes:
        id: The unique identifier for the message thread.
        contact: The contact associated with this message thread.
        section_count: The number of sections or messages in the thread.
        route: The API route for this message thread (optional).
    """

    id: int
    contact: Contact = Field(alias="contacts")
    section_count: int = Field(alias="sectionCount")
    route: str | None = None
