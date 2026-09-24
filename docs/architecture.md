# Architecture

## Pipeline

source data -> normalization -> validation -> optional AI enrichment -> static generation -> sitemap -> deployment

## Design rules

1. Runtime pages should not require an API.
2. Runtime pages should not require a database.
3. Calculations should run in the browser where practical.
4. Source data should be stored in versioned JSON.
5. Every generated page must provide a concrete user function.
6. Generated copy must be derived from structured facts and reviewed by validation rules.
7. AI is an optional build-time component.
8. Failed external sources must not silently replace valid data with invented values.

## Planned directories

src/passive_income_engine/collectors/
Public source adapters.

src/passive_income_engine/normalizer/
Schema normalization and deduplication.

src/passive_income_engine/ai/
Optional local Ollama integration.

src/passive_income_engine/generator/
Static HTML, metadata, sitemap and structured data.

data/raw/
Source snapshots.

data/processed/
Validated datasets used for builds.

site/
Generated static output.

scripts/
Build and maintenance commands.

.github/workflows/
Tests, data refreshes and deployment.

## Deployment

Target: Cloudflare Pages Free.

The public site should remain static. Server-side functionality is not part of the MVP.
