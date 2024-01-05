import asyncio
import logging
from enum import Enum
from typing import Any, Dict, Final, List

import aiohttp
from diskcache import Cache

from .exceptions import DataNotFound
from .models import (
    Book,
    BookDetail,
    ChangeLog,
    Character,
    CharacterDetail,
    Item,
    ItemDetail,
    LightCone,
    LightConeDetail,
    Message,
    RelicSet,
    RelicSetDetail,
)

__all__ = ("YattaAPI", "Language")


class Language(Enum):
    CHT = "cht"
    CN = "cn"
    DE = "de"
    EN = "en"
    ES = "es"
    FR = "fr"
    ID = "id"
    JP = "jp"
    KR = "kr"
    PT = "pt"
    RU = "ru"
    TH = "th"
    VI = "vi"


class YattaAPI:
    """
    The main class that is used to interact with the API.

    Parameters
    ----------
    lang : Language, optional
        The language to use for the API. Defaults to Language.EN.

    Attributes
    ----------
    BASE_URL : str
        The base URL for the API. This is used internally.
    lang : Language
        The language that is used for the API.
    """

    BASE_URL: Final[str] = "https://api.yatta.top/hsr/v2"

    def __init__(self, lang: Language = Language.EN):
        self.lang = lang
        self.session = aiohttp.ClientSession(headers={"User-Agent": "yatta.py"})
        self.cache = Cache(".cache/yatta")

    async def __aenter__(self) -> "YattaAPI":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def _request(
        self, endpoint: str, *, static: bool = False, use_cache: bool
    ) -> Dict[str, Any]:
        """
        A helper function to make requests to the API.

        Parameters
        ----------
        endpoint : str
            The endpoint to request from.
        static : bool, optional
            Whether to use the static endpoint or not. Defaults to False.
        use_cache : bool
            Whether to use the cache or not

        Returns
        -------
        Dict[str, Any]
            The response from the API.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        if static:
            url = f"{self.BASE_URL}/static/{endpoint}"
        else:
            url = f"{self.BASE_URL}/{self.lang.value}/{endpoint}"

        cache = await asyncio.to_thread(self.cache.get, url)
        if cache is not None and use_cache:
            return cache  # type: ignore

        logging.debug(f"Requesting {url}...")
        async with self.session.get(url) as resp:
            data = await resp.json()
            if "code" in data and data["code"] == 404:
                raise DataNotFound(data["data"])
            await asyncio.to_thread(self.cache.set, url, data, expire=86400)
            return data

    async def close(self) -> None:
        """
        Closes the client session and cache.
        """
        await self.session.close()
        self.cache.close()

    async def fetch_books(self, use_cache: bool = True) -> List[Book]:
        """
        Fetch all books from the API.

        Parameters
        ----------
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        List[Book]
            A list of Book objects.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request("book", use_cache=use_cache)
        books = [Book(**b) for b in data["data"]["items"].values()]
        return books

    async def fetch_book_detail(self, id: int, use_cache: bool = True) -> BookDetail:
        """
        Fetch a book's detail from the API.

        Parameters
        ----------
        id : int
            The ID of the book to fetch.
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        BookDetail
            A BookDetail object.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request(f"book/{id}", use_cache=use_cache)
        book = BookDetail(**data["data"])
        return book

    async def fetch_characters(self, use_cache: bool = True) -> List[Character]:
        """
        Fetch all characters from the API.

        Parameters
        ----------
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        List[Character]
            A list of Character objects.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request("avatar", use_cache=use_cache)
        characters = [Character(**c) for c in data["data"]["items"].values()]
        return characters

    async def fetch_character_detail(
        self, id: int, use_cache: bool = True
    ) -> CharacterDetail:
        """
        Fetch a character's detail from the API.

        Parameters
        ----------
        id : int
            The ID of the character to fetch.
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        CharacterDetail
            A CharacterDetail object.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request(f"avatar/{id}", use_cache=use_cache)
        character = CharacterDetail(**data["data"])
        return character

    async def fetch_items(self, use_cache: bool = True) -> List[Item]:
        """
        Fetch all items from the API.

        Parameters
        ----------
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        List[Item]
            A list of Item objects.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request("item", use_cache=use_cache)
        items = [Item(**i) for i in data["data"]["items"].values()]
        return items

    async def fetch_item_detail(self, id: int, use_cache: bool = True) -> ItemDetail:
        """
        Fetch an item's detail from the API.

        Parameters
        ----------
        id : int
            The ID of the item to fetch.
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        ItemDetail
            An ItemDetail object.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request(f"item/{id}", use_cache=use_cache)
        item = ItemDetail(**data["data"])
        return item

    async def fetch_light_cones(self, use_cache: bool = True) -> List[LightCone]:
        """
        Fetch all light cones from the API.

        Parameters
        ----------
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        List[LightCone]
            A list of LightCone objects.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request("equipment", use_cache=use_cache)
        light_cones = [LightCone(**lc) for lc in data["data"]["items"].values()]
        return light_cones

    async def fetch_light_cone_detail(
        self, id: int, use_cache: bool = True
    ) -> LightConeDetail:
        """
        Fetch a light cone's detail from the API.

        Parameters
        ----------
        id : int
            The ID of the light cone to fetch.
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        LightConeDetail
            A LightConeDetail object.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request(f"equipment/{id}", use_cache=use_cache)
        light_cone = LightConeDetail(**data["data"])
        return light_cone

    async def fetch_messages(self, use_cache: bool = True) -> List[Message]:
        """
        Fetch all messages from the API.

        Parameters
        ----------
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        List[Message]
            A list of Message objects.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request("message", use_cache=use_cache)
        messages = [Message(**m) for m in data["data"]["items"].values()]
        return messages

    async def fetch_message_types(self, use_cache: bool = True) -> Dict[str, str]:
        """
        Fetch all message types from the API.

        Parameters
        ----------
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        List[str]
            A list of message types.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request("message", use_cache=use_cache)
        return data["data"]["types"]

    async def fetch_relic_sets(self, use_cache: bool = True) -> List[RelicSet]:
        """
        Fetch all relic sets from the API.

        Parameters
        ----------
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        List[RelicSet]
            A list of RelicSet objects.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request("relic", use_cache=use_cache)
        relics = [RelicSet(**r) for r in data["data"]["items"].values()]
        return relics

    async def fetch_relic_set_detail(
        self, id: int, use_cache: bool = True
    ) -> RelicSetDetail:
        """
        Fetch a relic set's detail from the API.

        Parameters
        ----------
        id : int
            The ID of the relic set to fetch.
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        RelicSetDetail
            A RelicSetDetail object.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        logging.debug(f"Fetching relic set detail for ID {id}")
        data = await self._request(f"relic/{id}", use_cache=use_cache)
        relic = RelicSetDetail(**data["data"])
        return relic

    async def fetch_change_logs(self, use_cache: bool = True) -> List[ChangeLog]:
        """
        Fetch change logs from the API.

        Parameters
        ----------
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        List[ChangeLog]
            A list of ChangeLog objects.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request("changelog", static=True, use_cache=use_cache)
        change_logs: List[ChangeLog] = []
        for id, log in data["data"].items():
            change_logs.append(ChangeLog(id=int(id), **log))
        return change_logs

    async def fetch_manual_avatar(
        self, use_cache: bool = True
    ) -> Dict[str, Dict[str, str]]:
        """
        Fetch the manual avatar from the API.

        Parameters
        ----------
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        Dict[str, Dict[str, str]]
            A dictionary of avatar stat keys to their corresponding names and icons.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request("manualAvatar", use_cache=use_cache)
        return data["data"]
