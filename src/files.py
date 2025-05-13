from pathlib import Path


def get_gifts_urls(file_path: Path | str = Path("gifts.txt")) -> list[str]:
    with open(file_path, encoding="utf-8") as file:
        return [
            line.strip() for line in file.readlines() if line.strip() != ""
        ]


def write_gifts(text: list[str], file_path: Path | str):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(text))
