from typing import Any

from pydantic import Field, field_validator

from .base import BaseModel

__all__ = (
    "Book",
    "BookDetail",
    "BookSeries",
)


class BookSeries(BaseModel):
    """Represents a book series.

    Attributes:
        id (int): The ID of the series.
        name (str): The name of the series.
        story (str): The story of the series.
        image_list (list[str]): A list of image URLs.
    """

    id: int
    name: str
    story: str
    image_list: list[str] = Field(alias="imageList")

    @field_validator("image_list", mode="before")
    def _convert_image_list(cls, v: list[str] | None) -> list[str]:
        return v if v else []


class BookDetail(BaseModel):
    """Represents a book.

    Attributes:
        id (int): The ID of the book.
        name (str): The name of the book.
        world_type (str): The type of world the book is in.
        chapter_count (int): The number of chapters in the book.
        icon (str): The URL of the book's icon.
        description (str): The description of the book.
        series (list[BookSeries]): A list of book series.
    """

    id: int
    name: str
    world_type: str = Field(alias="worldType")
    chapter_count: int = Field(0)
    icon: str
    description: str
    series: list[BookSeries]

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/item/{v}.png"

    @field_validator("series", mode="before")
    def _convert_series(cls, v: dict[str, dict[str, Any]]) -> list[BookSeries]:
        return [BookSeries(id=int(series_id), **s) for series_id, s in v.items()]


class Book(BaseModel):
    """Represents a book.

    Attributes:
        id (int): The ID of the book.
        name (str): The name of the book.
        world_type (int): The type of world the book is in.
        chapter_count (int): The number of chapters in the book.
        icon (str): The URL of the book's icon.
        route (str): The route of the book.
    """

    id: int
    name: str
    world_type: int = Field(alias="worldType")
    chapter_count: int = Field(alias="chapterCount")
    icon: str
    route: str

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/item/{v}.png"
