import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "items.json"
SITE = ROOT / "site"
OUT = SITE / "index.html"


def main() -> None:
    SITE.mkdir(parents=True, exist_ok=True)

    items = []
    if DATA.exists():
        items = json.loads(DATA.read_text(encoding="utf-8"))

    cards = []
    for item in items:
        cards.append(
            f'<article><h2><a href="{item["url"]}">{item["title"]}</a></h2>'
            f'<p>{item.get("description", "")}</p></article>'
        )

    body = "\n".join(cards) or "<p>No data collected yet.</p>"
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Passive Income Engine</title>
<meta name="description" content="A useful data-driven static web product.">
</head>
<body>
<main>
<h1>Passive Income Engine</h1>
{body}
</main>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
