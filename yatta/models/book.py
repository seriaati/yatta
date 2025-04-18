from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from .base import BaseModel

__all__ = ("Book", "BookDetail", "BookSeries")


class BookSeries(BaseModel):
    """Represent a book series.

    Attributes:
        id: The ID of the series.
        name: The name of the series.
        story: The story or description of the series.
        image_list: A list of image URLs associated with the series.
    """

    id: int
    name: str
    story: str
    image_list: list[str] = Field(alias="imageList")

    @field_validator("image_list", mode="before")
    @classmethod
    def __convert_image_list(cls, v: list[str] | None) -> list[str]:
        return v or []


class BookDetail(BaseModel):
    """Represent detailed information about a book.

    Attributes:
        id: The ID of the book.
        name: The name of the book.
        world_type: The type of world the book is associated with.
        chapter_count: The number of chapters in the book.
        icon: The URL of the book's icon.
        description: The description of the book.
        series: A list of book series entries contained within this book.
    """

    id: int
    name: str
    world_type: str = Field(alias="worldType")
    chapter_count: int = Field(0)
    icon: str
    description: str
    series: list[BookSeries]

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/item/{v}.png"

    @field_validator("series", mode="before")
    @classmethod
    def __convert_series(cls, v: dict[str, dict[str, Any]]) -> list[BookSeries]:
        return [BookSeries(id=int(series_id), **s) for series_id, s in v.items()]


class Book(BaseModel):
    """Represent basic information about a book.

    Attributes:
        id: The ID of the book.
        name: The name of the book.
        world_type: The numeric ID representing the type of world the book is associated with.
        chapter_count: The number of chapters in the book.
        icon: The URL of the book's icon.
        route: The API route for this book.
    """

    id: int
    name: str
    world_type: int = Field(alias="worldType")
    chapter_count: int = Field(alias="chapterCount")
    icon: str
    route: str

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/item/{v}.png"
