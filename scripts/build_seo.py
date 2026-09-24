import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"site"
DATA=ROOT/"data"/"construction_calculators.json"
BASE="https://YOUR-CLOUDFLARE-DOMAIN.example"


def main():
    SITE.mkdir(parents=True,exist_ok=True)
    items=json.loads(DATA.read_text())
    urls=["/","/construction/"]+[f'/construction/{i["slug"]}/' for i in items]
    (SITE/"robots.txt").write_text("User-agent: *\\nAllow: /\\nSitemap: "+BASE+"/sitemap.xml\\n",encoding="utf-8")
    body="\\n".join(f"  <url><loc>{escape(BASE+u)}</loc></url>" for u in urls)
    sitemap=f'<?xml version="1.0" encoding="UTF-8"?>\\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n{body}\\n</urlset>\\n'
    (SITE/"sitemap.xml").write_text(sitemap,encoding="utf-8")

if __name__=="__main__":
    main()
