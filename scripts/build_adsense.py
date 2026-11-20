"""Apply the site's AdSense publisher code and ads.txt entry after all pages are generated."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PUBLISHER_ID = "pub-7560850346426622"
ADSENSE_SCRIPT = (
    '<script async '
    'src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7560850346426622" '
    'crossorigin="anonymous"></script>'
)
ADSENSE_RE = re.compile(
    r"""<script\b[^>]*src=["']https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-([^"']+)["'][^>]*>\s*</script>""",
    re.IGNORECASE,
)
HEAD_RE = re.compile(r"<head(?:\s[^>]*)?>", re.IGNORECASE)


def main() -> None:
    if not SITE.is_dir():
        raise FileNotFoundError(f"Generated site directory does not exist: {SITE}")

    pages = sorted(path for path in SITE.rglob("*.html") if path.name != "404.html")
    if not pages:
        raise RuntimeError("No generated HTML pages found for AdSense integration")

    for page in pages:
        html = page.read_text(encoding="utf-8")
        existing = ADSENSE_RE.search(html)
        if existing:
            if existing.group(1) != PUBLISHER_ID.removeprefix("pub-"):
                raise RuntimeError(f"Conflicting AdSense publisher ID in {page}")
            continue

        head = HEAD_RE.search(html)
        if not head:
            raise RuntimeError(f"HTML page has no head element: {page}")
        html = html[:head.end()] + "\n" + ADSENSE_SCRIPT + html[head.end():]
        page.write_text(html, encoding="utf-8")

    (SITE / "ads.txt").write_text(
        f"google.com, {PUBLISHER_ID}, DIRECT, f08c47fec0942fa0\n",
        encoding="utf-8",
    )
    print(f"Added AdSense publisher code to {len(pages)} HTML pages and generated ads.txt")


if __name__ == "__main__":
    main()
