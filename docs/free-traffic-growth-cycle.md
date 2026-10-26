# Free traffic growth cycle

This playbook is for the static construction calculator site. Use free tools and work on one evidence-backed improvement each cycle. Traffic is visitors/page views; search impressions and keyword estimates are separate discovery signals.

## Repeat every week

### 1. Record a baseline

Check the same date ranges in:

- Google Search Console: clicks, impressions, queries, pages, indexing coverage, sitemap status, and URL Inspection for a specific failure.
- Bing Webmaster Tools: clicks, impressions, indexed/discovered URLs, sitemap status, IndexNow history, and available free keyword research.
- Cloudflare Web Analytics: visits, page views, top pages, referrers, countries, and devices.

Record the date range and counts. Cloudflare visits are total measured site activity; call them search traffic only when a search referrer or search analytics confirms that source. Keyword tools estimate demand; they are not site visits.

### 2. Find one opportunity

Use free demand signals in this order:

1. Search Console queries/pages with impressions but few clicks: improve the matching page title, description, answer, and visible example.
2. Search Console and Bing queries with impressions or emerging long-tail questions: improve the relevant calculator or create one genuinely distinct guide/calculator.
3. With no query data, use Google autocomplete/People Also Ask and Bing Webmaster keyword research to find specific construction questions. Treat these as topic ideas or estimates, not measured visits.
4. Check internal links, sitemap/robots/canonical/HTTP status, mobile usability, and the existing production monitor for a concrete technical blocker.
5. If the site works and no content change is justified, prepare one useful answer for a relevant community or free directory. Follow that community's rules, provide the answer without requiring a click, disclose the site relationship, and do not mass-post or automate. Prepare a draft only; the user must approve external publication.

### 3. Choose and complete one action

Rank candidate actions by expected user value, evidence, effort, and risk. Choose one: fix a verified technical problem; improve one existing page; add one differentiated tool/guide with worked example and assumptions; strengthen relevant internal links; or prepare one tailored outreach contribution. Avoid thin pages, keyword stuffing, invented claims, copied supplier text, paid tools, and repetitive submissions.

For a content or code change, inspect sources and repository instructions, make the smallest source change, run the documented tests/build/CI, review the diff, and deploy through the existing GitHub-to-Cloudflare Pages flow only with the user's existing authorization and passing checks. Never deploy manually around CI. Submit to Google only after meaningful page changes; notify Bing through the existing IndexNow setup only for changed/new/deleted URLs. Repeated submissions do not create traffic or guarantee indexing. Never publish an outreach post or message on the user's behalf without separate explicit authorization.

### 4. Measure and adapt

After changes are live, verify the deployed page/monitor and record what changed. At the next cycle compare actual visits/referrers and search clicks/impressions against the same baseline window. If impressions rise but clicks do not, improve relevance and snippets; if clicks rise, strengthen related internal navigation and useful follow-up content; if neither changes, test a different evidenced question or distribution channel rather than repeating submissions.

## Done criteria for each cycle

- One dated baseline with source, time range, and distinct traffic vs demand counts.
- One selected opportunity with evidence and a completed action, or a precise blocker and next step.
- Verification evidence for any change, plus the deployment/PR state.
- No claim that submission guarantees indexing, ranking, or traffic.
