#!/usr/bin/env python3
"""Stage 3: pull ops-gap + hiring pain signals per verified studio (Blitz).

Per company in data/universe_verified.csv:
  1. employee-finder (Engineering + IT, all levels, paginated to 150) ->
     classify titles locally: senior eng leadership vs dedicated-ops roles.
  2. company-distribution-by-department -> engineering headcount share.
  3. jobs/company -> open postings; flag DevOps/build/release/IT/security reqs
     (acknowledged gap) and count engineering reqs.

Output: checkpoints/pain_signals.jsonl (resume-safe by linkedin_url)

Usage: python3 s5_pain_signals.py
"""
import csv
import re
import sys
import concurrent.futures as cf
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (ROOT, load_env, post_json, blitz_headers,  # noqa: E402
                    append_jsonl, read_jsonl)

IN = ROOT / "data" / "universe_verified.csv"
OUT = ROOT / "checkpoints" / "pain_signals.jsonl"
BASE = "https://api.blitz-api.ai/v2"

OPS_RE = re.compile(
    r"devops|dev ops|site reliab|sre\b|build engineer|release engineer"
    r"|infrastructure engineer|platform engineer|it manager|it director"
    r"|it support|it admin|system admin|sysadmin|security engineer|infosec"
    r"|information security|tools engineer|pipeline engineer|dev *tools", re.I)
SENIOR_ENG_RE = re.compile(
    r"tech(nical)? director|director of engineering|engineering director"
    r"|vp( of)? engineering|head of engineering|principal (software |game )?engineer"
    r"|staff (software |game )?engineer|lead (software |game |gameplay |graphics "
    r"|engine |network |backend |server )?engineer|senior (software |game |gameplay "
    r"|graphics |engine |network |backend |server )?engineer|cto"
    r"|chief technology", re.I)
ENG_RE = re.compile(r"engineer|programmer|developer|cto|technical director", re.I)
JOB_OPS_TITLES = ["DevOps", "Build Engineer", "Release Engineer", "Site Reliability",
                  "Infrastructure", "Platform Engineer", "IT Manager", "IT Support",
                  "Security Engineer", "Tools Engineer"]


def pull_employees(li_url):
    people, page = [], 1
    while page <= 4:
        r = post_json(f"{BASE}/search/employee-finder",
                      {"company_linkedin_url": li_url,
                       "job_function": ["Engineering", "Information Technology"],
                       "max_results": 50, "page": page},
                      blitz_headers(), timeout=120)
        res = r.get("results") or []
        for p in res:
            person = p.get("person") or p
            exps = person.get("experiences") or []
            slug = li_url.rstrip("/").split("/")[-1]
            cur = next((e for e in exps if e.get("job_is_current")
                        and slug in (e.get("company_linkedin_url") or "")), None) \
                or next((e for e in exps if e.get("job_is_current")), {})
            people.append({
                "name": person.get("full_name"),
                "headline": person.get("headline") or "",
                "title": cur.get("job_title") or "",
                "linkedin_url": person.get("linkedin_url"),
                "start": cur.get("job_start_date")})
        if len(res) < 50:
            break
        page += 1
    return people


def pull_jobs(li_url):
    r = post_json(f"{BASE}/jobs/company",
                  {"company_linkedin_url": li_url, "job": {}},
                  blitz_headers(), timeout=120)
    jobs = r.get("results") or r.get("jobs") or []
    out = []
    for j in jobs:
        out.append({"title": j.get("title") or j.get("job_title") or "",
                    "posted": j.get("posted_at") or j.get("date_posted") or "",
                    "location": j.get("location") or ""})
    return out


def signals_one(row):
    li = row["linkedin_url"]
    rec = {"name": row["name"], "domain": row["domain"], "linkedin_url": li}
    try:
        people = pull_employees(li)
        eng_people = [p for p in people
                      if ENG_RE.search(p["title"] + " " + p["headline"])]
        senior = [p for p in eng_people
                  if SENIOR_ENG_RE.search(p["title"] + " " + p["headline"])]
        ops = [p for p in people
               if OPS_RE.search(p["title"] + " " + p["headline"])]
        rec.update({
            "eng_people_found": len(eng_people),
            "senior_eng_count": len(senior),
            "senior_eng_titles": "; ".join(p["title"] or p["headline"]
                                           for p in senior)[:400],
            "ops_people_count": len(ops),
            "ops_titles": "; ".join(p["title"] or p["headline"] for p in ops)[:300],
        })
    except Exception as e:
        rec["people_err"] = str(e)[:120]
    try:
        dist = post_json(f"{BASE}/enrichment/company-distribution-by-department",
                         {"company_linkedin_url": li}, blitz_headers(), timeout=90)
        rec["dept_distribution"] = dist.get("distribution") or dist.get("departments") \
            or dist.get("result") or {}
    except Exception as e:
        rec["dept_err"] = str(e)[:120]
    try:
        jobs = pull_jobs(li)
        ops_jobs = [j for j in jobs if OPS_RE.search(j["title"])]
        eng_jobs = [j for j in jobs if ENG_RE.search(j["title"])]
        rec.update({
            "open_jobs": len(jobs),
            "eng_jobs": len(eng_jobs),
            "ops_jobs": len(ops_jobs),
            "ops_job_titles": "; ".join(j["title"] for j in ops_jobs)[:300],
            "eng_job_titles": "; ".join(j["title"] for j in eng_jobs[:12])[:400],
        })
    except Exception as e:
        rec["jobs_err"] = str(e)[:120]
    return rec


def main():
    load_env()
    done = {r["linkedin_url"] for r in read_jsonl(OUT)}
    rows = [r for r in csv.DictReader(open(IN, encoding="utf-8"))
            if r.get("linkedin_url") and r["linkedin_url"] not in done]
    print(f"to pull: {len(rows)} (done {len(done)})")
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        n = 0
        for rec in ex.map(signals_one, rows):
            append_jsonl(OUT, rec)
            n += 1
            if n % 10 == 0:
                print(f"  {n}/{len(rows)}")
    print("done")


if __name__ == "__main__":
    main()
