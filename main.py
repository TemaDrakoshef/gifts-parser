import asyncio
from pathlib import Path

from src.files import get_gifts_urls
from src.web import get_gift_info


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


async def main():
    setup_config()
    gifts = get_gifts_urls()
    if not gifts:
        return print("No gifts found in `gifts.txt`")

    for gift in gifts:
        data = await get_gift_info(gift)
        slug = gift.split("/")[-1]
        print(slug, data.get("owner_url"))


if __name__ == "__main__":
    asyncio.run(main())
