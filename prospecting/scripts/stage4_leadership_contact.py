#!/usr/bin/env python3
"""
Stage 4/6 DRY-RUN — Blitz leadership-gap detector + decision-maker contact.
Reads top candidates from stage1_top_candidates.csv, for each:
  1) waterfall-icp-keyword on CTO/VP-Eng titles (exclude fractional/interim) -> full-time CTO?
  2) waterfall-icp-keyword on Founder/CEO/CPO -> decision-maker contact
  3) enrichment/email on the decision-maker
Prints a table. All Blitz calls are free (unlimited plan, 50 QPS).
"""
import csv, os, sys, json, time, urllib.request, urllib.error

BASE = "https://api.blitz-api.ai"
KEY = None
for line in open(os.path.join(os.path.dirname(__file__), "..", "..", ".env"), encoding="utf-8"):
    if line.startswith("BLITZ_API_KEY="):
        KEY = line.strip().split("=", 1)[1]
assert KEY, "BLITZ_API_KEY not found in .env"

def post(path, body):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(),
        headers={"x-api-key": KEY, "content-type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_body": e.read().decode()[:200]}
    except Exception as e:
        return {"_error": str(e)}

def waterfall(company_url, titles, excl, n=3):
    return post("/v2/search/waterfall-icp-keyword", {
        "company_linkedin_url": company_url,
        "cascade": [{"include_title": titles, "exclude_title": excl,
                     "location": ["WORLD"], "include_headline_search": True}],
        "max_results": n})

CTO_TITLES = ["Chief Technology Officer","CTO","VP Engineering","VP of Engineering",
              "Head of Engineering","Chief Technical Officer","Director of Engineering"]
CTO_EXCL = ["fractional","interim","advisor","assistant","intern","junior","former"]
DM_TITLES = ["Founder","Co-Founder","CEO","Chief Executive Officer","President",
             "Chief Product Officer","Chief Operating Officer"]

def main(limit=12):
    rows = list(csv.DictReader(open("prospecting/data/stage1_top_candidates.csv", encoding="utf-8")))[:limit]
    print(f"{'company':26} {'fundr':12} {'FT-CTO?':8} {'cto/vp name':22} {'decision-maker':22} {'title':20} email")
    print("-"*150)
    out = []
    for r in rows:
        url = (r.get("LinkedIn Company URL") or "").strip()
        dom = (r.get("Domain") or "").strip()
        if not url and dom:
            res = post("/v2/enrichment/domain-to-linkedin", {"domain": dom})
            url = res.get("company_linkedin_url", "") if isinstance(res, dict) else ""
        cto_name = dm_name = dm_title = email = ""
        has_cto = "?"
        if url:
            c = waterfall(url, CTO_TITLES, CTO_EXCL, 3)
            if "_error" not in c:
                cur = [x for x in c.get("results", [])
                       if any(e.get("job_is_current") for e in x.get("person", {}).get("experiences", []))]
                has_cto = "YES" if cur else "no"
                if cur:
                    cto_name = cur[0].get("person", {}).get("full_name", "")[:21]
            d = waterfall(url, DM_TITLES, ["assistant","intern"], 1)
            if "_error" not in d and d.get("results"):
                p = d["results"][0].get("person", {})
                dm_name = p.get("full_name", "")[:21]
                exps = p.get("experiences", [])
                dm_title = (exps[0].get("job_title","") if exps else p.get("headline",""))[:19]
                pl = p.get("linkedin_url", "")
                if pl:
                    em = post("/v2/enrichment/email", {"person_linkedin_url": pl})
                    if isinstance(em, dict):
                        email = em.get("email") or (em.get("all_emails") or [""])[0] or ""
        print(f"{r['Company Name'][:25]:26} {r['Total Funding Range'][:11]:12} {has_cto:8} "
              f"{cto_name:22} {dm_name:22} {dm_title:20} {email}")
        out.append({**r, "has_full_time_cto": has_cto, "cto_vp_name": cto_name,
                    "decision_maker": dm_name, "dm_title": dm_title, "dm_email": email})
    csv.DictWriter(open("prospecting/data/stage4_dryrun.csv","w",newline="",encoding="utf-8"),
                   fieldnames=list(out[0].keys())).writerows([]) if not out else None
    if out:
        w = csv.DictWriter(open("prospecting/data/stage4_dryrun.csv","w",newline="",encoding="utf-8"),
                           fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    print(f"\nwrote prospecting/data/stage4_dryrun.csv ({len(out)} rows)")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 12)
