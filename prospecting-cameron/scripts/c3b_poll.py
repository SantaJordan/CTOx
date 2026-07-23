#!/usr/bin/env python3
"""C3b — Resilient re-poller. Reads FullEnrich job ids from output/c3_full.log,
polls each until FINISHED, appends results to output/people_enriched.jsonl
(idempotent, keyed by linkedin_url). Long timeout (~90 min). Safe to re-run."""
import os, re, sys, json, time, urllib.request, urllib.error
BASE = os.path.join(os.path.dirname(__file__), "..")
LOG = os.path.join(BASE, "output", "c3_full.log")
JL  = os.path.join(BASE, "output", "people_enriched.jsonl")
API = "https://app.fullenrich.com/api/v1"
def key():
    for p in ["/Users/jordan/Desktop/Blueprint-GTM-Skills/.env", os.path.join(BASE,"..",".env")]:
        if os.path.exists(p):
            for l in open(p):
                if l.startswith("FULLENRICH_API_KEY="): return l.split("=",1)[1].strip().strip("\"' ")
    sys.exit("no key")
KEY = key()
def get(eid):
    r = urllib.request.Request(f"{API}/contact/enrich/bulk/{eid}",
        headers={"Authorization": f"Bearer {KEY}"})
    try:
        with urllib.request.urlopen(r, timeout=40) as resp: return json.load(resp)
    except Exception as e: return {"_err": str(e)}
eids = re.findall(r"id=([0-9a-f-]{36})", open(LOG).read())
print("job ids:", len(eids))
done_li = set()
if os.path.exists(JL):
    for l in open(JL):
        try: done_li.add(json.loads(l)["linkedin_url"])
        except Exception: pass
def em(e): return e.get("email") if isinstance(e,dict) else e
def ph(p): return (p.get("number") or p.get("phone")) if isinstance(p,dict) else p
def pht(p): return (p.get("type") or p.get("phone_type") or "") if isinstance(p,dict) else ""
pending=set(eids); fh=open(JL,"a")
for cyc in range(270):                       # 270 * 20s = 90 min
    if not pending: break
    time.sleep(20)
    for eid in list(pending):
        d=get(eid); st=(d.get("status") or "").upper()
        if st not in ("FINISHED","COMPLETED","DONE"): continue
        cnt=0
        for r in d.get("datas", d.get("results", [])):
            c=r.get("contact",r) or {}
            emails=c.get("emails") or []; phones=c.get("phones") or []
            inp=r.get("input",{}) or {}
            li=r.get("linkedin_url") or inp.get("linkedin_url") or ""
            rec={"linkedin_url":li,
                 "fe_email":em(emails[0]) if emails else "",
                 "fe_all_emails":"; ".join(filter(None,(em(e) for e in emails))),
                 "fe_phone":ph(phones[0]) if phones else "",
                 "fe_all_phones":"; ".join(filter(None,(f"{ph(p)}({pht(p)})" for p in phones)))}
            fh.write(json.dumps(rec)+"\n"); cnt+=1
        fh.flush(); pending.discard(eid)
        print(f"[cyc{cyc}] {eid[:8]} FINISHED ({cnt}); pending {len(pending)}", flush=True)
fh.close()
tot=sum(1 for _ in open(JL))
print(f"poll complete. enriched rows in jsonl: {tot}  pending left: {len(pending)}")
