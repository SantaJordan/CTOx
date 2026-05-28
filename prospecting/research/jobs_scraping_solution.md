# Job Postings Scraping Solution (for Carl Maloney prospecting)

**Goal:** pull a company's job postings (by company name + domain + LinkedIn URL) to detect (a) integration/API hiring and (b) ops / data-entry "silo pain."

**Date proven:** 2026-05-28. All Apify tests run via REST (`run-sync-get-dataset-items`, token as `?token=`). Apify MCP is denied in this repo; REST works fine. WebSearch/WebFetch not used.

---

## TL;DR — Recommended method (ranked)

| Rank | Source | Why | Company scoping |
|---|---|---|---|
| **1 (PRIMARY)** | **Apify `fantastic-jobs/advanced-linkedin-job-search-api`** | Returns full `description_text` (5k–9k chars) **plus AI-enriched fields** (`ai_key_skills`, `ai_core_responsibilities`, `ai_requirements_summary`) that are perfect for silo-pain / integration-hiring detection. Filters by exact LinkedIn org slug. | `organizationSlugFilter` = the slug from the company's LinkedIn URL — no numeric ID lookup needed |
| 2 (fallback / confirm) | **Exa `POST /search` (+contents.text)** | Instantly surfaces careers pages + ATS boards (Greenhouse/Lever/Ashby) and returns page text. No setup, near-zero cost. Good for companies not well-indexed on LinkedIn, or to confirm. | query `"{company} integration engineer job"` |
| 3 (light, no descriptions) | Apify `valig/indeed-jobs-scraper` | Runs cleanly, returns titles + employer, but **`description` comes back empty** → can't read silo-pain. Use only for "is this company hiring" counts. | `title` param = company name |
| ✗ DO NOT USE | OpenWebNinja Jobs API | **Key in `.env` returns HTTP 401 on every endpoint** (even documented `realtime-web-search/search-light`). Key is `ak_…`, 50 chars, no whitespace — it is invalid/expired. Cannot test the Jobs API until a working key is supplied. |

---

## Key fixes for the things that failed before

- `bebity~indeed-scraper` → does not exist (404). Use **`valig~indeed-jobs-scraper`** or **`borderline~indeed-scraper`** (621k & 426k runs) instead.
- `misceres~indeed-scraper` circular-JSON crash → abandon; use `valig`.
- **`curious_coder~linkedin-jobs-scraper` HTTP 400 root cause = `count` must be `>= 10`.** Also `urls` must be an **array of plain strings**, not objects. With `count: 10` + string URLs it returns HTTP 201 with full 5001-char descriptions. BUT a free-text `?keywords=Reachdesk` search returns noisy, duplicated, off-company results (e.g. Atlassian jobs mentioning the keyword). To scope to a company you'd need the numeric `f_C=<companyId>` (hard to obtain reliably). **This is why `fantastic-jobs` (slug filter) is preferred.**

---

## #1 PRIMARY — exact working call

**Endpoint**
```
POST https://api.apify.com/v2/acts/fantastic-jobs~advanced-linkedin-job-search-api/run-sync-get-dataset-items?token=$APIFY_TOKEN
Content-Type: application/json
```

**Body (company-scoped, all roles):**
```json
{
  "organizationSlugFilter": ["reachdesk"],
  "limit": 10,
  "descriptionType": "text",
  "timeRange": "6m"
}
```

**Body (company-scoped + narrowed to integration / API / data-entry / ops roles):**
```json
{
  "organizationSlugFilter": ["gocardless"],
  "titleSearch": ["integration", "api", "data entry", "operations"],
  "limit": 10,
  "descriptionType": "text",
  "timeRange": "6m"
}
```

**Where the slug comes from:** the company's LinkedIn URL.
`https://www.linkedin.com/company/reachdesk` → slug = `reachdesk`. This is the only input Carl needs (he already has the LinkedIn URL per company).

**`timeRange` allowed values:** `1h`, `24h`, `7d`, `6m` (NOT "6 Months" — that 400s). `limit` minimum is 10.

**Output field names (load-bearing):**
- `title`, `organization`, `url` (LinkedIn job URL), `external_apply_url`, `date_posted`
- `description_text` ← **the full description (NOT `description`, which is empty)**
- `ai_key_skills` (array), `ai_core_responsibilities`, `ai_requirements_summary`, `ai_keywords` ← **use these for integration/API + silo-pain classification**
- Company firmographics, free per row: `linkedin_org_slug`, `linkedin_org_employees`, `linkedin_org_industry`, `linkedin_org_size`, `linkedin_org_url`, `linkedin_org_headquarters`, `linkedin_org_specialties`
- `recruiter_name`, `recruiter_title`, `recruiter_url` (LinkedIn profile of the recruiter — bonus contact)

**Proof it worked (3 companies, all HTTP 201):**

| slug | items | sample `description_text` len | scoping correct? |
|---|---|---|---|
| reachdesk | 10 | 5,371 | yes — all `organization = Reachdesk` (116 emp, Software Development) |
| gocardless | 10 | 5,668 – 8,361 | yes — all GoCardless |
| monzo-bank | 10 | 5,363 – 9,460 | yes — all Monzo Bank |

Title-filter proof: `gocardless` + `titleSearch:["integration","api","data entry","operations"]` narrowed 10 → 2 ops roles (`AML&E Operations Analyst III`, `People Operations Manager`).

**Note:** to get *all* a company's open roles (not just 10), raise `limit` (max is high) — for prospecting 400 companies, 10–25/company is plenty to read hiring signals.

---

## #2 Exa — works as discovery + fallback

**Endpoint**
```
POST https://api.exa.ai/search
Header: x-api-key: $EXA_API_KEY
```

**Body:**
```json
{
  "query": "GoCardless integration engineer API job opening",
  "numResults": 5,
  "type": "auto",
  "contents": { "text": { "maxCharacters": 1500 } }
}
```

**Proven:** surfaces careers pages + ATS boards directly — e.g. for Reachdesk it returned `job-boards.eu.greenhouse.io/reachdesk/jobs/4856869101`; for GoCardless it returned `job-boards.greenhouse.io/gocardless/jobs/7904230` plus a "Solutions Engineer — Payments & API Integrations" listing. With `contents.text` it returns ~page text per result.

**Strengths:** zero setup, instant, surfaces ATS (Greenhouse/Lever/Ashby) you can then crawl per-board; great for companies thin on LinkedIn.
**Weakness:** results are page-level, not a clean structured job table; dedupe/parse needed. Use to *confirm* a signal or as fallback, not as the bulk structured pull.

Useful query patterns: `"{company} integration engineer job"`, `"{company} careers integration"`, or domain-anchored: add `"includeDomains":["greenhouse.io","lever.co","ashbyhq.com"]` to jump straight to ATS boards.

---

## #3 valig/indeed-jobs-scraper — runs, but no descriptions

```
POST https://api.apify.com/v2/acts/valig~indeed-jobs-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN
{ "title": "Reachdesk", "country": "us", "limit": 5 }
```
HTTP 201, 5 items, `employer.name = "Reachdesk"`, fields include `title`, `employer`, `jobUrl`, `datePublished`, `baseSalary`, `description` — **but `description` is empty (len 2 = empty HTML).** No flag exists in its schema to enable descriptions (params: `country`, `title`, `location`, `limit`, `datePosted` only). Use only for "is X hiring / how many roles" — not for reading pain signals.

(`curious_coder` LinkedIn scraper does return full descriptions and is the most-used jobs actor (2.18M runs), but only company-scopes well with a numeric `f_C` ID; `fantastic-jobs` slug filtering avoids that entirely, so it wins.)

---

## OpenWebNinja — blocked

OpenWebNinja **does** have a Jobs/JSearch API, but the `OPENWEB_NINJA_API_KEY` in `.env` returns **HTTP 401 ("Unauthorized") on every endpoint**, including the documented working `GET /realtime-web-search/search-light`. Tested header variants (`x-api-key`, `X-API-KEY`, `apikey`, `Authorization: Bearer`, `?api_key=`) and whitespace-stripped key — all 401. Key is `ak_…`, 50 chars. **Conclusion: the key is invalid/expired.** Once a working key is provided, the JSearch jobs endpoint is the path to test (it aggregates LinkedIn/Indeed/Glassdoor/ZipRecruiter into structured JSON with descriptions). Not viable today.

---

## Cost notes

- All three Apify actors are **PAY_PER_EVENT** (charge per result/job row + a small per-run start fee). The Apify API does not expose the per-event USD amount (it lives on the store listing). Public listing rates: `fantastic-jobs` ≈ **$5 / 1,000 jobs**; `valig` ≈ low single-digit $ / 1,000; both bill mainly per result, so a 10-job/company pull is fractions of a cent per company.
- **400 companies × 10 jobs = ~4,000 job rows.** At ≈$5/1k that's **≈$20 total** on `fantastic-jobs` (plus tiny per-run start fees). Well within typical Apify monthly credit.
- Exa: ~$0.005–0.01 per search; 400 searches ≈ $2–4. Use only for fallback/confirm.

---

## Recommendation for scraping ~400 companies fast

1. **Bulk path:** loop the 400 companies, calling `fantastic-jobs/advanced-linkedin-job-search-api` once per company with `organizationSlugFilter:[slug]` (slug parsed from each company's LinkedIn URL), `limit: 25`, `descriptionType:"text"`, `timeRange:"6m"`. Run async (`POST /v2/acts/{actor}/runs`, `waitSecs:0`) in batches and poll, or fan out `run-sync` calls with modest concurrency (~5–10 parallel).
2. **Classify** each returned job from `title` + `ai_key_skills` + `ai_core_responsibilities`/`ai_requirements_summary`:
   - **Integration/API hiring** = title or ai_key_skills hit `integration|API|middleware|iPaaS|Zapier|Workato|data engineer|RevOps systems`.
   - **Silo / data-entry pain** = title/skills hit `data entry|manual|reconciliation|ops analyst|admin|coordinator` or descriptions mention copying between systems / spreadsheets.
3. **Fallback** for any company that returns 0 LinkedIn jobs: one Exa search `"{company} careers integration engineer"` with `includeDomains` for Greenhouse/Lever/Ashby, then read `contents.text`.
4. Capture per company: open-role count, the integration/silo classification, plus the free firmographics (`linkedin_org_employees`, `linkedin_org_industry`) and `recruiter_url` as a bonus contact.

This was a diagnose-and-prove task — no mass enrichment was run.
