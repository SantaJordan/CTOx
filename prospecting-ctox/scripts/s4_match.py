# /// script
# requires-python = ">=3.10"
# dependencies = ["duckdb", "pyarrow", "numpy"]
# ///
"""s4 — match the job universe against every CTO's signal spec, in ONE pass.

Per CTO with a dossiers/<slug>/signal_spec.json:
  1. Embed expertise_statements (text-embedding-3-small, cached).
  2. DuckDB structured+lexical pass -> candidate jobs with lexical evidence flags.
     Hard gate (doctrine): a job only survives with >=1 situation-evidence lexical
     hit (leadership-gap title, strong title, or jd_lexicon term). Cosine alone
     never admits a company.
  3. One streaming pass over the parquet scores candidates for ALL CTOs at once
     (cosine title/JD vs each CTO's statement matrix).
  4. Aggregate to companies, blend scores, boost leadership-gap + domain-pain
     co-occurrence, cap company size, write top shortlist + per-job evidence.

Outputs per CTO:
  checkpoints/match/<slug>_jobs.jsonl       (scored candidate jobs w/ evidence)
  checkpoints/match/<slug>_companies.csv    (ranked company shortlist)
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_common import DATA, DOSSIERS, checkpoint_path, http_json, key, say

import duckdb
import numpy as np
import pyarrow.dataset as ds

PARQUET = DATA / "open-jobs.parquet"
COUNTS = DATA / "company_job_counts.parquet"
SHORTLIST = 80            # ~2x the 20-50 target, pre-liveness churn
MAX_COMPANY_JOBS = 75     # default guard; spec can override
W_TITLE, W_JD, W_LEX = 0.45, 0.35, 0.20


def esc(s):
    return s.replace("'", "''").lower()


def embed(texts):
    resp = http_json("https://api.openai.com/v1/embeddings",
                     {"model": "text-embedding-3-small", "input": texts},
                     {"Authorization": f"Bearer {key('OPENAI_API_KEY')}"})
    m = np.array([d["embedding"] for d in resp["data"]], dtype=np.float32)
    return m / np.linalg.norm(m, axis=1, keepdims=True)


def load_specs():
    specs = {}
    for d in sorted(DOSSIERS.iterdir()):
        f = d / "signal_spec.json"
        if f.exists():
            specs[d.name] = json.loads(f.read_text())
    return specs


def any_like(col, terms):
    terms = [t for t in terms if t and len(t) >= 3]
    if not terms:
        return "FALSE"
    return "(" + " OR ".join(f"lower({col}) LIKE '%{esc(t)}%'" for t in terms) + ")"


def candidates_for(con, spec):
    tl = spec.get("title_lexicon", {})
    strong = tl.get("strong", [])
    supporting = tl.get("supporting", [])
    gap = spec.get("leadership_gap_titles", [])
    jdlex = spec.get("jd_lexicon", [])
    disq = spec.get("disqualifiers", [])
    industry = spec.get("industry_keywords", [])
    countries = spec.get("structured", {}).get("country_codes", ["US", "CA", ""])
    country_sql = ",".join(f"'{esc(c).upper() if c else ''}'" for c in countries)

    # Industry gate: the company itself must look like the CTO's vertical. Without
    # this a generic "DevOps Engineer" title matches every industry on earth, which
    # is exactly how a game-studio spec returned adtech companies.
    ind_expr = (f"({any_like('company_does', industry)} OR {any_like('industry', industry)}"
                f" OR {any_like('company', industry)})") if industry else "TRUE"

    q = f"""
    SELECT id, ats, company, url, title,
           coalesce(role_summary, '') AS role_summary,
           coalesce(company_does, '') AS company_does,
           coalesce(industry, '') AS industry,
           coalesce(company_stage, '') AS company_stage,
           coalesce(posted_at, '') AS posted_at,
           substr(jd_markdown, 1, 1800) AS jd_head,
           {any_like('title', strong)} AS hit_strong,
           {any_like('title', supporting)} AS hit_supporting,
           {any_like('title', gap)} AS hit_gap,
           {any_like('jd_markdown', jdlex)} AS hit_jdlex,
           {ind_expr} AS hit_industry
    FROM read_parquet('{PARQUET}')
    WHERE (upper(coalesce(country_code,'')) IN ({country_sql})
           OR coalesce(remote_scope,'') IN ('global','us-only','us-canada'))
      AND {ind_expr}
      AND ({any_like('title', strong)} OR {any_like('title', gap)}
           OR {any_like('jd_markdown', jdlex)})
      AND NOT ({any_like('company', disq)} OR {any_like('company_does', disq)})
    ORDER BY (CAST({any_like('title', strong)} AS INT) * 4
            + CAST({any_like('title', gap)} AS INT) * 3
            + CAST({any_like('jd_markdown', jdlex)} AS INT)) DESC
    LIMIT 40000
    """
    return {r[0]: r for r in con.execute(q).fetchall()}


def main():
    specs = load_specs()
    if not specs:
        sys.exit("No signal_spec.json files found yet — dossiers not done?")
    say(f"Matching for {len(specs)} CTOs: {', '.join(specs)}")

    con = duckdb.connect()
    counts = {(a, c): n for a, c, n in con.execute(
        f"SELECT ats, company, open_jobs FROM read_parquet('{COUNTS}')").fetchall()}

    cand, stmt_mats = {}, {}
    for slug, spec in specs.items():
        stmts = spec["expertise_statements"]
        stmt_mats[slug] = embed(stmts)
        cand[slug] = candidates_for(con, spec)
        say(f"{slug}: {len(cand[slug]):,} candidate jobs after structured+lexical gate")

    wanted = set().union(*[set(c) for c in cand.values()])
    say(f"Scoring embeddings for {len(wanted):,} distinct jobs (single streaming pass)…")

    sims = {slug: {} for slug in specs}
    dataset = ds.dataset(PARQUET)
    scanner = dataset.scanner(columns=["id", "title_embedding", "jd_embedding"],
                              batch_size=8192)
    seen = 0
    for batch in scanner.to_batches():
        ids = batch.column("id").to_pylist()
        pre = [i for i, x in enumerate(ids) if x in wanted]
        if not pre:
            continue
        te_raw = batch.column("title_embedding").take(pre).to_pylist()
        je_raw = batch.column("jd_embedding").take(pre).to_pylist()
        mask = [pre[i] for i in range(len(pre))
                if te_raw[i] is not None and len(te_raw[i]) == 1536
                and je_raw[i] is not None and len(je_raw[i]) == 1536]
        if not mask:
            continue
        keepi = [i for i in range(len(pre))
                 if te_raw[i] is not None and len(te_raw[i]) == 1536
                 and je_raw[i] is not None and len(je_raw[i]) == 1536]
        te = np.asarray([te_raw[i] for i in keepi], dtype=np.float32)
        je = np.asarray([je_raw[i] for i in keepi], dtype=np.float32)
        te /= np.clip(np.linalg.norm(te, axis=1, keepdims=True), 1e-9, None)
        je /= np.clip(np.linalg.norm(je, axis=1, keepdims=True), 1e-9, None)
        sel_ids = [ids[i] for i in mask]
        for slug, M in stmt_mats.items():
            ct = (te @ M.T).max(axis=1)
            cj = (je @ M.T).max(axis=1)
            pool = cand[slug]
            for j, jid in enumerate(sel_ids):
                if jid in pool:
                    sims[slug][jid] = (float(ct[j]), float(cj[j]))
        seen += len(mask)
    say(f"Embedded-scored {seen:,} job rows")

    for slug, spec in specs.items():
        max_jobs = spec.get("structured", {}).get("max_company_open_jobs", MAX_COMPANY_JOBS)
        jobs_out = checkpoint_path("match", f"{slug}_jobs.jsonl")
        jobs_out.write_text("")
        companies = {}
        for jid, row in cand[slug].items():
            (jid_, ats, company, url, title, role_summary, company_does, industry,
             company_stage, posted_at, jd_head, h_strong, h_sup, h_gap, h_jdlex,
             h_ind) = row
            if counts.get((ats, company), 0) > max_jobs:
                continue
            ct, cj = sims[slug].get(jid, (0.0, 0.0))
            lex = 0.5 * bool(h_strong) + 0.2 * bool(h_sup) + 0.3 * bool(h_jdlex)
            score = W_TITLE * ct + W_JD * cj + W_LEX * min(lex, 1.0) + 0.10 * bool(h_gap)
            rec = {"id": jid, "ats": ats, "company": company, "url": url,
                   "title": title, "score": round(score, 4),
                   "cos_title": round(ct, 4), "cos_jd": round(cj, 4),
                   "hit_strong": bool(h_strong), "hit_supporting": bool(h_sup),
                   "hit_gap": bool(h_gap), "hit_jdlex": bool(h_jdlex),
                   "role_summary": role_summary, "company_does": company_does,
                   "industry": industry, "company_stage": company_stage,
                   "posted_at": str(posted_at), "jd_head": jd_head}
            k = (ats, company)
            companies.setdefault(k, []).append(rec)

        ranked = []
        for (ats, company), jobs in companies.items():
            jobs.sort(key=lambda r: -r["score"])
            best = jobs[0]
            has_gap = any(j["hit_gap"] for j in jobs)
            has_pain = any(j["hit_jdlex"] or j["hit_strong"] for j in jobs)
            cscore = best["score"] + 0.05 * min(len(jobs) - 1, 3) \
                + (0.15 if (has_gap and has_pain) else 0.0)
            ranked.append({"ats": ats, "company": company,
                           "company_open_jobs": counts.get((ats, company), 0),
                           "fit_score": round(cscore, 4),
                           "n_matched_jobs": len(jobs),
                           "has_leadership_gap": has_gap,
                           "has_domain_pain": has_pain,
                           "best_job_title": best["title"],
                           "best_job_url": best["url"],
                           "company_does": best["company_does"],
                           "industry": best["industry"],
                           "company_stage": best["company_stage"]})
        ranked.sort(key=lambda r: -r["fit_score"])
        ranked = ranked[:SHORTLIST]
        keep_companies = {(r["ats"], r["company"]) for r in ranked}

        with open(jobs_out, "a") as f:
            for (ats, company), jobs in companies.items():
                if (ats, company) in keep_companies:
                    for j in jobs[:5]:
                        f.write(json.dumps(j, ensure_ascii=False) + "\n")

        csv_out = checkpoint_path("match", f"{slug}_companies.csv")
        with open(csv_out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(ranked[0].keys()) if ranked else
                               ["ats", "company"])
            w.writeheader()
            w.writerows(ranked)
        say(f"{slug}: shortlisted {len(ranked)} companies "
            f"(from {len(companies):,} matched, size-capped at {max_jobs} open jobs)")


if __name__ == "__main__":
    main()
