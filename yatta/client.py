from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Final, Self

import aiofiles
import anyio
from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession
from loguru import logger

from yatta.enums import Language

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
    from aiohttp_client_cache import CacheBackend

__all__ = ("YattaAPI",)

CACHE_PATH = anyio.Path("./.cache/yatta")


class YattaAPI:
    """The main class to interact with the Project Yatta API.

    Provide asynchronous methods to fetch various game data like characters,
    light cones, relics, items, etc. Support caching via aiohttp-client-cache.

    Args:
        lang: The language to use for API responses. Defaults to Language.EN.
        cache_ttl: The time-to-live for the cache in seconds. Defaults to 3600 (1 hour).
        headers: Optional dictionary of headers to include in requests.
        session: Optional existing aiohttp.ClientSession to use. If None, a new
                 CachedSession will be created.
        cache_backend: Optional CacheBackend instance for caching. If None,
                       a SQLite backend will be used with a default path.
    """

    BASE_URL: Final[str] = "https://sr.yatta.moe/api/v2"

    def __init__(
        self,
        *,
        lang: Language = Language.EN,
        cache_ttl: int = 3600,
        headers: dict[str, Any] | None = None,
        session: aiohttp.ClientSession | None = None,
        cache_backend: CacheBackend | None = None,
    ) -> None:
        self.lang = lang
        self.cache_ttl = cache_ttl

        self._session = session
        self._cache = cache_backend or SQLiteBackend(
            "./.cache/yatta/aiohttp-cache.db", expire_after=cache_ttl
        )
        self._headers = headers or {"User-Agent": "yatta-py"}

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        await self.close()

    async def _request(
        self, endpoint: str, *, static: bool = False, use_cache: bool
    ) -> dict[str, Any]:
        """Make an asynchronous request to the specified API endpoint.

        Handle adding the language path, version hash, and error checking.

        Args:
            endpoint: The API endpoint path (e.g., "avatar", "equipment/12345").
            static: If True, request the static endpoint without language prefix. Defaults to False.
            use_cache: Whether to allow the request to be served from cache.

        Returns:
            The JSON response data as a dictionary.

        Raises:
            RuntimeError: If the session hasn't been started via `start()`.
            DataNotFoundError: If the API returns a 404 status.
            ConnectionTimeoutError: If the API returns a 522 status.
            YattaAPIError: For other non-200 status codes.
        """
        if self._session is None:
            msg = f"Call `{self.__class__.__name__}.start` before making requests."
            raise RuntimeError(msg)

        if static:
            url = f"{self.BASE_URL}/static/{endpoint}"
        else:
            url = f"{self.BASE_URL}/{self.lang.value}/{endpoint}"

        if endpoint != "version":
            version = await self._get_version()
            if version is None:
                logger.debug("Version not found or outdated, fetching latest version.")
                version = await self.fetch_latest_version()
                await self._save_version(version)
            url += f"?vh={version}"

        logger.debug(f"Requesting {url}")

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
        """Raise appropriate exceptions based on HTTP status code.

        Args:
            code: The HTTP status code received from the API.

        Raises:
            DataNotFoundError: For 404 errors.
            ConnectionTimeoutError: For 522 errors.
            YattaAPIError: For other non-200 errors.
        """
        match code:
            case 404:
                raise DataNotFoundError
            case 522:
                raise ConnectionTimeoutError
            case _:
                raise YattaAPIError(code)

    async def start(self) -> None:
        """Initialize the internal aiohttp session.

        Must be called before making any API requests if not using `async with`.
        """
        self._session = self._session or CachedSession(headers=self._headers, cache=self._cache)

    async def close(self) -> None:
        """Close the internal aiohttp session.

        Should be called to release resources if not using `async with`.
        """
        if self._session is not None:
            await self._session.close()

    async def fetch_books(self, use_cache: bool = True) -> list[Book]:
        """Fetch a list of all available books.

        Args:
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A list of Book objects.

        Raises:
            DataNotFoundError: If the book list endpoint returns 404.
            YattaAPIError: For other API errors.
        """
        data = await self._request("book", use_cache=use_cache)
        return [Book(**b) for b in data["data"]["items"].values()]

    async def fetch_book_detail(self, id: int, use_cache: bool = True) -> BookDetail:
        """Fetch detailed information for a specific book.

        Args:
            id: The unique identifier of the book.
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A BookDetail object containing detailed book information.

        Raises:
            DataNotFoundError: If no book with the given ID is found.
            YattaAPIError: For other API errors.
        """
        data = await self._request(f"book/{id}", use_cache=use_cache)
        return BookDetail(**data["data"])

    async def fetch_characters(self, use_cache: bool = True) -> list[Character]:
        """Fetch a list of all available characters.

        Args:
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A list of Character objects.

        Raises:
            DataNotFoundError: If the character list endpoint returns 404.
            YattaAPIError: For other API errors.
        """
        data = await self._request("avatar", use_cache=use_cache)
        return [Character(**c) for c in data["data"]["items"].values()]

    async def fetch_character_detail(self, id: int, use_cache: bool = True) -> CharacterDetail:
        """Fetch detailed information for a specific character.

        Args:
            id: The unique identifier of the character.
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A CharacterDetail object containing detailed character information.

        Raises:
            DataNotFoundError: If no character with the given ID is found.
            YattaAPIError: For other API errors.
        """
        data = await self._request(f"avatar/{id}", use_cache=use_cache)
        return CharacterDetail(**data["data"])

    async def fetch_items(self, use_cache: bool = True) -> list[Item]:
        """Fetch a list of all available items.

        Args:
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A list of Item objects.

        Raises:
            DataNotFoundError: If the item list endpoint returns 404.
            YattaAPIError: For other API errors.
        """
        data = await self._request("item", use_cache=use_cache)
        return [Item(**i) for i in data["data"]["items"].values()]

    async def fetch_item_detail(self, id: int, use_cache: bool = True) -> ItemDetail:
        """Fetch detailed information for a specific item.

        Args:
            id: The unique identifier of the item.
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            An ItemDetail object containing detailed item information.

        Raises:
            DataNotFoundError: If no item with the given ID is found.
            YattaAPIError: For other API errors.
        """
        data = await self._request(f"item/{id}", use_cache=use_cache)
        return ItemDetail(**data["data"])

    async def fetch_light_cones(self, use_cache: bool = True) -> list[LightCone]:
        """Fetch a list of all available light cones.

        Args:
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A list of LightCone objects.

        Raises:
            DataNotFoundError: If the light cone list endpoint returns 404.
            YattaAPIError: For other API errors.
        """
        data = await self._request("equipment", use_cache=use_cache)
        return [LightCone(**lc) for lc in data["data"]["items"].values()]

    async def fetch_light_cone_detail(self, id: int, use_cache: bool = True) -> LightConeDetail:
        """Fetch detailed information for a specific light cone.

        Args:
            id: The unique identifier of the light cone.
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A LightConeDetail object containing detailed light cone information.

        Raises:
            DataNotFoundError: If no light cone with the given ID is found.
            YattaAPIError: For other API errors.
        """
        data = await self._request(f"equipment/{id}", use_cache=use_cache)
        return LightConeDetail(**data["data"])

    async def fetch_messages(self, use_cache: bool = True) -> list[Message]:
        """Fetch a list of all available message threads.

        Args:
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A list of Message objects.

        Raises:
            DataNotFoundError: If the message list endpoint returns 404.
            YattaAPIError: For other API errors.
        """
        data = await self._request("message", use_cache=use_cache)
        return [Message(**m) for m in data["data"]["items"].values()]

    async def fetch_message_types(self, use_cache: bool = True) -> dict[str, str]:
        """Fetch a mapping of message type IDs to their names.

        Args:
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A dictionary where keys are message type IDs (as strings) and values are type names.

        Raises:
            DataNotFoundError: If the message endpoint returns 404.
            YattaAPIError: For other API errors.
        """
        data = await self._request("message", use_cache=use_cache)
        return data["data"]["types"]

    async def fetch_relic_sets(self, use_cache: bool = True) -> list[RelicSet]:
        """Fetch a list of all available relic sets.

        Args:
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A list of RelicSet objects.

        Raises:
            DataNotFoundError: If the relic list endpoint returns 404.
            YattaAPIError: For other API errors.
        """
        data = await self._request("relic", use_cache=use_cache)
        return [RelicSet(**r) for r in data["data"]["items"].values()]

    async def fetch_relic_set_detail(self, id: int, use_cache: bool = True) -> RelicSetDetail:
        """Fetch detailed information for a specific relic set.

        Args:
            id: The unique identifier of the relic set.
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A RelicSetDetail object containing detailed relic set information.

        Raises:
            DataNotFoundError: If no relic set with the given ID is found.
            YattaAPIError: For other API errors.
        """
        data = await self._request(f"relic/{id}", use_cache=use_cache)
        return RelicSetDetail(**data["data"])

    async def fetch_changelogs(self, use_cache: bool = True) -> list[Changelog]:
        """Fetch a list of all available changelogs.

        Args:
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A list of Changelog objects.

        Raises:
            DataNotFoundError: If the changelog endpoint returns 404.
            YattaAPIError: For other API errors.
        """
        data = await self._request("changelog", static=True, use_cache=use_cache)
        change_logs: list[Changelog] = []
        for changelog_id, log in data["data"].items():
            change_logs.append(Changelog(id=int(changelog_id), **log))
        return change_logs

    async def fetch_manual_avatar(self, use_cache: bool = True) -> dict[str, dict[str, str]]:
        """Fetch manual avatar data, typically used for stat mappings.

        Args:
            use_cache: Whether to allow the response to be served from cache. Defaults to True.

        Returns:
            A dictionary containing manual avatar data, often mapping stat keys to names and icons.

        Raises:
            DataNotFoundError: If the manual avatar endpoint returns 404.
            YattaAPIError: For other API errors.
        """
        data = await self._request("manualAvatar", use_cache=use_cache)
        return data["data"]

    async def _save_version(self, version: str) -> None:
        await CACHE_PATH.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(CACHE_PATH / "version.txt", "w") as f:
            await f.write(f"{version},{time.time()}")

    async def _get_version(self) -> str | None:
        try:
            async with aiofiles.open(CACHE_PATH / "version.txt") as f:
                data = await f.read()
                version, timestamp = data.split(",")
                if time.time() - float(timestamp) > 60 * 60 * 24:  # 24 hours
                    return None
                return version
        except (FileNotFoundError, ValueError):
            return None

    async def fetch_latest_version(self) -> str:
        """Fetch the latest data version hash from the API.

        This bypasses the regular cache to ensure the absolute latest version is retrieved.

        Returns:
            The latest version hash string.

        Raises:
            YattaAPIError: For API errors during the fetch.
        """
        data = await self._request("version", static=True, use_cache=False)
        return data["data"]["vh"]
