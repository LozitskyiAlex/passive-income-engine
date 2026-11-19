import json
from datetime import date
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from passive_income_engine.construction import calculate

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE = "https://free-construction-calculators.pages.dev"


def assert_canonical(html, expected):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("link", rel="canonical")
    assert tag is not None and tag.get("href") == expected


def test_all_calculator_formulas():
    cases = {
        "concrete_volume": ([20, 10, 0.5], 100),
        "concrete_bags": ([10, 0.6], 17),
        "gravel_volume": ([20, 10, 0.25], 50),
        "mulch_volume": ([20, 10, 0.25], 50),
        "paint_quantity": ([800, 350, 2], 800 / 350 * 2),
        "flooring_quantity": ([20, 15, 10], 330),
        "tile_quantity": ([1000, 12, 12, 10], 1100),
        "drywall_sheets": ([20, 15, 8, 4, 8], 18),
        "board_feet": ([2, 6, 8, 1], 8),
        "material_cost": ([100, 4, 10], 440),
        "paver_quantity": ([20, 12, 12, 6, 5], 504),
        "sand_volume": ([20, 10, 0.1], 20),
        "soil_volume": ([10, 10, 0.5], 50),
        "fence_pickets": ([100, 5.5, 1.5], 172),
        "fence_posts": ([100, 8], 14),
        "decking_boards": ([20, 12, 6, 0.125, 12, 0], 48),
        "roofing_squares": ([2400], 24),
        "roofing_material": ([2400, 10], 2640),
        "gravel_weight": ([10, 1.6], 16),
        "concrete_weight": ([10, 150], 1500),
        "concrete_footing": ([20, 1, 0.5], 10),
        "rebar_length": ([20, 4], 80),
        "gravel_bags": ([10, 0.5], 20),
        "baseboard": ([100, 8], 13),
        "wallpaper": ([120, 25], 5),
        "stair_risers": ([96, 8], 12),
        "asphalt_volume": ([20, 10, 0.2], 40),
        "cubic_yards": ([27, 1, 1], 1),
        "area": ([20, 15], 300),
        "volume": ([20, 15, 2], 600),
    }
    for kind, (values, expected) in cases.items():
        actual = calculate(kind, values)
        assert abs(actual - expected) < 1e-9, (kind, actual, expected)


def test_generated_urls_match_catalog():
    subprocess.run(["python", "scripts/build.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "scripts/build_calculators.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "scripts/build_construction.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "scripts/build_construction_index.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "scripts/build_seo.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "scripts/build_blog.py"], cwd=ROOT, check=True)
    items = json.loads((ROOT / "data/construction_calculators.json").read_text())
    guides = json.loads((ROOT / "data/guides.json").read_text())
    locales = {"en": "en", "es": "es", "de": "de", "fr": "fr", "pt-br": "pt-BR", "ja": "ja", "it": "it", "nl": "nl", "pl": "pl", "zh-hans": "zh-Hans", "ko": "ko", "ar": "ar", "uk": "uk", "ru": "ru", "tr": "tr"}
    source_paths = {"/", "/construction/", "/blog/"}
    source_paths |= {f"/blog/{x['slug']}/" for x in __import__("scripts.build_blog", fromlist=["POSTS"]).POSTS}
    source_paths |= {f"/construction/{x['slug']}/" for x in items}
    source_paths |= {f"/guides/{x['slug']}/" for x in guides}
    source_paths |= {f"/calculators/{x['slug']}/" for x in json.loads((ROOT / "data/calculators.json").read_text())}
    expected = set()
    for path in source_paths:
        for locale in locales:
            localized = path if locale == "en" else f"/{locale}{'/' if path == '/' else path}"
            expected.add(BASE + localized)
    root = ET.fromstring((SITE / "sitemap.xml").read_text())
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    actual = {node.text for node in root.findall("sm:url/sm:loc", ns)}
    for node in root.findall("sm:url", ns):
        lastmod = node.find("sm:lastmod", ns)
        assert lastmod is not None and lastmod.text
        assert date.fromisoformat(lastmod.text) <= date.today()
    assert actual == expected
    assert len(actual) == len(source_paths) * len(locales)
    for locale, lang in locales.items():
        for path in source_paths:
            localized = path if locale == "en" else f"/{locale}{'/' if path == '/' else path}"
            rel = localized.lstrip("/") or "index.html"
            if rel.endswith("/"):
                rel += "index.html"
            page = SITE / rel
            assert page.exists(), (locale, path, page)
            html = page.read_text(encoding="utf-8")
            from bs4 import BeautifulSoup
            parsed = BeautifulSoup(html, "html.parser")
            assert parsed.html.get("lang") == lang
            if locale == "ar":
                assert parsed.html.get("dir") == "rtl"
            assert_canonical(html, BASE + localized)
            alternates = {node.get("hreflang"): node.get("href") for node in parsed.find_all("link", rel="alternate", hreflang=True)}
            assert set(alternates) == {"en", "es", "de", "fr", "pt-BR", "ja", "it", "nl", "pl", "zh-Hans", "ko", "ar", "uk", "ru", "tr", "x-default"}
            for alt_locale, alt_lang in locales.items():
                alt_path = path if alt_locale == "en" else f"/{alt_locale}{'/' if path == '/' else path}"
                assert alternates[alt_lang] == BASE + alt_path
            assert alternates["x-default"] == BASE + path
            selector = parsed.find("nav", attrs={"aria-label": "Language selector"})
            assert selector is not None and len(selector.find_all("a")) == 15
            for anchor in parsed.find_all("a", href=True):
                if anchor.find_parent("nav", attrs={"aria-label": "Language selector"}):
                    continue
                href = anchor["href"]
                if locale != "en" and (href == "/" or href.startswith(("/construction/", "/guides/", "/calculators/"))):
                    raise AssertionError(f"Unlocalized internal link on {locale}{path}: {href}")
    arabic = (SITE / "ar" / "construction" / "concrete-volume" / "index.html").read_text(encoding="utf-8")
    from bs4 import BeautifulSoup
    arabic_soup = BeautifulSoup(arabic, "html.parser")
    assert arabic_soup.html.get("dir") == "rtl" and arabic_soup.html.get("lang") == "ar"
    assert arabic_soup.find("link", attrs={"hreflang": "zh-Hans"}) is not None
    for locale in ("uk", "ru", "tr"):
        localized = (SITE / locale / "construction" / "concrete-volume" / "index.html").read_text(encoding="utf-8")
        localized_soup = BeautifulSoup(localized, "html.parser")
        assert localized_soup.html.get("lang") == locale
        assert localized_soup.html.get("dir") != "rtl"
    for locale in locales:
        if locale == "en":
            continue
        runtime = (SITE / locale / "calculator-runtime.js").read_text(encoding="utf-8")
        assert "Intl.NumberFormat" in runtime
    assert (SITE / "404.html").exists()
    assert (SITE / "calculator-runtime.js").exists()
    homepage = (SITE / "index.html").read_text(encoding="utf-8")
    assert "How to get a useful material estimate" in homepage
    assert "Metric and US customary measurements" in homepage
    assert 'data-unit-system="us"' in homepage
    priority_slugs = {"concrete-volume", "concrete-bags", "gravel-volume", "paint-quantity", "flooring-quantity", "tile-quantity", "drywall-sheets", "paver-quantity", "roofing-material", "material-cost"}
    for slug in priority_slugs:
        page_html = (SITE / "construction" / slug / "index.html").read_text(encoding="utf-8")
        assert "Worked project example" in page_html, slug
        assert "Frequently asked questions" in page_html, slug
    assert (SITE / "BingSiteAuth.xml").read_bytes() == (ROOT / "BingSiteAuth.xml").read_bytes()

    for item in items:
        page = SITE / "construction" / item["slug"] / "index.html"
        assert page.exists()
        html = page.read_text()
        assert_canonical(html, f"{BASE}/construction/{item['slug']}/")
        assert BeautifulSoup(html, "html.parser").find("link", rel="icon").get("href") == "/favicon.svg"
        assert "static.cloudflareinsights.com/beacon.min.js" not in html
        assert "2b43ef087bbd47b6847bb0613f03ace2" not in html
        assert "aria-label=\"Breadcrumb\"" in html
        assert '"@type":"FAQPage"' in html
        assert 'Frequently asked questions' in html
        assert 'Enter values greater than zero' in html
        assert 'Related calculators' in html
        assert '/calculator-runtime.js' in html

    for guide in guides:
        page = SITE / "guides" / guide["slug"] / "index.html"
        assert page.exists()
        html = page.read_text()
        assert guide["title"] in html
        assert guide["formula"] in html
        assert 'aria-label="Breadcrumb"' in html
        assert '"@type":"BreadcrumbList"' in html
        assert '"@type":"Article"' in html
        assert_canonical(html, f"{BASE}/guides/{guide['slug']}/")
        assert_canonical(html, f"{BASE}/guides/{guide['slug']}/")
        assert BeautifulSoup(html, "html.parser").find("meta", attrs={"name": "description"}) is not None
        if guide.get("calculator_slug"):
            assert f'/construction/{guide["calculator_slug"]}/' in html
        if guide.get("calculator_link_text"):
            assert guide["calculator_link_text"] in BeautifulSoup(html, "html.parser").get_text(" ")

    construction_index = (SITE / "construction" / "index.html").read_text()
    from bs4 import BeautifulSoup
    calculator_cards = BeautifulSoup(construction_index, "html.parser").select(".calculator-card")
    assert len(calculator_cards) == len(items)
    for card in calculator_cards:
        link = card.find("a", class_="calculator-card-link")
        assert link is not None and link.get("href", "").startswith("/construction/")
        assert card.find(class_="card-action") is not None
    assert "box-shadow:0 4px 16px" in construction_index
    assert 'href="/blog/"' in construction_index
    homepage_cards = BeautifulSoup((SITE / "index.html").read_text(), "html.parser").select(".calculator-card")
    assert homepage_cards
    assert all(card.find("a", class_="calculator-card-link") for card in homepage_cards)
    assert_canonical(construction_index, f"{BASE}/construction/")
    assert "static.cloudflareinsights.com/beacon.min.js" not in construction_index
    assert "2b43ef087bbd47b6847bb0613f03ace2" not in construction_index

    legacy_items = json.loads((ROOT / "data" / "calculators.json").read_text())
    for item in legacy_items:
        page = SITE / "calculators" / item["slug"] / "index.html"
        assert page.exists()
        assert_canonical(page.read_text(), f"{BASE}/calculators/{item['slug']}/")


def test_faq_covers_all_calculators():
    items = json.loads((ROOT / "data/construction_calculators.json").read_text())
    faqs = json.loads((ROOT / "data/calculator_faq.json").read_text())
    assert {x["slug"] for x in faqs} == {x["slug"] for x in items}
    assert all(len(x["faqs"]) >= 2 for x in faqs)


def test_favicon_exists():
    assert (SITE / "favicon.svg").exists()
    robots = (SITE / "robots.txt").read_text()
    assert "User-agent: *" in robots
    assert "Allow: /" in robots
    assert "Sitemap: " + BASE + "/sitemap.xml" in robots


def test_catalog_integrity():
    items = json.loads((ROOT / "data/construction_calculators.json").read_text())
    slugs = [x["slug"] for x in items]
    types = [x["type"] for x in items]
    assert len(items) == 30
    assert len(slugs) == len(set(slugs))
    assert len(types) == len(set(types))
    assert all(x.get("category") for x in items)
    related = json.loads((ROOT / "data/related_calculators.json").read_text())
    assert set(related) == set(slugs)
    assert all(target in slugs for targets in related.values() for target in targets)

def test_localized_priority_pages_render_metric_guidance():
    from bs4 import BeautifulSoup
    locales = [("es", "es"), ("de", "de"), ("fr", "fr"), ("pt-br", "pt_br"), ("ja", "ja"), ("it", "it"), ("nl", "nl"), ("pl", "pl"), ("zh-hans", "zh_hans"), ("ko", "ko"), ("ar", "ar"), ("uk", "uk"), ("ru", "ru"), ("tr", "tr")]
    slugs = ["concrete-volume", "concrete-bags", "gravel-volume", "paint-quantity", "flooring-quantity", "tile-quantity", "drywall-sheets", "paver-quantity", "roofing-material", "material-cost"]
    for page_locale, guidance_locale in locales:
        guidance = json.loads((ROOT / "data" / "locales" / "calculator_guidance" / f"{guidance_locale}.json").read_text(encoding="utf-8"))
        for slug in slugs:
            page = SITE / page_locale / "construction" / slug / "index.html"
            soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
            assert soup.html.get("data-measurement") == "metric", (page_locale, slug)
            assert soup.select_one("#how-to-content").get_text(strip=True) == guidance[slug]["how"], (page_locale, slug, "how")
            metric_example = soup.select_one("#metric-example-content")
            assert metric_example is not None and metric_example.get_text(strip=True) == guidance[slug]["example"], (page_locale, slug, "example")
            metric_section = metric_example.find_parent(attrs={"data-unit-system": "metric"})
            assert metric_section is not None and not metric_section.has_attr("hidden"), (page_locale, slug, "metric example hidden")
            us_section = soup.select_one('[data-unit-system="us"]')
            assert us_section is not None and us_section.has_attr("hidden"), (page_locale, slug, "US section visible")

def test_localized_priority_tips_and_faq_are_visible_and_translated():
    from bs4 import BeautifulSoup
    locales = ["es", "de", "fr", "pt-br", "ja", "it", "nl", "pl", "zh-hans", "ko", "ar", "uk", "ru", "tr"]
    slugs = ["concrete-volume", "concrete-bags", "gravel-volume", "paint-quantity", "flooring-quantity", "tile-quantity", "drywall-sheets", "paver-quantity", "roofing-material", "material-cost"]
    source_content = {x["slug"]: x for x in json.loads((ROOT / "data" / "calculator_content.json").read_text(encoding="utf-8"))}
    for locale in locales:
        translations = json.loads((ROOT / "data" / "locales" / (locale.replace("-", "_") + ".json")).read_text(encoding="utf-8"))
        for slug in slugs:
            page = SITE / locale / "construction" / slug / "index.html"
            soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
            tips = soup.select("#calculator-tips li")
            assert len(tips) == len(source_content[slug]["tips"]), (locale, slug, "tip count")
            for tip in tips:
                assert tip.get_text(strip=True) not in source_content[slug]["tips"], (locale, slug, "English tip")
                assert tip.get_text(strip=True) in translations.values(), (locale, slug, "tip not translated")
            faq = soup.select("#faq-section details")
            source_faq = {x["slug"]: x["faqs"] for x in json.loads((ROOT / "data" / "calculator_faq.json").read_text(encoding="utf-8"))}[slug]
            assert len(faq) == len(source_faq), (locale, slug, "FAQ count")
            for rendered, original in zip(faq, source_faq):
                question = rendered.select_one("summary").get_text(strip=True)
                answer = rendered.select_one("p").get_text(strip=True)
                assert question != original["question"], (locale, slug, "English FAQ question")
                assert answer != original["answer"], (locale, slug, "English FAQ answer")
                assert question in translations.values(), (locale, slug, "question not translated")
                assert answer in translations.values(), (locale, slug, "answer not translated")
            faq_schema = [json.loads(node.string or node.get_text()) for node in soup.select('script[type="application/ld+json"]')]
            faq_data = next((x for x in faq_schema if x.get("@type") == "FAQPage"), None)
            assert faq_data is not None, (locale, slug, "FAQ schema missing")
            assert len(faq_data.get("mainEntity", [])) == len(source_faq), (locale, slug, "FAQ schema count")
            assert not soup.select_one('#faq-section[hidden]')


def test_blog_has_six_localized_articles_and_accessible_navigation():
    from bs4 import BeautifulSoup
    locales = ["en", "es", "de", "fr", "pt-br", "ja", "it", "nl", "pl", "zh-hans", "ko", "ar", "uk", "ru", "tr"]
    for locale in locales:
        prefix = Path(locale) if locale != "en" else Path()
        listing = SITE / prefix / "blog" / "index.html"
        assert listing.exists(), (locale, "blog listing missing")
        soup = BeautifulSoup(listing.read_text(encoding="utf-8"), "html.parser")
        assert len(soup.select(".article-card")) == 6, (locale, "article count")
        assert soup.html.get("dir") == ("rtl" if locale == "ar" else "ltr"), (locale, "direction")
        assert soup.find("nav", attrs={"aria-label": "Language selector"}) is not None
        assert len(soup.select("footer .language-list a")) == 15
        assert soup.find("nav", attrs={"aria-label": "Main navigation"}) is not None
        assert soup.find("style") is not None
        for slug in (
            "how-to-estimate-concrete-volume",
            "gravel-sand-and-soil-quantity-guide",
            "flooring-and-tile-waste-calculation",
            "paint-coverage-and-quantity",
            "fence-and-deck-material-estimates",
            "construction-material-budget-planning",
        ):
            article = SITE / prefix / "blog" / slug / "index.html"
            assert article.exists(), (locale, slug)
            article_soup = BeautifulSoup(article.read_text(encoding="utf-8"), "html.parser")
            assert article_soup.find("link", rel="canonical") is not None
            assert article_soup.find("script", type="application/ld+json") is not None
            assert article_soup.find("article") is not None
