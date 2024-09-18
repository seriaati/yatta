from __future__ import annotations

import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Final, Self

from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession

from .exceptions import ConnectionTimeoutError, DataNotFoundError, YattaAPIError
from .models import (
    Book,
    BookDetail,
    Changelog,
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

if TYPE_CHECKING:
    import aiohttp

__all__ = ("Language", "YattaAPI")

LOGGER_ = logging.getLogger("yatta.py")


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

    Parameters:
        lang: The language to use for the API. Defaults to Language.EN.
        cache_ttl: The time-to-live for the cache in seconds. Defaults to 3600.
        headers: A dictionary of headers to use for the requests. Defaults to None.
        session: An aiohttp.ClientSession to use for the requests. Defaults to None.
    """

    BASE_URL: Final[str] = "https://sr.yatta.moe/api/v2"

    def __init__(
        self,
        *,
        lang: Language = Language.EN,
        cache_ttl: int = 3600,
        headers: dict[str, Any] | None = None,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        self.lang = lang
        self.cache_ttl = cache_ttl

        self._session = session
        self._cache = SQLiteBackend("./.cache/yatta/aiohttp-cache.db", expire_after=cache_ttl)
        self._headers = headers or {"User-Agent": "yatta-py"}

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        await self.close()

    async def _request(
        self, endpoint: str, *, static: bool = False, use_cache: bool
    ) -> dict[str, Any]:
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
        if self._session is None:
            msg = "Call `start` before making requests."
            raise RuntimeError(msg)

        if static:
            url = f"{self.BASE_URL}/static/{endpoint}"
        else:
            url = f"{self.BASE_URL}/{self.lang.value}/{endpoint}"

        LOGGER_.debug("Requesting %s...", url)

        if not use_cache and isinstance(self._session, CachedSession):
            async with self._session.disabled(), self._session.get(url) as resp:
                if resp.status != 200:
                    self._handle_error(resp.status)
                data: dict[str, Any] = await resp.json()
        else:
            async with self._session.get(url) as resp:
                if resp.status != 200:
                    self._handle_error(resp.status)
                data: dict[str, Any] = await resp.json()

        return data

    def _handle_error(self, code: int) -> None:
        """
        A helper function to handle errors.
        """
        match code:
            case 404:
                raise DataNotFoundError
            case 522:
                raise ConnectionTimeoutError
            case _:
                raise YattaAPIError(code)

    async def start(self) -> None:
        """
        Starts the client session.
        """
        self._session = self._session or CachedSession(headers=self._headers, cache=self._cache)

    async def close(self) -> None:
        """
        Closes the client session and cache.
        """
        if self._session is not None:
            await self._session.close()

    async def fetch_books(self, use_cache: bool = True) -> list[Book]:
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

    async def fetch_characters(self, use_cache: bool = True) -> list[Character]:
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

    async def fetch_character_detail(self, id: int, use_cache: bool = True) -> CharacterDetail:
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

    async def fetch_items(self, use_cache: bool = True) -> list[Item]:
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

    async def fetch_light_cones(self, use_cache: bool = True) -> list[LightCone]:
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

    async def fetch_light_cone_detail(self, id: int, use_cache: bool = True) -> LightConeDetail:
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

    async def fetch_messages(self, use_cache: bool = True) -> list[Message]:
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

    async def fetch_message_types(self, use_cache: bool = True) -> dict[str, str]:
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

    async def fetch_relic_sets(self, use_cache: bool = True) -> list[RelicSet]:
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

    async def fetch_relic_set_detail(self, id: int, use_cache: bool = True) -> RelicSetDetail:
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
        data = await self._request(f"relic/{id}", use_cache=use_cache)
        relic = RelicSetDetail(**data["data"])
        return relic

    async def fetch_changelogs(self, use_cache: bool = True) -> list[Changelog]:
        """
        Fetch changelogs from the API.

        Parameters
        ----------
        use_cache : bool, optional
            Whether to use the cache or not. Defaults to True.

        Returns
        -------
        List[Changelog]
            A list of Changelog objects.

        Raises
        ------
        DataNotFound
            If the requested data is not found.
        """
        data = await self._request("changelog", static=True, use_cache=use_cache)
        change_logs: list[Changelog] = []
        for changelog_id, log in data["data"].items():
            change_logs.append(Changelog(id=int(changelog_id), **log))
        return change_logs

    async def fetch_manual_avatar(self, use_cache: bool = True) -> dict[str, dict[str, str]]:
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
