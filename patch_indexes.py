from pathlib import Path
import re

DIST = Path(".")

AY_SIRASI = {
    "January.html": 1,
    "February.html": 2,
    "March.html": 3,
    "April.html": 4,
    "May.html": 5,
    "June.html": 6,
    "July.html": 7,
    "August.html": 8,
    "September.html": 9,
    "October.html": 10,
    "November.html": 11,
    "December.html": 12,
}

def sort_cards(html, card_class, keyfunc):
    pattern = re.compile(rf'(<a class=["\']{card_class}["\'].*?</a>)', re.DOTALL)
    cards = pattern.findall(html)
    if not cards:
        return html

    sorted_cards = sorted(cards, key=keyfunc)

    first = cards[0]
    last = cards[-1]
    start = html.find(first)
    end = html.rfind(last) + len(last)
    return html[:start] + "".join(sorted_cards) + html[end:]

for year_dir in DIST.iterdir():
    if not year_dir.is_dir():
        continue
    index_file = year_dir / "index.html"
    if not index_file.exists():
        continue

    html = index_file.read_text(encoding="utf-8")

    def month_key(card):
        m = re.search(r'href=["\']([^"\']+)["\']', card)
        href = m.group(1).strip() if m else ""
        return AY_SIRASI.get(href, 99)

    html = sort_cards(html, "month-card", month_key)
    index_file.write_text(html, encoding="utf-8")

root_index = DIST / "index.html"
if root_index.exists():
    html = root_index.read_text(encoding="utf-8")

    def year_key(card):
        m = re.search(r'<h2>(\d+)</h2>', card)
        return int(m.group(1)) if m else 9999

    html = sort_cards(html, "year-card", year_key)
    root_index.write_text(html, encoding="utf-8")

print("düzeldi")
