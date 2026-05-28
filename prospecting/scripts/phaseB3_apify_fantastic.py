#!/usr/bin/env python3
"""
Phase B3 — Apify job-posting pain via fantastic-jobs/advanced-linkedin-job-search-api,
scoped per company by LinkedIn slug (organizationSlugFilter). Reliable; returns full
description_text + AI skill fields. Writes prospecting/checkpoints/phaseB_apify.jsonl
(the file phaseD already merges, taking max(ATS, apify) job signal).
Usage: python3 phaseB3_apify_fantastic.py [LIMIT]
"""
import csv, os, sys, json, re, threading, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def p(*a): return os.path.join(ROOT, *a)
TOK = None
for line in open(p("..", ".env"), encoding="utf-8"):
    if line.startswith("APIFY_TOKEN="):
        TOK = line.strip().split("=", 1)[1]
assert TOK, "APIFY_TOKEN missing"
ACTOR = "fantastic-jobs~advanced-linkedin-job-search-api"
URL = f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items?token={TOK}"
OUT = p("checkpoints", "phaseB_apify.jsonl")

INTEG = re.compile(r'(?<![a-z0-9])(integration|integrations|api|webhook|epic|athenahealth|workday|salesforce|netsuite|hl7|fhir|edi|interoperability|middleware|etl|data pipeline|integration engineer|solutions engineer|implementation|data engineer|platform engineer|sql)(?![a-z0-9])')
SILO = re.compile(r'(?<![a-z0-9])(data entry|operations analyst|revops|sales operations|reconciliation|billing coordinator|data coordinator|order entry|manual data|spreadsheet|reporting analyst|data integrity)(?![a-z0-9])')
_lock = threading.Lock()

def slug_of(url):
    m = re.search(r'linkedin\.com/company/([^/?#]+)', url or '', re.I)
    return m.group(1).lower() if m else ""

def run(slug):
    body = json.dumps({"organizationSlugFilter": [slug], "limit": 10,
                       "descriptionType": "text", "timeRange": "6m"}).encode()
    req = urllib.request.Request(URL, data=body, method="POST",
        headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"_error": e.code}
    except Exception:
        return {"_error": "timeout"}

def score(dom, slug):
    rec = {"domain": dom, "slug": slug, "apify_jobs": 0, "integration_jobs": 0,
           "silo_jobs": 0, "integration_titles": "", "jobs_pain_score": 0}
    items = run(slug)
    if isinstance(items, dict):
        rec["status"] = f"err:{items.get('_error')}"; return rec
    rec["apify_jobs"] = len(items)
    itit = []
    for j in items:
        blob = " ".join(str(j.get(k, "")) for k in
                        ("title", "description_text", "ai_key_skills",
                         "ai_core_responsibilities", "ai_requirements_summary")).lower()
        if INTEG.search(blob): itit.append((j.get("title") or "")[:50])
        if SILO.search(blob): rec["silo_jobs"] += 1
    rec["integration_jobs"] = len(itit)
    rec["integration_titles"] = " | ".join(dict.fromkeys(itit))[:250]
    rec["jobs_pain_score"] = min(5, len(itit) + 2 * rec["silo_jobs"])
    rec["status"] = "ok"
    return rec

def main(limit=None):
    rows = list(csv.DictReader(open(p("data", "stage1_top_candidates.csv"), encoding="utf-8")))
    A = {}
    for ln in open(p("checkpoints", "phaseA.jsonl"), encoding="utf-8"):
        try:
            r = json.loads(ln); A[r.get("domain")] = r.get("linkedin_company", "")
        except Exception: pass
    work = []
    for r in rows:
        dom = (r.get("Domain") or "").strip()
        url = (r.get("LinkedIn Company URL") or "").strip() or A.get(dom, "")
        s = slug_of(url)
        if s: work.append((dom, s))
    if limit: work = work[:limit]
    done = set()
    if os.path.exists(OUT):
        for ln in open(OUT, encoding="utf-8"):
            try: done.add(json.loads(ln).get("domain"))
            except Exception: pass
    work = [(d, s) for d, s in work if d not in done]
    print(f"companies with LinkedIn slug to scrape: {len(work)}")
    n = 0
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(score, d, s) for d, s in work]
        for f in as_completed(futs):
            rec = f.result()
            with _lock:
                open(OUT, "a", encoding="utf-8").write(json.dumps(rec) + "\n")
            n += 1
            if n % 25 == 0: print(f"  {n}/{len(work)}", flush=True)
    recs = [json.loads(l) for l in open(OUT, encoding="utf-8")]
    ok = sum(1 for r in recs if r.get("status") == "ok")
    pain = sum(1 for r in recs if r.get("jobs_pain_score", 0) > 0)
    print(f"done: {ok} scraped ok, {pain} with job pain signal -> {OUT}")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
