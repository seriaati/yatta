# yatta
 An async API wrapper for [hsr.yatta.top](https://hsr.yatta.top/) written in Python.  

## Features
 - Uses `async` and `await`.
 - Support caching using [diskcache](https://github.com/grantjenks/python-diskcache).
 - Supports [pydantic](https://github.com/pydantic/pydantic) V2, all of the data is parsed into pydantic models.
 - Supports the majority of the popular endpoints.

## Installing
```
# pip
pip install git+https://github.com/seriaati/yatta

# poetry
poetry add git+https://github.com/seriaati/yatta
```

## Quick Example
```py
from yatta import YattaAPI, Language

async with YattaAPI(Language.CHT) as api:
    characters = await api.fetch_characters()
    for character in characters:
        print(character.name)

    light_cones = await api.fetch_light_cones(use_cache=False)
    for light_cone in light_cones:
        print(light_cone.id)
```
