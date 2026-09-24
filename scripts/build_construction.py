import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "construction_calculators.json"
CONTENT = ROOT / "data" / "calculator_content.json"
SITE = ROOT / "site" / "construction"
BASE = "https://passive-income-engine.oleksoleks07.workers.dev"

FIELDS = {
    "concrete_volume": ["Length", "Width", "Thickness"],
    "concrete_bags": ["Volume", "Bag Yield"],
    "gravel_volume": ["Length", "Width", "Depth"],
    "mulch_volume": ["Length", "Width", "Depth"],
    "paint_quantity": ["Wall Area", "Coverage per Unit", "Coats"],
    "flooring_quantity": ["Length", "Width", "Waste %"],
    "tile_quantity": ["Area", "Tile Length", "Tile Width", "Waste %"],
    "drywall_sheets": ["Room Length", "Room Width", "Wall Height", "Sheet Length", "Sheet Width"],
    "board_feet": ["Thickness", "Width", "Length", "Quantity"],
    "material_cost": ["Quantity", "Unit Price", "Waste %"],
}

def formula_js(kind):
    return {
        "concrete_volume": "return (v[0]*v[1]*v[2]).toFixed(3) + ' cubic units';",
        "concrete_bags": "return Math.ceil(v[0]/v[1]) + ' bags';",
        "gravel_volume": "return (v[0]*v[1]*v[2]).toFixed(3) + ' cubic units';",
        "mulch_volume": "return (v[0]*v[1]*v[2]).toFixed(3) + ' cubic units';",
        "paint_quantity": "return ((v[0]/v[1])*v[2]).toFixed(2) + ' units';",
        "flooring_quantity": "return (v[0]*v[1]*(1+v[2]/100)).toFixed(2) + ' square units';",
        "tile_quantity": "return Math.ceil((v[0]/(v[1]*v[2]))*(1+v[3]/100)) + ' tiles';",
        "drywall_sheets": "return Math.ceil(((2*(v[0]+v[1])*v[2])/(v[3]*v[4])));",
        "board_feet": "return ((v[0]*v[1]*v[2]/12)*v[3]).toFixed(2) + ' board feet';",
        "material_cost": "return (v[0]*v[1]*(1+v[2]/100)).toFixed(2);",
    }[kind]

def page(item, content):
    title, desc, kind = map(item.get, ["title","description","type"])
    tips = "".join(f"<li>{escape(t)}</li>" for t in content.get("tips", []))
    inputs = "".join(
        f'<label>{escape(name)}<input id="v{i}" type="number" min="0" step="any" inputmode="decimal" required></label>'
        for i, name in enumerate(FIELDS[kind])
    )
    js = formula_js(kind)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{BASE}/construction/{escape(item["slug"])}/">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebApplication","name":"{escape(title)}","applicationCategory":"UtilitiesApplication","operatingSystem":"Any","description":"{escape(desc)}"}}
</script>
<style>
body{{font-family:system-ui,sans-serif;max-width:760px;margin:40px auto;padding:0 20px;line-height:1.5}}
.card{{border:1px solid #ddd;border-radius:12px;padding:20px}}
label{{display:block;margin:12px 0 4px}}input{{padding:10px;width:100%;box-sizing:border-box}}
button{{margin-top:16px;padding:10px 16px}}#result{{margin-top:20px;font-size:1.3rem;font-weight:600}}
</style>
</head>
<body><main>
<a href="/construction/">All construction calculators</a>
<h1>{escape(title)}</h1><p>{escape(desc)}</p>
<div class="card">{inputs}<button id="calculate">Calculate</button><div id="result" aria-live="polite"></div></div>
<section><h2>How to use this calculator</h2><p>{escape(content.get("how", ""))}</p><h2>Example</h2><p>{escape(content.get("example", ""))}</p><h2>Tips</h2><ul>{tips}</ul></section><section><h2>Related calculators</h2><p><a href="/construction/">Browse all construction calculators</a></p></section><p>Use the same unit system for all dimensions. Results are estimates and should be checked against project specifications, local requirements, and manufacturer instructions.</p>
</main>
<script>
document.querySelector("#calculate").onclick=()=>{{
 const v=[...document.querySelectorAll("input")].map(x=>Number(x.value));
 const result=document.querySelector("#result");
 if(v.some(x=>!Number.isFinite(x)||x<0)){{result.textContent="Enter valid non-negative values.";return;}}
 {js}
}};
</script></body></html>"""

def main():
    items=json.loads(DATA.read_text())
    content={x["slug"]: x for x in json.loads(CONTENT.read_text(encoding="utf-8"))}
    for item in items:
        out=SITE/item["slug"]/ "index.html"
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(page(item, content.get(item["slug"], {})),encoding="utf-8")

if __name__=="__main__":
    main()
