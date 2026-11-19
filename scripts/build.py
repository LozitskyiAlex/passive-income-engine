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
            f'<article class="calculator-card"><a class="calculator-card-link" href="/construction/{escape(i["slug"])}/" aria-label="{escape(i["title"])}"><span class="card-meta">{escape(category)}</span><h3>{escape(i["title"])}</h3>'
            f'<p>{escape(i.get("description", ""))}</p><span class="card-action">Open the related calculator <span aria-hidden="true">→</span></span></a></article>' for i in entries
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
<meta name="description" content="Free construction calculators for estimating material quantities, project costs, areas and volumes.">
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
:root{{color-scheme:light}}*{{box-sizing:border-box}}body{{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;width:100%;max-width:1168px;margin:0 auto;padding:32px 24px;line-height:1.6;color:#17202a;background:#fff}}
header{{margin-bottom:22px}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.1;margin:0 0 14px}}h2{{margin:34px 0 12px}}h3{{margin:0 0 8px;font-size:1.1rem}}p{{color:#53606b}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:18px}}.calculator-card{{border:1px solid #e5e5ea;border-radius:20px;background:#fff;min-height:230px;box-shadow:0 4px 16px rgba(0,0,0,.045);transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease;overflow:hidden}}.calculator-card:hover{{transform:translateY(-3px);border-color:#c7c7cc;box-shadow:0 12px 32px rgba(0,0,0,.09)}}.calculator-card-link{{display:flex;flex-direction:column;align-items:flex-start;min-height:230px;height:100%;padding:24px;color:inherit;text-decoration:none!important}}.calculator-card-link:focus-visible{{outline:3px solid #0071e3;outline-offset:-4px;border-radius:20px}}.calculator-card h3{{font-size:22px;line-height:1.2;letter-spacing:-.03em;margin:14px 0 10px}}.calculator-card p{{color:#6e6e73;margin:0 0 20px}}.card-meta{{font-size:12px;color:#6e6e73;font-weight:600}}.card-action{{margin-top:auto;color:#06c;font-weight:600;font-size:14px}}.small{{font-size:.9rem;color:#687580}}footer{{margin-top:46px;border-top:1px solid #e5e7eb;padding-top:18px}}@media(max-width:560px){{body{{padding:20px 14px}}.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body><main>
<header><h1>Free Construction Calculators</h1><p class="small">Calculate material quantities for your construction and home projects.</p></header>
{''.join(sections)}
{"<section><h2>Other calculators</h2><div class='grid'>" + legacy_html + "</div></section>" if legacy_html else ""}
<footer><p class="small">Calculations are estimates. Verify project specifications and supplier requirements before ordering.</p><p><a href="/blog/">Construction guides and blog</a></p></footer>
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
