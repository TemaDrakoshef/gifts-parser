from bs4 import BeautifulSoup
from httpx import AsyncClient


async def get_gift_info(gift_url: str) -> dict[str, str | None]:
    """Fetches and parses gift information from the provided URL."""
    async with AsyncClient() as client:
        response = await client.get(gift_url)
        if response.status_code != 200:
            return {}

        soup = BeautifulSoup(response.text, "lxml")
        data = {
            "owner_url": None,
            "model": None,
            "backdrop": None,
            "symbol": None,
            "quantity": None,
        }

        table = soup.find("table", class_="tgme_gift_table")
        if not table:
            return data

        for row in table.find_all("tr"):
            th_elem = row.find("th")
            td_elem = row.find("td")

            if not th_elem or not td_elem:
                continue

            key = th_elem.get_text(strip=True)

            if key == "Owner":
                link = td_elem.find("a")
                if link and link.has_attr("href"):
                    data["owner_url"] = link["href"]

            elif key in {"Model", "Backdrop", "Symbol"}:
                content = []
                for elem in td_elem.contents:
                    if elem.name == "mark":
                        break
                    if isinstance(elem, str):
                        content.append(elem.strip())
                    else:
                        content.append(elem.get_text(strip=True))
                data[key.lower()] = " ".join(content).strip() or None

            elif key == "Quantity":
                quantity_text = td_elem.get_text(strip=True).replace(
                    "\xa0", " "
                )
                data["quantity"] = quantity_text or None

        return data
