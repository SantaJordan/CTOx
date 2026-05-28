# Carl Maloney — Integration-Gap Leads

**Google Sheet (top 25, pain-sorted, with CEO/COO contacts — verified accurate):**
https://docs.google.com/spreadsheets/d/1n1pVRGD7BdnU8s98blpgG6TQxDU2EWUQiYEifMHT53k/edit

> Sharing is private to the owner — share directly with Carl. (An earlier draft sheet
> `1rsrlOrdPWdjL3WcKkrpn7ijzGYFXf32VB8y7somFcIA` had transcription errors and should be trashed.)

## The full dataset
- **`companies_by_pain_PUBLIC.csv`** (in this repo, redacted — no names/emails/phones): all **617**
  Series A integration-gap targets, pain-sorted, with axis scores, integration opportunity,
  tech-team ratio, full-time-CTO flag, job-pain signal, and openers.
- **Full contact version** (CEO/COO + top technical contacts with **emails + phones**) lives only
  in the local, git-ignored `prospecting/output/companies_by_pain.csv` (617) and
  `prospecting/output/people.csv` (1,088 people) — kept out of this public repo as personal data.

### Load all 617 + the full people roster into the Sheet (10 seconds)
In the Google Sheet: **File → Import → Upload** → `prospecting/output/companies_by_pain.csv`
(and add a second tab from `people.csv`). This streams the complete, exact data straight from
the local files (the model can't reliably stream 600+ rows through a tool call, so import is the
clean path for the full set).

## Coverage (617 companies)
- CEO found: 407 · COO: 106 · **with email: 395 · with phone: 410** (Blitz + FullEnrich)
- No full-time CTO (the booster): ~419 · tech-team count/ratio populated: 431
- Job-pain signal (Apify `fantastic-jobs` + free ATS): 121 companies

## Data-quality notes for Carl
- `dm_email_domain_ok = no` flags an email whose domain ≠ the company domain (a founder's
  personal/alt address, or a stale match). Treat those emails as lower-confidence; the
  **phone** is usually still good for cold-calling.
- A few "decision-makers" resolved to advisors (title contains "Advisor", sometimes with an
  email on a different company's domain). Re-verify on LinkedIn before outreach in those cases.
- Method, rubric, and reproducible pipeline: see `../CASE_STUDY.md` and `research/axis*.md`.
