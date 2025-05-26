import asyncio
from pathlib import Path
from telethon import TelegramClient

from config import API_ID, API_HASH


async def fetch_clients(
    sessions_path: str | Path = Path("sessions"),
) -> list[TelegramClient]:
    sessions_path = Path(sessions_path)
    if not sessions_path.exists():
        raise FileNotFoundError(
            f"Sessions path '{sessions_path}' does not exist."
        )

    tasks_clients = []
    for session_file in sessions_path.glob("*.session"):
        client = TelegramClient(session_file, api_id=API_ID, api_hash=API_HASH)
        tasks_clients.append(asyncio.create_task(start_client(client)))
    clients = await asyncio.gather(*tasks_clients)
    clients = [client for client in clients if client is not None]

    return clients


async def start_client(client: TelegramClient) -> None:
    if not client.is_connected():
        await client.connect()
    is_authorized = await client.is_user_authorized()
    print(
        f"Аккаунт `{client.session.filename.split('\\')[-1]}` {'авторизован' if is_authorized else 'не авторизован'}"
    )
    return client if is_authorized else None


async def disconnect_clients(
    clients: list[TelegramClient],
) -> None:
    for client in clients:
        if not client or not client.is_connected():
            continue
        await client.disconnect()
