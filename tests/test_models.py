import asyncio
from typing import TYPE_CHECKING, Any

import pytest
import pytest_asyncio

import yatta

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Generator


async def fetch_ids(fetch_func: "Callable[[], Awaitable[list[Any]]]") -> list[int | str]:
    items = await fetch_func()
    return [item.id for item in items]


@pytest.fixture(scope="module")
def api_client() -> yatta.YattaAPI:
    return yatta.YattaAPI()


@pytest.fixture(scope="module")
def event_loop() -> "Generator[asyncio.AbstractEventLoop, Any, None]":
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def _fetch_ids(api_client: yatta.YattaAPI) -> list[list[int | str]]:
    fetch_funcs = [
        api_client.fetch_books,
        api_client.fetch_characters,
        api_client.fetch_items,
        api_client.fetch_light_cones,
        api_client.fetch_relic_sets,
    ]
    ids = await asyncio.gather(*(fetch_ids(func) for func in fetch_funcs))
    return ids


@pytest.mark.asyncio
async def test_books(api_client: yatta.YattaAPI, _fetch_ids: list[list[int]]) -> None:
    book_ids = _fetch_ids[0]
    for book_id in book_ids:
        await api_client.fetch_book_detail(book_id)


@pytest.mark.asyncio
async def test_characters(api_client: yatta.YattaAPI, _fetch_ids: list[list[int]]) -> None:
    character_ids = _fetch_ids[1]
    for character_id in character_ids:
        await api_client.fetch_character_detail(character_id)


@pytest.mark.asyncio
async def test_items(api_client: yatta.YattaAPI, _fetch_ids: list[list[int]]) -> None:
    item_ids = _fetch_ids[2]
    for item_id in item_ids:
        await api_client.fetch_item_detail(item_id)


@pytest.mark.asyncio
async def test_light_cones(api_client: yatta.YattaAPI, _fetch_ids: list[list[int]]) -> None:
    light_cone_ids = _fetch_ids[3]
    for light_cone_id in light_cone_ids:
        await api_client.fetch_light_cone_detail(light_cone_id)


@pytest.mark.asyncio
async def test_relic_sets(api_client: yatta.YattaAPI, _fetch_ids: list[list[int]]) -> None:
    relic_ids = _fetch_ids[4]
    for relic_id in relic_ids:
        await api_client.fetch_relic_set_detail(relic_id)


@pytest.mark.asyncio
async def test_messages(api_client: yatta.YattaAPI) -> None:
    await api_client.fetch_messages()


@pytest.mark.asyncio
async def test_change_log(api_client: yatta.YattaAPI) -> None:
    await api_client.fetch_changelogs()


@pytest.mark.asyncio
async def test_invalid_id(api_client: yatta.YattaAPI) -> None:
    with pytest.raises(yatta.DataNotFoundError):
        await api_client.fetch_character_detail(0)


@pytest.mark.asyncio
async def test_manual_avatar(api_client: yatta.YattaAPI) -> None:
    await api_client.fetch_manual_avatar()
