import asyncio
from pathlib import Path
import time

from telethon import TelegramClient

from config import API_HASH, API_ID, PREMIUM_ONLY, THREADS
from src.files import get_gifts_urls, write_gifts
from src.web import get_gift_info


client = TelegramClient(Path("sessions", "account"), API_ID, API_HASH)
sem = asyncio.Semaphore(THREADS)
results = []


def setup_config():
    results = Path("results")
    if not results.exists():
        results.mkdir()
    sessions = Path("sessions")
    if not sessions.exists():
        sessions.mkdir()
    gifts_file = Path("gifts.txt")
    if not gifts_file.exists():
        gifts_file.touch()


async def parser(gift_url: str):
    async with sem:
        data = await get_gift_info(gift_url)
        slug = gift_url.split("/")[-1]
        owner_url = data.get("owner_url", None)
        if not owner_url:
            return

        entity = await client.get_entity(owner_url)
        if not entity:
            return
        print(
            f"[{slug}]\tUsername: @{entity.username}\tPremium: {entity.premium}"
        )
        if (not entity.premium) and PREMIUM_ONLY:
            return
        if not entity.username:
            return
        results.append(
            f"{entity.first_name or ''} {entity.last_name or ''}https://t.me/{entity.username}"
        )


async def main():
    setup_config()
    gifts = get_gifts_urls()
    if not gifts:
        return print("Подарки не найдены в файле `gifts.txt`")

    try:
        await client.start()

        tasks = []
        for gift in gifts:
            tasks.append(asyncio.create_task(parser(gift)))
        await asyncio.gather(*tasks)

        result_file_name = "users_premium" if PREMIUM_ONLY else "users"
        result_file_name += f"_{int(time.time())}.txt"
        write_gifts(results, Path("results", result_file_name))
        print(f"Записано {len(results)} строк в файл `{result_file_name}`")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
