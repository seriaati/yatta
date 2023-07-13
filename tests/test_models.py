import pytest

import yatta


@pytest.mark.asyncio
async def test_books():
    client = yatta.YattaAPI()
    books = await client.fetch_books()
    for book in books:
        await client.fetch_book_detail(book.id)


@pytest.mark.asyncio
async def test_characters():
    client = yatta.YattaAPI()
    characters = await client.fetch_characters()
    for character in characters:
        await client.fetch_character_detail(character.id)


@pytest.mark.asyncio
async def test_items():
    client = yatta.YattaAPI()
    items = await client.fetch_items()
    for item in items:
        await client.fetch_item_detail(item.id)


@pytest.mark.asyncio
async def test_light_cones():
    client = yatta.YattaAPI()
    light_cones = await client.fetch_light_cones()
    for light_cone in light_cones:
        await client.fetch_light_cone_detail(light_cone.id)


@pytest.mark.asyncio
async def test_messages():
    client = yatta.YattaAPI()
    await client.fetch_messages()


@pytest.mark.asyncio
async def test_relics():
    client = yatta.YattaAPI()
    relics = await client.fetch_relic_sets()
    for relic in relics:
        await client.fetch_relic_set_detail(relic.id)


@pytest.mark.asyncio
async def test_change_log():
    client = yatta.YattaAPI()
    await client.fetch_change_logs()
