import json
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = "https://passive-income-engine.oleksoleks07.workers.dev"
KEY = "00800de33f7d4649b742eaac38d8a68b"
SITE = Path(__file__).resolve().parents[1] / "site" / "sitemap.xml"

def main():
    if not SITE.exists():
        raise SystemExit("IndexNow: sitemap not found")

    root = ET.parse(SITE).getroot()
    urls = [node.text for node in root.iter() if node.tag.endswith("loc") and node.text]
    if not urls:
        raise SystemExit("IndexNow: no URLs found")

    payload = {
        "host": "passive-income-engine.oleksoleks07.workers.dev",
        "key": KEY,
        "keyLocation": BASE + "/" + KEY + ".txt",
        "urlList": urls,
    }

    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            print(f"IndexNow: submitted {len(urls)} URLs, HTTP {response.status}")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"IndexNow: HTTP {exc.code}: {body}") from exc

if __name__ == "__main__":
    main()
