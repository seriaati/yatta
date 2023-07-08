import logging
from enum import Enum
from typing import Any, Dict, Final, List

import aiohttp

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
    lang: :class:`Language`
        The language to use for the API. Defaults to ``Language.EN``.

    Attributes
    ----------
    BASE_URL: :class:`str`
        The base URL for the API. This is used internally.
    lang: :class:`Language`
        The language that is used for the API.
    """

    BASE_URL: Final[str] = "https://api.yatta.top/hsr/v2"

    def __init__(self, lang: Language = Language.EN):
        self.lang = lang

    async def _request(self, endpoint: str, *, static: bool = False) -> Dict[str, Any]:
        """
        A helper function to make requests to the API.

        Parameters
        ----------
        endpoint: :class:`str`
            The endpoint to request from.
        static: :class:`bool`
            Whether to use the static endpoint or not. Defaults to ``False``.

        Returns
        -------
        Dict[str, Any]
            The response from the API.
        """
        if static:
            url = f"{self.BASE_URL}/static/{endpoint}"
        else:
            url = f"{self.BASE_URL}/{self.lang.value}/{endpoint}"
        logging.debug(f"Requesting {url}...")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()

    async def fetch_books(self) -> List[Book]:
        """
        Fetch all books from the API.

        Returns
        -------
        List[Book]
            A list of Book objects.
        """
        data = await self._request("book")
        books = [Book(**b) for b in data["data"]["items"].values()]
        return books

    async def fetch_book_detail(self, id: int) -> BookDetail:
        """
        Fetch a book's detail from the API.

        Parameters
        ----------
        id: :class:`int`
            The ID of the book to fetch.

        Returns
        -------
        BookDetail
            A BookDetail object.
        """
        data = await self._request(f"book/{id}")
        book = BookDetail(**data["data"])
        return book

    async def fetch_characters(self) -> List[Character]:
        """
        Fetch all characters from the API.

        Returns
        -------
        List[Character]
            A list of Character objects.
        """
        data = await self._request("avatar")
        characters = [Character(**c) for c in data["data"]["items"].values()]
        return characters

    async def fetch_character_detail(self, id: int) -> CharacterDetail:
        """
        Fetch a character's detail from the API.

        Parameters
        ----------
        id: :class:`int`
            The ID of the character to fetch.

        Returns
        -------
        CharacterDetail
            A CharacterDetail object.
        """
        data = await self._request(f"avatar/{id}")
        character = CharacterDetail(**data["data"])
        return character

    async def fetch_items(self) -> List[Item]:
        """
        Fetch all items from the API.

        Returns
        -------
        List[Item]
            A list of Item objects.
        """
        data = await self._request("item")
        items = [Item(**i) for i in data["data"]["items"].values()]
        return items

    async def fetch_item_detail(self, id: int) -> ItemDetail:
        """
        Fetch an item's detail from the API.

        Parameters
        ----------
        id: :class:`int`
            The ID of the item to fetch.

        Returns
        -------
        ItemDetail
            An ItemDetail object.
        """
        data = await self._request(f"item/{id}")
        item = ItemDetail(**data["data"])
        return item

    async def fetch_light_cones(self) -> List[LightCone]:
        """
        Fetch all light cones from the API.

        Returns
        -------
        List[LightCone]
            A list of LightCone objects.
        """
        data = await self._request("equipment")
        light_cones = [LightCone(**lc) for lc in data["data"]["items"].values()]
        return light_cones

    async def fetch_light_cone_detail(self, id: int) -> LightConeDetail:
        """
        Fetch a light cone's detail from the API.

        Parameters
        ----------
        id: :class:`int`
            The ID of the light cone to fetch.

        Returns
        -------
        LightConeDetail
            A LightConeDetail object.
        """
        data = await self._request(f"equipment/{id}")
        light_cone = LightConeDetail(**data["data"])
        return light_cone

    async def fetch_messages(self) -> List[Message]:
        """
        Fetch all messages from the API.

        Returns
        -------
        List[Message]
            A list of Message objects.
        """
        data = await self._request("message")
        messages = [Message(**m) for m in data["data"]["items"].values()]
        return messages

    async def fetch_message_types(self) -> Dict[str, str]:
        """
        Fetch all message types from the API.

        Returns
        -------
        List[str]
            A list of message types.
        """
        data = await self._request("message")
        return data["data"]["types"]

    async def fetch_relic_sets(self) -> List[RelicSet]:
        """
        Fetch all relic sets from the API.

        Returns
        -------
        List[RelicSet]
            A list of RelicSet objects.
        """
        data = await self._request("relic")
        relics = [RelicSet(**r) for r in data["data"]["items"].values()]
        return relics

    async def fetch_relic_set_detail(self, id: int) -> RelicSetDetail:
        """
        Fetch a relic set's detail from the API.

        Parameters
        ----------
        id: :class:`int`
            The ID of the relic set to fetch.

        Returns
        -------
        RelicSetDetail
            A RelicSetDetail object.
        """
        logging.debug(f"Fetching relic set detail for ID {id}")
        data = await self._request(f"relic/{id}")
        relic = RelicSetDetail(**data["data"])
        return relic

    async def fetch_change_logs(self) -> List[ChangeLog]:
        """
        Fetch change logs from the API.

        Returns
        -------
        List[ChangeLog]
            A list of ChangeLog objects.
        """
        data = await self._request("changelog", static=True)
        change_logs: List[ChangeLog] = []
        for id, log in data["data"].items():
            change_logs.append(ChangeLog(id=int(id), **log))
        return change_logs