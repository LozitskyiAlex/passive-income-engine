import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "items.json"
CALCS = ROOT / "data" / "construction_calculators.json"
SITE = ROOT / "site"
OUT = SITE / "index.html"


def main() -> None:
    SITE.mkdir(parents=True, exist_ok=True)
    items = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else []
    calculators = json.loads(CALCS.read_text(encoding="utf-8")) if CALCS.exists() else []

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
<meta name="description" content="Free construction calculators for estimating material quantities, project costs, areas and volumes.">
<meta name="google-site-verification" content="RWL8Q7FqS7ZvGU7HS2FrQvNV5XznwpVk7MqIEaDcZXQ">
<link rel="canonical" href="https://passive-income-engine.oleksoleks07.workers.dev/">
<meta property="og:type" content="website">
<meta property="og:title" content="Free Construction Calculators">
<meta property="og:description" content="Free construction calculators for material quantities and project planning.">
<meta property="og:url" content="https://passive-income-engine.oleksoleks07.workers.dev/">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"Free Construction Calculators","url":"https://passive-income-engine.oleksoleks07.workers.dev/"}}</script>
<style>
:root{{color-scheme:light}}*{{box-sizing:border-box}}body{{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:1100px;margin:0 auto;padding:44px 20px;line-height:1.6;color:#17202a;background:#fff}}
header{{margin-bottom:38px}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.1;margin:0 0 14px}}h2{{margin:34px 0 12px}}h3{{margin:0 0 8px;font-size:1.1rem}}p{{color:#53606b}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:14px}}.card{{border:1px solid #d9dee3;border-radius:14px;padding:18px;background:#fff}}.card a{{color:inherit;text-decoration:none}}.card a:hover{{text-decoration:underline}}.small{{font-size:.9rem;color:#687580}}footer{{margin-top:46px;border-top:1px solid #e5e7eb;padding-top:18px}}@media(max-width:560px){{body{{padding:28px 14px}}.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body><main>
<header><p class="small">Free tools for home improvement and construction projects</p><h1>Construction Calculators</h1><p>Estimate material quantities, project costs, areas and volumes directly in your browser. No account required.</p></header>
{''.join(sections)}
{"<section><h2>Other tools</h2><div class='grid'>" + legacy_html + "</div></section>" if legacy_html else ""}
<footer><p class="small">Calculations are estimates. Check project specifications, local requirements and manufacturer instructions before purchasing materials.</p></footer>
</main></body></html>"""
    OUT.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
