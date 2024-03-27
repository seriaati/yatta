from typing import Any

from pydantic import Field, field_validator

from .base import BaseModel

__all__ = (
    "BookSeries",
    "BookDetail",
    "Book",
)


class BookSeries(BaseModel):
    id: int
    name: str
    story: str
    image_list: list[str] = Field(alias="imageList")

    @field_validator("image_list", mode="before")
    def _convert_image_list(cls, v: list[str] | None) -> list[str]:
        return v if v else []


class BookDetail(BaseModel):
    id: int
    name: str
    world_type: str = Field(alias="worldType")
    chapter_count: int = Field(0)
    icon: str
    description: str
    series: list[BookSeries]

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/item/{v}.png"

    @field_validator("series", mode="before")
    def _convert_series(cls, v: dict[str, dict[str, Any]]) -> list[BookSeries]:
        return [BookSeries(id=int(series_id), **s) for series_id, s in v.items()]


class Book(BaseModel):
    id: int
    name: str
    world_type: int = Field(alias="worldType")
    chapter_count: int = Field(alias="chapterCount")
    icon: str
    route: str

    @field_validator("icon", mode="before")
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/item/{v}.png"
