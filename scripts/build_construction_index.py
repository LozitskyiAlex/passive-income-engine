import json
import os
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "construction_calculators.json"
OUT = ROOT / "site" / "construction" / "index.html"
BASE = os.environ.get("SITE_BASE_URL", "https://free-construction-calculators.pages.dev").rstrip("/")


def main():
    items = json.loads(DATA.read_text(encoding="utf-8"))
    guides = json.loads((ROOT / "data" / "guides.json").read_text(encoding="utf-8"))
    groups = {}
    for item in items:
        groups.setdefault(item.get("category", "Other"), []).append(item)

    sections = []
    for category, entries in groups.items():
        cards = "\n".join(
            f'<article class="calculator-card"><a class="calculator-card-link" href="/construction/{escape(i["slug"])}/" aria-label="Open {escape(i["title"])} calculator"><span class="card-meta">{escape(category)} calculator</span><h2>{escape(i["title"])}</h2><p>{escape(i["description"])}</p><span class="card-action">Open calculator <span aria-hidden="true">→</span></span></a></article>'
            for i in entries
        )
        sections.append(f"<h2>{escape(category)}</h2><div class='grid'>{cards}</div>")

    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Construction Calculators", "item": f"{BASE}/construction/"},
        ],
    }
    schema_items = ",".join(
        f'{{"@type":"ListItem","position":{n},"name":{json.dumps(i["title"])},"url":"{BASE}/construction/{i["slug"]}/"}}'
        for n, i in enumerate(items, 1)
    )
    guide_cards = "".join(
        f'<article class="calculator-card"><a class="calculator-card-link" href="/guides/{escape(g["slug"])}/" aria-label="Read guide: {escape(g["title"])}"><span class="card-meta">Practical guide</span><h2>{escape(g["title"])}</h2><p>{escape(g["description"])}</p><span class="card-action">Read guide <span aria-hidden="true">→</span></span></a></article>'
        for g in guides
    )
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Construction Calculators | Free Home Project Tools</title>
<meta name="description" content="Free construction calculators for concrete, gravel, flooring, fencing, decking, roofing, quantities, costs and more.">
<link rel="canonical" href="{BASE}/construction/"><meta property="og:type" content="website">
<meta property="og:title" content="Construction Calculators | Free Home Project Tools">
<meta property="og:description" content="Free construction calculators for material quantities and project planning."><meta property="og:url" content="{BASE}/construction/">
<meta name="twitter:card" content="summary"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>*{{box-sizing:border-box}}:root{{--ink:#1d1d1f;--muted:#6e6e73;--line:#e5e5ea;--accent:#06c}}body{{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",sans-serif;max-width:1050px;margin:40px auto;padding:0 20px;line-height:1.65;color:var(--ink);-webkit-font-smoothing:antialiased}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:18px}}.calculator-card{{border:1px solid var(--line);border-radius:20px;background:#fff;min-height:230px;box-shadow:0 4px 16px rgba(0,0,0,.045);transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease;overflow:hidden}}.calculator-card:hover{{transform:translateY(-3px);border-color:#c7c7cc;box-shadow:0 12px 32px rgba(0,0,0,.09)}}.calculator-card-link{{display:flex;flex-direction:column;align-items:flex-start;min-height:230px;height:100%;padding:24px;color:inherit;text-decoration:none!important}}.calculator-card-link:focus-visible{{outline:3px solid #0071e3;outline-offset:-4px;border-radius:20px}}.calculator-card h2{{font-size:22px;line-height:1.2;letter-spacing:-.03em;margin:14px 0 10px}}.calculator-card p{{color:var(--muted);margin:0 0 20px}}.card-meta{{font-size:12px;color:var(--muted);font-weight:600}}.card-action{{margin-top:auto;color:var(--accent);font-weight:600;font-size:14px}}a{{color:var(--accent)}}.small{{color:var(--muted)}}@media(max-width:560px){{body{{padding:20px 14px}}.grid{{grid-template-columns:1fr}}.calculator-card,.calculator-card-link{{min-height:215px}}}}</style></head>
<body><nav aria-label="Breadcrumb"><a href="/">Home</a> / Construction Calculators</nav><h1>Construction Calculators</h1><p class="small">Choose a calculator by material or project. Open any card to enter your measurements and see an estimate. Each calculator explains the required inputs, formula, result and important assumptions.</p><p><strong>Popular:</strong> <a href="/construction/concrete-volume/">Concrete</a> · <a href="/construction/gravel-volume/">Gravel</a> · <a href="/construction/roofing-squares/">Roofing</a> · <a href="/construction/fence-pickets/">Fencing</a></p>{''.join(sections)}<h2>Practical Guides</h2><p class="small">Step by step explanations to help you measure, choose materials and understand your estimate.</p><div class='grid'>{guide_cards}</div><p><a href="/blog/">Visit the blog for more construction advice</a></p>
<script type="application/ld+json">{json.dumps(breadcrumb_schema,separators=(",",":"))}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Construction Calculators","url":"{BASE}/construction/","mainEntity":{{"@type":"ItemList","numberOfItems":{len(items)},"itemListElement":[{schema_items}]}}}}</script>
</body></html>"""
    OUT.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
