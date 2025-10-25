import asyncio
import random
import time
from pathlib import Path

from telethon import TelegramClient, errors

from config import PREMIUM_ONLY, THREADS
from src.files import get_gifts_urls, write_gifts
from src.telegram import disconnect_clients, fetch_clients
from src.utils import logo
from src.web import get_gift_info

sem = asyncio.Semaphore(THREADS)
results = []
processed_slugs = set()


def setup_config():
    """Creates necessary directories and files."""
    Path("results").mkdir(exist_ok=True)
    Path("sessions").mkdir(exist_ok=True)
    Path("gifts.txt").touch(exist_ok=True)


async def parser(client: TelegramClient, gift_url: str) -> bool:
    """
    Parses a single gift URL using the provided Telegram client.
    Returns True if successful, else False.
    """
    async with sem:
        slug = gift_url.split("/")[-1]
        if slug in processed_slugs:
            return True

        try:
            data = await get_gift_info(gift_url)
            owner_url = data.get("owner_url")
            if not owner_url:
                return True

            entity = await client.get_entity(owner_url)
            if not entity or not entity.username:
                return True

            print(
                f"[{slug}] Username: @{entity.username} Premium: {entity.premium}"
            )
            if PREMIUM_ONLY and not entity.premium:
                return True

            results.append(
                f"{entity.first_name or ''} {entity.last_name or ''}https://t.me/{entity.username}"
            )
            processed_slugs.add(slug)
            return True

        except (
            errors.FloodWaitError,
            errors.AuthKeyUnregisteredError,
            errors.UserDeactivatedError,
            errors.rpcerrorlist.AuthKeyInvalidError,
        ) as e:
            print(f"[{slug}] Аккаунт заблокирован или не авторизован: {e}")
            return False

        except Exception as e:
            print(f"[{slug}] Ошибка при парсинге: {e}")
            return True


async def main():
    """
    Main function to run the script.
    Initializes config, fetches gifts and clients, and processes gifts.
    """
    setup_config()
    gifts = get_gifts_urls()
    print(logo)
    if not gifts:
        return print("Подарки не найдены в файле `gifts.txt`")

    all_clients = await fetch_clients()
    if not all_clients:
        return print("Нет авторизованных клиентов в папке `sessions`.")
    clients = random.sample(all_clients, len(all_clients))

    try:
        gift_queue = [gift for gift in gifts]
        current_gift_index = 0

        for client in clients:
            print(f"▶ Используется аккаунт: {client.session.filename}")

            while current_gift_index < len(gift_queue):
                gift_url = gift_queue[current_gift_index]
                success = await parser(client, gift_url)

                if not success:
                    print(
                        "⚠️ Проблемы с аккаунтом, переключаюсь на следующий..."
                    )
                    break

                current_gift_index += 1

            if current_gift_index >= len(gift_queue):
                break

        if current_gift_index < len(gift_queue):
            print(
                f"❌ Не удалось обработать {len(gift_queue) - current_gift_index} подарков — закончились аккаунты."
            )
        else:
            print("✅ Все подарки обработаны.")

        result_file_name = "users_premium" if PREMIUM_ONLY else "users"
        result_file_name += f"_{int(time.time())}.txt"
        write_gifts(results, Path("results", result_file_name))
        print(f"💾 Записано {len(results)} строк в файл `{result_file_name}`")

    finally:
        await disconnect_clients(clients)


if __name__ == "__main__":
    asyncio.run(main())
