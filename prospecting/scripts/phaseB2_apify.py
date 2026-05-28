#!/usr/bin/env python3
"""
Phase B2 — Apify LinkedIn-jobs pass for companies with NO detectable ATS.
Submits ONE async run (curious_coder/linkedin-jobs-scraper) over per-company
keyword search URLs, polls, matches jobs back to companies by normalized name,
and scores integration/silo job pain. Writes prospecting/checkpoints/phaseB_apify.jsonl.

Enterprise Apify plan; token from .env (never printed).
"""
import csv, os, json, re, time, urllib.request, urllib.parse, urllib.error

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def p(*a): return os.path.join(ROOT, *a)
TOK = None
for line in open(p("..", ".env"), encoding="utf-8"):
    if line.startswith("APIFY_TOKEN="):
        TOK = line.strip().split("=", 1)[1]
assert TOK, "APIFY_TOKEN missing"
ACTOR = "curious_coder~linkedin-jobs-scraper"
OUT = p("checkpoints", "phaseB_apify.jsonl")

INTEG = re.compile(r'(?<![a-z0-9])(integration|integrations|api|webhook|epic|athenahealth|workday|salesforce|netsuite|hl7|fhir|edi|interoperability|middleware|etl|data pipeline|integration engineer|solutions engineer|implementation|data engineer|platform engineer)(?![a-z0-9])')
SILO = re.compile(r'(?<![a-z0-9])(data entry|operations analyst|revops|sales operations|reconciliation|billing coordinator|data coordinator|order entry|manual data|spreadsheet|reporting analyst|data integrity)(?![a-z0-9])')
norm = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower())

def api(method, path, body=None):
    url = f"https://api.apify.com/v2/{path}{'&' if '?' in path else '?'}token={TOK}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def main(limit=None):
    cand = list(csv.DictReader(open(p("data", "stage1_top_candidates.csv"), encoding="utf-8")))
    ats = {}
    for ln in open(p("checkpoints", "phaseB.jsonl"), encoding="utf-8"):
        try:
            r = json.loads(ln); ats[r.get("domain")] = r.get("status")
        except Exception: pass
    # companies with no clean ATS job data
    need = [c for c in cand if ats.get((c.get("Domain") or "").strip()) != "ok"]
    if limit: need = need[:limit]
    by_norm = {norm(c["Company Name"]): (c.get("Domain") or "").strip() for c in need}
    urls = ["https://www.linkedin.com/jobs/search/?keywords=" +
            urllib.parse.quote(c["Company Name"]) + "&location=United%20States&f_TPR=r7776000"
            for c in need if c.get("Company Name")]
    print(f"no-ATS companies needing Apify: {len(need)} ; urls: {len(urls)}")
    run = api("POST", f"acts/{ACTOR}/runs", {"urls": urls, "count": 6, "scrapeCompany": False})
    rid = run["data"]["id"]; dsid = run["data"]["defaultDatasetId"]
    print(f"run {rid} started; polling…")
    for _ in range(120):  # up to ~20 min
        time.sleep(10)
        st = api("GET", f"actor-runs/{rid}")["data"]["status"]
        if st in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            print("run status:", st); break
    # fetch dataset
    items, off = [], 0
    while True:
        batch = api("GET", f"datasets/{dsid}/items?clean=true&offset={off}&limit=1000")
        if not batch: break
        items += batch; off += len(batch)
        if len(batch) < 1000: break
    print(f"jobs scraped: {len(items)}")
    # match jobs -> company, tally
    agg = {}
    for j in items:
        co = norm(j.get("companyName") or j.get("company") or "")
        dom = None
        if co in by_norm: dom = by_norm[co]
        else:
            for n, d in by_norm.items():
                if co and (co in n or n in co) and len(co) > 4:
                    dom = d; break
        if not dom: continue
        blob = ((j.get("title") or "") + " " + (j.get("description") or "")).lower()
        a = agg.setdefault(dom, {"domain": dom, "apify_jobs": 0, "integration_jobs": 0,
                                 "silo_jobs": 0, "integration_titles": []})
        a["apify_jobs"] += 1
        if INTEG.search(blob):
            a["integration_jobs"] += 1; a["integration_titles"].append((j.get("title") or "")[:50])
        if SILO.search(blob):
            a["silo_jobs"] += 1
    with open(OUT, "w", encoding="utf-8") as f:
        for d, a in agg.items():
            a["jobs_pain_score"] = min(5, a["integration_jobs"] + 2 * a["silo_jobs"])
            a["integration_titles"] = " | ".join(dict.fromkeys(a["integration_titles"]))[:200]
            f.write(json.dumps(a) + "\n")
    print(f"matched companies with apify jobs: {len(agg)} -> {OUT}")

if __name__ == "__main__":
    import sys
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
