#!/usr/bin/env python3
"""
C2 — For each target account, resolve the company on LinkedIn and pull the RIGHT people
via Blitz waterfall-ICP, using Cameron/BrassHelm's buyer cascade:
  - decision-maker  : CEO / President / Founder / COO  (economic buyer)
  - tech/ops owner  : CTO/CIO/VP-Tech  then  VP Ops / Member Experience / Patient Access /
                      Contact Center / Growth  (the "nobody owns the technical side" seat)
Blitz is flat-rate/free (50 QPS). Also grabs Blitz email (free) as a baseline.

In : output/accounts.csv
Out: output/people.jsonl (resumable) + output/people.csv
"""
import csv, os, sys, json, time, urllib.request, urllib.error, threading
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = os.path.join(os.path.dirname(__file__), "..")
ACCOUNTS = os.path.join(BASE, "output", "accounts.csv")
JL = os.path.join(BASE, "output", "people.jsonl")
OUT = os.path.join(BASE, "output", "people.csv")
BLITZ = "https://api.blitz-api.ai"

def load_key(name):
    for p in ["/Users/jordan/Desktop/Blueprint-GTM-Skills/.env",
              os.path.join(BASE, "..", ".env")]:
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                if line.startswith(name + "="):
                    v = line.split("=",1)[1].strip().strip("\"' ")
                    if v: return v
    sys.exit(f"missing {name}")
KEY = load_key("BLITZ_API_KEY")

def post(path, body):
    req = urllib.request.Request(BLITZ + path, data=json.dumps(body).encode(),
        headers={"x-api-key": KEY, "content-type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_body": e.read().decode()[:160]}
    except Exception as e:
        return {"_error": str(e)}

DM_TIER = ["Chief Executive Officer","CEO","President","Founder","Co-Founder","Owner",
           "Chief Operating Officer","COO","Executive Director"]
TECH_TIER = ["Chief Technology Officer","CTO","Chief Information Officer","CIO",
             "Chief Digital Officer","Chief Digital and Information Officer","VP Engineering",
             "VP of Engineering","VP Technology","VP of Technology","VP Information Technology",
             "Head of Technology","Head of Engineering","Director of IT","Director of Technology"]
OPS_TIER = ["VP Operations","VP of Operations","Director of Operations","Chief Member Experience Officer",
            "VP Member Experience","Director of Member Services","VP Patient Access","Director of Patient Access",
            "Director of Contact Center","Director of Call Center","VP Customer Experience",
            "VP Customer Service","Chief Growth Officer","VP Marketing","Director of Patient Experience"]
# SMB / clinic operational owners — the real voice/phone buyer at small practices & home-services shops
SMB_TIER = ["Practice Manager","Office Manager","Practice Administrator","Administrator",
            "Operations Manager","General Manager","Front Office Manager","Practice Owner",
            "Managing Partner","Managing Director","Director of First Impressions","Owner Operator"]
EXCL = ["fractional","interim","advisor","assistant","intern","junior","former","consultant","retired"]

def waterfall(url, cascade_tiers, n):
    return post("/v2/search/waterfall-icp-keyword", {
        "company_linkedin_url": url,
        "cascade": [{"include_title": t, "exclude_title": EXCL,
                     "location": ["WORLD"], "include_headline_search": True} for t in cascade_tiers],
        "max_results": n})

def resolve_company(acc):
    """Return (company_linkedin_url, domain)."""
    dom = (acc.get("domain") or "").strip()
    if dom:
        r = post("/v2/enrichment/domain-to-linkedin", {"domain": dom})
        if isinstance(r, dict) and r.get("company_linkedin_url"):
            return r["company_linkedin_url"], dom
    # search by name (MA plans / collections)
    name = acc["company_name"]
    r = post("/v2/search/companies", {
        "company": {"name": {"include": [name]}, "hq": {"country_code": ["US"]}},
        "max_results": 5})
    res = (r or {}).get("results") or []
    if res:
        best = res[0]
        return best.get("linkedin_url",""), (best.get("domain","") or dom)
    return "", dom

def person_row(acc, p, bucket, icp_tier):
    exps = p.get("experiences", []) or []
    cur = next((e for e in exps if e.get("job_is_current")), exps[0] if exps else {})
    title = cur.get("job_title") or p.get("headline","")
    li = p.get("linkedin_url","")
    email = ""
    if li:
        em = post("/v2/enrichment/email", {"person_linkedin_url": li})
        if isinstance(em, dict):
            email = em.get("email") or (em.get("all_emails") or [""])[0] or ""
    return {
        "account_id": acc["account_id"], "vertical": acc["vertical"],
        "company_name": acc["company_name"], "domain": acc.get("domain",""),
        "company_evidence": acc["evidence"], "company_score": acc["score"],
        "role_bucket": bucket, "matched_tier": icp_tier,
        "full_name": p.get("full_name",""),
        "first_name": p.get("first_name","") or (p.get("full_name","").split() or [""])[0],
        "last_name": p.get("last_name","") or " ".join(p.get("full_name","").split()[1:]),
        "title": title, "headline": p.get("headline",""),
        "location": p.get("location",""), "linkedin_url": li,
        "blitz_email": email,
    }

def process_account(acc):
    url, dom = resolve_company(acc)
    people = []
    if url:
        seen = set()
        a = waterfall(url, [DM_TIER], 2)
        for x in (a.get("results") or []):
            p = x.get("person", {})
            if p.get("linkedin_url") in seen: continue
            seen.add(p.get("linkedin_url"))
            people.append(person_row(acc, p, "decision_maker", x.get("icp","")))
        b = waterfall(url, [TECH_TIER, OPS_TIER, SMB_TIER], 3)
        for x in (b.get("results") or []):
            p = x.get("person", {})
            if p.get("linkedin_url") in seen: continue
            seen.add(p.get("linkedin_url"))
            people.append(person_row(acc, p, "tech_ops", x.get("icp","")))
    return {"_account_id": acc["account_id"], "company_linkedin_url": url,
            "resolved_domain": dom, "people": people}

def main(limit=None, workers=12):
    accs = list(csv.DictReader(open(ACCOUNTS, encoding="utf-8")))
    if limit: accs = accs[:limit]
    done = set()
    if os.path.exists(JL):
        for ln in open(JL, encoding="utf-8"):
            try: done.add(json.loads(ln)["_account_id"])
            except Exception: pass
    todo = [a for a in accs if a["account_id"] not in done]
    print(f"accounts: {len(accs)}  already done: {len(done)}  to process: {len(todo)}")
    fh = open(JL, "a", encoding="utf-8"); lock = threading.Lock(); n = [0]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(process_account, acc): acc for acc in todo}
        for fut in as_completed(futs):
            rec = fut.result()
            with lock:
                fh.write(json.dumps(rec) + "\n"); fh.flush()
                n[0] += 1
                if n[0] % 25 == 0:
                    print(f"  ...{n[0]}/{len(todo)} processed", flush=True)
    fh.close()

    # flatten -> CSV
    rows = []
    for ln in open(JL, encoding="utf-8"):
        rec = json.loads(ln)
        for p in rec.get("people", []):
            p["company_linkedin_url"] = rec.get("company_linkedin_url","")
            p["resolved_domain"] = rec.get("resolved_domain","")
            rows.append(p)
    if rows:
        cols = list(rows[0].keys())
        with open(OUT, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    n_li = sum(1 for ln in open(JL) if json.loads(ln).get("company_linkedin_url"))
    print(f"\naccounts processed: {sum(1 for _ in open(JL))}  resolved-on-LinkedIn: {n_li}")
    print(f"people found: {len(rows)}  with blitz email: {sum(1 for r in rows if r['blitz_email'])}")
    print(f"-> {OUT}")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
