# yatta-py

## Introduction

yatta-py is an async API wrapper for [Project Yatta](https://sr.yatta.moe/) written in Python.  
Project Yatta is a beautiful website that displays Honkai: Star Rail game data.  
Developing something for Hoyoverse games? You might be interested in [other API wrappers](https://github.com/seriaati#api-wrappers) written by me.

> Note: I am not the developer of Project Yatta.

### Features

- Fully typed.
- Fully asynchronous by using `aiofiles`, `aiohttp`, and `asyncio`, suitable for Discord bots.
- Provides direct icon URLs.
- Supports Python 3.11+.
- Supports all game languages.
- Supports persistent caching using SQLite.
- Supports [Pydantic V2](https://github.com/pydantic/pydantic), this also means full autocomplete support.

## Installation

```bash
# poetry
poetry add yatta-py

# pip
pip install yatta-py
```

## Quick Example

```py
import yatta
import asyncio

async def main() -> None:
    async with yatta.YattaAPI(yatta.Language.CHT) as client:
        await client.fetch_characters()

asyncio.run(main())
```

## Getting Started

Read the [wiki](https://github.com/seriaati/yatta/wiki) to learn more about on how to use this wrapper.

## Questions, Issues, Feedback, Contributions

Whether you want to make any bug reports, feature requests, or contribute to the wrapper, simply open an issue or pull request in this repository.  
If GitHub is not your type, you can find me on [Discord](https://discord.com/invite/b22kMKuwbS), my username is @seria_ati.
