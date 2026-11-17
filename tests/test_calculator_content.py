import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_every_calculator_has_content():
    calculators = json.loads((ROOT / "data" / "construction_calculators.json").read_text())
    content = {x["slug"]: x for x in json.loads((ROOT / "data" / "calculator_content.json").read_text())}
    assert {x["slug"] for x in calculators} == set(content)
    for item in content.values():
        assert item["how"]
        assert item["example"]
        assert item["tips"]

def test_priority_calculators_have_detailed_guidance_and_faqs():
    priority = {"concrete-volume", "concrete-bags", "gravel-volume", "paint-quantity", "flooring-quantity", "tile-quantity", "drywall-sheets", "paver-quantity", "roofing-material", "material-cost"}
    content = {x["slug"]: x for x in json.loads((ROOT / "data" / "calculator_content.json").read_text())}
    faqs = {x["slug"]: x["faqs"] for x in json.loads((ROOT / "data" / "calculator_faq.json").read_text())}
    for slug in priority:
        assert len(content[slug]["how"]) >= 250, slug
        assert len(content[slug]["example"]) >= 180, slug
        assert len(content[slug]["tips"]) >= 3, slug
        assert len(faqs[slug]) >= 4, slug
