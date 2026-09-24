import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_every_calculator_has_units():
    calculators = json.loads((ROOT / "data" / "construction_calculators.json").read_text())
    units = json.loads((ROOT / "data" / "calculator_units.json").read_text())
    for item in calculators:
        assert item["type"] in units
        assert len(units[item["type"]]) > 0
