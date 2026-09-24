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
