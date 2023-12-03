import asyncio
from typing import Any, Awaitable, Callable, List, Union

import pytest
import pytest_asyncio

import yatta


async def fetch_ids(
    fetch_func: Callable[[], Awaitable[List[Any]]]
) -> List[Union[int, str]]:
    items = await fetch_func()
    return [item.id for item in items]


@pytest.fixture(scope="module")
def api_client() -> yatta.YattaAPI:
    return yatta.YattaAPI()


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def _fetch_ids(api_client: yatta.YattaAPI) -> List[List[Union[int, str]]]:
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
async def test_books(api_client: yatta.YattaAPI, _fetch_ids: List[List[int]]):
    book_ids = _fetch_ids[0]
    for book_id in book_ids:
        await api_client.fetch_book_detail(book_id)


@pytest.mark.asyncio
async def test_characters(api_client: yatta.YattaAPI, _fetch_ids: List[List[int]]):
    character_ids = _fetch_ids[1]
    for character_id in character_ids:
        await api_client.fetch_character_detail(character_id)


@pytest.mark.asyncio
async def test_items(api_client: yatta.YattaAPI, _fetch_ids: List[List[int]]):
    item_ids = _fetch_ids[2]
    for item_id in item_ids:
        await api_client.fetch_item_detail(item_id)


@pytest.mark.asyncio
async def test_light_cones(api_client: yatta.YattaAPI, _fetch_ids: List[List[int]]):
    light_cone_ids = _fetch_ids[3]
    for light_cone_id in light_cone_ids:
        await api_client.fetch_light_cone_detail(light_cone_id)


@pytest.mark.asyncio
async def test_relic_sets(api_client: yatta.YattaAPI, _fetch_ids: List[List[int]]):
    relic_ids = _fetch_ids[4]
    for relic_id in relic_ids:
        await api_client.fetch_relic_set_detail(relic_id)


@pytest.mark.asyncio
async def test_messages(api_client: yatta.YattaAPI):
    await api_client.fetch_messages()


@pytest.mark.asyncio
async def test_change_log(api_client: yatta.YattaAPI):
    await api_client.fetch_change_logs()


@pytest.mark.asyncio
async def test_invalid_id(api_client: yatta.YattaAPI):
    with pytest.raises(yatta.DataNotFound):
        await api_client.fetch_character_detail(0)
