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
<link rel="canonical" href="https://passive-income-engine.oleksoleks07.workers.dev/construction/"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
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
<p class="small">Results are estimates. Verify dimensions, product coverage, waste allowances and local requirements before purchasing materials.</p>
</body>
</html>"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    main()
