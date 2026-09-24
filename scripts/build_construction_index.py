import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "construction_calculators.json"
OUT = ROOT / "site" / "construction" / "index.html"

def main():
    items = json.loads(DATA.read_text(encoding="utf-8"))
    cards = "\n".join(
        f'<article><h2><a href="/construction/{escape(i["slug"])}/">{escape(i["title"])}</a></h2>'
        f'<p>{escape(i["description"])}</p></article>'
        for i in items
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Construction Calculators | Free Home Project Tools</title>
<meta name="description" content="Free construction calculators for concrete, gravel, mulch, paint, flooring, tile, drywall, lumber and material costs.">
<link rel="canonical" href="https://passive-income-engine.oleksoleks07.workers.dev/construction/">
<meta property="og:type" content="website">
<meta property="og:title" content="Construction Calculators | Free Home Project Tools">
<meta property="og:description" content="Free construction calculators for concrete, gravel, mulch, paint, flooring, tile, drywall, lumber and material costs.">
<meta property="og:url" content="https://passive-income-engine.oleksoleks07.workers.dev/construction/">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>
body{{font-family:system-ui,sans-serif;max-width:900px;margin:40px auto;padding:0 20px;line-height:1.6;color:#17202a}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}}
article{{border:1px solid #ddd;border-radius:12px;padding:18px}}@media(max-width:560px){{body{{padding:20px 14px}}.grid{{grid-template-columns:1fr}}}}
a{{color:inherit}}
.small{{color:#5f6b75}}
</style>
</head>
<body>
<a href="/">Home</a>
<h1>Construction Calculators</h1>
<p class="small">Free browser based tools for estimating materials and basic project costs.</p>
<div class="grid">{cards}</div>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CollectionPage","name":"Construction Calculators","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/","mainEntity":{{"@type":"ItemList","numberOfItems":20,"itemListElement":[{{"@type":"ListItem","position":1,"name":"Concrete Volume Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/concrete-volume/"}},{{"@type":"ListItem","position":2,"name":"Concrete Bag Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/concrete-bags/"}},{{"@type":"ListItem","position":3,"name":"Gravel Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/gravel-volume/"}},{{"@type":"ListItem","position":4,"name":"Mulch Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/mulch-volume/"}},{{"@type":"ListItem","position":5,"name":"Paint Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/paint-quantity/"}},{{"@type":"ListItem","position":6,"name":"Flooring Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/flooring-quantity/"}},{{"@type":"ListItem","position":7,"name":"Tile Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/tile-quantity/"}},{{"@type":"ListItem","position":8,"name":"Drywall Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/drywall-sheets/"}},{{"@type":"ListItem","position":9,"name":"Board Feet Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/board-feet/"}},{{"@type":"ListItem","position":10,"name":"Material Cost Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/material-cost/"}},{{"@type":"ListItem","position":11,"name":"Paver Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/paver-quantity/"}},{{"@type":"ListItem","position":12,"name":"Sand Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/sand-volume/"}},{{"@type":"ListItem","position":13,"name":"Soil Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/soil-volume/"}},{{"@type":"ListItem","position":14,"name":"Fence Picket Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/fence-pickets/"}},{{"@type":"ListItem","position":15,"name":"Fence Post Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/fence-posts/"}},{{"@type":"ListItem","position":16,"name":"Decking Board Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/decking-boards/"}},{{"@type":"ListItem","position":17,"name":"Roofing Squares Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/roofing-squares/"}},{{"@type":"ListItem","position":18,"name":"Roofing Material Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/roofing-material/"}},{{"@type":"ListItem","position":19,"name":"Gravel Weight Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/gravel-weight/"}},{{"@type":"ListItem","position":20,"name":"Concrete Weight Calculator","url":"https://passive-income-engine.oleksoleks07.workers.dev/construction/concrete-weight/"}}]}}}}
</script>
<p class="small">Results are estimates. Verify dimensions, product coverage, waste allowances and local requirements before purchasing materials.</p>
</body>
</html>"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    main()
