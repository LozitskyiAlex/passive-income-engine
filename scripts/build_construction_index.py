import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "construction_calculators.json"
OUT = ROOT / "site" / "construction" / "index.html"
BASE = "https://passive-income-engine.oleksoleks07.workers.dev"


def main():
    items = json.loads(DATA.read_text(encoding="utf-8"))
    groups = {}
    for item in items:
        groups.setdefault(item.get("category", "Other"), []).append(item)

    sections = []
    for category, entries in groups.items():
        cards = "\n".join(
            f'<article><h2><a href="/construction/{escape(i["slug"])}/">{escape(i["title"])}</a></h2><p>{escape(i["description"])}</p></article>'
            for i in entries
        )
        sections.append(f"<h2>{escape(category)}</h2><div class='grid'>{cards}</div>")

    schema_items = ",".join(
        f'{{"@type":"ListItem","position":{n},"name":{json.dumps(i["title"])},"url":"{BASE}/construction/{i["slug"]}/"}}'
        for n, i in enumerate(items, 1)
    )
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Construction Calculators | Free Home Project Tools</title>
<meta name="description" content="Free construction calculators for concrete, gravel, flooring, fencing, decking, roofing, quantities, costs and more.">
<link rel="canonical" href="{BASE}/construction/"><meta property="og:type" content="website">
<meta property="og:title" content="Construction Calculators | Free Home Project Tools">
<meta property="og:description" content="Free construction calculators for material quantities and project planning."><meta property="og:url" content="{BASE}/construction/">
<meta name="twitter:card" content="summary"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token":"f5f27f5b7b9b45f3b74c48e6f44b56c0"}}'></script>
<style>*{{box-sizing:border-box}}body{{font-family:system-ui,sans-serif;max-width:1050px;margin:40px auto;padding:0 20px;line-height:1.6;color:#17202a}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:14px}}article{{border:1px solid #ddd;border-radius:12px;padding:18px}}a{{color:inherit}}.small{{color:#5f6b75}}@media(max-width:560px){{body{{padding:20px 14px}}.grid{{grid-template-columns:1fr}}}}</style></head>
<body><a href="/">Home</a><h1>Construction Calculators</h1><p class="small">Free browser based tools for estimating materials, quantities and basic project costs.</p>{''.join(sections)}
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Construction Calculators","url":"{BASE}/construction/","mainEntity":{{"@type":"ItemList","numberOfItems":{len(items)},"itemListElement":[{schema_items}]}}}}</script>
</body></html>"""
    OUT.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
