import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from passive_income_engine.construction import calculate

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE = "https://passive-income-engine.oleksoleks07.workers.dev"


def test_all_calculator_formulas():
    cases = {
        "concrete_volume": ([20, 10, 0.5], 100),
        "concrete_bags": ([10, 0.6], 17),
        "gravel_volume": ([20, 10, 0.25], 50),
        "mulch_volume": ([20, 10, 0.25], 50),
        "paint_quantity": ([800, 350, 2], 800 / 350 * 2),
        "flooring_quantity": ([20, 15, 10], 330),
        "tile_quantity": ([1000, 12, 12, 10], 8),
        "drywall_sheets": ([20, 15, 8, 4, 8], 18),
        "board_feet": ([2, 6, 8, 1], 8),
        "material_cost": ([100, 4, 10], 440),
        "paver_quantity": ([20, 12, 12, 6, 5], 504),
        "sand_volume": ([20, 10, 0.1], 20),
        "soil_volume": ([10, 10, 0.5], 50),
        "fence_pickets": ([100, 5.5, 1.5], 172),
        "fence_posts": ([100, 8], 14),
        "decking_boards": ([20, 12, 6, 0.125, 12, 0], 48),
        "roofing_squares": ([2400], 24),
        "roofing_material": ([2400, 10], 2640),
        "gravel_weight": ([10, 1.6], 16),
        "concrete_weight": ([10, 150], 1500),
        "concrete_footing": ([20, 1, 0.5], 10),
        "rebar_length": ([20, 4], 80),
        "gravel_bags": ([10, 0.5], 20),
        "baseboard": ([100, 8], 13),
        "wallpaper": ([120, 25], 5),
        "stair_risers": ([96, 8], 12),
        "asphalt_volume": ([20, 10, 0.2], 40),
        "cubic_yards": ([27, 1, 1], 1),
        "area": ([20, 15], 300),
        "volume": ([20, 15, 2], 600),
    }
    for kind, (values, expected) in cases.items():
        actual = calculate(kind, values)
        assert abs(actual - expected) < 1e-9, (kind, actual, expected)


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
    assert len(actual) == len(items) + 2
    for item in items:
        page = SITE / "construction" / item["slug"] / "index.html"
        assert page.exists()
        html = page.read_text()
        assert '<link rel="icon" href="/favicon.svg"' in html
        assert "static.cloudflareinsights.com/beacon.min.js" in html
        assert "aria-label=\"Breadcrumb\"" in html
        assert '"@type":"FAQPage"' in html
        assert 'Frequently asked questions' in html
        assert 'Enter values greater than zero' in html
        assert 'Related calculators' in html


def test_faq_covers_all_calculators():
    items = json.loads((ROOT / "data/construction_calculators.json").read_text())
    faqs = json.loads((ROOT / "data/calculator_faq.json").read_text())
    assert {x["slug"] for x in faqs} == {x["slug"] for x in items}
    assert all(len(x["faqs"]) >= 2 for x in faqs)


def test_favicon_exists():
    assert (SITE / "favicon.svg").exists()



def test_catalog_integrity():
    items = json.loads((ROOT / "data/construction_calculators.json").read_text())
    slugs = [x["slug"] for x in items]
    types = [x["type"] for x in items]
    assert len(items) == 30
    assert len(slugs) == len(set(slugs))
    assert len(types) == len(set(types))
    assert all(x.get("category") for x in items)
    related = json.loads((ROOT / "data/related_calculators.json").read_text())
    assert set(related) == set(slugs)
    assert all(target in slugs for targets in related.values() for target in targets)
