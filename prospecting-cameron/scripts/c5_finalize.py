#!/usr/bin/env python3
"""C5 — Build the final outreach-ready CSV: clean column order + per-vertical opener.
In: output/prospects.csv  ->  Out: output/prospects_FINAL.csv"""
import csv, os
BASE = os.path.join(os.path.dirname(__file__), "..")
IN  = os.path.join(BASE, "output", "prospects.csv")
OUT = os.path.join(BASE, "output", "prospects_FINAL.csv")

def opener(v):
    return {
"medicare_advantage":"Your CMS Star Ratings show the member-facing phone measures slipping — that's where rebate dollars leak. I rebuilt exactly this for a health plan doing 10-20k calls/day and found 67% of 'successful transfers' were actually voicemails. Worth a look at your real numbers?",
"provider":"Your Google reviews show a booking/phone bottleneck at real patient volume — every missed call is a lost high-value patient. I own voice-AI deployments end-to-end so the phone converts instead of dropping to voicemail.",
"collections":"You run a large outbound dialer operation and it's generating CFPB communication complaints. I build compliant, verified voice-AI calling (right-party contact + voicemail detection) and prove the numbers are real.",
"home_services":"High inbound call volume and every missed call is a lost job. I deploy voice AI that books the call instead of dropping it — bridged into the phone system you already run.",
    }.get(v,"")

import ast
def clean_loc(s):
    s=(s or "").strip()
    if s.startswith("{"):
        try:
            d=ast.literal_eval(s)
            parts=[d.get("city",""), d.get("state_code") or d.get("state","")]
            return ", ".join(p for p in parts if p) or s
        except Exception: return s
    return s

rows = list(csv.DictReader(open(IN, encoding="utf-8")))
out = []
for r in rows:
    r["location"]=clean_loc(r.get("location",""))
    out.append({
        "account_id": r["account_id"], "vertical": r["vertical"],
        "company": r["company_name"], "person": r["full_name"], "title": r["title"],
        "role_bucket": r["role_bucket"], "best_email": r.get("best_email",""),
        "mobile_phone": r.get("mobile_phone",""), "all_phones": r.get("all_phones",""),
        "all_emails": r.get("all_emails",""), "linkedin_url": r["linkedin_url"],
        "location": r["location"], "company_score": r.get("company_score",""),
        "why_target": r.get("company_evidence",""), "suggested_opener": opener(r["vertical"]),
    })
# sort: vertical priority, then has-contact, then score
vpri = {"medicare_advantage":0,"provider":1,"collections":2,"home_services":3}
out.sort(key=lambda x:(vpri.get(x["vertical"],9), 0 if x["best_email"] or x["mobile_phone"] else 1))
cols = list(out[0].keys())
with open(OUT,"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(out)

tot=len(out); em=sum(1 for x in out if x["best_email"]); mob=sum(1 for x in out if x["mobile_phone"])
both=sum(1 for x in out if x["best_email"] and x["mobile_phone"])
from collections import Counter
print(f"FINAL prospects: {tot}")
print(f"  with email      : {em} ({100*em//tot}%)")
print(f"  with mobile     : {mob} ({100*mob//tot}%)")
print(f"  with email+mobile: {both}")
print("  by vertical:", dict(Counter(x['vertical'] for x in out)))
print("  reachable (email or mobile):", sum(1 for x in out if x['best_email'] or x['mobile_phone']))
print("->", OUT)
