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

    cards = []
    for item in calculators:
        cards.append(
            f'<article class="card"><h2><a href="/construction/{escape(item["slug"])}/">{escape(item["title"])}</a></h2>'
            f'<p>{escape(item.get("description", ""))}</p></article>'
        )

    legacy = []
    for item in items:
        legacy.append(
            f'<article class="card"><h2><a href="{escape(item["url"])}">{escape(item["title"])}</a></h2>'
            f'<p>{escape(item.get("description", ""))}</p></article>'
        )

    calculator_html = "\n".join(cards)
    legacy_html = "\n".join(legacy)

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free Construction Calculators</title>
<meta name="description" content="Free construction and home project calculators for concrete, gravel, mulch, paint, flooring, tile, drywall, lumber and material costs.">
<link rel="canonical" href="https://passive-income-engine.oleksoleks07.workers.dev/">
<meta property="og:type" content="website">
<meta property="og:title" content="Free Construction Calculators">
<meta property="og:description" content="Free construction and home project calculators for material quantities and project planning.">
<meta property="og:url" content="https://passive-income-engine.oleksoleks07.workers.dev/">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"Free Construction Calculators","url":"https://passive-income-engine.oleksoleks07.workers.dev/"}</script>
<style>
:root{{color-scheme:light}}
body{{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:1000px;margin:0 auto;padding:48px 20px;line-height:1.6;color:#17202a;background:#fff}}
header{{margin-bottom:40px}}
h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.1;margin:0 0 16px}}
h2{{margin:0 0 8px;font-size:1.15rem}}
p{{color:#53606b}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}}
.card{{border:1px solid #d9dee3;border-radius:14px;padding:20px;background:#fff}}
.card a{{color:inherit;text-decoration:none}}
.card a:hover{{text-decoration:underline}}
.small{{font-size:.9rem;color:#687580}}
footer{{margin-top:48px;border-top:1px solid #e5e7eb;padding-top:20px}}@media(max-width:560px){{body{{padding:28px 14px}}.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<main>
<header>
<p class="small">Free tools for home improvement and construction projects</p>
<h1>Construction Calculators</h1>
<p>Calculate material quantities and project costs quickly. These tools run in your browser and do not require an account.</p>
</header>
<section>
<h2>Free calculators</h2>
<div class="grid">{calculator_html}</div>
</section>
{"<section style='margin-top:40px'><h2>Other tools</h2><div class='grid'>" + legacy_html + "</div></section>" if legacy_html else ""}
<footer><p class="small">Calculations are estimates. Check project specifications, local requirements and manufacturer instructions before purchasing materials.</p></footer>
</main>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
