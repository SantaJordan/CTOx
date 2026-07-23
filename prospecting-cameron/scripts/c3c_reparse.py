#!/usr/bin/env python3
"""C3c — Re-fetch all FullEnrich jobs and parse with the CORRECT key path
(contact.profile.linkedin_url). Rewrites people_enriched.jsonl keyed by normalized
LinkedIn handle. Also captures any newly-finished batches."""
import os, re, sys, json, time, urllib.request
BASE = os.path.join(os.path.dirname(__file__), "..")
LOG = os.path.join(BASE, "output", "c3_full.log")
JL  = os.path.join(BASE, "output", "people_enriched.jsonl")
API = "https://app.fullenrich.com/api/v1"
def key():
    for p in ["/Users/jordan/Desktop/Blueprint-GTM-Skills/.env"]:
        for l in open(p):
            if l.startswith("FULLENRICH_API_KEY="): return l.split("=",1)[1].strip().strip("\"' ")
KEY=key()
def get(eid):
    r=urllib.request.Request(f"{API}/contact/enrich/bulk/{eid}", headers={"Authorization":f"Bearer {KEY}"})
    try:
        with urllib.request.urlopen(r,timeout=45) as resp: return json.load(resp)
    except Exception as e: return {"_err":str(e)}
def norm(li):
    li=(li or "").lower().split("?")[0].rstrip("/")
    return li.split("/in/")[-1] if "/in/" in li else li
def em(e): return e.get("email") if isinstance(e,dict) else e
def ph(p): return (p.get("number") or p.get("phone")) if isinstance(p,dict) else p
def pht(p): return (p.get("type") or p.get("phone_type") or "") if isinstance(p,dict) else ""

eids=re.findall(r"id=([0-9a-f-]{36})", open(LOG).read())
recs={}; pending=[]
for eid in eids:
    d=get(eid); st=(d.get("status") or "").upper()
    if st not in ("FINISHED","COMPLETED","DONE"):
        pending.append((eid,st)); continue
    for r in d.get("datas",d.get("results",[])):
        c=r.get("contact",r) or {}
        prof=c.get("profile") or {}
        handle=norm(prof.get("linkedin_url") or c.get("linkedin_url") or "")
        emails=c.get("emails") or []; phones=c.get("phones") or []
        rec={"linkedin_url":handle,
             "fe_email":em(emails[0]) if emails else "",
             "fe_all_emails":"; ".join(filter(None,(em(e) for e in emails))),
             "fe_phone":ph(phones[0]) if phones else "",
             "fe_all_phones":"; ".join(filter(None,(f"{ph(p)}({pht(p)})" for p in phones)))}
        if handle: recs[handle]=rec
with open(JL,"w") as f:
    for r in recs.values(): f.write(json.dumps(r)+"\n")
print(f"re-parsed jobs: {len(eids)-len(pending)} finished, {len(pending)} pending {pending}")
print(f"enriched (keyed by handle): {len(recs)}  emails: {sum(1 for r in recs.values() if r['fe_email'])}  phones: {sum(1 for r in recs.values() if r['fe_phone'])}")
