import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = os.environ.get("SITE_BASE_URL", "https://free-construction-calculators.pages.dev").rstrip("/")
HOST = BASE.removeprefix("https://").removeprefix("http://")
ROOT = Path(__file__).resolve().parents[1]
KEY_DIR = ROOT / "site"
MAX_URLS = 10_000


def load_key():
    key = os.environ.get("INDEX_NOW_KEY", "").strip()
    if not key:
        candidates = [path for path in KEY_DIR.glob("*.txt") if re.fullmatch(r"[0-9a-fA-F]{32}", path.stem)]
        candidates = [path for path in candidates if path.read_text(encoding="utf-8").strip() == path.stem]
        if len(candidates) != 1:
            raise SystemExit("IndexNow: expected exactly one valid public 32-character key file in site/")
        key = candidates[0].stem
    if not re.fullmatch(r"[0-9a-fA-F]{32}", key):
        raise SystemExit("IndexNow: key must be a 32-character hexadecimal value")
    key_file = KEY_DIR / f"{key}.txt"
    if not key_file.is_file() or key_file.read_text(encoding="utf-8").strip() != key:
        raise SystemExit("IndexNow: public key file is missing or its contents do not match the key")
    return key


def fetch_sitemap():
    req = urllib.request.Request(
        f"{BASE}/sitemap.xml",
        headers={"User-Agent": "PassiveIncomeEngine/1.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return ET.fromstring(response.read())


def submit_post(urls, key):
    if not urls or len(urls) > MAX_URLS:
        raise ValueError(f"IndexNow accepts between 1 and {MAX_URLS} URLs per request")
    if len(urls) != len(set(urls)):
        raise ValueError("IndexNow sitemap contains duplicate URLs")
    if any(not url.startswith(BASE + "/") and url != BASE for url in urls):
        raise ValueError("IndexNow sitemap contains a URL outside SITE_BASE_URL")

    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"{BASE}/{key}.txt",
        "urlList": urls,
    }
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        if response.status not in (200, 202):
            raise RuntimeError(f"IndexNow returned unexpected HTTP status {response.status}")
        return response.status


def main():
    key = load_key()
    try:
        root = fetch_sitemap()
        urls = [node.text.strip() for node in root.iter() if node.tag.endswith("loc") and node.text and node.text.strip()]
        if not urls:
            raise ValueError("Live sitemap contains no URLs")
        status = submit_post(urls, key)
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError, RuntimeError) as exc:
        detail = getattr(exc, "reason", None) or str(exc)
        raise SystemExit(f"IndexNow submission failed: {detail}") from exc
    print(f"IndexNow: submitted {len(urls)} live sitemap URLs, HTTP {status}")


if __name__ == "__main__":
    main()
