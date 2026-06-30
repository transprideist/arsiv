from pathlib import Path
from bs4 import BeautifulSoup

DIST = Path(".")

TR_AY_SIRASI = {
    "Ocak": 1,
    "Şubat": 2,
    "Mart": 3,
    "Nisan": 4,
    "Mayıs": 5,
    "Haziran": 6,
    "Temmuz": 7,
    "Ağustos": 8,
    "Eylül": 9,
    "Ekim": 10,
    "Kasım": 11,
    "Aralık": 12,
}

for year_dir in DIST.iterdir():
    if not year_dir.is_dir():
        continue
    index_file = year_dir / "index.html"
    if not index_file.exists():
        continue

    soup = BeautifulSoup(index_file.read_text(encoding="utf-8"), "html.parser")
    grid = soup.select_one(".grid")
    if not grid:
        continue

    cards = grid.select("a.month-card")
    cards_sorted = sorted(
        cards,
        key=lambda a: TR_AY_SIRASI.get(
            (a.select_one("h2").get_text(strip=True) if a.select_one("h2") else ""),
            99
        )
    )

    grid.clear()
    for card in cards_sorted:
        grid.append(card)

    index_file.write_text(str(soup), encoding="utf-8")

root_index = DIST / "index.html"
if root_index.exists():
    soup = BeautifulSoup(root_index.read_text(encoding="utf-8"), "html.parser")
    grid = soup.select_one(".grid")
    if grid:
        cards = grid.select("a.year-card")
        cards_sorted = sorted(
            cards,
            key=lambda a: int(a.select_one("h2").get_text(strip=True))
        )
        grid.clear()
        for card in cards_sorted:
            grid.append(card)
        root_index.write_text(str(soup), encoding="utf-8")

print("indexler düzeldi")
