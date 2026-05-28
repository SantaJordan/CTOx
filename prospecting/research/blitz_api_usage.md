# Blitz API — Company Search + Enrichment for the CTOx Prospecting Pipeline

Source: https://docs.blitz-api.ai (OpenAPI spec `https://docs.blitz-api.ai/api-reference/v2.openapi.json`, fetched 2026-05-28).
Base URL: `https://api.blitz-api.ai` | Auth: `x-api-key` header | Plan: **Unlimited (flat-rate, all endpoints free, 50 QPS)**.

> Doc shortcut: every page has a `.md` variant; full machine index at `https://docs.blitz-api.ai/llms.txt`.

## TL;DR for the pipeline

- Blitz is **firmographic + people data only**. It has **NO funding / Series-A / round / tech-stack data anywhere** in the v2 schema (verified: zero `funding|series|stage|tech_stack|round|investor` fields in the OpenAPI spec). It cannot, on its own, tell you a company is Series A.
- We already have LinkedIn URLs, headcount, funding-range, revenue in the 900k CSV. So **do NOT re-buy firmographics from Blitz.** Blitz's job in this pipeline is **people: detect CTO/VP-Eng presence and pull contacts.**
- The `waterfall-icp-keyword` endpoint named in the brief = the **Waterfall ICP Search** people endpoint (`POST /v2/search/waterfall-icp-keyword`). There is no separate keyword product.

---

## 1. `POST /v2/search/companies` — Company Search

Find companies by ICP. All filters under `company` are optional; filters AND together, values within a filter OR together. Free on Unlimited.

### Request body (full filter set)
```jsonc
{
  "company": {
    "name":        { "include": [], "exclude": [] },          // keyword match on company name
    "industry":    { "include": [], "exclude": [] },          // EXACT, normalized enum (534 values, case-sensitive)
    "type":        { "include": [], "exclude": [] },          // enum: Privately Held, Public Company, Nonprofit, Partnership, Educational, Government Agency, Self-Employed, Self-Owned, Sole Proprietorship, Educational Institution
    "employee_range": ["1-10","11-50","51-200","201-500","501-1000","1001-5000","5001-10000","10001+"],
    "employee_count": { "min": 0, "max": 0 },                 // exact LinkedIn headcount range; 0 = unset
    "min_linkedin_followers": 1,
    "revenue":     { "min": 0, "max": 0 },                    // USD range; 0 = unset
    "naics_code":  { "include": ["541511"], "exclude": [] },
    "sic_code":    { "include": ["7372"], "exclude": [] },
    "web_traffic": { "min": 0, "max": 0 },                    // monthly visits range
    "ad_spend":    { "min": 0, "max": 0 },                    // monthly Google ad spend USD range
    "keywords":    { "include": ["SaaS"], "exclude": [] },    // matches description, specialties, NAICS/SIC desc, Crunchbase/G2 CATEGORIES
    "founded_year":{ "min": 0, "max": 0 },                    // range
    "hq": {
      "city":         { "include": [], "exclude": [] },
      "country_code": ["US"],                                  // 2-letter ISO
      "continent":    ["North America"],                       // enum
      "sales_region": ["NORAM"]                                // enum: NORAM, LATAM, EMEA, APAC
    }
  },
  "max_results": 25,        // default 10, max 25 (spec says enum max 50; guide says 25 — treat 25 as safe ceiling)
  "cursor": null            // cursor-based pagination; null = first page; response cursor null = end. Hard cap 1,000 pages.
}
```

### Response (per result)
`results_length`, `cursor`, and `results[]` each containing:
`name, linkedin_url, linkedin_id, about, specialties[], industry, type, size (band), employees_on_linkedin, followers, founded_year, hq{city,state,country_code,country_name,region,continent}, domain, website`.

### Could it REPLACE or AUGMENT our CSV?
- **No funding-stage filter exists** — so it cannot do the core Series-A targeting any better than our CSV. It would be a sidegrade on firmographics, not an upgrade.
- **AUGMENT (optional), do not replace.** Useful only to *discover companies the CSV misses* (e.g., via `keywords`, `naics_code`, `sic_code`, `web_traffic`, `ad_spend`, `founded_year` — signals our CSV lacks). For the current plan (filter the CSV we already own → enrich), Company Search is **not on the critical path**. Skip it unless we want net-new accounts beyond the 900k.
- Note: `keywords` searches Crunchbase/**G2 categories** (a "multi-platform / category" proxy) — mildly relevant to the "multi-platform" thesis, but it is category text, not integration data.

---

## 2. `POST /v2/enrichment/company` — Company Enrichment

### Request
```json
{ "company_linkedin_url": "https://www.linkedin.com/company/blitz-api" }
```
### Response
```json
{ "found": true, "company": {
    "linkedin_url","linkedin_id","name","about","specialties","industry",
    "type","size","employees_on_linkedin","founded_year",
    "hq": {...}, "domain","website" } }
```

**Does it return funding stage / Series A / tech stack?** **NO.** It returns the same firmographic fields as Company Search (industry, size band, employees_on_linkedin, hq, domain, type, about, specialties). **No funding, no round, no investors, no tech stack.** It **cannot determine Series A.**

We already have all of these fields in the CSV → **calling company enrichment is redundant. Skip it.**

---

## 3. Confirming Series A with Blitz

**Blitz cannot confirm Series A.** No endpoint or field carries funding-round data.

Recommended approach for the Series-A gate:
1. **Primary: trust the CSV** `Total Funding Range` + `Annual Revenue` + `Founded` + headcount band, and define a Series-A heuristic on those columns (e.g., funding range ~$2M–$20M, headcount 11–50/51–200, founded within last ~8 yrs). This is the cheapest filter and requires zero Blitz calls.
2. **Confirmation (outside Blitz): Exa / Serper news.** For true round confirmation you still need a news/Crunchbase-type source — Exa MCP semantic search ("[company] raises Series A") with a date filter, per this repo's Exa-required policy. Blitz does not replace that.
3. The Blitz `keywords` field (Crunchbase/G2 *categories*) is **not** a funding signal — do not mistake it for one.

---

## 4. `domain-to-linkedin` and `waterfall-icp-keyword`

### `POST /v2/enrichment/domain-to-linkedin` — resolve CSV domains → company LinkedIn URL
Request: `{ "domain": "example.com" }`
Response: `{ "found": true, "company_linkedin_url": "https://www.linkedin.com/company/..." }`
On `found: false`: no LinkedIn page maps (private / very small / different brand domain).
**We already have `LinkedIn Company URL` in the CSV → only call this as a FALLBACK for rows where that column is blank/invalid.**

### `POST /v2/search/waterfall-icp-keyword` — Waterfall ICP Search (decision-maker cascade)
This is the right tool to **detect whether a full-time CTO/VP-Eng exists** and grab the contact in one call. It tries each cascade tier in order and stops once `max_results` is hit.

Request:
```jsonc
{
  "company_linkedin_url": "https://www.linkedin.com/company/acme",   // required
  "cascade": [                                                       // required, ordered tiers
    {
      "include_title": ["Chief Technology Officer","CTO","VP Engineering","VP of Engineering","Head of Engineering"],
      "exclude_title": ["fractional","interim","advisor","assistant","intern","junior"],
      "location": ["WORLD"],                                         // "WORLD" = no geo restriction
      "include_headline_search": true                               // also scans LinkedIn headline text
    }
    // optional lower tiers, e.g. Director of Engineering, Lead Engineer, founder-who-is-technical
  ],
  "max_results": 5                                                    // 1–100
}
```
Response: `company_linkedin_url, max_results, results_length, results[]` where each result has:
- `icp` (which cascade tier matched), `ranking`,
- `person`: `full_name, first_name, last_name, headline, about_me, location, linkedin_url, connections_count, profile_picture_url, skills[], education[], certifications[]`, and
- `person.experiences[]`: `job_title, company_linkedin_url, company_domain, job_description, job_start_date, job_end_date, job_is_current, job_location`.

**CTO-detection logic:**
- `results_length == 0` on a CTO/VP-Eng tier → **no full-time eng exec exists** = strong "no full-time CTO" signal (matches the ICP).
- A match with `job_is_current: true` and `job_start_date` → there IS a full-time CTO → **disqualify** (or flag for a different play). Use `exclude_title` to drop fractional/interim/advisor titles so they don't count as a full-time CTO.
- `experiences[].job_start_date` gives tenure — useful to distinguish a brand-new hire from an entrenched exec.

Alternative for batch: `POST /v2/search/employee-finder` (single company) supports `job_level: ["C-Team","VP"]` + `job_function: ["Engineering","Information Technology"]` — a cleaner boolean "is there an eng exec?" check, paginated. Either works; waterfall is better because it returns the contact you'd actually email in the same call.

---

## 5. What to actually call Blitz for (minimize redundancy)

Given the CSV already has Domain, LinkedIn URL, Industry, Headcount, Employee Size Range, Funding Range, Revenue, Founded, Locality:

| CSV already has it | Blitz endpoint | Verdict |
|---|---|---|
| Firmographics (industry, headcount, size, locality) | Company Search / Company Enrichment | **SKIP** — redundant, and Blitz adds no funding/stack data |
| Funding / Series A | (none in Blitz) | **SKIP Blitz**, use CSV columns + Exa/Serper news to confirm |
| Company LinkedIn URL | `domain-to-linkedin` | **FALLBACK ONLY** — call when CSV's LinkedIn URL is missing/bad |
| Full-time CTO / VP-Eng presence | `waterfall-icp-keyword` (or `employee-finder`) | **CALL** — core Blitz value here |
| Contact email | `enrichment/email` | **CALL** — to make the contact actionable |
| Contact phone (optional) | `enrichment/phone` | Optional |

### Minimal Blitz call plan — per qualified company
After the CSV is filtered to the ICP (Series A + tech-enabled + multi-platform + integration/silo pain — all done in-CSV / Exa, **no Blitz**):

1. **(Fallback only)** `POST /v2/enrichment/domain-to-linkedin` — *only if* the CSV LinkedIn URL is blank/invalid. Otherwise 0 calls.
2. `POST /v2/search/waterfall-icp-keyword` with the CTO/VP-Eng cascade →
   - 0 results = "no full-time CTO" ✔ keep; or a current-CTO match = disqualify.
   - On keep, this **also returns the decision-maker** you want (founder / technical lead / VP-Eng) for outreach.
3. `POST /v2/enrichment/email` on the chosen `person.linkedin_url` → verified work email.

**= 2 Blitz calls per company in the common case (waterfall + email), 3 if domain resolution is needed.** All free + parallelizable up to 50 QPS, so 900k→filtered set enriches fast.

Health-check the key with `GET /v2/account/key-info` (no cost) before any batch run.

---

## Recommended PLAN MODIFICATIONS
1. **Drop Company Search and Company Enrichment from the plan** — they duplicate CSV data and provide no funding/tech-stack lift. Keep Company Search in your back pocket only to source net-new accounts beyond the 900k (it has NAICS/SIC/web-traffic/ad-spend/founded-year filters the CSV lacks).
2. **Series A gating stays CSV-first + Exa/Serper for confirmation** — Blitz contributes nothing to the funding signal.
3. **Use the CSV's LinkedIn URL directly**; reserve `domain-to-linkedin` for blanks only.
4. **Put `waterfall-icp-keyword` at the heart of the "no full-time CTO" detector** (with `exclude_title` for fractional/interim), then chain `enrichment/email`.
