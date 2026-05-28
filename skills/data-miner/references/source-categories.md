# The 7 Source Categories

Sweep all seven when mining a vertical. Each tends to carry a *different kind of pain*, so skipping a
category means missing a class of signal. For each: what it is, the pain it tends to reveal, public example
sources to anchor your search, and how to search for the vertical-specific ones.

> The named examples are **public, well-known starting points** — not an endorsement and not exhaustive.
> Your job is to find the *specific* registry/dataset for the user's exact vertical. Use semantic search and
> `findSimilar`, then **verify every source in Phase 2** before trusting it.

---

## 1. Government — federal / national

**What it is:** regulators, registries, mandatory filings, inspections, recalls, spending, and statistics
published by national agencies. The highest-authority data on earth, and usually free.

**Pain it reveals:** violations, citations, recalls, lapsed registrations, fines, contract wins/losses,
expirations, safety events — *facts a company is legally obligated to disclose.*

**Public anchors:**
- `data.gov` (US open-data catalog — the master index)
- SEC EDGAR (US public-company filings)
- openFDA (drugs, devices, food — recalls & adverse events)
- OSHA establishment search / enforcement data (workplace safety citations)
- US Census / County Business Patterns, Bureau of Labor Statistics (industry/firm statistics)
- USAspending.gov (federal contracts & grants)
- UK Companies House (free company register + filings)
- EU Open Data Portal, and national portals (e.g., data.gouv.fr, GOV.UK data)

**How to search:** `"[company type]" regulator OR registry site:*.gov`, `"[vertical]" inspection OR
violation OR recall dataset`, `open data "[company type]" bulk download`, then `findSimilar` the best hit.
Identify *which agency regulates this vertical first*, then hunt that agency's data page, API docs, and bulk
downloads.

---

## 2. Government — state / regional & licensing boards

**What it is:** state/provincial licensing boards, professional registries, permits, and inspections. Most
regulated professions and facilities are licensed at this level, not the federal one.

**Pain it reveals:** license status & **expiration dates**, disciplinary actions, new permits, lapsed
permits, fresh registrations (a brand-new license = a brand-new business in onboarding pain).

**Public anchors:**
- State professional licensing board lookups (medical, dental, contractor, cosmetology, etc.)
- State business entity / Secretary of State registrations
- Building-permit portals (city/county)
- State health-department facility licenses

**How to search:** `"[company type]" license lookup [state]`, `[state] [profession] board verify license`,
`[city/county] building permits search`. **Test 3–5 large states** (e.g., CA, TX, FL, NY, IL) to estimate
national coverage and effort, since each state is its own file/format. Look for multi-state aggregators that
save you from 50 scrapers — but verify they're current.

---

## 3. Industry associations, accreditation & certification bodies

**What it is:** trade associations, accreditation/certification registries, standards bodies, and member
directories. Often the *cleanest* picture of "serious operators in this niche."

**Pain it reveals:** accreditation status & lapses, certification expirations, membership (or conspicuous
*absence* of it), conference exhibitor lists (active-spend signal).

**Public anchors:**
- Accreditation/certification bodies' public "find a [member/center]" directories
- Trade-association member rosters
- Standards/ISO certificate registries
- Conference & trade-show exhibitor lists
- Better Business Bureau and similar accountability directories

**How to search:** `"[vertical]" trade association member directory`, `"[company type]" accreditation OR
certification registry`, `[vertical] conference exhibitors [year]`. The exhibitor list of the industry's
biggest annual show is a high-intent, public goldmine.

---

## 4. Local business & maps data

**What it is:** place/maps data for physical, locally-operating businesses (clinics, shops, contractors,
restaurants). Best for SMB verticals with storefronts.

**Pain it reveals:** new openings, closures (permanently-closed flags), low-review / low-rating signals,
missing website, recent relocation.

**Public anchors:**
- Google Places API (BYO key)
- OpenStreetMap / Overpass API (free, open)
- Yelp Fusion API
- Apple/Bing place data

**How to search:** query the maps provider directly with the business category + geo, then measure **website
inclusion rate** and **phone/address quality** on a sample — those determine whether the join key survives.
Test 2–3 category synonyms ("ambulatory surgery center" vs "ASC" vs "outpatient surgery") to gauge coverage.

---

## 5. Open data & web datasets

**What it is:** open-data portals beyond the core gov catalogs, academic/research datasets, and scrapable
public web directories.

**Pain it reveals:** depends entirely on the dataset — but this is where unusual, hard-to-copy signals hide
(research panels, niche registries, specialized directories).

**Public anchors:**
- Kaggle Datasets, Hugging Face Datasets, data.world
- Academic / institutional data repositories
- Common Crawl / public web indexes (for scrapable directories at scale)
- Niche industry directories and review sites

**How to search:** `"[vertical]" dataset kaggle OR github`, `"[company type]" directory -site:linkedin.com`,
`academic dataset "[topic]"`. When you find one scrapable directory, `findSimilar` it to surface the rest.
**Mind the terms of service** on anything scraped.

---

## 6. Commercial / enrichment APIs

**What it is:** paid APIs that enrich or supply company/contact data (firmographics, tech stack, contacts,
revenue, signals). Treat as the **join-key and fill-the-gap layer**, rarely the primary trigger.

**Pain it reveals:** some carry genuine triggers (hiring data, tech-stack changes, funding). Most just
identify and enrich — valuable for resolving a domain or adding contacts to a trigger you already found.

**Public anchors (categories, not endorsements):** semantic search providers, company/firmographic enrichment
APIs, contact-data APIs, tech-stack detection APIs, web-scraping APIs.

**Public-safety + cost discipline:**
- **Bring your own key**, set via an env var (e.g. `EXA_API_KEY`). **Never** hardcode or paste a key.
- Before recommending a paid API, ask: *is it just reselling a public record I can get for free?* If yes,
  route to the upstream source and use the API only for the join key.
- Prefer providers with transparent per-record pricing over "contact sales" annual contracts.

**How to search:** `"[data type] API" pricing`, `enrich company domain API free tier`, then score on the
rubric — Price and Pain-signal usually decide whether it earns a slot.

---

## 7. Data marketplaces & exchanges

**What it is:** marketplaces where datasets are listed for purchase/subscription, often delivered straight
into a warehouse or as a download.

**Pain it reveals:** packaged industry datasets, sometimes with real signals — but frequently **repackaged
public data at a markup**, so apply the cost discipline hard.

**Public anchors:** AWS Data Exchange, Snowflake Marketplace, Google Cloud public datasets, and similar cloud
data exchanges; data.world.

**How to search:** browse the marketplace for the vertical, then for each listing ask *"what's the upstream
source, and is it public?"* If it's public, score the marketplace listing low on Price and go to the source.
A marketplace earns its keep only when it offers genuinely proprietary or hard-to-assemble data.

---

## Sweep checklist

- [ ] Identified which **regulator(s)** own this vertical (Cat 1 & 2)
- [ ] Found the **trigger source(s)** that carry the actual pain signal
- [ ] Found at least one strong **join-key source** (domain or name+address)
- [ ] Checked for a **cheaper upstream** of any paid option (Cat 6 & 7)
- [ ] Have ≥2 sources that can be **synthesized** (see `synthesis-patterns.md`)
- [ ] Every source slated for the report is **verified** (Phase 2), not assumed
