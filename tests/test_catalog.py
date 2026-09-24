import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_catalog_has_20_unique_slugs():
    items=json.loads((ROOT/"data"/"construction_calculators.json").read_text())
    slugs=[x["slug"] for x in items]
    assert len(items)==20
    assert len(slugs)==len(set(slugs))

def test_required_fields_exist():
    items=json.loads((ROOT/"data"/"construction_calculators.json").read_text())
    for item in items:
        assert item["slug"]
        assert item["title"]
        assert item["description"]
        assert item["type"]
