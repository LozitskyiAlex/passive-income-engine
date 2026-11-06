import json
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
LOCALES = {"en": ("US", "us"), "es": ("ES", "metric"), "de": ("DE", "metric"), "fr": ("FR", "metric"), "pt-br": ("BR", "metric"), "ja": ("JP", "metric"), "it": ("IT", "metric"), "nl": ("NL", "metric"), "pl": ("PL", "metric"), "zh-hans": ("CN", "metric"), "ko": ("KR", "metric"), "ar": ("001", "metric"), "uk": ("UA", "metric"), "ru": ("RU", "metric"), "tr": ("TR", "metric")}


def test_all_locale_routes_have_regional_measurement_defaults():
    for locale, (region, measurement) in LOCALES.items():
        page = SITE / ("index.html" if locale == "en" else locale + "/index.html")
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        assert soup.html.get("data-region") == region
        assert soup.html.get("data-measurement") == measurement


def test_all_calculator_pages_expose_switchable_regional_units():
    items = json.loads((ROOT / "data/construction_calculators.json").read_text())
    for locale, (_, measurement) in LOCALES.items():
        for item in items:
            page = SITE / ("" if locale == "en" else locale + "/") / "construction" / item["slug"] / "index.html"
            soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
            selector = soup.select_one("#measurement-system")
            assert selector is not None
            assert {x.get("value") for x in selector.find_all("option")} == {"metric", "us"}
            assert soup.html.get("data-measurement") == measurement
            assert soup.select(".unit[data-dimension]")
            if measurement == "metric":
                assert all(x.get_text(strip=True) not in {"ft", "in", "sq ft", "cu ft", "lb/cu ft"} for x in soup.select(".unit[data-dimension]"))


def test_metric_conversion_adapter_converts_inputs_and_outputs():
    runtime = SITE / "calculator-runtime.js"
    cases = {
        "concrete_volume": ([6.096, 3.048, 0.1524], "2.832 m³"),
        "gravel_volume": ([6.096, 3.048, 0.0762], "1.416 m³"),
        "tile_quantity": ([92.90304, 304.8, 304.8, 10], "1100 tiles"),
        "board_feet": ([50.8, 152.4, 2.4384, 4], "0.076 m³"),
        "roofing_squares": ([240], "240.00 m²"),
        "concrete_weight": ([0.28316846592, 2402.769], "680.389 kg"),
        "rebar_length": ([20, 1.2192], "24.384 m"),
        "cubic_yards": ([8.2296, 0.3048, 0.3048], "0.765 m³"),
        "area": ([6.096, 4.572], "27.871 m²"),
    }
    payload = {key: value[0] for key, value in cases.items()}
    script = "import { calculateRegional } from " + json.dumps(str(runtime)) + ";\n"
    script += "const cases = " + json.dumps(payload) + ";\n"
    script += "console.log(JSON.stringify(Object.fromEntries(Object.entries(cases).map(([kind, values]) => [kind, calculateRegional(kind, values, 'metric')]))));"
    result = subprocess.run(["node", "--input-type=module", "-e", script], cwd=ROOT, check=True, capture_output=True, text=True)
    actual = json.loads(result.stdout)
    assert actual == {key: value[1] for key, value in cases.items()}
