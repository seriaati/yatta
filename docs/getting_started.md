# Getting Started

## Installation

```bash
pip install yatta-py
```

## Usage

Every API call goes through the `YattaAPI` class. You can see more details in the [API Reference](./client.md#yatta.client.YattaAPI).

```py
import yatta

async with yatta.YattaAPI(yatta.Language.CHT) as api:
    characters = await api.fetch_characters()
    print(characters)
```

Overall, it's pretty straightforward. You can find all the available methods in the [API Reference](./client.md#yatta.client.YattaAPI).

## Tips

### Starting and Closing the Client Properly

Remember to call `start()` and `close()` or use `async with` to ensure proper connection management.

```py
import yatta

async with yatta.YattaAPI() as api:
    ...

# OR
api = yatta.YattaAPI()
await api.start()
...
await api.close()
```

### Finding Model Attributes

Refer to the [Models](./models.md) section for a list of all available models and their attributes.

### Catching Errors

Refer to the [Exceptions](./exceptions.md) section for a list of all available exceptions, catch them with `try/except` blocks.

```py
import yatta

async with yatta.YattaAPI() as api:
    try:
        await api.fetch_character(0)
    except yatta.exceptions.DataNotFoundError:
        print("Character does not exist.")
```
