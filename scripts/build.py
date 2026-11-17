import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "items.json"
CALCS = ROOT / "data" / "construction_calculators.json"
GUIDES = ROOT / "data" / "guides.json"
SITE = ROOT / "site"
OUT = SITE / "index.html"
BASE = "https://free-construction-calculators.pages.dev"


def main() -> None:
    SITE.mkdir(parents=True, exist_ok=True)
    items = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else []
    calculators = json.loads(CALCS.read_text(encoding="utf-8")) if CALCS.exists() else []
    guides = json.loads(GUIDES.read_text(encoding="utf-8")) if GUIDES.exists() else []

    groups = {}
    for item in calculators:
        groups.setdefault(item.get("category", "Other"), []).append(item)

    sections = []
    for category, entries in groups.items():
        cards = "\n".join(
            f'<article class="card"><h3><a href="/construction/{escape(i["slug"])}/">{escape(i["title"])}</a></h3>'
            f'<p>{escape(i.get("description", ""))}</p></article>' for i in entries
        )
        sections.append(f'<section><h2>{escape(category)}</h2><div class="grid">{cards}</div></section>')

    guide_cards = "\n".join(
        f'<article class="card"><h3><a href="/guides/{escape(g["slug"])}/">{escape(g["title"])}</a></h3>'
        f'<p>{escape(g["description"])}</p></article>' for g in guides
    )

    legacy = []
    for item in items:
        legacy.append(
            f'<article class="card"><h3><a href="{escape(item["url"])}">{escape(item["title"])}</a></h3>'
            f'<p>{escape(item.get("description", ""))}</p></article>'
        )
    legacy_html = "\n".join(legacy)

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free Construction Calculators</title>
<meta name="description" content="Free concrete, gravel, paint, flooring, tile and roofing calculators with formulas, worked examples and metric or US customary units.">
<meta name="google-site-verification" content="i1hT9Vac2DfM1lZl4p70A1feeiP6Vmq-tGaFSfHTfqQ">\n<meta name="msvalidate.01" content="525510C1BE000729AE171411BBC091D8">
<link rel="canonical" href="https://free-construction-calculators.pages.dev/">
<meta property="og:type" content="website">
<meta property="og:title" content="Free Construction Calculators">
<meta property="og:description" content="Free construction calculators for material quantities and project planning.">
<meta property="og:url" content="https://free-construction-calculators.pages.dev/">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"Free Construction Calculators","url":"https://free-construction-calculators.pages.dev/"}}</script>
<style>
:root{{color-scheme:light}}*{{box-sizing:border-box}}body{{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:1100px;margin:0 auto;padding:44px 20px;line-height:1.6;color:#17202a;background:#fff}}
header{{margin-bottom:38px}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.1;margin:0 0 14px}}h2{{margin:34px 0 12px}}h3{{margin:0 0 8px;font-size:1.1rem}}p{{color:#53606b}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:14px}}.card{{border:1px solid #d9dee3;border-radius:14px;padding:18px;background:#fff}}.card a{{color:inherit;text-decoration:none}}.card a:hover{{text-decoration:underline}}.small{{font-size:.9rem;color:#687580}}footer{{margin-top:46px;border-top:1px solid #e5e7eb;padding-top:18px}}@media(max-width:560px){{body{{padding:28px 14px}}.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body><main>
<header><p class="small">Free tools for home improvement and construction projects</p><h1>Free Construction Calculators</h1><p>Plan material quantities for concrete pours, landscaping, painting, flooring, tiling, drywall, paving and roofing. Use free browser based calculators with metric or US customary inputs, worked examples and practical notes. No account or sign up required.</p></header><section><h2>Popular calculators</h2><p>Start with <a href="/construction/concrete-volume/">concrete volume</a>, <a href="/construction/concrete-bags/">concrete bags</a>, <a href="/construction/gravel-volume/">gravel volume</a>, <a href="/construction/paint-quantity/">paint</a>, <a href="/construction/flooring-quantity/">flooring</a> or <a href="/construction/roofing-material/">roofing materials</a>.</p></section>
<section data-unit-system="us"><h2>How to get a useful material estimate</h2><ol><li><strong>Measure the finished work area.</strong> Record each length, width, depth or height. Split irregular spaces into simple sections and add their results.</li><li><strong>Use the product specification.</strong> Check coverage, bag yield, package size or bulk density on the exact product you intend to buy.</li><li><strong>Choose a realistic allowance.</strong> Cutting, patterns, uneven ground, compaction and breakage affect waste. Use manufacturer or installer guidance rather than assuming one percentage suits every project.</li><li><strong>Convert to purchase units.</strong> Round up to full bags, boxes or packs after applying the allowance. Check supplier minimums and delivery units.</li></ol><p>Each calculator states the formula and its assumptions. The examples are planning illustrations, not product guarantees or engineering specifications.</p><h2>Metric and US customary measurements</h2><p>Choose the measurement system that matches your project. Metric pages use metres, square metres, cubic metres, millimetres and kilograms where relevant. US customary pages use feet, inches, square feet, cubic feet and pounds. Do not mix units within a calculation. Regional defaults are selected for each language, and you can switch systems in the calculator.</p><h2>What these estimates do not replace</h2><p>Quantity calculators do not design structural elements, determine code compliance, assess site conditions or replace manufacturer installation instructions. Confirm dimensions, product coverage, local requirements and supplier ordering conventions before purchasing. For structural concrete, foundations, stairs, roofs and other safety critical work, use qualified project design and professional advice.</p></section>
{''.join(sections)}
{"<section><h2>Practical guides</h2><div class='grid'>" + guide_cards + "</div></section>" if guide_cards else ""}
{"<section><h2>Other tools</h2><div class='grid'>" + legacy_html + "</div></section>" if legacy_html else ""}
<footer><p class="small">Calculations are estimates. Check project specifications, local requirements and manufacturer instructions before purchasing materials.</p></footer>
</main></body></html>"""
    OUT.write_text(html, encoding="utf-8")
    not_found = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page not found | Free Construction Calculators</title><meta name="robots" content="noindex">
<link rel="canonical" href="https://free-construction-calculators.pages.dev/404.html"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>body{font-family:system-ui,sans-serif;max-width:720px;margin:0 auto;padding:48px 20px;line-height:1.6;color:#17202a}a{color:inherit}</style></head>
<body><main><h1>Page not found</h1><p>The requested page does not exist.</p><p><a href="/">Return to Free Construction Calculators</a></p></main></body></html>"""
    (SITE / "404.html").write_text(not_found, encoding="utf-8")


if __name__ == "__main__":
    main()
