import json
import os
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("SITE_BASE_URL", "https://passive-income-engine.oleksoleks07.workers.dev").rstrip("/")


def fetch(path):
    request = urllib.request.Request(BASE + path, headers={"User-Agent": "PassiveIncomeEngineSmokeTest/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")


def main():
    catalog = json.loads((ROOT / "data/construction_calculators.json").read_text(encoding="utf-8"))
    guides = json.loads((ROOT / "data/guides.json").read_text(encoding="utf-8"))
    checks = [
        "/",
        "/robots.txt",
        "/sitemap.xml",
        "/construction/",
        f'/construction/{catalog[0]["slug"]}/',
        f'/guides/{guides[0]["slug"]}/',
    ]

    for path in checks:
        status, body = fetch(path)
        if status != 200:
            raise SystemExit(f"Smoke test failed: {path} returned HTTP {status}")
        if path == "/" and '<link rel="canonical"' not in body:
            raise SystemExit("Smoke test failed: homepage canonical is missing")
        if path.startswith("/construction/") and path != "/construction/" and 'id="calculate"' not in body:
            raise SystemExit(f"Smoke test failed: calculator UI missing at {path}")

    status, body = fetch("/sitemap.xml")
    if status != 200:
        raise SystemExit(f"Smoke test failed: sitemap returned HTTP {status}")
    root = ET.fromstring(body)
    locs = [node.text for node in root.iter() if node.tag.endswith("loc") and node.text]
    expected_count = len(catalog) + len(guides) + 2
    if len(locs) != expected_count:
        raise SystemExit(f"Smoke test failed: sitemap has {len(locs)} URLs, expected {expected_count}")

    status, _ = fetch("/this-page-does-not-exist-qa-check")
    if status != 404:
        raise SystemExit(f"Smoke test failed: unknown URL returned HTTP {status}, expected 404")

    print(f"Smoke test passed for {BASE}: {len(checks)} pages, sitemap with {len(locs)} URLs, 404 handling verified.")


if __name__ == "__main__":
    main()
