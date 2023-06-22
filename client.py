from enum import Enum
from typing import Any, Dict, Final, List

import aiohttp

from .models import Book, Character, Item, LightCone, Message, Relic


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

    async def _request(self, endpoint: str) -> Dict[str, Any]:
        """
        A helper function to make requests to the API.

        Parameters
        ----------
        endpoint: :class:`str`
            The endpoint to request from.

        Returns
        -------
        Dict[str, Any]
            The response from the API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/{self.lang.value}/{endpoint}"
            ) as resp:
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
        books = [Book(**b) for b in data["data"]["items"]]
        return books

    async def fetch_characters(self) -> List[Character]:
        """
        Fetch all characters from the API.

        Returns
        -------
        List[Character]
            A list of Character objects.
        """
        data = await self._request("avatar")
        characters = [Character(**c) for c in data["data"]["items"]]
        return characters

    async def fetch_character_ids(self) -> List[int]:
        """
        Fetch all character ids from the API.

        Returns
        -------
        List[int]
            A list of character ids.
        """
        data = await self._request("avatar")
        return [int(c) for c in data["data"]["items"]]

    async def fetch_items(self) -> List[Item]:
        """
        Fetch all items from the API.

        Returns
        -------
        List[Item]
            A list of Item objects.
        """
        data = await self._request("item")
        items = [Item(**i) for i in data["data"]["items"]]
        return items

    async def fetch_light_cones(self) -> List[LightCone]:
        """
        Fetch all light cones from the API.

        Returns
        -------
        List[LightCone]
            A list of LightCone objects.
        """
        data = await self._request("equipment")
        light_cones = [LightCone(**lc) for lc in data["data"]["items"]]
        return light_cones

    async def fetch_messages(self) -> List[Message]:
        """
        Fetch all messages from the API.

        Returns
        -------
        List[Message]
            A list of Message objects.
        """
        data = await self._request("message")
        messages = [Message(**m) for m in data["data"]["items"]]
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

    async def fetch_relics(self) -> List[Relic]:
        """
        Fetch all relics from the API.

        Returns
        -------
        List[Relic]
            A list of Relic objects.
        """
        data = await self._request("relic")
        relics = [Relic(**r) for r in data["data"]["items"]]
        return relics
