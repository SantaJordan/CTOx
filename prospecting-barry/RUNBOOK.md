# prospecting-barry — Barry Hess "Lab-to-Field Disconnect" pipeline

Ranked prospect list for **Barry Hess** (Quantum Surge Technologies — TS/SCI-cleared
fractional CTO, 30 yrs DoD/IC). Finds early-stage defense tech companies (mobile /
sensors / data collection / AI-ML / cyber, selling to DoD) and ranks them by how
**disconnected their own language is from deployed-environment reality** — the more
lab-blind, the better the prospect, because that gap is exactly what Barry closes.

Barry's dossier + signal spec: `../prospecting-ctox/dossiers/barry-hess/`.
Doctrine injected into every scoring agent: `../prospecting-ctox/dossiers/DOCTRINE-BRIEF.md`.

**Deliverable:** Google Sheet "Barry Hess — Lab-to-Field Disconnect Prospects"
(id in `checkpoints/sheet_id.txt`) + `output/barry_final.csv`.

## Results (run of 2026-07-23)

| | |
|---|---|
| Candidates sourced (4 channels, deduped) | 895 |
| Verified US early-stage defense companies | 569 |
| Scored by agents | 568 (259 keep / 274 drop / 35 insufficient evidence) |
| Ranked companies after dedup | 258 |
| Companies with contacts pulled | 108 |
| People (CEO + CTO) | 207 — 90% with email, 97% with mobile |

## Run order

| # | Command | What it does |
|---|---|---|
| 1 | `uv run --with aiohttp python3 scripts/s1_vc_portfolios.py` | Cache portfolio pages of 15 defense/natsec VC funds → `data/page_cache/`. Agents then extract companies → `checkpoints/portco_extract_{A,B,C}.jsonl`. |
| 2 | `python3 scripts/s2_exa_agent.py create` → `poll` → `more` → `poll` | Exa Agent API: 5 defense-domain queries + a "find 25 more" continuation each → `checkpoints/exa_agent_runs.jsonl` (238 companies). |
| 3 | `python3 scripts/s3_sbir_awards.py` | DoD SBIR/STTR **Phase II** 2022+ from the bulk CSV (`data/sbir_award_data.csv`, from `data.www.sbir.gov/awarddatapublic/award_data.csv` — the public JSON API returns TooManyRequests). Lexicon-filtered; SBIR mills flagged and excluded. |
| 4 | *(reuse)* `../prospecting-ctox` `s4_match.py barry-hess` | Jobs-are-confessions channel: candidates + JD evidence from the 967k-job parquet. |
| 5 | `python3 scripts/s4_merge.py` | Dedupe all channels by domain→name, keeping provenance. |
| 6 | `python3 scripts/s5_blitz_verify.py` | Blitz firmographics; drop non-US / >300 headcount / primes / staffing; derive `stage_band`. |
| 7 | `python3 scripts/s6_build_packs.py` | One evidence pack per company → `research/packs/`. Their own site copy (Exa), SBIR abstracts, news, live jobs, plus Barry's niche/EDP and the deployed-reality checklist. |
| 8 | Agent fan-out per `scripts/AGENT_PROMPT.md` | Disconnect-scoring verdicts → `research/verdicts/<slug>.json`. Run a 10-pack pilot first and re-check calibration. |
| 9 | `python3 scripts/s7_rank.py` | Validate verdicts, sort keeps → `data/ranked_companies.csv`. |
| 10 | `python3 scripts/s8_people.py --top 135` | Blitz people: CEO + CTO buckets (fractional/interim excluded) → `output/people.csv`. |
| 11 | `python3 scripts/s9_fullenrich.py` | FullEnrich bulk waterfall → `checkpoints/enrich.jsonl`. |
| 12 | `python3 scripts/s9b_repair_join.py` | **Required.** FullEnrich does not echo `linkedin_url` back in the response body, so the join key arrives empty; this restores it positionally (verified against name matches) and flags off-domain emails. |
| 13 | `python3 scripts/s10_assemble.py --qa` | `output/barry_final.csv` + `_public.csv` (no mobiles). |
| 14 | `python3 scripts/s11_sheet.py` | Google Sheet via the `gws` CLI. |

## The disconnect score (0–100, higher = better prospect)

Five 0–20 subscores, verbatim quote required for any subscore above 10:
`lab_language_intensity`, `deployment_awareness_absence`, `operator_absence`,
`hiring_profile_skew`, `stage_pressure`.

**Two gates run before any scoring:**
1. **DoD intent** must appear in the company's *own* artifacts (SBIR award, explicit
   military-customer language, DIU/AFWERX engagement). Defense-VC portfolio membership
   alone is not enough. Primes, systems integrators, staffing/services shops, SBIR mills,
   and companies already fielded at scale are dropped.
2. **Evidence sufficiency** — under ~500 words of own language → `insufficient_evidence`,
   never ranked. Absence of deployment awareness only counts when the product is
   described in enough detail that the topic would naturally come up.

Companies fluent in ATAK/ATO/DDIL score LOW and sit at the bottom — they already get it.

## Gotchas found during the run

- **iCloud deleted this directory mid-run.** The repo lives on an iCloud-synced Desktop;
  `research/packs/` and all of `scripts/` were removed while the pipeline was running
  (the `.git 2` / `.git 3` conflict copies at the repo root are the same phenomenon).
  The run was finished from a non-iCloud scratchpad and copied back. Re-run outside iCloud.
- **Exa news false positives.** The "News (Exa, top 3)" pack section frequently returns
  articles about a *different* company with a similar name (Deca Defense → DeCA the
  commissary agency; Ursa Inc → Ursa Major; also Lonestar, Lumos, Odyssey, Omni, Walaris,
  Kirkwall, Misram). Scoring agents were instructed to disregard news that doesn't match
  the company's own description. Worth adding a name-similarity check to `s6_build_packs.py`.
- **Own-language word counts are inflated** by nav menus, cookie banners, repeated
  homepage crawls, and in one case reCAPTCHA's privacy policy. Treat the count as a
  floor, not a measurement.
- **`pison` / `pison-technology`** were one company arriving from two source records.
  `s7_rank.py` output is deduped by domain; watch for this pattern.

## Secrets

Keys live only in the gitignored repo-root `.env` (`EXA_API_KEY`, `BLITZ_API_KEY`,
`FULLENRICH_API_KEY`, `OPENAI_API_KEY`). `data/`, `checkpoints/`, and `output/` are
gitignored — `output/` holds emails and mobile numbers. Run
`bash ../prospecting-ctox/scripts/keyscan.sh` before every commit.
