# From a Voice Memo to 617 Pain-Sorted Leads: Building a Fractional-CTO Prospecting Engine with Claude Code

*A Blueprint GTM case study by Jordan Crawford*

---

## The mission

Carl Maloney spent roughly a decade at Veeva Systems as a principal technical consultant and migration-services practice manager — the person who took business requirements and made them happen technically, the translator between the people who want the outcome and the engineers who build it. Now he runs **Extension Cloud Solutions** as a fractional CTO. His pitch is simple and unfashionable: *"I fix data silos across systems that don't talk, and I eliminate manual data entry."*

The hard part of any fractional-CTO practice isn't the work — it's finding the companies who need it *right now*. So we built a prospecting engine to do exactly that, encoding Carl's ideal customer into a repeatable, scorable rubric.

The ICP we landed on, after several rounds of sharpening, is a company that is:

1. **Missing a business-critical integration** that would unlock real growth — a connection to a major system-of-record (Epic, Athena, Workday, Salesforce, NetSuite, and so on — *not* a fixed list).
2. **Running multiple platforms** that must talk to each other (high integration complexity).
3. **Showing silo pain** — staff manually re-keying or re-reporting data from one system into another, with a human acting as the API between two tools.
4. **Thin on technical leadership** — no full-time CTO to own the build (a strong booster signal).

The canonical example is **Solved Health**, a gamified, CAPCE-accredited EMS continuing-education app. We had three interview transcripts in which Carl was being evaluated as the fractional-CTO candidate — by founder John Kepley, CEO Kevin Jacobs, and CPO Tara Massarelli. Solved Health is the textbook instance of the pattern: a product-and-dev team with no technical quarterback sitting between product and engineering, plus a data-quality pain in the reporting layer. It's the persona we scored and messaged *against*, even though it isn't (yet) a paying client.

---

## The ordered process

The real requests came in as messy, voice-dictated bursts over a working session. Cleaned up and put in order, the build went like this:

**(a) Load the context and map the tools.** Read the two CTO-interview PDFs into project memory, and inventory every relevant primitive in the Blueprint-GTM-Skills toolkit so we knew what we had to work with.

**(b) Stand up the healthcare data lake.** Connect the mimilabs healthcare-data MCP (`databricks-mimi` — NPPES, CMS, OpenPayments, FDA, HRSA, X12, CDC tables) and *validate it returns genuine data* before trusting it for anything.

**(c) Define the target.** Using Carl's LinkedIn plus his own worked examples (a WayPave→Workday connection, a Zion Healthcare→benefits integration, and Solved Health), articulate the target as: companies where building one integration unlocks a large market, and where technical leadership is thin enough that they'd hire help.

**(d) Add the third voice.** Read the third interview PDF (Tara Massarelli, CPO) to round out the Solved Health persona.

**(e) Get a free TAM.** Find Eric Nowoslawski's GrowthEngineX `coldoutboundskills` repo and adopt its bundled US software/SaaS list — roughly **173,000 companies** with domain, LinkedIn, industry, headcount, funding range, and description — as the free total addressable market. Document the repo so collaborators can clone it as a sibling, and pull the Exa key from the Blueprint GTM repo's environment.

**(f) Iterate the ICP.** Drop the Veeva-only framing (that market is a "bloodbath") in favor of *any* growth-unlocking integration; add the integration-complexity and silo-pain axes; set Blitz as the primary data engine (unlimited) with Exa as fallback; keep every key out of the public repo.

**(g) Build the rubric and filter.** Stand up the three scoring axes via parallel research subagents, then filter the 173k TAM down to **617 clean Series-A-band candidates**, and validate the Blitz contact engine on a small dry-run sample.

**(h) Expand and enrich.** Enrich all 617: CEO and COO with email *and* phone (Carl cold-calls), a technical-team count and ratio plus the top technical contacts, job-posting scrapes for pain signal, a per-company opener and a "why I believed" rationale, all sorted by pain — delivered as a people list, a company list, and an HTML playbook.

---

## The primitives that mattered most

A handful of tools and techniques carried the whole build. Here's what each did and why it earned its place.

**Blitz (the people engine).** On its unlimited, flat-rate plan (50 QPS, every endpoint free), Blitz became the workhorse for everything people-related: detecting whether a full-time CTO exists, finding decision-makers, counting the engineering team, and pulling emails and phones. One important discovery: Blitz holds firmographics and people data only — it has **no funding, round, or stage data anywhere** in its schema. That's why we deliberately *didn't* re-buy firmographics from it. The 173k CSV already had funding ranges; Blitz's job was strictly people.

**Exa (semantic search).** Reserved as the fallback for the things keyword filters miss — confirming a company is actually Series A, surfacing recent news, and finding lookalikes from a single URL.

**The mimilabs / Databricks healthcare data lake.** A genuine claims-and-provider data source for grounding the healthcare slice of the ICP, validated against real tables before we leaned on it.

**Eric Nowoslawski's free SaaS TAM.** Instead of paying for a list, we started from a 173k-company open dataset and let the rubric do the qualifying. The free starting corpus is what made the whole thing economical.

**The 4-axis pain rubric.** Each axis (missing integration, integration complexity, silo pain, leadership gap) was written as a 0–5 scoring guide with explicit anchors, keyword banks, and — crucially — a *false-positives* section. The biggest trap the rubric guards against: a company whose **product** is integration (an iPaaS or ETL vendor) lights up every keyword but is the worst possible fit. The filter demotes those automatically, the same way it demotes consultancies and agencies that merely *sell* integration labor.

**Word-boundary keyword scoring (and the bug it fixed).** Naive substring matching is a disaster — searching for "api" matches "therapist," "edi" matches "media." Every keyword scan uses a word-boundary regex (`(?<![a-z0-9])term(?![a-z0-9])`) so a token only counts as a whole word. This single guard removed a large class of false matches across all three axes.

**The email domain-match guard.** When an enrichment call returns an email whose domain doesn't match the company's own domain, that's almost always a wrong-person match (we hit one where a contact's email came back on an unrelated company's domain). Every returned email is flagged `email_domain_ok = yes/no` so Carl never cold-calls the wrong person.

**Free ATS APIs for job signal.** Rather than pay a scraper, we detect a company's applicant-tracking system from its careers page and hit the **free public JSON** endpoints for Greenhouse, Lever, and Ashby. Job titles and descriptions are then scored for two things: integration/API roles (reinforcing axes 1–2) and ops/data-entry/RevOps/reconciliation roles (the smoking gun for axis 3 — a human being paid to be the API). Companies with no detectable ATS are *logged*, never silently dropped.

**Concurrent enrichment plus agent fan-out.** The architecture splits cleanly by task type. Deterministic, high-volume API work runs as **concurrent Python** (thread pools of ~20–24 workers, checkpointed to JSONL so any rerun is cheap and resumable). Qualitative judgment — writing the pain narrative, the keep/drop call, the opener — runs as **batched agent fan-out**, ~15–20 companies per agent. Fast where speed matters, smart where judgment matters.

**Strict secrets hygiene.** This repo is public. Every key (BLITZ_API_KEY, EXA_API_KEY, and the rest) lives only in a **gitignored `.env`**, referenced by name in code and never hardcoded. The publishing skill that pushes the HTML playbook live is invoked *in place* from its existing global location — it is never copied into this repo, because it carries credentials. A final grep for key patterns runs before any commit.

---

## How to recreate this

This recipe builds directly on Jordan Crawford's Blueprint GTM methodology — PVP (Permissionless Value Prop), PQS (pain-qualified segments), EDP (the Existential Data Point a vertical lives or dies by), and the governing rule that **"the message is a redescription of the targeting."** If your targeting is precise, the outreach writes itself.

1. **TAM.** Start from a free, rich company list (Eric Nowoslawski's `coldoutboundskills` SaaS corpus is an excellent default). Don't pay for what's already open.
2. **Rubric.** Encode your ICP as scoring axes — each 0–5, with keyword banks *and* an explicit false-positives section. Build the axes in parallel with research subagents.
3. **Filter.** Score the TAM from CSV text alone first (funding band, industry, axis keywords). Use word-boundary matching. Demote anyone who *is* the cure or who merely *sells* the cure. This cheaply collapses 173k → a few hundred real candidates.
4. **Enrich.** Run concurrent, checkpointed API calls for the people layer: leadership detection, decision-makers with email and phone, team count and ratio. Guard every email with a domain match.
5. **Pain-sort.** Add real-world pain signal — free ATS job feeds for hiring signals, news confirmation via semantic search — then compute a composite pain score and sort. Log everything you drop.
6. **Message.** For each kept company, write a one-to-two-line opener that is a redescription of *why it scored* — plus a "why I believed" rationale — and grade the openers (Eric's `cold-email-copy-grader` works well) before shipping.
7. **Deliver.** Output a people list, a company-by-pain list, and an HTML playbook. Publish the playbook with your existing publishing tooling; keep its credentials out of the repo.

The result is an engine, not a one-off list: rerun it monthly, and the pain re-sorts itself as companies post new jobs, raise new rounds, and lose (or fail to hire) their technical quarterback.

---

*Built with Claude Code on the Blueprint GTM methodology by Jordan Crawford — [blueprintgtm.com](https://blueprintgtm.com).*
