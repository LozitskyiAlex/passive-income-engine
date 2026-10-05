import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = os.environ.get("SITE_BASE_URL", "https://free-construction-calculators.pages.dev").rstrip("/")
HOST = BASE.removeprefix("https://").removeprefix("http://")
KEY = os.environ.get("INDEX_NOW_KEY")
if not KEY:
    raise SystemExit("IndexNow: INDEX_NOW_KEY environment variable is required")
KEY_LOCATION = f"{BASE}/{KEY}.txt"
SITE = Path(__file__).resolve().parents[1] / "site" / "sitemap.xml"


def submit_post(urls):
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
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.status


def submit_get(url):
    params = urllib.parse.urlencode(
        {
            "url": url,
            "key": KEY,
            "keyLocation": KEY_LOCATION,
        }
    )
    endpoint = f"https://www.bing.com/indexnow?{params}"
    req = urllib.request.Request(endpoint, headers={"User-Agent": "PassiveIncomeEngine/1.0"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.status


def main():
    if not SITE.exists():
        raise SystemExit("IndexNow: sitemap not found")

    root = ET.parse(SITE).getroot()
    urls = [node.text for node in root.iter() if node.tag.endswith("loc") and node.text]
    if not urls:
        raise SystemExit("IndexNow: no URLs found")

    try:
        status = submit_post(urls)
        print(f"IndexNow: submitted {len(urls)} URLs via global endpoint, HTTP {status}")
        return
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"IndexNow global endpoint failed: HTTP {exc.code}: {body}")
        if exc.code != 403:
            raise SystemExit(f"IndexNow: HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        print(f"IndexNow global endpoint connection failed: {exc}")

    # Bing documents the direct /indexnow GET endpoint as an alternative.
    # Use it as a fallback if the global endpoint rejects a batch submission.
    fallback_urls = [urls[0]]
    if len(urls) > 1:
        fallback_urls.append(urls[1])

    successful = 0
    for url in fallback_urls:
        try:
            status = submit_get(url)
            print(f"IndexNow: fallback submitted {url}, HTTP {status}")
            successful += 1
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            print(f"IndexNow fallback failed for {url}: HTTP {exc.code}: {body}")
        except urllib.error.URLError as exc:
            print(f"IndexNow fallback connection failed for {url}: {exc}")

    if successful == 0:
        raise SystemExit("IndexNow: both global POST and Bing GET fallback failed")


if __name__ == "__main__":
    main()
