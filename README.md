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
* Automated catalog and formula tests.

## Build pipeline

`data -> Python generators -> generated HTML/SEO files -> tests -> GitHub -> Cloudflare Worker`

The build is deterministic and does not require an AI API or database. Local Ollama can be used later for optional batch content assistance before content is committed.

## Next growth stages

1. Validate the 30-calculator release.
2. Monitor search indexing and search queries.
3. Add calculators only when they provide distinct user value.
4. Improve internal linking and category pages from observed demand.
5. Add free analytics and measure actual usage.
6. Introduce monetization only after useful traffic exists.

Potential monetization paths include contextual advertising, relevant affiliate offers and paid digital resources. No monetization is embedded until the underlying product has demonstrated demand.

## Cost model

Target recurring infrastructure cost: $0.

The project intentionally avoids per-visitor AI inference. Visitor calculations execute in the browser, so normal calculator usage does not require a paid API call.

<!-- Cloudflare rebuild trigger -->
