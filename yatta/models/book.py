from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator

from ..utils import remove_html_tags


class BookSeries(BaseModel):
    id: int
    name: str
    story: str
    image_list: List[str] = Field(alias="imageList")

    @validator("story", pre=True)
    def _format_story(cls, v: str) -> str:
        return remove_html_tags(v)

    @validator("image_list", pre=True)
    def _convert_image_list(cls, v: Optional[List[str]]) -> List[str]:
        return v if v else []


class BookDetail(BaseModel):
    id: int
    name: str
    world_type: str = Field(alias="worldType")
    chapter_count: int = Field(0)
    icon: str
    description: str
    series: List[BookSeries]

    @validator("name", pre=True)
    def _format_name(cls, v: str) -> str:
        return remove_html_tags(v)

    @validator("icon", pre=True)
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/book/{v}.png"

    @validator("series", pre=True)
    def _convert_series(cls, v: Dict[str, Dict[str, Any]]) -> List[BookSeries]:
        return [BookSeries(id=int(id), **s) for id, s in v.items()]


class Book(BaseModel):
    id: int
    name: str
    world_type: int = Field(alias="worldType")
    chapter_count: int = Field(alias="chapterCount")
    icon: str
    route: str

    @validator("icon", pre=True)
    def _convert_icon(cls, v: str) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/book/{v}.png"
