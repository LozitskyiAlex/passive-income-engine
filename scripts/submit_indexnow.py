import json
import os
import urllib.error
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = os.environ.get("SITE_BASE_URL", "https://free-construction-calculators.pages.dev").rstrip("/")
HOST = BASE.removeprefix("https://").removeprefix("http://")
KEY = os.environ.get("INDEX_NOW_KEY", "").strip()
KEY_LOCATION = f"{BASE}/{KEY}.txt"
SITE = Path(__file__).resolve().parents[1] / "site" / "sitemap.xml"
MAX_URLS = 10_000


def submit_post(urls):
    if not urls or len(urls) > MAX_URLS:
        raise ValueError(f"IndexNow accepts between 1 and {MAX_URLS} URLs per request")
    if len(urls) != len(set(urls)):
        raise ValueError("IndexNow sitemap contains duplicate URLs")
    if any(not url.startswith(BASE + "/") and url != BASE for url in urls):
        raise ValueError("IndexNow sitemap contains a URL outside SITE_BASE_URL")

    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
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
    if not KEY:
        raise SystemExit("IndexNow: INDEX_NOW_KEY environment variable is required")
    if not SITE.exists():
        raise SystemExit("IndexNow: sitemap not found")

    root = ET.parse(SITE).getroot()
    urls = [node.text.strip() for node in root.iter() if node.tag.endswith("loc") and node.text and node.text.strip()]
    if not urls:
        raise SystemExit("IndexNow: no URLs found")

    try:
        status = submit_post(urls)
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError, RuntimeError) as exc:
        detail = getattr(exc, "reason", None) or str(exc)
        raise SystemExit(f"IndexNow submission failed: {detail}") from exc
    print(f"IndexNow: submitted {len(urls)} sitemap URLs, HTTP {status}")


if __name__ == "__main__":
    main()
