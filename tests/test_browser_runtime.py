import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "site" / "calculator-runtime.js"


def test_generated_browser_runtime_matches_examples():
    subprocess.run(["python", "scripts/build_construction.py"], cwd=ROOT, check=True)
    assert RUNTIME.exists()

    cases = {
        "concrete_volume": [20, 10, 0.5],
        "concrete_bags": [10, 0.6],
        "gravel_volume": [20, 10, 0.25],
        "mulch_volume": [20, 10, 0.25],
        "paint_quantity": [800, 350, 2],
        "flooring_quantity": [20, 15, 10],
        "tile_quantity": [1000, 12, 12, 10],
        "drywall_sheets": [20, 15, 8, 4, 8],
        "board_feet": [2, 6, 8, 1],
        "material_cost": [100, 4, 10],
        "paver_quantity": [20, 12, 12, 6, 5],
        "sand_volume": [20, 10, 0.1],
        "soil_volume": [10, 10, 0.5],
        "fence_pickets": [100, 5.5, 1.5],
        "fence_posts": [100, 8],
        "decking_boards": [20, 12, 6, 0.125, 12, 0],
        "roofing_squares": [2400],
        "roofing_material": [2400, 10],
        "gravel_weight": [10, 1.6],
        "concrete_weight": [10, 150],
        "concrete_footing": [20, 1, 0.5],
        "rebar_length": [20, 4],
        "gravel_bags": [10, 0.5],
        "baseboard": [100, 8],
        "wallpaper": [120, 25],
        "stair_risers": [96, 8],
        "asphalt_volume": [20, 10, 0.2],
        "cubic_yards": [27, 1, 1],
        "area": [20, 15],
        "volume": [20, 15, 2],
    }

    node_script = f"""
import {{ calculate }} from {json.dumps(str(RUNTIME))};
const cases = {json.dumps(cases)};
const results = Object.fromEntries(
  Object.entries(cases).map(([kind, values]) => [kind, calculate(kind, values)])
);
console.log(JSON.stringify(results));
"""
    completed = subprocess.run(
        ["node", "--input-type=module", "-e", node_script],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    actual = json.loads(completed.stdout)

    expected = {
        "concrete_volume": "100.000 cubic units",
        "concrete_bags": "17 bags",
        "gravel_volume": "50.000 cubic units",
        "mulch_volume": "50.000 cubic units",
        "paint_quantity": "4.57 units",
        "flooring_quantity": "330.00 square units",
        "tile_quantity": "1100 tiles",
        "drywall_sheets": "18 sheets",
        "board_feet": "8.00 board feet",
        "material_cost": "440.00",
        "paver_quantity": "504 pavers",
        "sand_volume": "20.000 cubic units",
        "soil_volume": "50.000 cubic units",
        "fence_pickets": "172 pickets",
        "fence_posts": "14 posts",
        "decking_boards": "48 boards",
        "roofing_squares": "24.00 roofing squares",
        "roofing_material": "2640.00 sq ft",
        "gravel_weight": "16.00 weight units",
        "concrete_weight": "1500.00 weight units",
        "concrete_footing": "10.000 cubic units",
        "rebar_length": "80.00 length units",
        "gravel_bags": "20 bags",
        "baseboard": "13 boards",
        "wallpaper": "5 rolls",
        "stair_risers": "12 risers",
        "asphalt_volume": "40.000 cubic units",
        "cubic_yards": "1.000 cubic yards",
        "area": "300.00 square units",
        "volume": "600.000 cubic units",
    }
    assert actual == expected
