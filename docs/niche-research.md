# Niche research, September 2026

## Objective

Find a product that can be operated for $0 in recurring infrastructure cost, can be generated from code and public data, solves a specific user problem, and has a realistic path to organic traffic and monetization.

## Constraints

* No paid API
* No paid hosting
* No VPS
* No mandatory subscription
* No domain required for MVP
* No user accounts
* No database
* Prefer browser-side computation
* Automation must add real utility, not mass-produce thin SEO pages

## Evidence

### 1. Focused free tools

Recent side-project reports show that users search for individual problems rather than for generic collections of tools. One 2026 report about a 170+ tool site explicitly identified discovery as the main challenge. This supports a focused problem-first architecture rather than a generic "1000 tools" website.

### 2. Calculator websites

CalcSmith is an open source zero-dependency static generator specifically designed for calculator sites. It generates individual calculator pages, structured data, sitemap and SEO elements. The project documents live niche sites built with this model.

This is technically aligned with our zero-cost architecture because calculations can execute entirely in the browser and the site can be static.

### 3. Utility networks

An open source 2026 utility network demonstrates a larger static-tool model using browser-side HTML, JavaScript and CSS, with Cloudflare Pages and advertising/affiliate monetization. This confirms that the architecture can scale across many tools without a backend.

### 4. Organic traffic and monetization

A 2026 side-project report described a baking substitution site that generated hundreds of programmatic pages around specific user questions and later reported substantial search impressions and revenue. This is self-reported and should be treated as a case study, not a guaranteed outcome.

Other 2026 community reports show free tool sites receiving organic traffic while struggling to monetize. The recurring lesson is that traffic alone does not guarantee affiliate revenue.

## Important SEO constraint

Google states that generating many pages primarily to manipulate search rankings can qualify as scaled content abuse. Google also says AI-assisted content is acceptable when it provides useful, original value, but generating large quantities of low-value pages is not.

Therefore this project will not generate pages merely because a keyword exists. Every generated page must correspond to a useful tool, dataset, comparison, calculation, or other concrete user function.

## Infrastructure decision

GitHub Pages is not appropriate as the intended commercial host because GitHub explicitly says Pages is not intended to operate an online business or commercial SaaS.

Cloudflare Pages is a better target for the public site. As of September 2026, its Free plan allows up to 500 builds per month, 20,000 files per site and 25 MiB per individual asset.

## Candidate directions

### A. Focused calculator suite

Examples:
* construction and renovation calculators
* material quantity calculators
* household cost calculators
* conversion calculators for specific professions
* shipping and packaging calculators

Advantages:
* browser-side computation
* no database
* easy static deployment
* strong long-tail structure
* useful output is deterministic
* affiliate opportunities can be attached to relevant products

Risks:
* generic calculator space is competitive
* formulas must be accurate
* some financial and health calculators create higher trust requirements

### B. Public-data directory

Examples:
* grants and funding opportunities
* public programs
* events
* free resources
* software or service directories

Advantages:
* data can be refreshed automatically
* pages can contain genuinely changing information
* easier differentiation than generic tools

Risks:
* source terms and data licenses must be checked
* stale data damages trust
* scraping is not automatically permitted

### C. Narrow comparison and decision tools

Examples:
* product compatibility checkers
* material selectors
* file-format decision tools
* travel packing calculators
* equipment selection helpers

Advantages:
* higher commercial intent
* useful affiliate placement can be contextual
* tool output can be more valuable than generic articles

Risks:
* factual maintenance
* affiliate programs may require approval
* product data sources can change

## Current direction

Build the engine so that a focused calculator or decision-tool product can be launched first. Keep collectors and data adapters generic so a public-data product can be added later without rewriting the core.

The first implementation should prioritize browser-side tools and deterministic data. AI should remain an optional enrichment layer for research, taxonomy, explanations and metadata, not the calculation itself.

## Decision criteria

Before launching the first public niche, score candidates internally against:

1. User problem clarity
2. Search intent
3. Competition
4. Ease of producing genuinely useful pages
5. Data availability
6. Accuracy requirements
7. Automation potential
8. Monetization fit
9. Infrastructure cost
10. Maintenance burden

No candidate is considered validated until it has evidence for demand and a concrete set of useful tools.
