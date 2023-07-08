import asyncio
import logging

from yatta import YattaAPI

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()],
)


async def main():
    yatta = YattaAPI()

    change_logs = await yatta.fetch_change_logs()
    logging.info(f"Fetched {len(change_logs)} change logs.")

    books = await yatta.fetch_books()
    logging.info(f"Fetched {len(books)} books.")
    for book in books:
        book_detail = await yatta.fetch_book_detail(book.id)
        logging.info(f"Fetched book {book_detail.name}.")

    characters = await yatta.fetch_characters()
    logging.info(f"Fetched {len(characters)} characters.")
    for character in characters:
        character_detail = await yatta.fetch_character_detail(character.id)
        logging.info(f"Fetched character {character_detail.name}.")

    items = await yatta.fetch_items()
    logging.info(f"Fetched {len(items)} items.")
    for item in items:
        item_detail = await yatta.fetch_item_detail(item.id)
        logging.info(f"Fetched item {item_detail.name}.")

    light_cones = await yatta.fetch_light_cones()
    logging.info(f"Fetched {len(light_cones)} light cones.")
    for light_cone in light_cones:
        light_cone_detail = await yatta.fetch_light_cone_detail(light_cone.id)
        logging.info(f"Fetched light cone {light_cone_detail.name}.")

    messages = await yatta.fetch_messages()
    logging.info(f"Fetched {len(messages)} messages.")

    relic_sets = await yatta.fetch_relic_sets()
    logging.info(f"Fetched {len(relic_sets)} relic sets.")
    for relic_set in relic_sets:
        relic_set_detail = await yatta.fetch_relic_set_detail(relic_set.id)
        logging.info(f"Fetched relic set {relic_set_detail.name}.")


asyncio.run(main())
