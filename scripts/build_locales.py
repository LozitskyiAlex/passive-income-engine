"""Build fully localized static site variants from translated locale datasets.

The English site remains at the root. Every other locale is generated into
site/<locale>/ and receives locale-specific canonical URLs and sitemap entries.
This script intentionally fails closed when any locale dataset is missing.
"""
from __future__ import annotations

import importlib
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE = "https://free-construction-calculators.pages.dev"
DATA = ROOT / "data"
LOCALE_DATA = DATA / "locales"

LOCALES = {
    "es": "es",
    "de": "de",
    "fr": "fr",
    "pt-br": "pt-BR",
    "ja": "ja",
    "it": "it",
    "nl": "nl",
    "pl": "pl",
    "zh-hans": "zh-Hans",
    "ko": "ko",
    "ar": "ar",
}
LANGUAGE_NAMES = {
    "en": "English", "es": "Español", "de": "Deutsch", "fr": "Français",
    "pt-br": "Português (Brasil)", "ja": "日本語", "it": "Italiano",
    "nl": "Nederlands", "pl": "Polski", "zh-hans": "简体中文",
    "ko": "한국어", "ar": "العربية",
}
UI = {
    "es": {
        "Home": "Inicio", "Construction Calculators": "Calculadoras de construcción",
        "Calculate": "Calcular", "Reset": "Restablecer",
        "Calculation example": "Ejemplo de cálculo", "Formula": "Fórmula",
        "How to use this calculator": "Cómo usar esta calculadora",
        "Before you calculate": "Antes de calcular", "Understanding the result": "Cómo interpretar el resultado",
        "Tips": "Consejos", "Frequently asked questions": "Preguntas frecuentes",
        "Related calculators": "Calculadoras relacionadas", "Browse all construction calculators": "Ver todas las calculadoras de construcción",
        "Practical Guides": "Guías prácticas", "Popular calculators": "Calculadoras populares",
        "Enter valid non-negative numbers.": "Introduce números válidos no negativos.",
        "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.": "Introduce valores mayores que cero para dimensiones, cantidades, precios, cobertura, densidad o separación.",
        "Length": "Longitud", "Width": "Anchura", "Thickness": "Grosor", "Volume": "Volumen",
        "Bag Yield": "Rendimiento por saco", "Depth": "Profundidad", "Height": "Altura",
        "Area": "Área", "Waste %": "Desperdicio %", "Quantity": "Cantidad",
        "Unit Price": "Precio unitario", "Room Length": "Longitud de la habitación",
        "Room Width": "Anchura de la habitación", "Wall Height": "Altura de pared",
    },
    "de": {
        "Home": "Startseite", "Construction Calculators": "Bau-Rechner",
        "Calculate": "Berechnen", "Reset": "Zurücksetzen",
        "Calculation example": "Berechnungsbeispiel", "Formula": "Formel",
        "How to use this calculator": "So verwenden Sie diesen Rechner",
        "Before you calculate": "Vor der Berechnung", "Understanding the result": "Ergebnis verstehen",
        "Tips": "Tipps", "Frequently asked questions": "Häufig gestellte Fragen",
        "Related calculators": "Ähnliche Rechner", "Browse all construction calculators": "Alle Bau-Rechner anzeigen",
        "Practical Guides": "Praktische Anleitungen", "Popular calculators": "Beliebte Rechner",
        "Enter valid non-negative numbers.": "Geben Sie gültige nicht negative Zahlen ein.",
        "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.": "Geben Sie für Maße, Mengen, Preise, Abdeckung, Dichte oder Abstände Werte größer als null ein.",
        "Length": "Länge", "Width": "Breite", "Thickness": "Dicke", "Volume": "Volumen",
        "Bag Yield": "Ertrag pro Sack", "Depth": "Tiefe", "Height": "Höhe",
        "Area": "Fläche", "Waste %": "Verschnitt %", "Quantity": "Menge",
        "Unit Price": "Stückpreis", "Room Length": "Raumlänge", "Room Width": "Raumbreite",
        "Wall Height": "Wandhöhe",
    },
    "fr": {
        "Home": "Accueil", "Construction Calculators": "Calculateurs de construction",
        "Calculate": "Calculer", "Reset": "Réinitialiser",
        "Calculation example": "Exemple de calcul", "Formula": "Formule",
        "How to use this calculator": "Comment utiliser ce calculateur",
        "Before you calculate": "Avant le calcul", "Understanding the result": "Comprendre le résultat",
        "Tips": "Conseils", "Frequently asked questions": "Questions fréquentes",
        "Related calculators": "Calculateurs associés", "Browse all construction calculators": "Voir tous les calculateurs de construction",
        "Practical Guides": "Guides pratiques", "Popular calculators": "Calculateurs populaires",
        "Enter valid non-negative numbers.": "Saisissez des nombres valides positifs ou nuls.",
        "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.": "Saisissez des valeurs supérieures à zéro pour les dimensions, quantités, prix, rendements, densités ou espacements.",
        "Length": "Longueur", "Width": "Largeur", "Thickness": "Épaisseur", "Volume": "Volume",
        "Bag Yield": "Rendement par sac", "Depth": "Profondeur", "Height": "Hauteur",
        "Area": "Surface", "Waste %": "Marge de perte %", "Quantity": "Quantité",
        "Unit Price": "Prix unitaire", "Room Length": "Longueur de la pièce", "Room Width": "Largeur de la pièce",
        "Wall Height": "Hauteur du mur",
    },
    "pt-br": {
        "Home": "Início", "Construction Calculators": "Calculadoras de construção",
        "Calculate": "Calcular", "Reset": "Redefinir",
        "Calculation example": "Exemplo de cálculo", "Formula": "Fórmula",
        "How to use this calculator": "Como usar esta calculadora",
        "Before you calculate": "Antes de calcular", "Understanding the result": "Entenda o resultado",
        "Tips": "Dicas", "Frequently asked questions": "Perguntas frequentes",
        "Related calculators": "Calculadoras relacionadas", "Browse all construction calculators": "Ver todas as calculadoras de construção",
        "Practical Guides": "Guias práticos", "Popular calculators": "Calculadoras populares",
        "Enter valid non-negative numbers.": "Digite números válidos não negativos.",
        "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.": "Digite valores maiores que zero para dimensões, quantidades, preços, rendimento, densidade ou espaçamento.",
        "Length": "Comprimento", "Width": "Largura", "Thickness": "Espessura", "Volume": "Volume",
        "Bag Yield": "Rendimento por saco", "Depth": "Profundidade", "Height": "Altura",
        "Area": "Área", "Waste %": "Margem de perda %", "Quantity": "Quantidade",
        "Unit Price": "Preço unitário", "Room Length": "Comprimento do cômodo", "Room Width": "Largura do cômodo",
        "Wall Height": "Altura da parede",
    },
    "ja": {
        "Home": "ホーム", "Construction Calculators": "建設計算ツール",
        "Calculate": "計算する", "Reset": "リセット",
        "Calculation example": "計算例", "Formula": "計算式",
        "How to use this calculator": "この計算ツールの使い方",
        "Before you calculate": "計算する前に", "Understanding the result": "結果について",
        "Tips": "ヒント", "Frequently asked questions": "よくある質問",
        "Related calculators": "関連する計算ツール", "Browse all construction calculators": "すべての建設計算ツールを見る",
        "Practical Guides": "実用ガイド", "Popular calculators": "人気の計算ツール",
        "Enter valid non-negative numbers.": "0以上の有効な数値を入力してください。",
        "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.": "寸法、数量、価格、被覆率、密度、間隔には0より大きい値を入力してください。",
        "Length": "長さ", "Width": "幅", "Thickness": "厚さ", "Volume": "体積",
        "Bag Yield": "袋あたりの量", "Depth": "深さ", "Height": "高さ",
        "Area": "面積", "Waste %": "ロス率 %", "Quantity": "数量",
        "Unit Price": "単価", "Room Length": "部屋の長さ", "Room Width": "部屋の幅",
        "Wall Height": "壁の高さ",
    },
    "it": {
        "Home": "Home", "Construction Calculators": "Calcolatori per l'edilizia",
        "Calculate": "Calcola", "Reset": "Reimposta",
        "Calculation example": "Esempio di calcolo", "Formula": "Formula",
        "How to use this calculator": "Come usare questo calcolatore",
        "Before you calculate": "Prima del calcolo", "Understanding the result": "Interpretare il risultato",
        "Tips": "Suggerimenti", "Frequently asked questions": "Domande frequenti",
        "Related calculators": "Calcolatori correlati", "Browse all construction calculators": "Visualizza tutti i calcolatori per l'edilizia",
        "Practical Guides": "Guide pratiche", "Popular calculators": "Calcolatori più usati",
        "Enter valid non-negative numbers.": "Inserisci numeri validi non negativi.",
        "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.": "Inserisci valori maggiori di zero per dimensioni, quantità, prezzi, copertura, densità o spaziatura.",
        "Length": "Lunghezza", "Width": "Larghezza", "Thickness": "Spessore", "Volume": "Volume",
        "Bag Yield": "Resa per sacco", "Depth": "Profondità", "Height": "Altezza",
        "Area": "Area", "Waste %": "Sfrido %", "Quantity": "Quantità",
        "Unit Price": "Prezzo unitario", "Room Length": "Lunghezza della stanza", "Room Width": "Larghezza della stanza",
        "Wall Height": "Altezza della parete",
    },
    "nl": {
        "Home": "Home", "Construction Calculators": "Bouwcalculators",
        "Calculate": "Berekenen", "Reset": "Wissen",
        "Calculation example": "Rekenvoorbeeld", "Formula": "Formule",
        "How to use this calculator": "Deze calculator gebruiken",
        "Before you calculate": "Voordat u berekent", "Understanding the result": "Het resultaat begrijpen",
        "Tips": "Tips", "Frequently asked questions": "Veelgestelde vragen",
        "Related calculators": "Gerelateerde calculators", "Browse all construction calculators": "Bekijk alle bouwcalculators",
        "Practical Guides": "Praktische handleidingen", "Popular calculators": "Populaire calculators",
        "Enter valid non-negative numbers.": "Voer geldige niet-negatieve getallen in.",
        "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.": "Voer waarden groter dan nul in voor afmetingen, hoeveelheden, prijzen, dekking, dichtheid of tussenruimte.",
        "Length": "Lengte", "Width": "Breedte", "Thickness": "Dikte", "Volume": "Volume",
        "Bag Yield": "Opbrengst per zak", "Depth": "Diepte", "Height": "Hoogte",
        "Area": "Oppervlakte", "Waste %": "Snijverlies %", "Quantity": "Hoeveelheid",
        "Unit Price": "Prijs per eenheid", "Room Length": "Kamerlengte", "Room Width": "Kamerbreedte",
        "Wall Height": "Wandhoogte",
    },
    "pl": {
        "Home": "Strona główna", "Construction Calculators": "Kalkulatory budowlane",
        "Calculate": "Oblicz", "Reset": "Wyczyść",
        "Calculation example": "Przykład obliczenia", "Formula": "Wzór",
        "How to use this calculator": "Jak korzystać z kalkulatora",
        "Before you calculate": "Przed obliczeniem", "Understanding the result": "Interpretacja wyniku",
        "Tips": "Wskazówki", "Frequently asked questions": "Często zadawane pytania",
        "Related calculators": "Powiązane kalkulatory", "Browse all construction calculators": "Zobacz wszystkie kalkulatory budowlane",
        "Practical Guides": "Praktyczne poradniki", "Popular calculators": "Popularne kalkulatory",
        "Enter valid non-negative numbers.": "Wprowadź prawidłowe liczby nieujemne.",
        "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.": "Wprowadź wartości większe od zera dla wymiarów, ilości, cen, wydajności, gęstości lub odstępów.",
        "Length": "Długość", "Width": "Szerokość", "Thickness": "Grubość", "Volume": "Objętość",
        "Bag Yield": "Wydajność worka", "Depth": "Głębokość", "Height": "Wysokość",
        "Area": "Powierzchnia", "Waste %": "Zapas %", "Quantity": "Ilość",
        "Unit Price": "Cena jednostkowa", "Room Length": "Długość pomieszczenia", "Room Width": "Szerokość pomieszczenia",
        "Wall Height": "Wysokość ściany",
    },
    "zh-hans": {
        "Home": "首页", "Construction Calculators": "建筑计算器",
        "Calculate": "计算", "Reset": "重置",
        "Calculation example": "计算示例", "Formula": "公式",
        "How to use this calculator": "如何使用此计算器",
        "Before you calculate": "计算前须知", "Understanding the result": "结果说明",
        "Tips": "提示", "Frequently asked questions": "常见问题",
        "Related calculators": "相关计算器", "Browse all construction calculators": "浏览所有建筑计算器",
        "Practical Guides": "实用指南", "Popular calculators": "热门计算器",
        "Enter valid non-negative numbers.": "请输入有效的非负数。",
        "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.": "尺寸、数量、价格、覆盖率、密度或间距请输入大于零的数值。",
        "Length": "长度", "Width": "宽度", "Thickness": "厚度", "Volume": "体积",
        "Bag Yield": "每袋产量", "Depth": "深度", "Height": "高度",
        "Area": "面积", "Waste %": "损耗率 %", "Quantity": "数量",
        "Unit Price": "单价", "Room Length": "房间长度", "Room Width": "房间宽度",
        "Wall Height": "墙面高度",
    },
    "ko": {
        "Home": "홈", "Construction Calculators": "건설 계산기",
        "Calculate": "계산", "Reset": "초기화",
        "Calculation example": "계산 예시", "Formula": "공식",
        "How to use this calculator": "계산기 사용 방법",
        "Before you calculate": "계산 전 확인 사항", "Understanding the result": "결과 이해하기",
        "Tips": "팁", "Frequently asked questions": "자주 묻는 질문",
        "Related calculators": "관련 계산기", "Browse all construction calculators": "모든 건설 계산기 보기",
        "Practical Guides": "실용 가이드", "Popular calculators": "인기 계산기",
        "Enter valid non-negative numbers.": "유효한 0 이상의 숫자를 입력하세요.",
        "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.": "치수, 수량, 가격, 적용 범위, 밀도 또는 간격에는 0보다 큰 값을 입력하세요.",
        "Length": "길이", "Width": "너비", "Thickness": "두께", "Volume": "부피",
        "Bag Yield": "포대당 수율", "Depth": "깊이", "Height": "높이",
        "Area": "면적", "Waste %": "여유율 %", "Quantity": "수량",
        "Unit Price": "단가", "Room Length": "방 길이", "Room Width": "방 너비",
        "Wall Height": "벽 높이",
    },
    "ar": {
        "Home": "الرئيسية", "Construction Calculators": "حاسبات البناء",
        "Calculate": "احسب", "Reset": "إعادة ضبط",
        "Calculation example": "مثال على الحساب", "Formula": "المعادلة",
        "How to use this calculator": "كيفية استخدام هذه الحاسبة",
        "Before you calculate": "قبل الحساب", "Understanding the result": "فهم النتيجة",
        "Tips": "نصائح", "Frequently asked questions": "الأسئلة الشائعة",
        "Related calculators": "حاسبات ذات صلة", "Browse all construction calculators": "عرض جميع حاسبات البناء",
        "Practical Guides": "أدلة عملية", "Popular calculators": "الحاسبات الشائعة",
        "Enter valid non-negative numbers.": "أدخل أرقامًا صحيحة غير سالبة.",
        "Enter values greater than zero for dimensions, quantities, prices, coverage, density or spacing.": "أدخل قيمًا أكبر من صفر للأبعاد والكميات والأسعار والتغطية والكثافة والمسافات.",
        "Length": "الطول", "Width": "العرض", "Thickness": "السماكة", "Volume": "الحجم",
        "Bag Yield": "مردود الكيس", "Depth": "العمق", "Height": "الارتفاع",
        "Area": "المساحة", "Waste %": "نسبة الهدر %", "Quantity": "الكمية",
        "Unit Price": "سعر الوحدة", "Room Length": "طول الغرفة", "Room Width": "عرض الغرفة",
        "Wall Height": "ارتفاع الجدار",
    },
}

def require_locale_data(code: str) -> dict[str, Path]:
    folder = LOCALE_DATA / code
    names = ("construction_calculators.json", "calculator_content.json", "calculator_faq.json", "guides.json")
    paths = {name: folder / name for name in names}
    missing = [str(path.relative_to(ROOT)) for path in paths.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Locale {code} is incomplete. Missing translated datasets: {', '.join(missing)}")
    for path in paths.values():
        json.loads(path.read_text(encoding="utf-8"))
    return paths

def import_builders():
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    return (
        importlib.import_module("build"),
        importlib.import_module("build_construction"),
        importlib.import_module("build_construction_index"),
        importlib.import_module("build_seo"),
    )

def localize_html(locale: str, root: Path) -> None:
    replacements = UI.get(locale, {})
    for path in root.rglob("*.html"):
        html = path.read_text(encoding="utf-8")
        html = html.replace('<html lang="en"', f'<html lang="{LOCALES[locale]}"')
        if locale == "ar":
            html = html.replace(f'<html lang="{LOCALES[locale]}"', f'<html lang="{LOCALES[locale]}" dir="rtl"')
        html = html.replace('href="/', f'href="/{locale}/')
        html = html.replace('src="/', f'src="/{locale}/')
        html = html.replace('from "/', f'from "/{locale}/')
        for source, target in replacements.items():
            html = html.replace(source, target)
        path.write_text(html, encoding="utf-8")

def add_language_navigation() -> None:
    for path in SITE.rglob("*.html"):
        relative = path.relative_to(SITE)
        if relative.parts and relative.parts[0] in LOCALES:
            current = relative.parts[0]
            page = Path(*relative.parts[1:])
        else:
            current = "en"
            page = relative
        links = []
        for code, name in LANGUAGE_NAMES.items():
            target = (SITE / code / page) if code in LOCALES else (SITE / page)
            if target.is_file():
                href = f"/{code}/{page.as_posix()}" if code in LOCALES else f"/{page.as_posix()}"
                links.append(f'<a lang="{LOCALES.get(code, "en")}" href="{href}">{name}</a>')
        nav = '<nav class="language-switcher" aria-label="Language selector">' + " · ".join(links) + "</nav>"
        html = path.read_text(encoding="utf-8")
        html = html.replace("</head>", '<style>.language-switcher{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 18px;font-size:.9rem}.language-switcher a{color:inherit}</style></head>', 1)
        html = html.replace("<body>", "<body>" + nav, 1)
        alternates = []
        for code, lang in {"en": "en", **LOCALES}.items():
            target = (SITE / code / page) if code in LOCALES else (SITE / page)
            if target.is_file():
                href = f"{BASE}/{code}/{page.as_posix()}" if code in LOCALES else f"{BASE}/{page.as_posix()}"
                alternates.append(f'<link rel="alternate" hreflang="{lang}" href="{href}">')
        if (SITE / page).is_file():
            alternates.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/{page.as_posix()}">')
        html = html.replace("</head>", "".join(alternates) + "</head>", 1)
        path.write_text(html, encoding="utf-8")

def merge_sitemaps() -> None:
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    seen = set()
    sitemap_paths = [SITE / "sitemap.xml"] + [SITE / code / "sitemap.xml" for code in LOCALES]
    for sitemap_path in sitemap_paths:
        if not sitemap_path.is_file():
            continue
        tree = ET.parse(sitemap_path)
        for url in tree.findall("sm:url", namespace):
            loc = url.findtext("sm:loc", default="", namespaces=namespace)
            if loc and loc not in seen:
                seen.add(loc)
                root.append(url)
    ET.ElementTree(root).write(SITE / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    for code in LOCALES:
        for name in ("sitemap.xml", "robots.txt"):
            nested = SITE / code / name
            if nested.exists():
                nested.unlink()

def main() -> None:
    for code in LOCALES:
        require_locale_data(code)
    home, construction, index, seo = import_builders()
    for code in LOCALES:
        paths = require_locale_data(code)
        locale_root = SITE / code
        locale_base = f"{BASE}/{code}"
        home.DATA = LOCALE_DATA / code / "items.json"
        home.CALCS = paths["construction_calculators.json"]
        home.GUIDES = paths["guides.json"]
        home.SITE = locale_root
        home.BASE = locale_base
        home.main()

        construction.DATA = paths["construction_calculators.json"]
        construction.CONTENT = paths["calculator_content.json"]
        construction.FAQ = paths["calculator_faq.json"]
        construction.SITE = locale_root / "construction"
        construction.BASE = locale_base
        construction.main()

        index.DATA = paths["construction_calculators.json"]
        index.GUIDES = paths["guides.json"]
        index.OUT = locale_root / "construction" / "index.html"
        index.BASE = locale_base
        index.main()

        seo.SITE = locale_root
        seo.DATA = paths["construction_calculators.json"]
        seo.GUIDES = paths["guides.json"]
        seo.BASE = locale_base
        seo.INDEXNOW_KEY = ""
        seo.main()
        localize_html(code, locale_root)
    add_language_navigation()
    merge_sitemaps()

if __name__ == "__main__":
    main()
