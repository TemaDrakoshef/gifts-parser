# Telegram Gifts Parser

This script is designed to parse Telegram gift links to extract the sender's user information. It uses multiple Telegram accounts to process links efficiently and avoid API rate limits.

## 🔥 Features

- **User Info Extraction**: Gathers usernames, full names, and premium status from gift links.
- **Multi-Account Support**: Rotates through multiple Telegram accounts to prevent rate-limiting and blocks.
- **Asynchronous Processing**: Utilizes `asyncio` for fast and concurrent link checking.
- **Premium Filter**: An option to save only users with a Telegram Premium subscription.
- **Simple Setup**: Easy to configure with your Telegram accounts and gift links.

## 💾 Stack

This project is built with Python and relies on the following key libraries:

- **Telethon**: A Python library to interact with the Telegram API.
- **HTTPX**: For asynchronous HTTP requests to get gift info.

## ⚙️ Setup and Configuration

### 1. Add Telegram Sessions

This script requires valid Telethon session files to log into Telegram accounts.

1.  Create a `sessions` folder in the project's root directory.
2.  Add your `.session` files to this folder. If you don't have any, you can generate them using a separate script with Telethon. The script will automatically detect and use all session files inside the `sessions` directory.

```
project-root/
├── sessions/
│   ├── account1.session
│   └── account2.session
├── main.py
└── ...
```

### 2. Add Gift Links

1.  Open the `gifts.txt` file (it will be created automatically on the first run if it doesn't exist).
2.  Paste the Telegram gift links you want to parse, with each link on a new line.

**Example `gifts.txt`:**

```
https://t.me/nft/xxxxxxxxxxxxxx
https://t.me/nft/yyyyyyyyyyyyyy
```

```
https://t.me/nft/LunarSnake-90053
https://t.me/nft/LunarSnake-90054
```

## 🚀 Installation and Launch

### Using `pip` (Standard)

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the script:
    ```bash
    python main.py
    ```

### Using `uv`

1.  Install dependencies:
    ```bash
    uv sync
    ```
2.  Run the script:
    ```bash
    uv run python ./main.py
    ```

## 📝 Output

The script will save the extracted user information into a `.txt` file inside the `results` directory. The filename will be generated based on the current timestamp and whether the `PREMIUM_ONLY` filter was active (e.g., `users_1678886400.txt` or `users_premium_1678886400.txt`).
