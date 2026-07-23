# prospecting-barry — Barry Hess "Lab-to-Field Disconnect" pipeline

Sorted prospect list for Barry Hess (Quantum Surge Technologies — TS/SCI-cleared
fractional CTO, 30 yrs DoD/IC). Finds early-stage defense tech companies (mobile /
sensors / data collection / AI-ML / cyber, selling to DoD) and ranks them by how
**disconnected their own language is from deployed-environment reality** — the more
lab-blind, the better the prospect (that gap is exactly what Barry fixes).

Barry's dossier + signal spec: `../prospecting-ctox/dossiers/barry-hess/`.
Doctrine injected into agents: `../prospecting-ctox/dossiers/DOCTRINE-BRIEF.md`.

## Run order

| # | Command | What it does |
|---|---|---|
| 1 | `uv run --with aiohttp python3 scripts/s1_vc_portfolios.py` | Cache portfolio pages of 15 defense/natsec VC funds → `data/page_cache/`, manifest in `checkpoints/`. Extraction agents then write `checkpoints/portco_extract.jsonl`. |
| 2 | `python3 scripts/s2_exa_agent.py create` → `poll` → `more` → `poll` | Exa Agent API: 5 defense-domain queries + one "find 25 more" each → `checkpoints/exa_agent_runs.jsonl`. |
| 3 | `python3 scripts/s3_sbir_awards.py` | DoD SBIR/STTR **Phase II** 2022+ from the bulk CSV (`data/sbir_award_data.csv`, from data.www.sbir.gov/awarddatapublic/award_data.csv — public API is offline). Lexicon-filtered, mills flagged → `checkpoints/sbir_awards.jsonl`. |
| 4 | *(reuse)* `../prospecting-ctox` `s4_match.py barry-hess` + `s5_liveness.py` | Jobs-are-confessions channel: candidates + JD evidence from the 967k-job parquet. |
| 5 | `python3 scripts/s4_merge.py` | Dedupe all channels by domain→name, provenance kept → `data/candidates_merged.csv`. |
| 6 | `python3 scripts/s5_blitz_verify.py` | Blitz firmographics; drop non-US / >300 headcount / primes / staffing; `stage_band` → `checkpoints/blitz_verify.jsonl`, `data/universe_verified.csv`. |
| 7 | `python3 scripts/s6_build_packs.py` | One evidence pack per company (their own words via Exa, SBIR abstracts, news, hiring profile, Barry context + deployed-reality checklist) → `research/packs/`. |
| 8 | Agent fan-out per `scripts/AGENT_PROMPT.md` (pilot 10 first) | Disconnect-scoring verdicts → `research/verdicts/<slug>.json`. |
| 9 | `python3 scripts/s7_rank.py` | Validate verdicts, sort keeps by disconnect_score → `data/ranked_companies.csv`. |
| 10 | `python3 scripts/s8_people.py` | Blitz people: CEO + CTO buckets (EXCL fractional/interim) for top 100 → `output/people.csv`. |
| 11 | `python3 scripts/s9_fullenrich.py` → `poll` | FullEnrich bulk waterfall: work email + mobile → `checkpoints/enrich.jsonl`. |
| 12 | `python3 scripts/s10_assemble.py [--qa]` | `output/barry_final.csv` + `_public.csv` (no mobiles), sorted by disconnect score. |
| 13 | `python3 scripts/s11_sheet.py` | Google Sheet "Barry Hess — Lab-to-Field Disconnect Prospects". |
| 14 | `bash ../prospecting-ctox/scripts/keyscan.sh` then commit | Keys never committed; `data/ checkpoints/ output/` gitignored. |

## Disconnect score (0–100, higher = more lab-blind = better prospect)

Five 0–20 subscores, quotes required above 10, gated on genuine DoD intent first:
`lab_language_intensity`, `deployment_awareness_absence`, `operator_absence`,
`hiring_profile_skew`, `stage_pressure`. Companies fluent in ATAK/ATO/DDIL score
LOW. <500 words of own language → `insufficient_evidence`, never ranked.
