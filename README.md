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

The first product is a construction calculator site deployed as static assets through a Cloudflare Worker.

**Live site:** https://passive-income-engine.oleksoleks07.workers.dev/

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

## Build and deployment pipeline

`data -> Python generators -> generated HTML/SEO files -> pytest -> GitHub Actions validation -> GitHub main -> Cloudflare Git integration -> Cloudflare build -> Cloudflare Worker`

GitHub Actions is responsible for validation only. It runs the full test suite, generates the production site and validates the generated output.

Cloudflare Git integration is the single production deployment mechanism. A push to `main` is picked up by the connected Cloudflare project, which runs the configured build command and deploys the resulting Worker assets.

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

## Cloudflare build command

The Cloudflare Git integration should use:

```text
pip install -e ".[dev]" && python -m pytest && python scripts/build.py && python scripts/build_calculators.py && python scripts/build_construction.py && python scripts/build_construction_index.py && python scripts/build_seo.py
```

The Cloudflare project deploys the generated `site/` directory using the repository's `wrangler.jsonc`.

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

<!-- Cloudflare Git integration is the production deployment source of truth. -->
