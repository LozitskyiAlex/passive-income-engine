import json
import os
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "calculators.json"
SITE = ROOT / "site" / "calculators"
BASE = os.environ.get("SITE_BASE_URL", "https://free-construction-calculators.pages.dev").rstrip("/")


def page(item: dict) -> str:
    title = escape(item["title"])
    description = escape(item["description"])
    slug = escape(item["slug"])
    formula = escape(item["formula"])

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{BASE}/calculators/{slug}/">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "{title}",
  "applicationCategory": "UtilitiesApplication",
  "description": "{description}",
  "operatingSystem": "Any"
}}
</script>
<style>
body{{font-family:system-ui,sans-serif;max-width:760px;margin:40px auto;padding:0 20px;line-height:1.5}}
.card{{border:1px solid #ddd;border-radius:12px;padding:20px;margin-top:20px}}
label{{display:block;margin-top:12px}}input{{padding:10px;width:100%;box-sizing:border-box}}
button{{margin-top:16px;padding:10px 16px;cursor:pointer}}
#result{{font-size:1.2rem;font-weight:600;margin-top:20px}}
</style>
</head>
<body>
<main>
<a href="/">Home</a>
<h1>{title}</h1>
<p>{description}</p>
<div class="card">
<label>First value <input id="a" type="number" step="any"></label>
<label>Second value <input id="b" type="number" step="any"></label>
<button id="calculate">Calculate</button>
<div id="result" aria-live="polite"></div>
</div>
<h2>Formula</h2>
<p><code>{formula}</code></p>
</main>
<script>
const slug = "{slug}";
document.querySelector("#calculate").addEventListener("click", () => {{
  const a = Number(document.querySelector("#a").value);
  const b = Number(document.querySelector("#b").value);
  const result = document.querySelector("#result");

  if (!Number.isFinite(a) || !Number.isFinite(b)) {{
    result.textContent = "Enter both values.";
    return;
  }}

  if (slug === "percentage-change") {{
    if (a === 0) {{
      result.textContent = "Original value cannot be zero.";
      return;
    }}
    result.textContent = (((b - a) / a) * 100).toFixed(2) + "%";
  }} else if (slug === "markup") {{
    result.textContent = (a * (1 + b / 100)).toFixed(2);
  }} else if (slug === "unit-price") {{
    if (b === 0) {{
      result.textContent = "Quantity cannot be zero.";
      return;
    }}
    result.textContent = (a / b).toFixed(4);
  }}
}});
</script>
</body>
</html>
"""


def main() -> None:
    items = json.loads(DATA.read_text(encoding="utf-8"))
    for item in items:
        output = SITE / item["slug"] / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(page(item), encoding="utf-8")


if __name__ == "__main__":
    main()
