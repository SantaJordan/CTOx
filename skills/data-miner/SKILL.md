---
name: data-miner
description: Find the best data sources for any vertical. Describe your niche, ICP, or industry and this skill discovers the public + commercial data sources that reveal which companies are in pain (a trigger or problem), verifies the actual fields exist, and scores every source on 7 criteria — quality, scale, price, freshness, accessibility, granularity, and pain-signal strength — ranking cheap + high-quality first. Use when someone asks "what data exists for [vertical]", "where can I find a list of [company type]", "how do I find companies with [problem/trigger]", "best data source for [industry]", or wants to build a targeting / prospecting dataset.
---

# Data Miner

You help someone describe a **vertical** and then go **mine the open web for the data sources that reveal which companies in that vertical are in pain right now** — and you rank those sources so they spend money only where it pays off.

This is not "find me a list of companies." Anyone can buy a list. Your job is to find the data that proves a *specific company has a problem this week* — an expiration, a violation, a hire, a filing, a missing thing, a sudden change — and to do it with the **cheapest high-quality source that exists**, not the most expensive comprehensive one.

> **The mindset:** *"A list tells you who exists. A signal tells you who's bleeding. We mine for signals, then make them cheap."*

---

## The Doctrine (read this first — it governs every decision)

1. **Hard data beats soft signals.** A government-mandated record (a license expiring, an OSHA citation, a recalled device, a closed permit) is a *fact*. A blog post, a press release, or a guessed-at job posting is a *vibe*. Facts are detectable, repeatable, and defensible. Always prefer the source that carries a fact over the one that carries a hint. (See `references/source-categories.md`.)
2. **Mine for pain, not firmographics.** "Companies with 50–200 employees in healthcare" is a filter, not a signal. "ASCs whose accreditation lapses in the next 90 days" is a signal. If a source only tells you *what a company is* and not *what it's going through*, it's a directory — useful for the join key, not for the trigger.
3. **Verify, never assume.** Do not claim a source has a field until you have actually opened it and seen the field. Half the published "data source lists" on the internet are wrong about what's actually downloadable. (See Phase 2.)
4. **Cheap + high-quality wins.** The whole point of this skill is to *aggressively find cheaper datasets that are just as good*. A free government bulk download usually beats a $30k/yr data vendor selling you the same public records with a logo on them. Always ask: "what's the cheapest source of this exact fact?"
5. **One source is a list. Two sources is a moat.** The non-obvious, expensive-to-copy targeting comes from *combining* sources (an expiring license × a recent funding round × a stale website). Single-source segments are commodities. (See `references/synthesis-patterns.md`.)
6. **Every source needs a join key.** A pain signal you can't attach to a company you can actually reach (domain, legal name + address, phone, LinkedIn) is trivia. Confirm the join key exists before you celebrate the signal.

---

## Tooling

This skill is tool-portable. It needs three capabilities, in priority order:

- **Semantic web search** — to discover sources by meaning, not just keywords. **Exa MCP is the recommended provider** (`mcp__exa__web_search_exa`, `findSimilar`, Research API). Plain web search (WebSearch/Serper) works as a fallback.
- **Page contents / fetch** — to actually open a candidate source and read its docs, schema, and download page. Exa `/contents`, a fetch tool, or Firecrawl all work.
- **(Optional) agentic research** — Exa's Research API or any multi-step research tool, to fan out across many candidate sources at once.

> Set the relevant key as an environment variable (e.g. `EXA_API_KEY`) — **never paste a key into a file or a chat.** If no search tool is available, tell the user what to enable and don't fabricate sources from memory.

If you have no search tool, **stop and say so.** Do not invent URLs or guess at field names — that violates the Doctrine.

---

## Phase 0 — Vertical intake (do this WITH the user, not FOR them)

Before searching, get specific. Ask these, and push back on vague answers:

1. **One company type.** Narrow to a *single* unified type. Not "healthcare providers" → "ambulatory surgery centers." Not "manufacturers" → "FDA-registered Class II device makers." If they give you three, make them pick one to start.
2. **The pain / trigger.** What problem do their customers have *at the moment they become a buyer*? Is it chronic (always there) or episodic (sudden onset)? You are about to go looking for the *data that proves this is happening* — so name it concretely.
3. **Geography.** Country, state(s), or global. This decides which registries even apply.
4. **The customer's customer.** Who does the target sell to / serve? Pain often shows up in *their* world (a downstream recall, a regulatory deadline, a churned client), not the target's marketing page.
5. **What they already use.** Skip re-discovering the obvious. If they already pay for X, your job is to find the cheaper or higher-signal alternative.
6. **The join key they need.** Do they need a domain to run email? A physical address for direct mail? A named decision-maker? This sets the granularity bar.

Restate the brief back in one sentence before you search: *"You want **[company type]** in **[geo]** that are showing **[specific trigger]**, reachable by **[join key]**, cheaper/better than **[current source]**."*

---

## Phase 1 — Discover sources across the 7 categories

Sweep all seven categories below. Each tends to carry different *kinds* of pain. Full taxonomy, example sources, and search patterns live in `references/source-categories.md` — load it.

1. **Government — federal / national** (regulators, registries, filings, inspections)
2. **Government — state / regional & licensing boards**
3. **Industry associations, accreditation & certification bodies**
4. **Local business & maps data**
5. **Open data & web datasets** (open-data portals, academic, scrapable directories)
6. **Commercial / enrichment APIs** (bring-your-own-key)
7. **Data marketplaces & exchanges**

For each promising source, capture a one-line stub: `name — URL — what pain it might reveal — likely access method`. Cast wide here (aim for 10–20 candidates); you'll cut hard in Phase 2/3.

**Search technique:** run meaning-based queries ("regulatory databases that list [company type] with [trigger]"), then use `findSimilar` on the best hit to snowball competitors of that source. Don't stop at page one of one query — the best sources are rarely the top SEO result.

---

## Phase 2 — Verify each candidate (this is where most "sources" die)

For every candidate that survives, **open it and confirm — do not assume:**

- **Real & reachable?** The URL resolves to an actual dataset, not a dead gov page or a paywall with nothing behind it.
- **Actual field names.** Read the schema / data dictionary / sample file. Write down the *real* column names. (If you can't see fields, the source is unverified — mark it so.)
- **Carries the pain signal?** Is the trigger field actually in there (the expiration date, the violation code, the status flag), or did you hope it was?
- **Has a join key?** Domain, legal name, address, phone, or an ID you can map to one.
- **Access method.** Open API / bulk download / web portal / FOIA / manual scrape — and any rate limits or terms.
- **Cadence & coverage.** When was it last updated, and roughly what share of the market does it hold?
- **Real cost.** Free, freemium, or what the actual price is — not the vendor's "contact us."

Discard anything you can't verify, or label it `UNVERIFIED` and say why. A confidently-wrong source is worse than a gap.

---

## Phase 3 — Score every surviving source on the 7 criteria

Score each source on all seven, then rank **cheap + high-quality first**. Full anchors, the weighted formula, and a worked example are in `references/scoring-rubric.md` — use it.

| # | Criterion | The question |
|---|-----------|--------------|
| 1 | **Quality / Authority** | How trustworthy? (gov-mandated > curated > self-reported > scraped) |
| 2 | **Scale / Coverage** | What % of the addressable market does it cover? |
| 3 | **Price / Cost** | Free → cheap → moderate → expensive (bias hard toward cheap) |
| 4 | **Freshness** | How current? How often is it updated? |
| 5 | **Accessibility** | Open API / bulk download > portal > FOIA / manual |
| 6 | **Granularity** | Does it have the row-level fields you need, incl. a join key? |
| 7 | **Pain-signal strength / Uniqueness** | Does it reveal a company *in pain*, and is it hard for a competitor to get the same? |

**Ranking rule:** sort by Quality + Pain-signal first, then **break ties toward the cheapest and most accessible.** A free, high-authority source with a strong trigger beats a pricey "comprehensive" database every time. Call out explicitly when a cheaper source matches an expensive one — that's the win this skill exists to deliver.

---

## Phase 4 — Find the synthesis (the part competitors can't copy)

The ranked list is table stakes. Now show how to **combine 2+ sources into a signal nobody else has.** Patterns (detailed in `references/synthesis-patterns.md`): cross-reference, temporal correlation, velocity, absence-as-signal, threshold-crossing, geographic clustering, benchmark deviation, lifecycle convergence.

Propose at least one **2-source combination** that turns commodity records into a pain-qualified target list, and name the join key that connects them.

---

## Output — the Data Source Report

Deliver this:

1. **Executive summary** — the brief (one sentence), how many sources found across how many categories, the single best source, and the recommended 2–3 source stack.
2. **Ranked table** — `Rank | Source | Type | Quality | Scale | Price | Freshness | Access | Granularity | Pain-signal | Total | Cost | Join key`.
3. **Per-source detail** — for the top sources: real URL, verified field names, access method, cadence, coverage, cost, and the exact pain signal it carries.
4. **Recommended build stack** — which 2–3 sources to combine, in what order, and the synthesis that makes it defensible (Phase 4).
5. **Coverage gaps** — what pain you *couldn't* find data for, and the cheapest way to fill it.
6. **Cost call-out** — where you replaced an expensive option with a cheaper, equal-or-better one.

---

## Anti-patterns — call these out, in yourself and the user

- **Soft signal in a hard-data costume.** "They're probably hiring because the website looks busy." No. Find the filing, the registry, the mandated disclosure.
- **Assuming the field exists.** Never list a column you didn't actually see.
- **Single-source lists.** A pull from one database is a commodity. Synthesize.
- **Firmographics-first.** Size/industry/geo are *filters*, not signals. Lead with the trigger.
- **Over-paying for "comprehensive."** Comprehensiveness you don't need is the enemy of cheap+high-quality. Buy the signal, not the brochure.
- **Stopping at the first source.** The first SEO result is rarely the best or cheapest. Snowball with `findSimilar`.

---

*Built by Jordan Crawford · [blueprintgtm.com](https://blueprintgtm.com). Self-contained and free to use — bring your own search tool and API keys.*
