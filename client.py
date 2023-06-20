from typing import Any, Dict, Final, List

import aiohttp

from enums import Language
from models.character import Character


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
        return [c["id"] for c in data["data"]["items"]]
