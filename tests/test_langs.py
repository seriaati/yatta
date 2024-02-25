import pytest

import yatta


@pytest.mark.asyncio
async def test_langs() -> None:
    client = yatta.YattaAPI()
    for lang in yatta.Language:
        client.lang = lang
        await client.fetch_characters()
