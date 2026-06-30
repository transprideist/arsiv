from pathlib import Path
import re

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

def sort_month_cards(html):
    pattern = re.compile(r'(<a class="month-card".*?</a>)', re.DOTALL)
    cards = pattern.findall(html)

    def key(card):
        m = re.search(r"<h2>(.*?)</h2>", card, re.DOTALL)
        month = m.group(1).strip() if m else ""
        return TR_AY_SIRASI.get(month, 99)

    sorted_cards = sorted(cards, key=key)

    if cards:
        first = cards[0]
        last = cards[-1]
        start = html.find(first)
        end = html.rfind(last) + len(last)
        html = html[:start] + "".join(sorted_cards) + html[end:]
    return html

def sort_year_cards(html):
    pattern = re.compile(r'(<a class="year-card".*?</a>)', re.DOTALL)
    cards = pattern.findall(html)

    def key(card):
        m = re.search(r"<h2>(\d+)</h2>", card, re.DOTALL)
        year = int(m.group(1)) if m else 9999
        return year

    sorted_cards = sorted(cards, key=key)

    if cards:
        first = cards[0]
        last = cards[-1]
        start = html.find(first)
        end = html.rfind(last) + len(last)
        html = html[:start] + "".join(sorted_cards) + html[end:]
    return html

dist = Path(".")

for year_dir in dist.iterdir():
    if year_dir.is_dir():
        index_file = year_dir / "index.html"
        if index_file.exists():
            html = index_file.read_text(encoding="utf-8")
            html = sort_month_cards(html)
            index_file.write_text(html, encoding="utf-8")

root_index = dist / "index.html"
if root_index.exists():
    html = root_index.read_text(encoding="utf-8")
    html = sort_year_cards(html)
    root_index.write_text(html, encoding="utf-8")

print("indexler düzeldi")
