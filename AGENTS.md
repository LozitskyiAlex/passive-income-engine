# Repository instructions

## Project at a glance

This repository builds the static construction calculator site at
https://free-construction-calculators.pages.dev/. Source data lives in `data/`,
build and SEO generators in `scripts/`, browser-side code in `src/`, tests in
`tests/`, and generated output in `site/`. See `README.md` and
`docs/architecture.md` for product and architecture context.

Keep the product and its operating costs at $0: do not introduce paid APIs,
hosting, subscriptions, or per-visitor services. Prefer static pages and
browser-side calculations. Do not add thin/repetitive pages, unsupported
claims, fabricated measurements, or copied supplier text. Search traffic is
not guaranteed by deployment or sitemap submission.

## Set up

Requirements: Python 3.11 and Node.js 22 (Node is used by browser-runtime
checks). From the repository root:

```sh
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The package has no runtime dependencies. The `dev` extra installs pytest.
Playwright/browser dependencies are provisioned by CI as configured in the
workflow; inspect the workflow before adding local setup assumptions.

## Build

Generate the site in the same order as CI:

```sh
python scripts/build.py
python scripts/build_calculators.py
python scripts/build_construction.py
python scripts/build_construction_index.py
python scripts/build_seo.py
```

Generated production files go to `site/`. Do not hand-edit generated output;
change source data, templates, or generators and rebuild.

## Verify changes

Run the full suite and generated-output checks after relevant code/content
changes:

```sh
python -m pytest
python -m pytest tests/test_generated_site.py -q
```

CI also validates the production package:

```sh
test -f wrangler.jsonc
test -f site/index.html
test -f site/404.html
test -f site/robots.txt
test -f site/sitemap.xml
test -f site/deployment-version.txt
```

If Node.js 22 is available, run the browser-runtime checks included in the
full suite; report clearly if the required browser runtime is unavailable.

## Linting and formatting

No dedicated linter or formatter is configured in `pyproject.toml` or the
current CI workflows. Do not claim lint/format checks passed or introduce a
formatter solely to silence style differences. Follow the surrounding Python,
JavaScript, HTML, JSON, and YAML style.

## Deployment and external services

- GitHub Actions validates pull requests and builds; it does not deploy.
- Cloudflare Pages Git integration deploys pushes to `main`. Keep it the
  single production deploy mechanism; do not add Wrangler deploys or require
  Cloudflare deployment secrets in CI.
- Production SEO monitoring and IndexNow submission are separate from the
  build/deploy path. Never expose IndexNow keys or other secrets in logs,
  source, reports, or chat.
- Treat Search Console, Bing Webmaster Tools, Cloudflare Analytics, and
  browser observations as separate evidence. Record date range, counts, status,
  and limitations; keyword volume is not site traffic.
- Submit only changed or newly published URLs within the available free quota.
  Do not repeatedly submit unchanged URLs or claim that a submission guarantees
  indexing or visitors.
- Do not post outreach or messages to third-party communities on the user's
  behalf without explicit authorization.

## Work process

For each bounded task:
1. State the short plan and observable completion criteria before editing.
2. Inspect the relevant source, existing instructions, and git status first.
3. Make the smallest coherent change in source files.
4. Run the applicable build and verification commands above; report exact
   commands and outcomes. Fix failures caused by the change.
5. Review the final diff and leave unrelated user changes untouched.
6. If blocked, stop the dependent step and record the concrete blocker, what
   was attempted, and the next actionable step. Do not describe waiting as
   progress.

For recurring free traffic work, follow
`docs/free-traffic-growth-cycle.md`: record dated Search Console, Bing, and
Cloudflare baselines; distinguish measured visits/search clicks from keyword
demand; select and complete one evidence-backed growth action per cycle; verify
changes and adapt from observed results. Prefer useful page improvements,
internal links, and targeted human participation over repeated submissions.
Prepare external outreach drafts only; publish them only after separate explicit
authorization.

Do not commit directly to `main` or deploy manually unless the user explicitly
requests that action. Changes should be reviewable in a pull request; merge only
when the user has authorized publishing and required checks pass.
