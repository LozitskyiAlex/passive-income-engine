import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
LOCALES_DIR = ROOT / "data" / "locales"
BASE = "https://free-construction-calculators.pages.dev"
LOCALES = {
    "en": {"hreflang": "en", "name": "English", "region": "US", "measurement": "us"},
    "es": {"hreflang": "es", "name": "Español", "region": "ES", "measurement": "metric"},
    "de": {"hreflang": "de", "name": "Deutsch", "region": "DE", "measurement": "metric"},
    "fr": {"hreflang": "fr", "name": "Français", "region": "FR", "measurement": "metric"},
    "pt-br": {"hreflang": "pt-BR", "name": "Português", "region": "BR", "measurement": "metric"},
    "ja": {"hreflang": "ja", "name": "日本語", "region": "JP", "measurement": "metric"},
    "it": {"hreflang": "it", "name": "Italiano", "region": "IT", "measurement": "metric"},
    "nl": {"hreflang": "nl", "name": "Nederlands", "region": "NL", "measurement": "metric"},
    "pl": {"hreflang": "pl", "name": "Polski", "region": "PL", "measurement": "metric"},
    "zh-hans": {"hreflang": "zh-Hans", "name": "简体中文", "region": "CN", "measurement": "metric"},
    "ko": {"hreflang": "ko", "name": "한국어", "region": "KR", "measurement": "metric"},
    "ar": {"hreflang": "ar", "name": "العربية", "region": "001", "measurement": "metric"},
    "uk": {"hreflang": "uk", "name": "Українська", "region": "UA", "measurement": "metric"},
    "ru": {"hreflang": "ru", "name": "Русский", "region": "RU", "measurement": "metric"},
    "tr": {"hreflang": "tr", "name": "Türkçe", "region": "TR", "measurement": "metric"},
}
STATIC_ROOTS = ("/favicon.svg", "/calculator-runtime.js", "/robots.txt", "/sitemap.xml", "/BingSiteAuth.xml", "/indexnow-key.txt", "/404.html")


def locale_path(path, locale):
    path = path if path.startswith("/") else "/" + path
    if locale == "en":
        return path
    return "/" + locale + ("/" if path == "/" else path)


def absolute_url(path):
    return BASE + path


def translate_json(value, translations, locale):
    if isinstance(value, dict):
        return {k: translate_json(v, translations, locale) for k, v in value.items()}
    if isinstance(value, list):
        return [translate_json(v, translations, locale) for v in value]
    if isinstance(value, str):
        if value.startswith(BASE):
            return absolute_url(locale_path(value[len(BASE):] or "/", locale))
        return translations.get(value, value)
    return value


def translate_script(script, translations):
    source = script.string or script.get_text()
    pattern = re.compile(r'''(["\'])(.*?)(?<!\\)\1''', re.S)
    def replace(match):
        quote, value = match.group(1), match.group(2)
        translated = translations.get(value)
        if translated is None:
            return match.group(0)
        safe = translated.replace("\\", "\\\\").replace(quote, "\\" + quote).replace("\n", "\\n")
        return quote + safe + quote
    result = pattern.sub(replace, source)
    if "/calculator-runtime.js" in result:
        result = result.replace('"/calculator-runtime.js"', '"/calculator-runtime.js"')
    script.string = result


def add_hreflang(soup, path):
    head = soup.head
    if head is None:
        return
    for node in head.find_all("link", rel="alternate", hreflang=True):
        node.decompose()
    for locale, meta in LOCALES.items():
        href = absolute_url(locale_path(path, locale))
        tag = soup.new_tag("link", rel="alternate", hreflang=meta["hreflang"], href=href)
        head.append(tag)
    tag = soup.new_tag("link", rel="alternate", hreflang="x-default", href=absolute_url(path))
    head.append(tag)


def add_language_switcher(soup, path, current):
    body = soup.body
    if body is None:
        return
    old = body.find("nav", attrs={"aria-label": "Language selector"})
    if old:
        old.decompose()
    nav = soup.new_tag("nav", attrs={"aria-label": "Language selector", "class": "language-switcher"})
    for locale, meta in LOCALES.items():
        link = soup.new_tag("a", href=locale_path(path, locale), lang=meta["hreflang"])
        link.string = meta["name"]
        if locale == current:
            link["aria-current"] = "page"
        nav.append(link)
    body.insert(0, nav)


def localize_internal_links(soup, locale):
    if locale == "en":
        return
    for tag in soup.find_all(["a", "link"]):
        href = tag.get("href")
        if not isinstance(href, str) or not href.startswith("/"):
            continue
        if href.startswith(STATIC_ROOTS):
            continue
        if href == "/":
            tag["href"] = "/" + locale + "/"
        elif href.startswith(("/construction/", "/guides/", "/calculators/")):
            tag["href"] = "/" + locale + href
    for script in soup.find_all("script"):
        if script.get("type") == "application/ld+json":
            continue
        source = script.string or script.get_text()
        source = source.replace('"/calculator-runtime.js"', '"/' + locale + '/calculator-runtime.js"')
        script.string = source


REGIONAL_UNIT_SYMBOLS = {
    "metric": {"length_ft": "m", "length_in": "mm", "area_sqft": "m²", "volume_cuft": "m³", "density_lb_cuft": "kg/m³"},
    "us": {"length_ft": "ft", "length_in": "in", "area_sqft": "sq ft", "volume_cuft": "cu ft", "density_lb_cuft": "lb/cu ft"},
}


def localize_page(source_html, path, locale, translations):
    soup = BeautifulSoup(source_html, "html.parser")
    html = soup.find("html")
    if html:
        html["lang"] = LOCALES[locale]["hreflang"]
        html["data-region"] = LOCALES[locale]["region"]
        html["data-measurement"] = LOCALES[locale]["measurement"]
        for unit_node in soup.select(".unit[data-dimension]"):
            unit_node.string = REGIONAL_UNIT_SYMBOLS[LOCALES[locale]["measurement"]].get(unit_node.get("data-dimension", ""), "")
        if locale == "ar":
            html["dir"] = "rtl"
        else:
            html.attrs.pop("dir", None)
    for node in list(soup.find_all(string=True)):
        if node.parent and node.parent.name in ("script", "style"):
            continue
        original = str(node)
        stripped = original.strip()
        if stripped in translations:
            leading = original[:len(original) - len(original.lstrip())]
            trailing = original[len(original.rstrip()):]
            node.replace_with(NavigableString(leading + translations[stripped] + trailing))
    for tag in soup.find_all(True):
        for attr in ("title", "content", "aria-label", "placeholder", "alt", "value"):
            value = tag.get(attr)
            if isinstance(value, str) and value in translations:
                if attr == "content" and tag.name == "meta":
                    prop = tag.get("property", "")
                    name = tag.get("name", "")
                    if not (prop in ("og:title", "og:description") or name == "description"):
                        continue
                tag[attr] = translations[value]
    for script in soup.find_all("script"):
        if script.get("type") == "application/ld+json":
            try:
                data = json.loads(script.string or script.get_text())
                script.string = json.dumps(translate_json(data, translations, locale), ensure_ascii=False, separators=(",", ":"))
            except (ValueError, TypeError):
                pass
        elif script.get("type") != "module" or script.string:
            translate_script(script, translations)
    for field_name in soup.select(".field-name"):
        field_name.string = re.sub(r"\s*\([^)]*\)\s*$", "", field_name.get_text("", strip=True))
    if LOCALES[locale]["measurement"] == "metric":
        neutral_how = "Measure the project dimensions as accurately as practical and keep all measurements in compatible units. For material products, use the coverage, yield, density, or package size stated by the manufacturer or supplier rather than a generic assumption."
        how_node = soup.select_one("#how-to-content")
        if how_node:
            how_node.string = translations.get(neutral_how, neutral_how)
        for regional_node in soup.select('[data-unit-system="us"]'):
            regional_node["hidden"] = True
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                schema = json.loads(script.string or script.get_text())
                if isinstance(schema, dict) and schema.get("@type") == "FAQPage":
                    script.decompose()
            except (ValueError, TypeError):
                pass
    localize_internal_links(soup, locale)
    canonical = absolute_url(locale_path(path, locale))
    canonical_tag = soup.find("link", rel="canonical")
    if canonical_tag:
        canonical_tag["href"] = canonical
    for meta in soup.find_all("meta", property="og:url"):
        meta["content"] = canonical
    add_hreflang(soup, path)
    add_language_switcher(soup, path, locale)
    if soup.head:
        old_style = soup.find("style", id="language-switcher-styles")
        if old_style:
            old_style.decompose()
        style = soup.new_tag("style", id="language-switcher-styles")
        style.string = ".language-switcher{display:flex;flex-wrap:wrap;gap:8px 14px;margin:0 auto 22px;max-width:1100px;padding:10px 0;border-bottom:1px solid #e5e7eb;font-size:.9rem}.language-switcher a{color:inherit;text-decoration:none}.language-switcher a[aria-current=page]{font-weight:700;text-decoration:underline}" + ("html[dir=rtl] body{direction:rtl;text-align:right}.formula,.example,code{direction:ltr;unicode-bidi:plaintext;text-align:left}" if locale == "ar" else "")
        soup.head.append(style)
    return str(soup)


def page_path(file_path):
    rel = file_path.relative_to(SITE).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("index.html")]
    if rel.endswith(".html"):
        return "/" + rel
    return "/" + rel


def build_localized_runtime(locale, translations):
    source = (SITE / "calculator-runtime.js").read_text(encoding="utf-8")
    source = re.sub(r'''(["\'])(.*?)(?<!\\)\1''', lambda m: m.group(1) + translations.get(m.group(2), m.group(2)).replace(m.group(1), "\\" + m.group(1)) + m.group(1), source, flags=re.S)
    source = source.replace("return formula(values);", "return formula(values).replace(/\\d+(?:\\.\\d+)?/g, value => new Intl.NumberFormat(" + json.dumps(LOCALES[locale]["hreflang"]) + ", { maximumFractionDigits: 3 }).format(Number(value)));")
    out = SITE / locale / "calculator-runtime.js"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(source, encoding="utf-8")


def build_sitemap(paths):
    ns_sm = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ns_xhtml = "http://www.w3.org/1999/xhtml"
    ET.register_namespace("", ns_sm)
    ET.register_namespace("xhtml", ns_xhtml)
    original = ET.parse(SITE / "sitemap.xml").getroot()
    lastmods = {}
    for node in original.findall("{*}url"):
        loc = node.find("{*}loc")
        last = node.find("{*}lastmod")
        if loc is not None and last is not None and loc.text:
            lastmods[loc.text[len(BASE):] or "/"] = last.text
    root = ET.Element("{" + ns_sm + "}urlset")
    for path in paths:
        lastmod = lastmods.get(path)
        for locale in LOCALES:
            loc = absolute_url(locale_path(path, locale))
            url = ET.SubElement(root, "{" + ns_sm + "}url")
            ET.SubElement(url, "{" + ns_sm + "}loc").text = loc
            if lastmod:
                ET.SubElement(url, "{" + ns_sm + "}lastmod").text = lastmod
            for alt_locale, meta in LOCALES.items():
                ET.SubElement(url, "{" + ns_xhtml + "}link", {"rel": "alternate", "hreflang": meta["hreflang"], "href": absolute_url(locale_path(path, alt_locale))})
            ET.SubElement(url, "{" + ns_xhtml + "}link", {"rel": "alternate", "hreflang": "x-default", "href": absolute_url(path)})
    ET.ElementTree(root).write(SITE / "sitemap.xml", encoding="utf-8", xml_declaration=True)


RUNTIME_STRINGS = [
    " cubic units", " bags", " cu ft", " cu yd", " units", " square units", " tiles", " sheets",
    " board feet", " pavers", " posts", " boards", " roofing squares", " sq ft", " weight units",
    " length units", " rolls", " risers", " cubic yards", "Enter valid non-negative numbers.",
    "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.",
]


def required_translation_strings(source_pages):
    required = set(RUNTIME_STRINGS)
    numeric_or_punctuation = re.compile(r"[\d.,%$€£¥₹\s×÷=+()\-]+")
    for page in list(source_pages) + ([SITE / "404.html"] if (SITE / "404.html").exists() else []):
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        for node in soup.find_all(string=True):
            value = str(node).strip()
            if not value or (node.parent and node.parent.name in ("script", "style")):
                continue
            if value in ("html", "·", "/", "|") or numeric_or_punctuation.fullmatch(value):
                continue
            if len(value) > 1:
                required.add(value)
        for tag in soup.find_all(True):
            for attr in ("title", "content", "aria-label", "placeholder", "alt", "value"):
                if attr == "value" and tag.name == "option":
                    continue
                value = tag.get(attr)
                if isinstance(value, str) and len(value.strip()) > 1 and not numeric_or_punctuation.fullmatch(value.strip()):
                    required.add(value.strip())
    return required


def main():
    source_pages = sorted(p for p in SITE.rglob("*.html") if not any(part in LOCALES for part in p.relative_to(SITE).parts))
    source_pages = [p for p in source_pages if p.name != "404.html"]
    if not source_pages:
        raise RuntimeError("No source HTML pages found for localization")
    paths = [page_path(p) for p in source_pages]
    if len(paths) != len(set(paths)):
        raise RuntimeError("Duplicate source URL paths found")
    for locale in list(LOCALES)[1:]:
        translations_path = LOCALES_DIR / (locale.replace("-", "_") + ".json")
        if not translations_path.is_file():
            raise FileNotFoundError(f"Missing translation file: {translations_path}")
        translations = json.loads(translations_path.read_text(encoding="utf-8"))
        required = required_translation_strings(source_pages)
        missing = sorted(required - set(translations))
        if missing:
            raise ValueError(f"Incomplete translation file for {locale}: missing {len(missing)} strings, including {missing[:8]}")
        if any(not isinstance(value, str) or not value.strip() for value in translations.values()):
            raise ValueError(f"Blank or invalid translation values found for {locale}")
        build_localized_runtime(locale, translations)
        for source, path in zip(source_pages, paths):
            dest = SITE / locale / (source.relative_to(SITE))
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(localize_page(source.read_text(encoding="utf-8"), path, locale, translations), encoding="utf-8")
        not_found = SITE / "404.html"
        if not_found.exists():
            dest = SITE / locale / "404.html"
            dest.write_text(localize_page(not_found.read_text(encoding="utf-8"), "/404.html", locale, translations), encoding="utf-8")
    # Add language navigation and reciprocal hreflang links to English source pages without translating their content.
    for source, path in zip(source_pages, paths):
        source.write_text(localize_page(source.read_text(encoding="utf-8"), path, "en", {}), encoding="utf-8")
    build_sitemap(paths)
    expected = len(paths) * len(LOCALES)
    sitemap_root = ET.parse(SITE / "sitemap.xml").getroot()
    actual = len(sitemap_root.findall("{*}url"))
    if actual != expected:
        raise RuntimeError(f"Sitemap URL count mismatch: expected {expected}, got {actual}")
    print(f"Built {len(LOCALES)} locales, {len(paths)} pages per locale, {actual} sitemap URLs")


if __name__ == "__main__":
    main()
