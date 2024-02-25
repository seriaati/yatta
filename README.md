# yatta
 An async API wrapper for [Project Yatta](https://yatta.top/) written in Python. Project Yatta displays Honkai Star Rail game data on a beautiful website.
 > Note: I am not the developer of Project Yatta.  

## Quick Links
Developing something for Hoyoverse games? Check out my other API wrappers:
 - [enka.py](https://github.com/seriaati/enka-py) is an Enka Network API wrapper for fetching in-game showcase.
 - [ambr](https://github.com/seriaati/ambr) is a Project Amber API wrapper for fetching Genshin Impact game data.

## Features
 - Fully typed.
 - Provides direct icon URLs.
 - Fully asynchronous by using `aiosqlite`, `aiohttp`, and `asyncio`.
 - Supports persistent caching using SQLite.
 - Supports [Pydantic V2](https://github.com/pydantic/pydantic).
 - Supports the majority of popular endpoints (create an issue if the one you need is missing).
 - 100% test coverage.

## Installing
```
# poetry
poetry add git+https://github.com/seriaati/yatta

# pip
pip install git+https://github.com/seriaati/yatta
```

## Quick Example
```py
from yatta import YattaAPI, Language

async with YattaAPI(lang=Language.CHT) as api:
    characters = await api.fetch_characters()
    for character in characters:
        print(character.name)

    light_cones = await api.fetch_light_cones(use_cache=False)
    for light_cone in light_cones:
        print(light_cone.id)
```

# Usage
## Starting and closing the client properly
To use the client properly, you can either:  
Manually call `start()` and `close()`  
```py
import yatta
import asyncio

async def main() -> None:
    api = yatta.YattaAPI()
    await api.start()
    response = await api.fetch_characters()
    await api.close()

asyncio.run(main())
```
Or use the `async with` syntax:  
```py
import yatta
import asyncio

async def main() -> None:
   async with yatta.YattaAPI() as api:
     await api.fetch_characters()

asyncio.run(main())
```
> [!IMPORTANT]  
> You ***need*** to call `start()` or the api client will not function properly; the `close()` method closes the request session and database properly.

## Client parameters
Currently, the `YattaAPI` class allows you to pass in 3 parameters:
### Language
This will affect the languages of names of weapon, character, constellations, etc. You can find all the languages [here](https://github.com/seriaati/yatta/blob/820871827fc362b8ec1011282e665ac739c0c671/yatta/client.py#L29-L42).
### Headers
Custom headers used when requesting the Yatta API, it is recommended to set a user agent, the default is `{"User-Agent": "yatta-py"}`.
### Cache TTL
Default is 3600 seconds (1 hour), the cache is evicted when this time expires. Note that setting a longer TTL might result in inconsistent data.

## Finding models' attributes
If you're using an IDE like VSCode or Pycharm, then you can see all the attributes and methods the model has in the autocomplete.
> [!TIP]
> If you're using VSCode, `alt` + `left click` on the attribute, then the IDE will bring you to the source code of this wrapper for you to see all the fields defined, most classes and methods have docstrings for you to reference to.

## Catching exceptions
If data is not found (API returns 404), then `yatta.exceptions.DataNotFoundError` will be raised.

# Questions, issues, contributions
For questions, you can contact me on [Discord](https://discord.com/users/410036441129943050) or open an [issue](https://github.com/seriaati/yatta/issues).  
To report issues with this wrapper, open an [issue](https://github.com/seriaati/yatta/issues).  
To contribute, fork this repo and submit a [pull request](https://github.com/seriaati/yatta/pulls).