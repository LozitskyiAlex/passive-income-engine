import os
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = "https://passive-income-engine.oleksoleks07.workers.dev"
KEY = "1bd47cdd1ffc5c4b2caa7e4d4cc3397c"
SITE = Path(__file__).resolve().parents[1] / "site" / "sitemap.xml"

def main():
    if not SITE.exists():
        print("IndexNow: sitemap not found; skipping")
        return
    root = ET.parse(SITE).getroot()
    urls = [node.text for node in root.iter() if node.tag.endswith("loc") and node.text]
    if not urls:
        print("IndexNow: no URLs found; skipping")
        return

    payload = (
        '{"host":"passive-income-engine.oleksoleks07.workers.dev",'
        '"key":"' + KEY + '",'
        '"keyLocation":"' + BASE + '/indexnow-key.txt",'
        '"urlList":' + str(urls).replace("'", '"') + "}"
    )
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=payload.encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            print(f"IndexNow: submitted {len(urls)} URLs, HTTP {response.status}")
    except Exception as exc:
        print(f"IndexNow: submission skipped/failed: {exc}")

if __name__ == "__main__":
    main()
