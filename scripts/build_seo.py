import json
import os
from html import escape
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA = ROOT / "data" / "construction_calculators.json"
GUIDES = ROOT / "data" / "guides.json"
BASE = "https://passive-income-engine.oleksoleks07.workers.dev"
INDEXNOW_KEY = os.environ.get("INDEX_NOW_KEY")

def build_guide(guide):
    steps = "".join(f"<li>{escape(x)}</li>" for x in guide["steps"])
    notes = "".join(f"<li>{escape(x)}</li>" for x in guide["notes"])
    calc = guide.get("calculator_slug")
    calc_link = (
        f'<p><a href="/construction/{escape(calc)}/">Use the {escape(guide["title"])} calculator</a></p>'
        if calc else ""
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": guide["title"],
        "description": guide["description"],
        "mainEntityOfPage": f"{BASE}/guides/{guide['slug']}/",
        "author": {"@type": "Organization", "name": "Free Construction Calculators"},
        "publisher": {"@type": "Organization", "name": "Free Construction Calculators"},
    }
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Construction Calculators", "item": f"{BASE}/construction/",},
            {"@type": "ListItem", "position": 3, "name": guide["title"], "item": f"{BASE}/guides/{guide['slug']}/"},
        ],
    }
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(guide["title"])}</title>
<meta name="description" content="{escape(guide["description"])}">
<link rel="canonical" href="{BASE}/guides/{escape(guide["slug"])}/">
<meta property="og:type" content="article">
<meta property="og:title" content="{escape(guide["title"])}">
<meta property="og:description" content="{escape(guide["description"])}">
<meta property="og:url" content="{BASE}/guides/{escape(guide["slug"])}/">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token":"f5f27f5b7b9b45f3b74c48e6f44b56c0"}}'></script>
<script type="application/ld+json">{json.dumps(schema,separators=(",",":"))}</script>
<script type="application/ld+json">{json.dumps(breadcrumb_schema,separators=(",",":"))}</script>
<style>
*{{box-sizing:border-box}}body{{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:820px;margin:0 auto;padding:32px 20px;line-height:1.65;color:#17202a}}h1{{line-height:1.2}}h2{{margin-top:30px}}.formula,.example{{padding:16px;border:1px solid #d9dee3;border-radius:10px;background:#f7f9fb}}.formula{{font-weight:650}}li{{margin:8px 0}}.small{{color:#5d6872}}@media(max-width:560px){{body{{padding:20px 14px}}}}
</style>
</head>
<body>
<main>
<nav aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/construction/">Construction Calculators</a> / {escape(guide["title"])}</nav>
<article>
<h1>{escape(guide["title"])}</h1>
<p>{escape(guide["intro"])}</p>
<h2>How to calculate it</h2>
<ol>{steps}</ol>
<h2>Formula</h2>
<p class="formula">{escape(guide["formula"])}</p>
<h2>Example</h2>
<p class="example">{escape(guide["example"])}</p>
<h2>Important notes</h2>
<ul>{notes}</ul>
{calc_link}
<p class="small">This page provides a practical estimating method. Verify project specifications, local requirements and manufacturer instructions before purchasing materials.</p>
</article>
</main>
</body>
</html>'''

def main():
    SITE.mkdir(parents=True, exist_ok=True)
    items = json.loads(DATA.read_text(encoding="utf-8"))
    guides = json.loads(GUIDES.read_text(encoding="utf-8"))
    (SITE / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: " + BASE + "/sitemap.xml\n",
        encoding="utf-8",
    )
    if INDEXNOW_KEY:
        (SITE / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
        (SITE / "indexnow-key.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    for guide in guides:
        out = SITE / "guides" / guide["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_guide(guide), encoding="utf-8")
    urls = ["/", "/construction/"]
    urls += [f'/construction/{i["slug"]}/' for i in items]
    urls += [f'/guides/{g["slug"]}/' for g in guides]
    body = "\n".join(f"  <url><loc>{xml_escape(BASE + u)}</loc></url>" for u in urls)
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )
    (SITE / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    commit_sha = os.environ.get("WORKERS_CI_COMMIT_SHA") or os.environ.get("GITHUB_SHA")
    if commit_sha:
        (SITE / "deployment-version.txt").write_text(commit_sha + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
