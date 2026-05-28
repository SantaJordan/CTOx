#!/usr/bin/env python3
"""
Phase B — job-posting pain signal via FREE ATS APIs (Greenhouse / Lever / Ashby).
Detects, per company, whether they're hiring (a) integration/API roles (reinforces
axis 1/2) and (b) ops/data-entry/RevOps roles (axis 3 silo pain).
Companies with no detectable ATS are logged for an optional Apify pass.

Output: prospecting/data/phaseB_jobs.csv  (+ checkpoints/phaseB.jsonl)
Usage: python3 phaseB_jobs.py [LIMIT]
"""
import csv, os, sys, json, re, html, threading, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IN = os.path.join(ROOT, "data", "stage1_top_candidates.csv")
CKPT = os.path.join(ROOT, "checkpoints", "phaseB.jsonl")
OUT = os.path.join(ROOT, "data", "phaseB_jobs.csv")

INTEG_KW = ["integration", "integrations", "api", "webhook", "epic", "athenahealth", "workday",
            "salesforce", "netsuite", "hl7", "fhir", "edi", "interoperability", "middleware",
            "etl", "data pipeline", "systems integration", "integration engineer",
            "solutions engineer", "implementation engineer", "implementation specialist",
            "sql", "data engineer", "platform engineer"]
SILO_KW = ["data entry", "data entry clerk", "operations analyst", "revops", "sales operations",
           "reconciliation", "billing coordinator", "billing specialist", "data coordinator",
           "order entry", "manual data", "spreadsheet", "reporting analyst", "data integrity",
           "manual process", "re-key", "double entry", "copy and paste"]
_rx = lambda terms: re.compile(r'(?<![a-z0-9])(' + '|'.join(re.escape(t) for t in terms) + r')(?![a-z0-9])')
INTEG_RX, SILO_RX = _rx(INTEG_KW), _rx(SILO_KW)
_lock = threading.Lock()

def get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 prospecting"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        return None

def slugs(domain, name):
    base = (domain or "").lower().split("//")[-1].split("/")[0].replace("www.", "")
    stem = base.split(".")[0] if base else ""
    nm = re.sub(r'[^a-z0-9]+', '', (name or "").lower())
    nmh = re.sub(r'[^a-z0-9]+', '-', (name or "").lower()).strip('-')
    out = []
    for s in [stem, stem.replace("-", ""), nm, nmh]:
        if s and s not in out:
            out.append(s)
    return out[:4]

def greenhouse(slug):
    raw = get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true")
    if not raw: return None
    try:
        d = json.loads(raw)
        if "jobs" not in d: return None
        return [(j.get("title", ""), html.unescape(re.sub("<[^>]+>", " ", j.get("content", "") or ""))) for j in d["jobs"]]
    except Exception:
        return None

def lever(slug):
    raw = get(f"https://api.lever.co/v0/postings/{slug}?mode=json")
    if not raw: return None
    try:
        d = json.loads(raw)
        if not isinstance(d, list): return None
        return [(j.get("text", ""), (j.get("descriptionPlain", "") or "") + " " +
                 " ".join(li.get("text", "") for li in j.get("lists", []))) for j in d]
    except Exception:
        return None

def ashby(slug):
    raw = get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
    if not raw: return None
    try:
        d = json.loads(raw)
        js = d.get("jobs", [])
        if not js: return None
        return [(j.get("title", ""), j.get("departmentName", "") + " " + j.get("locationName", "")) for j in js]
    except Exception:
        return None

ATS_SITE_RX = [
    ("greenhouse", re.compile(r'(?:boards|job-boards)\.greenhouse\.io/(?:embed/job_board\?for=)?([a-z0-9]+)', re.I)),
    ("greenhouse", re.compile(r'greenhouse\.io/embed/job_board\?for=([a-z0-9]+)', re.I)),
    ("lever", re.compile(r'jobs\.lever\.co/([a-z0-9\-]+)', re.I)),
    ("ashby", re.compile(r'(?:jobs\.ashbyhq\.com|ashbyhq\.com/)([a-z0-9\-]+)', re.I)),
]
ATS_FN = {"greenhouse": greenhouse, "lever": lever, "ashby": ashby}

def find_ats_from_site(domain):
    base = (domain or "").strip().split("//")[-1].split("/")[0].replace("www.", "")
    if not base:
        return None
    for path in ("", "/careers", "/jobs", "/company/careers", "/about/careers"):
        page = get(f"https://{base}{path}", timeout=12)
        if not page:
            continue
        for ats, rx in ATS_SITE_RX:
            m = rx.search(page)
            if m:
                tok = m.group(1)
                if tok and tok.lower() not in ("embed", "www"):
                    return ats, tok
        if "myworkdayjobs.com" in page:
            return "workday", ""   # detected but no free API parse
    return None

def probe(row):
    dom = (row.get("Domain") or "").strip()
    rec = {"domain": dom, "company": row.get("Company Name", ""), "ats": "", "jobs_found": 0,
           "integration_jobs": 0, "silo_jobs": 0, "jobs_pain_score": 0,
           "integration_titles": "", "silo_titles": ""}
    jobs = None
    # 1) discover the real ATS token from the company's careers page
    found = find_ats_from_site(dom)
    if found:
        ats, tok = found
        rec["ats"], rec["ats_slug"] = ats, tok
        if ats in ATS_FN and tok:
            jobs = ATS_FN[ats](tok)
        if ats == "workday":
            rec["status"] = "workday_no_api"; return rec
    # 2) fallback: guess slugs
    if jobs is None:
        for slug in slugs(dom, row.get("Company Name", "")):
            for ats, fn in (("greenhouse", greenhouse), ("lever", lever), ("ashby", ashby)):
                j = fn(slug)
                if j:
                    jobs, rec["ats"], rec["ats_slug"] = j, ats, slug
                    break
            if jobs is not None:
                break
    if jobs is None:
        rec["status"] = "no_ats"; return rec
    rec["jobs_found"] = len(jobs)
    itit, stit = [], []
    for title, content in jobs:
        blob = (title + " " + content).lower()
        if INTEG_RX.search(blob): itit.append(title[:60])
        if SILO_RX.search(blob): stit.append(title[:60])
    rec["integration_jobs"] = len(itit); rec["silo_jobs"] = len(stit)
    rec["integration_titles"] = " | ".join(dict.fromkeys(itit))[:300]
    rec["silo_titles"] = " | ".join(dict.fromkeys(stit))[:300]
    rec["jobs_pain_score"] = min(5, len(itit) + 2 * len(stit))
    rec["status"] = "ok"
    return rec

def main(limit=None):
    rows = list(csv.DictReader(open(IN, encoding="utf-8")))
    if limit: rows = rows[:limit]
    done = set()
    if os.path.exists(CKPT):
        for ln in open(CKPT, encoding="utf-8"):
            try: done.add(json.loads(ln).get("domain"))
            except Exception: pass
    todo = [r for r in rows if (r.get("Domain") or "").strip() not in done]
    print(f"total={len(rows)} done={len(done)} todo={len(todo)}")
    n = 0
    with ThreadPoolExecutor(max_workers=24) as ex:
        futs = [ex.submit(probe, r) for r in todo]
        for f in as_completed(futs):
            rec = f.result()
            with _lock:
                open(CKPT, "a", encoding="utf-8").write(json.dumps(rec) + "\n")
            n += 1
            if n % 50 == 0: print(f"  {n}/{len(todo)}", flush=True)
    recs = [json.loads(l) for l in open(CKPT, encoding="utf-8")]
    ats = sum(1 for r in recs if r.get("status") == "ok")
    withpain = sum(1 for r in recs if r.get("jobs_pain_score", 0) > 0)
    print(f"\nATS found: {ats}/{len(recs)} | with job pain signal: {withpain}")
    print(f"(no ATS: {len(recs)-ats} -> candidates for optional Apify pass)")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
