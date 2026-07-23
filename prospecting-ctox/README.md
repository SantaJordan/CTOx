# prospecting-ctox — CTOx cohort target lists from live job postings

Built live at the CTOx session, 2026-07-23. For each of the 8 cohort CTOs:
20–50 genuinely good-fit companies (sourced from job postings that *confess* the
exact problem that CTO has already fixed), 2–5 enriched decision-makers per
company, and a letter-style talk track per company.

## Run order (each script resumes if killed)

| # | Script | What it does |
|---|--------|--------------|
| 1 | `scripts/s1_cto_enrich.py` | Pull each CTO's full profile from FullEnrich (LinkedIn URLs as data) |
| — | *(agents)* | 8 dossier research agents → `dossiers/<slug>/dossier.md` + `signal_spec.json` |
| 2 | `scripts/s2 (curl)` | Download the open-jobs dataset (~21.7 GB parquet, CC0) to `data/` |
| 3 | `scripts/s3_build_index.py` | Integrity check + per-company open-postings counts |
| 4 | `scripts/s4_match.py` | Match all specs against ~967k jobs in one pass → company shortlists |
| 5 | `scripts/s5_liveness.py` | Re-verify every matched job against the company's live ATS feed |
| — | *(agents)* | One research agent per company → keep/drop + talk track (`research/companies/`) |
| 6 | `scripts/s6_blitz_people.py <slug>` | 2–5 buyers per kept company via Blitz |
| 7 | `scripts/s7_fullenrich.py <slug>` | Work email + mobile via FullEnrich bulk |
| 8 | `scripts/s8_assemble.py <slug>` | Merge into `output/<slug>_final.csv` (+ `--qa` checks) |
| 9 | `scripts/s9_google_sheet.py` | One Google Sheet: Summary + a people-list tab per CTO |

`scripts/keyscan.sh` — run before every commit; blocks the commit if any real
key value appears in staged changes.

Secrets live only in the repo-root `.env` (gitignored). Never commit keys;
never rotate keys. LinkedIn URLs are only ever passed to enrichment APIs as
data — no browser automation.

Data doctrine: match jobs whose EXISTENCE signals the problem (a "first Head of
Engineering" posting = no technical leadership), require a quotable line from a
live posting for every kept company, and compute all summary numbers from run
artifacts — never assert them by hand.
