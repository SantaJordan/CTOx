#!/usr/bin/env python3
"""Merge Blitz people.csv + FullEnrich people_enriched.jsonl -> prospects.csv (no API).
Run anytime to refresh the merged output as enrichment completes."""
import csv, os, json
BASE = os.path.join(os.path.dirname(__file__), "..")
PEOPLE = os.path.join(BASE, "output", "people.csv")
JL  = os.path.join(BASE, "output", "people_enriched.jsonl")
OUT = os.path.join(BASE, "output", "prospects.csv")
def norm(li):
    li=(li or "").lower().split("?")[0].rstrip("/")
    return li.split("/in/")[-1] if "/in/" in li else li
done={}
if os.path.exists(JL):
    for l in open(JL):
        try: d=json.loads(l); done[norm(d["linkedin_url"])]=d
        except Exception: pass
rows=[]
for r in csv.DictReader(open(PEOPLE, encoding="utf-8")):
    e=done.get(norm(r.get("linkedin_url","")),{})
    rows.append({**r,
        "best_email": e.get("fe_email") or r.get("blitz_email",""),
        "mobile_phone": e.get("fe_phone",""),
        "all_phones": e.get("fe_all_phones",""),
        "all_emails": e.get("fe_all_emails","") or r.get("blitz_email","")})
cols=["account_id","vertical","company_name","title","role_bucket","full_name",
      "best_email","mobile_phone","all_phones","all_emails","blitz_email","linkedin_url",
      "location","company_score","company_evidence","company_linkedin_url","resolved_domain",
      "matched_tier","headline"]
with open(OUT,"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore"); w.writeheader(); w.writerows(rows)
em=sum(1 for x in rows if x["best_email"]); mob=sum(1 for x in rows if x["mobile_phone"])
print(f"prospects: {len(rows)}  email: {em}  mobile: {mob}  enriched-cached: {len(done)} -> {OUT}")
