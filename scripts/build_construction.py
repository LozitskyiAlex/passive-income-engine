import json
import os
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "construction_calculators.json"
CONTENT = ROOT / "data" / "calculator_content.json"
RELATED = ROOT / "data" / "related_calculators.json"
UNITS = ROOT / "data" / "calculator_units.json"
FAQ = ROOT / "data" / "calculator_faq.json"
SITE = ROOT / "site" / "construction"
BASE = os.environ.get("SITE_BASE_URL", "https://free-construction-calculators.pages.dev").rstrip("/")

FIELDS = {
    "concrete_volume":["Length","Width","Thickness"],"concrete_bags":["Volume","Bag Yield"],
    "gravel_volume":["Length","Width","Depth"],"mulch_volume":["Length","Width","Depth"],
    "paint_quantity":["Wall Area","Coverage per Unit","Coats"],"flooring_quantity":["Length","Width","Waste %"],
    "tile_quantity":["Area","Tile Length","Tile Width","Waste %"],
    "drywall_sheets":["Room Length","Room Width","Wall Height","Sheet Length","Sheet Width"],
    "board_feet":["Thickness","Width","Length","Quantity"],"material_cost":["Quantity","Unit Price","Waste %"],
    "paver_quantity":["Area Length (ft)","Area Width (ft)","Paver Length (in)","Paver Width (in)","Waste %"],
    "sand_volume":["Length","Width","Depth"],"soil_volume":["Length","Width","Depth"],
    "fence_pickets":["Fence Length (ft)","Picket Width (in)","Gap (in)"],"fence_posts":["Fence Length (ft)","Post Spacing (ft)"],
    "decking_boards":["Deck Length (ft)","Deck Width (ft)","Board Width (in)","Gap (in)","Board Length (ft)","Waste %"],
    "roofing_squares":["Roof Area (sq ft)"],"roofing_material":["Roof Area (sq ft)","Waste %"],
    "gravel_weight":["Volume","Bulk Density"],"concrete_weight":["Volume","Density"],
    "concrete_footing":["Length","Width","Depth"],"rebar_length":["Number of Bars","Length per Bar"],
    "gravel_bags":["Required Volume","Bag Coverage"],"baseboard":["Total Length","Board Length"],
    "wallpaper":["Wall Area","Coverage per Roll"],"stair_risers":["Total Rise","Riser Height"],
    "asphalt_volume":["Length","Width","Depth"],"cubic_yards":["Length","Width","Depth"],
    "area":["Length","Width"],"volume":["Length","Width","Height"],
}


# Every calculator accepts values in canonical US customary base units internally.
# The browser adapter converts metric input to these units before calculation.
INPUT_DIMENSIONS = {
    "concrete_volume": ["length_ft", "length_ft", "length_ft"],
    "concrete_bags": ["volume_cuft", "volume_cuft"],
    "gravel_volume": ["length_ft", "length_ft", "length_ft"],
    "mulch_volume": ["length_ft", "length_ft", "length_ft"],
    "paint_quantity": ["area_sqft", "area_sqft", ""],
    "flooring_quantity": ["length_ft", "length_ft", ""],
    "tile_quantity": ["area_sqft", "length_in", "length_in", ""],
    "drywall_sheets": ["length_ft", "length_ft", "length_ft", "length_ft", "length_ft"],
    "board_feet": ["length_in", "length_in", "length_ft", ""],
    "material_cost": ["", "", ""],
    "paver_quantity": ["length_ft", "length_ft", "length_in", "length_in", ""],
    "sand_volume": ["length_ft", "length_ft", "length_ft"],
    "soil_volume": ["length_ft", "length_ft", "length_ft"],
    "fence_pickets": ["length_ft", "length_in", "length_in"],
    "fence_posts": ["length_ft", "length_ft"],
    "decking_boards": ["length_ft", "length_ft", "length_in", "length_in", "length_ft", ""],
    "roofing_squares": ["area_sqft"],
    "roofing_material": ["area_sqft", ""],
    "gravel_weight": ["volume_cuft", "density_lb_cuft"],
    "concrete_weight": ["volume_cuft", "density_lb_cuft"],
    "concrete_footing": ["length_ft", "length_ft", "length_ft"],
    "rebar_length": ["", "length_ft"],
    "gravel_bags": ["volume_cuft", "volume_cuft"],
    "baseboard": ["length_ft", "length_ft"],
    "wallpaper": ["area_sqft", "area_sqft"],
    "stair_risers": ["length_in", "length_in"],
    "asphalt_volume": ["length_ft", "length_ft", "length_ft"],
    "cubic_yards": ["length_ft", "length_ft", "length_ft"],
    "area": ["length_ft", "length_ft"],
    "volume": ["length_ft", "length_ft", "length_ft"],
}

FORMULAS = {
    "concrete_volume":"result.textContent=(v[0]*v[1]*v[2]).toFixed(3)+' cubic units';",
    "concrete_bags":"result.textContent=Math.ceil(v[0]/v[1])+' bags';",
    "gravel_volume":"const cubicFeet=v[0]*v[1]*v[2];result.textContent=cubicFeet.toFixed(2)+' cu ft ('+(cubicFeet/27).toFixed(2)+' cu yd)';",
    "mulch_volume":"result.textContent=(v[0]*v[1]*v[2]).toFixed(3)+' cubic units';",
    "paint_quantity":"result.textContent=((v[0]/v[1])*v[2]).toFixed(2)+' units';",
    "flooring_quantity":"result.textContent=(v[0]*v[1]*(1+v[2]/100)).toFixed(2)+' square units';",
    "tile_quantity":"result.textContent=Math.ceil(((v[0]*144)/(v[1]*v[2]))*(1+v[3]/100)-1e-9)+' tiles';",
    "drywall_sheets":"result.textContent=Math.ceil((2*(v[0]+v[1])*v[2])/(v[3]*v[4]))+' sheets';",
    "board_feet":"result.textContent=((v[0]*v[1]*v[2]/12)*v[3]).toFixed(2)+' board feet';",
    "material_cost":"result.textContent=(v[0]*v[1]*(1+v[2]/100)).toFixed(2);",
    "paver_quantity":"result.textContent=Math.ceil(((v[0]*v[1])*144/(v[2]*v[3]))*(1+v[4]/100))+' pavers';",
    "sand_volume":"result.textContent=(v[0]*v[1]*v[2]).toFixed(3)+' cubic units';",
    "soil_volume":"result.textContent=(v[0]*v[1]*v[2]).toFixed(3)+' cubic units';",
    "fence_pickets":"result.textContent=Math.ceil((v[0]*12)/(v[1]+v[2]))+' pickets';",
    "fence_posts":"result.textContent=(Math.ceil(v[0]/v[1])+1)+' posts';",
    "decking_boards":"const rows=Math.ceil((v[1]*12)/(v[2]+v[3]));const perRow=Math.ceil(v[0]/v[4]);result.textContent=Math.ceil(rows*perRow*(1+v[5]/100))+' boards';",
    "roofing_squares":"result.textContent=(v[0]/100).toFixed(2)+' roofing squares';",
    "roofing_material":"result.textContent=(v[0]*(1+v[1]/100)).toFixed(2)+' sq ft';",
    "gravel_weight":"result.textContent=(v[0]*v[1]).toFixed(2)+' weight units';",
    "concrete_weight":"result.textContent=(v[0]*v[1]).toFixed(2)+' weight units';",
    "concrete_footing":"result.textContent=(v[0]*v[1]*v[2]).toFixed(3)+' cubic units';",
    "rebar_length":"result.textContent=(v[0]*v[1]).toFixed(2)+' length units';",
    "gravel_bags":"result.textContent=Math.ceil(v[0]/v[1])+' bags';",
    "baseboard":"result.textContent=Math.ceil(v[0]/v[1])+' boards';",
    "wallpaper":"result.textContent=Math.ceil(v[0]/v[1])+' rolls';",
    "stair_risers":"result.textContent=Math.ceil(v[0]/v[1])+' risers';",
    "asphalt_volume":"result.textContent=(v[0]*v[1]*v[2]).toFixed(3)+' cubic units';",
    "cubic_yards":"result.textContent=((v[0]*v[1]*v[2])/27).toFixed(3)+' cubic yards';",
    "area":"result.textContent=(v[0]*v[1]).toFixed(2)+' square units';",
    "volume":"result.textContent=(v[0]*v[1]*v[2]).toFixed(3)+' cubic units';",
}

EXAMPLES = {
"concrete_volume":([20,10,0.5],"100 cubic units"),"concrete_bags":([33.33,0.6],"56 bags"),
"gravel_volume":([20,10,0.25],"50.00 cu ft (1.85 cu yd)"),"mulch_volume":([20,10,0.25],"50 cubic units"),
"paint_quantity":([800,350,2],"4.57 units"),"flooring_quantity":([20,15,10],"330 square units"),
"tile_quantity":([1000,12,12,10],"1100 tiles"),"drywall_sheets":([20,15,8,4,8],"18 sheets"),
"board_feet":([2,6,8,1],"8 board feet"),"material_cost":([100,4,10],"440"),
"paver_quantity":([20,12,12,6,5],"504 pavers"),"sand_volume":([20,10,0.1],"20 cubic units"),
"soil_volume":([10,10,0.5],"50 cubic units"),"fence_pickets":([100,5.5,1.5],"172 pickets"),
"fence_posts":([100,8],"14 posts"),"decking_boards":([20,12,6,0.125,12,0],"48 boards"),
"roofing_squares":([2400],"24 roofing squares"),"roofing_material":([2400,10],"2640 sq ft"),
"gravel_weight":([10,1.6],"16 weight units"),"concrete_weight":([10,150],"1500 weight units"),
"concrete_footing":([20,1,0.5],"10 cubic units"),"rebar_length":([20,4],"80 length units"),
"gravel_bags":([10,0.5],"20 bags"),"baseboard":([100,8],"13 boards"),"wallpaper":([120,25],"5 rolls"),
"stair_risers":([96,8],"12 risers"),"asphalt_volume":([20,10,0.2],"40 cubic units"),
"cubic_yards":([27,1,1],"1 cubic yard"),"area":([20,15],"300 square units"),"volume":([20,15,2],"600 cubic units")
}

POSITIVE = {k:list(range(len(v))) for k,v in FIELDS.items()}
for k in ["flooring_quantity","material_cost","roofing_material"]:
    POSITIVE[k]=list(range(len(FIELDS[k])-1))
for k in ["tile_quantity","paver_quantity","decking_boards"]:
    POSITIVE[k]=list(range(len(FIELDS[k])-1))

def page(item, content, related, titles, units, faq):
    title, desc, kind = item["title"], item["description"], item["type"]

    seo_title = f"{title} | Free Estimate Tool"
    seo_desc = f"{desc} Enter your measurements, calculate the estimate, and review practical guidance before ordering materials."
    formula_text = {
        "concrete_volume":"Concrete volume = length × width × thickness.",
        "concrete_bags":"Bags needed = required volume ÷ yield per bag, rounded up.",
        "gravel_volume":"Volume = length × width × depth. The result is displayed in the selected measurement system.",
        "mulch_volume":"Mulch volume = length × width × depth.",
        "paint_quantity":"Paint quantity = wall area ÷ coverage per unit × number of coats.",
        "flooring_quantity":"Flooring required = length × width × (1 + waste percentage ÷ 100).",
        "tile_quantity":"Tiles needed = project area ÷ tile area × (1 + waste percentage ÷ 100), rounded up. Use compatible units for area and tile dimensions.",
        "drywall_sheets":"Sheets needed = wall surface area ÷ sheet area, rounded up.",
        "board_feet":"Lumber volume = thickness × width × length × quantity. The result is displayed in the selected measurement system.",
        "material_cost":"Material cost = quantity × unit price × (1 + waste percentage ÷ 100).",
        "paver_quantity":"Pavers needed = project area ÷ paver area × (1 + waste percentage ÷ 100), rounded up.",
        "sand_volume":"Sand volume = length × width × depth.",
        "soil_volume":"Soil volume = length × width × depth.",
        "fence_pickets":"Pickets needed = fence length ÷ (picket width + gap), rounded up. Use compatible units for all dimensions.",
        "fence_posts":"Posts needed = ceiling(fence length ÷ post spacing) + 1.",
        "decking_boards":"Boards needed = board rows × boards per row, adjusted by the selected waste percentage.",
        "roofing_squares":"Roofing material area is shown in the selected measurement system.",
        "roofing_material":"Roofing material area = roof area × (1 + waste percentage ÷ 100).",
        "gravel_weight":"Estimated weight = volume × bulk density.",
        "concrete_weight":"Estimated weight = volume × concrete density.",
        "concrete_footing":"Footing volume = length × width × depth.",
        "rebar_length":"Total rebar length = number of bars × length per bar.",
        "gravel_bags":"Bags needed = required volume ÷ coverage per bag, rounded up.",
        "baseboard":"Boards needed = total length ÷ board length, rounded up.",
        "wallpaper":"Rolls needed = wall area ÷ coverage per roll, rounded up.",
        "stair_risers":"Risers = total rise ÷ planned riser height, rounded up.",
        "asphalt_volume":"Asphalt volume = length × width × depth.",
        "cubic_yards":"Volume = length × width × depth, converted to the selected output unit.",
        "area":"Area = length × width.",
        "volume":"Volume = length × width × height."
    }[kind]
    unit_list=units.get(kind,[""]*len(FIELDS[kind]))
    inputs="".join(f'<label><span class="field-name">{escape(name)}</span> <span class="unit" data-dimension="{INPUT_DIMENSIONS[kind][i]}">{escape(unit_list[i])}</span><input id="v{i}" type="number" min="0" step="any" inputmode="decimal" required></label>' for i,name in enumerate(FIELDS[kind]))
    faq_html="".join(f"<details><summary>{escape(x['question'])}</summary><p>{escape(x['answer'])}</p></details>" for x in faq.get("faqs",[]))
    faq_schema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":x["question"],"acceptedAnswer":{"@type":"Answer","text":x["answer"]}} for x in faq.get("faqs",[])]}
    related_html="".join(f'<li><a href="/construction/{escape(slug)}/">{escape(titles.get(slug,slug))}</a></li>' for slug in related.get(item["slug"],[]))
    values,result=EXAMPLES[kind]
    example_values_json=json.dumps(values)
    example_inputs=""
    tips="".join(f"<li>{escape(t)}</li>" for t in content.get("tips",[]))
    positive_js=json.dumps(POSITIVE[kind])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(seo_title)}</title><meta name="description" content="{escape(seo_desc)}"><link rel="canonical" href="{BASE}/construction/{escape(item["slug"])}/">
<meta property="og:type" content="website"><meta property="og:title" content="{escape(seo_title)}"><meta property="og:description" content="{escape(seo_desc)}"><meta property="og:url" content="{BASE}/construction/{escape(item["slug"])}/">
<meta name="twitter:card" content="summary"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token":"2b43ef087bbd47b6847bb0613f03ace2"}}'></script>
<script type="application/ld+json">{json.dumps(faq_schema,separators=(',',':'))}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{BASE}/"}},{{"@type":"ListItem","position":2,"name":"Construction Calculators","item":"{BASE}/construction/"}},{{"@type":"ListItem","position":3,"name":"{escape(title)}","item":"{BASE}/construction/{escape(item["slug"])}/"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"{escape(title)}","applicationCategory":"UtilitiesApplication","operatingSystem":"Any","description":"{escape(desc)}"}}</script>
<style>*{{box-sizing:border-box}}body{{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:820px;margin:0 auto;padding:32px 20px;line-height:1.55;color:#17202a}}.card{{border:1px solid #ddd;border-radius:12px;padding:20px}}label{{display:block;margin:12px 0 4px}}.unit{{color:#667;font-size:.85rem}}input{{padding:10px;width:100%}}button{{margin-top:16px;padding:11px 16px;margin-right:8px;border:1px solid #9aa5ae;border-radius:8px;background:#f5f7f9;font:inherit}}#result{{margin-top:18px;min-height:1.5em;font-size:1.25rem;font-weight:650}}details{{border-top:1px solid #e2e6ea;padding:12px 0}}summary{{cursor:pointer;font-weight:650}}.example{{background:#f7f9fb;border-left:4px solid #9aa5ae;padding:14px 16px;border-radius:6px}}@media(max-width:560px){{body{{padding:20px 14px}}button{{width:100%;margin-right:0}}}}</style></head>
<body><main><nav aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/construction/">Construction Calculators</a> / {escape(title)}</nav><h1>{escape(title)}</h1><p>{escape(desc)}</p>
<div class="card"><label>Measurement system <select id="measurement-system"><option value="metric">Metric</option><option value="us">US customary</option></select></label><div class="calculator-fields">{inputs}</div><button id="calculate">Calculate</button><button id="reset" type="button">Reset</button><div id="result" aria-live="polite"></div></div>
<section><h2>Calculation example</h2><div class="example"><p><strong>Inputs:</strong> <span id="example-inputs" data-values='{escape(example_values_json)}'></span></p><p><strong>Result:</strong> <span id="example-result"></span></p></div>
<h2>Formula</h2><p>{escape(formula_text)}</p>
<h2>How to use this calculator</h2><p>{escape(content.get("how",""))}</p>
<h2>Before you calculate</h2><p>Measure the project dimensions as accurately as practical and keep all measurements in compatible units. For material products, use the coverage, yield, density, or package size stated by the manufacturer or supplier rather than a generic assumption.</p><p>Choose the waste allowance based on the project shape, installation method, cutting requirements, and material characteristics. A simple rectangular estimate may need adjustment for openings, corners, slopes, joints, patterns, compaction, or other site conditions.</p>
<h2>Understanding the result</h2><p>The calculator provides a planning estimate based on the inputs shown above. It is not a substitute for project drawings, structural design, manufacturer instructions, or local requirements. Before ordering, compare the calculated quantity with the supplier's package sizes and ordering units.</p>
<h2>Tips</h2><ul>{tips}</ul></section>
<section><h2>Frequently asked questions</h2>{faq_html}</section><section><h2>Related calculators</h2><ul>{related_html}</ul><p><a href="/construction/">Browse all construction calculators</a></p></section>
<p>Use compatible units and verify estimates against project specifications, local requirements and manufacturer instructions.</p></main>
<script type="module">
import {{ calculateRegional, formatRegionalInput }} from "/calculator-runtime.js";
const kind="{kind}";
const systemSelect=document.querySelector("#measurement-system");
const defaultSystem=document.documentElement.dataset.measurement||"us";
systemSelect.value=defaultSystem;
function renderRegionalUnits(){{
 const system=systemSelect.value;
 document.querySelectorAll(".unit[data-dimension]").forEach(node=>{{node.textContent=formatRegionalInput(node.dataset.dimension,system);}});
 const exampleValues=JSON.parse(document.querySelector("#example-inputs").dataset.values);
 const labels=[...document.querySelectorAll(".calculator-fields .field-name")].map(node=>node.textContent.trim());
 const dimensions=[...document.querySelectorAll(".unit[data-dimension]")].map(node=>node.dataset.dimension);
 const displayedExampleValues=exampleValues.map((value,i)=>system==="metric"?Number(formatRegionalInputValue(value,dimensions[i],system)):value);
 document.querySelector("#example-inputs").textContent=displayedExampleValues.map((value,i)=>{{const shown=formatRegionalInput(dimensions[i],system);const converted=Number(value.toFixed(3)).toString();return labels[i]+": "+converted+(shown?" "+shown:"");}}).join(", ");
 document.querySelector("#example-result").textContent=calculateRegional(kind,displayedExampleValues,system);
}}
function formatRegionalInputValue(value,dimension,system){{
 if(system!=="metric")return String(value);
 const factors={{length_ft:1/3.280839895013123,length_in:25.4,area_sqft:1/10.763910416709722,volume_cuft:1/35.31466672148859,density_lb_cuft:16.01846337396014}};
 const converted=value*(factors[dimension]||1);
 return Number(converted.toFixed(3)).toString();
}}
systemSelect.addEventListener("change",renderRegionalUnits);
renderRegionalUnits();
document.querySelector("#calculate").onclick=()=>{{const v=[...document.querySelectorAll(".calculator-fields input")].map(x=>Number(x.value));const result=document.querySelector("#result");if(v.some(x=>!Number.isFinite(x)||x<0)){{result.textContent="Enter valid non-negative numbers.";return;}}const positive={positive_js};if(positive.some(i=>v[i]<=0)){{result.textContent="Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.";return;}}result.textContent=calculateRegional(kind,v,systemSelect.value);}};
document.querySelector("#reset").onclick=()=>{{document.querySelectorAll(".calculator-fields input").forEach(x=>x.value="");document.querySelector("#result").textContent="";}};
</script></body></html>"""

def main():
    items=json.loads(DATA.read_text(encoding="utf-8"))
    content={x["slug"]:x for x in json.loads(CONTENT.read_text(encoding="utf-8"))}
    related=json.loads(RELATED.read_text(encoding="utf-8"))
    units=json.loads(UNITS.read_text(encoding="utf-8"))
    faq={x["slug"]:x for x in json.loads(FAQ.read_text(encoding="utf-8"))}
    titles={x["slug"]:x["title"] for x in items}
    for item in items:
        out=SITE/item["slug"]/"index.html"; out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(page(item,content[item["slug"]],related,titles,units,faq[item["slug"]]),encoding="utf-8")

    runtime = """// Generated from the same formula snippets used by calculator pages.
const formulas = {
""" + "\n".join(
        f'  "{kind}": (v) => {{ const result = {{ textContent: "" }}; {formula} return result.textContent; }},'
        for kind, formula in FORMULAS.items()
    ) + """
};

export function calculate(kind, values) {
  const formula = formulas[kind];
  if (!formula) throw new Error("Unknown calculator type: " + kind);
  return formula(values);
}

const inputDimensions = {"concrete_volume": ["length_ft", "length_ft", "length_ft"], "concrete_bags": ["volume_cuft", "volume_cuft"], "gravel_volume": ["length_ft", "length_ft", "length_ft"], "mulch_volume": ["length_ft", "length_ft", "length_ft"], "paint_quantity": ["area_sqft", "area_sqft", ""], "flooring_quantity": ["length_ft", "length_ft", ""], "tile_quantity": ["area_sqft", "length_in", "length_in", ""], "drywall_sheets": ["length_ft", "length_ft", "length_ft", "length_ft", "length_ft"], "board_feet": ["length_in", "length_in", "length_ft", ""], "material_cost": ["", "", ""], "paver_quantity": ["length_ft", "length_ft", "length_in", "length_in", ""], "sand_volume": ["length_ft", "length_ft", "length_ft"], "soil_volume": ["length_ft", "length_ft", "length_ft"], "fence_pickets": ["length_ft", "length_in", "length_in"], "fence_posts": ["length_ft", "length_ft"], "decking_boards": ["length_ft", "length_ft", "length_in", "length_in", "length_ft", ""], "roofing_squares": ["area_sqft"], "roofing_material": ["area_sqft", ""], "gravel_weight": ["volume_cuft", "density_lb_cuft"], "concrete_weight": ["volume_cuft", "density_lb_cuft"], "concrete_footing": ["length_ft", "length_ft", "length_ft"], "rebar_length": ["", "length_ft"], "gravel_bags": ["volume_cuft", "volume_cuft"], "baseboard": ["length_ft", "length_ft"], "wallpaper": ["area_sqft", "area_sqft"], "stair_risers": ["length_in", "length_in"], "asphalt_volume": ["length_ft", "length_ft", "length_ft"], "cubic_yards": ["length_ft", "length_ft", "length_ft"], "area": ["length_ft", "length_ft"], "volume": ["length_ft", "length_ft", "length_ft"]};
const metricToUs = { length_ft: 3.280839895013123, length_in: 1/25.4, area_sqft: 10.763910416709722, volume_cuft: 35.31466672148859, density_lb_cuft: 1/16.01846337396014 };
const metricSymbols = { length_ft: "m", length_in: "mm", area_sqft: "m²", volume_cuft: "m³", density_lb_cuft: "kg/m³" };
const usSymbols = { length_ft: "ft", length_in: "in", area_sqft: "sq ft", volume_cuft: "cu ft", density_lb_cuft: "lb/cu ft" };
const outputDimensions = { concrete_volume: "volume_cuft", gravel_volume: "volume_cuft", mulch_volume: "volume_cuft", sand_volume: "volume_cuft", soil_volume: "volume_cuft", concrete_footing: "volume_cuft", asphalt_volume: "volume_cuft", volume: "volume_cuft", flooring_quantity: "area_sqft", roofing_material: "area_sqft", area: "area_sqft", roofing_squares: "roofing_squares", gravel_weight: "weight_lb", concrete_weight: "weight_lb", rebar_length: "length_ft", cubic_yards: "volume_yd", board_feet: "board_feet" };
const outputMetric = { volume_cuft: [0.028316846592, "m³"], area_sqft: [0.09290304, "m²"], weight_lb: [0.45359237, "kg"], length_ft: [0.3048, "m"], volume_yd: [0.764554857984, "m³"], roofing_squares: [9.290304, "m²"], board_feet: [0.002359737216, "m³"] };
export function formatRegionalInput(dimension, system) { return dimension ? (system === "metric" ? metricSymbols[dimension] : usSymbols[dimension]) || "" : ""; }
export function calculateRegional(kind, values, system="us") {
  const dims = inputDimensions[kind] || [];
  const normalized = values.map((value, index) => system === "metric" ? value * (metricToUs[dims[index]] || 1) : value);
  const result = calculate(kind, normalized);
  if (system !== "metric") return result;
  const dimension = outputDimensions[kind];
  if (!dimension) return result;
  if (dimension === "roofing_squares") return (normalized[0] * 0.09290304).toFixed(2) + " m²";
  const [factor, unit] = outputMetric[dimension];
  const numeric = Number.parseFloat(String(result));
  if (!Number.isFinite(numeric)) return result;
  return (numeric * factor).toFixed(3) + " " + unit;
}
"""
    (SITE.parent / "calculator-runtime.js").write_text(runtime, encoding="utf-8")

if __name__=="__main__":
    main()
