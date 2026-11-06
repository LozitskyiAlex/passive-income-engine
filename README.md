# Passive Income Engine

A zero-cost, data-driven engine for building useful static web products.

## Principles

1. No paid APIs.
2. No paid hosting.
3. No database or VPS unless a future product requires one and the cost is justified.
4. Prefer public data sources with permitted access.
5. Automate collection, normalization, generation, testing and deployment.
6. AI is optional and batch-oriented, not required per visitor.
7. Do not copy supplier text or generate low-value pages at scale.
8. Monetization is added only after the tools are useful and there is evidence of traffic.

## Current product

The first product is a construction calculator site deployed as static assets through Cloudflare Pages.

**Live site:** https://free-construction-calculators.pages.dev/

Current catalog: 30 calculators covering concrete, gravel and soil, interior projects, lumber, fencing and decking, roofing, general quantities and project costs.

Every calculator page includes:

* Browser-side calculation.
* Formula/example content.
* FAQ content.
* FAQ, breadcrumb and WebApplication structured data.
* Canonical and social metadata.
* Related calculator links.

The generated site also includes:

* Category-based homepage.
* Construction calculator index.
* robots.txt.
* XML sitemap.
* Automated catalog, formula and generated browser-runtime tests.
* A real 404 page with HTTP 404 handling.

## Multilingual site

The site is generated in fifteen languages from one shared calculator and content source:

* English (`/`) is the default version and keeps the existing URL structure.
* Spanish (`/es/`), German (`/de/`), French (`/fr/`), Brazilian Portuguese (`/pt-br/`), Japanese (`/ja/`), Italian (`/it/`), Dutch (`/nl/`), Polish (`/pl/`), Simplified Chinese (`/zh-hans/`), Korean (`/ko/`), Arabic (`/ar/`), Ukrainian (`/uk/`), Russian (`/ru/`) and Turkish (`/tr/`) use language subdirectories.
* All 44 current source pages are generated in each language. Calculator formulas and browser-side logic are shared; visible page copy, titles, descriptions, FAQ content, guide content, navigation, validation messages and result labels are localized.
* Arabic pages use right-to-left document direction. Calculator result numbers use the browser's locale-aware `Intl.NumberFormat`.
* Every page has a self-referencing canonical URL, reciprocal `hreflang` alternates for all fifteen languages, and an English `x-default` alternate. The XML sitemap contains 660 localized page URLs and alternate-language references.
* The language selector is available on every page. Language choice is explicit; the site does not force IP-based redirects.

Translations are stored in `data/locales/`. The final `build_seo.py` step invokes `build_locales.py`, so the existing Cloudflare Pages build command automatically creates all language versions. The locale generator validates translation coverage and fails the build if newly added visible text or metadata has no translation. Add the corresponding source-string translations to all locale dictionaries whenever page content changes.

## Build and deployment pipeline

`data -> Python generators -> generated HTML/SEO files -> pytest -> GitHub Actions validation -> GitHub main -> Cloudflare Pages Git integration -> Cloudflare Pages deployment`

GitHub Actions is responsible for validation only. It runs the full test suite, generates the production site and validates the generated output.

Cloudflare Pages Git integration is the single production deployment mechanism. A push to `main` is picked up by the connected Pages project, which runs the configured build command and deploys the generated `site/` directory.

GitHub Actions does **not** run Wrangler deployment and does **not** require `CLOUDFLARE_API_TOKEN` or `CLOUDFLARE_ACCOUNT_ID`.

This separation prevents two independent deployment systems from competing with each other.

### Production monitoring and indexing

The separate `Production monitor` workflow periodically checks the public production site.

It verifies:

* Homepage availability.
* robots.txt.
* sitemap.xml.
* Construction calculator pages.
* Guide pages.
* Canonical metadata.
* Calculator UI.
* Sitemap URL count.
* HTTP 404 handling.

When `INDEX_NOW_KEY` is configured in the GitHub Actions environment, the monitor also verifies the public IndexNow key file and submits the sitemap URLs to IndexNow.

IndexNow notification is intentionally separate from the production deployment pipeline because Cloudflare deployment is asynchronous relative to the GitHub validation workflow.

## Cloudflare Pages build command

The Cloudflare Pages Git integration uses:

```text
pip install -e ".[dev]" && python -m pytest && python scripts/build.py && python scripts/build_calculators.py && python scripts/build_construction.py && python scripts/build_construction_index.py && python scripts/build_seo.py
```

Build output directory:

```text
site
```

The Pages project is connected directly to the `LozitskyiAlex/passive-income-engine` GitHub repository and uses `main` as the production branch.

## Cost model

Target recurring infrastructure cost: $0.

The project intentionally avoids per-visitor AI inference. Visitor calculations execute in the browser, so normal calculator usage does not require a paid API call.

## Next growth stages

1. Validate the 30-calculator release.
2. Monitor search indexing and search queries.
3. Add calculators only when they provide distinct user value.
4. Improve internal linking and category pages from observed demand.
5. Add free analytics and measure actual usage.
6. Introduce monetization only after useful traffic exists.

Potential monetization paths include contextual advertising, relevant affiliate offers and paid digital resources. No monetization is embedded until the underlying product has demonstrated demand.


## Regional measurement systems

Construction calculators use locale-specific regional defaults. English defaults to US customary units. Spanish, German, French, Brazilian Portuguese, Japanese, Italian, Dutch, Polish, Simplified Chinese, Korean, Arabic, Ukrainian, Russian and Turkish default to metric units. Locale metadata records the region and default measurement system.

Every construction calculator exposes a selector to switch between Metric and US customary units. Inputs are normalized to the existing calculation units, while metric outputs are converted to m, mm, m², m³, kg and kg/m³ as appropriate. Count outputs remain counts. Board feet and roofing squares are converted to metric volume and area in metric mode.

Input dimensions are declared per calculator in `scripts/build_construction.py`. The localized HTML includes regional defaults and unit labels. Conversion behavior is covered by `tests/test_regional_units.py`.
