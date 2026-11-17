import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_every_calculator_has_content():
    calculators = json.loads((ROOT / "data" / "construction_calculators.json").read_text())
    content = {x["slug"]: x for x in json.loads((ROOT / "data" / "calculator_content.json").read_text())}
    assert {x["slug"] for x in calculators} == set(content)
    for item in content.values():
        assert item["how"]
        assert item["example"]
        assert item["tips"]

def test_priority_calculators_have_detailed_guidance_and_faqs():
    priority = {"concrete-volume", "concrete-bags", "gravel-volume", "paint-quantity", "flooring-quantity", "tile-quantity", "drywall-sheets", "paver-quantity", "roofing-material", "material-cost"}
    content = {x["slug"]: x for x in json.loads((ROOT / "data" / "calculator_content.json").read_text())}
    faqs = {x["slug"]: x["faqs"] for x in json.loads((ROOT / "data" / "calculator_faq.json").read_text())}
    for slug in priority:
        assert len(content[slug]["how"]) >= 250, slug
        assert len(content[slug]["example"]) >= 180, slug
        assert len(content[slug]["tips"]) >= 3, slug
        assert len(faqs[slug]) >= 4, slug

def test_priority_calculator_guidance_is_translated_for_all_metric_locales():
    locales = ["es", "de", "fr", "pt_br", "ja", "it", "nl", "pl", "zh_hans", "ko", "ar", "uk", "ru", "tr"]
    priority = {"concrete-volume", "concrete-bags", "gravel-volume", "paint-quantity", "flooring-quantity", "tile-quantity", "drywall-sheets", "paver-quantity", "roofing-material", "material-cost"}
    for locale in locales:
        path = ROOT / "data" / "locales" / "calculator_guidance" / f"{locale}.json"
        guidance = json.loads(path.read_text(encoding="utf-8"))
        assert priority <= set(guidance), locale
        for slug in priority:
            item = guidance[slug]
            assert item["how"].strip(), (locale, slug, "how")
            assert item["example"].strip(), (locale, slug, "example")
            assert item["example_heading"].strip(), (locale, slug, "example_heading")

def test_priority_tips_and_faq_are_translated_for_all_metric_locales():
    locales = ["es", "de", "fr", "pt_br", "ja", "it", "nl", "pl", "zh_hans", "ko", "ar", "uk", "ru", "tr"]
    priority = {"concrete-volume", "concrete-bags", "gravel-volume", "paint-quantity", "flooring-quantity", "tile-quantity", "drywall-sheets", "paver-quantity", "roofing-material", "material-cost"}
    tips = {x["slug"]: x["tips"] for x in json.loads((ROOT / "data" / "calculator_content.json").read_text(encoding="utf-8")) if x["slug"] in priority}
    faqs = {x["slug"]: x["faqs"] for x in json.loads((ROOT / "data" / "calculator_faq.json").read_text(encoding="utf-8")) if x["slug"] in priority}
    for locale in locales:
        translations = json.loads((ROOT / "data" / "locales" / f"{locale}.json").read_text(encoding="utf-8"))
        for slug in priority:
            for tip in tips[slug]:
                assert translations.get(tip, "").strip(), (locale, slug, "missing tip translation")
            for faq in faqs[slug]:
                assert translations.get(faq["question"], "").strip(), (locale, slug, "missing FAQ question translation")
                assert translations.get(faq["answer"], "").strip(), (locale, slug, "missing FAQ answer translation")
