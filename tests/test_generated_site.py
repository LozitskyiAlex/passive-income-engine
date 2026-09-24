import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE = "https://passive-income-engine.oleksoleks07.workers.dev"


def test_generated_urls_match_catalog():
    subprocess.run(["python", "scripts/build.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "scripts/build_construction.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "scripts/build_construction_index.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "scripts/build_seo.py"], cwd=ROOT, check=True)
    items = json.loads((ROOT / "data/construction_calculators.json").read_text())
    expected = {BASE + "/", BASE + "/construction/"} | {BASE + f"/construction/{x['slug']}/" for x in items}
    root = ET.fromstring((SITE / "sitemap.xml").read_text())
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    actual = {node.text for node in root.findall("sm:url/sm:loc", ns)}
    assert actual == expected
    assert len(actual) == 22
    for item in items:
        page = SITE / "construction" / item["slug"] / "index.html"
        assert page.exists()
        html = page.read_text()
        assert '<link rel="icon" href="/favicon.svg"' in html
        assert '"@type":"FAQPage"' in html
        assert 'Frequently asked questions' in html
        assert 'Enter values greater than zero' in html


def test_faq_covers_all_20_calculators():
    items = json.loads((ROOT / "data/construction_calculators.json").read_text())
    faqs = json.loads((ROOT / "data/calculator_faq.json").read_text())
    assert {x["slug"] for x in faqs} == {x["slug"] for x in items}
    assert all(len(x["faqs"]) >= 2 for x in faqs)


def test_favicon_exists():
    assert (SITE / "favicon.svg").exists()
