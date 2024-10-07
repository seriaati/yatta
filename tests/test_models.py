from __future__ import annotations

import pytest

import yatta


@pytest.mark.asyncio
async def test_books() -> None:
    async with yatta.YattaAPI() as api:
        books = await api.fetch_books()
        for book in books:
            await api.fetch_book_detail(book.id)


@pytest.mark.asyncio
async def test_characters() -> None:
    async with yatta.YattaAPI() as api:
        characters = await api.fetch_characters()
        for character in characters:
            await api.fetch_character_detail(character.id)


@pytest.mark.asyncio
async def test_items() -> None:
    async with yatta.YattaAPI() as api:
        items = await api.fetch_items()
        for item in items:
            await api.fetch_item_detail(item.id)


@pytest.mark.asyncio
async def test_light_cones() -> None:
    async with yatta.YattaAPI() as api:
        light_cones = await api.fetch_light_cones()
        for light_cone in light_cones:
            await api.fetch_light_cone_detail(light_cone.id)


@pytest.mark.asyncio
async def test_relic_sets() -> None:
    async with yatta.YattaAPI() as api:
        relic_sets = await api.fetch_relic_sets()
        for relic_set in relic_sets:
            await api.fetch_relic_set_detail(relic_set.id)


@pytest.mark.asyncio
async def test_messages() -> None:
    async with yatta.YattaAPI() as api:
        await api.fetch_messages()


@pytest.mark.asyncio
async def test_change_log() -> None:
    async with yatta.YattaAPI() as api:
        await api.fetch_changelogs()


@pytest.mark.asyncio
async def test_invalid_id() -> None:
    with pytest.raises(yatta.DataNotFoundError):
        async with yatta.YattaAPI() as api:
            await api.fetch_character_detail(0)


@pytest.mark.asyncio
async def test_manual_avatar() -> None:
    async with yatta.YattaAPI() as api:
        await api.fetch_manual_avatar()
