# The 7-Criteria Scoring Rubric

Score every *verified* data source (one that survived Phase 2) on all seven criteria. Then rank
**cheap + high-quality first.** The point of this skill is to aggressively find the *cheapest source of a
given fact that is still high-quality* — so price and quality both carry real weight, and the pain signal
is what separates a useful source from a phone book.

You can score two ways:

- **Fast:** rate each criterion `HIGH / MED / LOW` and eyeball the ranking with the ranking rule below.
- **Rigorous:** rate each criterion `0–5`, apply the default weights, and sort by weighted total.

Use Fast for a quick scan; use Rigorous when the user is about to spend money.

---

## The criteria and their anchors

### 1. Quality / Authority — *how much can you trust it?*
The single most important quality question: **who is forced to keep this accurate, and why?**

| Score | Anchor |
|-------|--------|
| 5 (HIGH) | Government-mandated record. Someone is legally required to report it accurately (licenses, filings, inspections, recalls). |
| 4 | Curated by a body with skin in the game (accreditation lists, certification registries, audited member directories). |
| 3 (MED) | Self-reported but structured (a directory companies opt into and maintain). |
| 2 | Aggregated/third-party compiled from multiple sources of unknown freshness. |
| 1 (LOW) | Scraped, crowdsourced, or modeled/inferred with no accountability. |

### 2. Scale / Coverage — *what share of the market is in it?*
| Score | Anchor |
|-------|--------|
| 5 | ~Complete census of the company type in scope. |
| 3 | Partial but representative (e.g., the large states, the certified subset). |
| 1 | A thin slice; useful only as a seed or for enrichment. |

Estimate with evidence — a sample query, a stated record count — not a guess. State your basis.

### 3. Price / Cost — *what does the exact fact actually cost?* (bias hard toward cheap)
| Score | Anchor |
|-------|--------|
| 5 | Free — open download or open API. |
| 4 | Effectively free at your volume (generous free tier / cents per record). |
| 3 | Cheap and transparent (clear per-record or low monthly price). |
| 2 | Moderate (a real subscription, but justifiable for the signal). |
| 1 | Expensive / "contact sales" / annual contract. |

**Always ask: is the same fact available cheaper somewhere?** A vendor reselling public records at a premium
scores low here — find the upstream source it's reselling.

### 4. Freshness — *how current, and how often refreshed?*
| Score | Anchor |
|-------|--------|
| 5 | Real-time or updated daily/weekly. |
| 3 | Monthly/quarterly — fine for slow-moving triggers. |
| 1 | Annual or stale/unknown — risky for episodic pain. |

Freshness only matters relative to the trigger: a yearly license file is fine for "expires in 90 days,"
useless for "filed for bankruptcy yesterday."

### 5. Accessibility — *how hard is it to actually get the data out?*
| Score | Anchor |
|-------|--------|
| 5 | Open API or one-click bulk download (CSV/JSON/Parquet). |
| 4 | Documented API with a key, or scheduled bulk export. |
| 3 | Web portal you can query and export from. |
| 2 | Scrape-only (HTML, no export) — possible but brittle; respect terms. |
| 1 | FOIA request, manual lookup, or behind a hard paywall. |

### 6. Granularity — *does it carry the row-level fields you need, including a join key?*
| Score | Anchor |
|-------|--------|
| 5 | Row-level records with the trigger field **and** a strong join key (domain, or legal name + address). |
| 3 | Row-level but a weak/missing join key (name only — you'll have to resolve it). |
| 1 | Aggregated/rolled-up only (counts, regional totals) — no individual companies. |

A source with no join key is enrichment fodder, not a target list. Note exactly which join key it provides.

### 7. Pain-signal strength / Uniqueness — *does it prove a company is in pain, and is it hard to copy?*
This is the criterion that makes this skill different from a TAM/list-building exercise.

| Score | Anchor |
|-------|--------|
| 5 | A specific, dated, verifiable trigger (an expiration, a citation, a recall, a status change) that few competitors are using. |
| 3 | A real but commoditized signal (everyone targeting this vertical already pulls it). |
| 1 | No trigger — it's a directory of *who exists*, not *who's hurting*. |

Two questions decide this: **(a)** Does a row tell you something is *happening* to that company? **(b)** Could a
competitor send the exact same insight from the same place tomorrow? Specific + hard-to-copy = high.

---

## Default weights (for the Rigorous method)

These weights encode this skill's bias — **pain signal, quality, and price lead; coverage and plumbing
follow.** Adjust per use case (e.g., bump Coverage if the user genuinely needs a full census), but state any
change.

| Criterion | Weight |
|-----------|--------|
| Pain-signal strength / Uniqueness | 25% |
| Quality / Authority | 20% |
| Price / Cost | 20% |
| Granularity | 15% |
| Scale / Coverage | 10% |
| Accessibility | 5% |
| Freshness | 5% |

`Weighted total = Σ (criterion score 0–5 × weight)`, giving a 0–5 number. Higher = better.

---

## Ranking rule

1. Sort by **Quality + Pain-signal** (or weighted total).
2. **Break ties toward the cheapest and most accessible** source.
3. Explicitly flag any case where a **cheaper source matches or beats an expensive one** — that swap is the
   deliverable. ("You don't need the $24k/yr vendor; the same records are a free bulk download here.")
4. A source scoring LOW on Pain-signal can still earn a spot **as the join-key / enrichment layer** — label
   it that way, don't rank it as a primary trigger source.

---

## Worked example

**Brief:** ambulatory surgery centers (ASCs), US, trigger = *accreditation lapsing in next 90 days*, join key
needed = domain.

| Source | Qual | Scale | Price | Fresh | Access | Gran | Pain | Weighted | Verdict |
|--------|:----:|:-----:|:-----:|:-----:|:------:|:----:|:----:|:--------:|---------|
| State health-dept ASC license files (bulk) | 5 | 4 | 5 | 3 | 4 | 4 | 4 | **4.25** | **Primary trigger** — free, authoritative, carries license/expiry + name+address. |
| Accreditation body public "find a center" directory | 4 | 3 | 5 | 4 | 3 | 4 | 5 | **4.20** | **Primary trigger** — directly shows accreditation status; strongest signal. |
| National provider registry (open download) | 5 | 5 | 5 | 4 | 5 | 3 | 2 | 4.05 | **Join-key layer** — best coverage + identifiers, but no pain on its own. |
| Commercial healthcare data vendor (subscription) | 4 | 5 | 1 | 4 | 4 | 5 | 3 | 3.55 | **Skip** — resells mostly-public records at a premium; cheaper sources match it. |

**Read-out:** combine the accreditation directory (the trigger) with the open provider registry (the domain
join key) → ASCs with lapsing accreditation, reachable by email — built from two free sources. The
subscription vendor is the cost we *removed.*
