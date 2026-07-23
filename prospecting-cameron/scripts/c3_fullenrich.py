#!/usr/bin/env python3
"""
C3 — FullEnrich waterfall for email + MOBILE/CELL phone on every person from Blitz.
In : output/people.csv
Out: output/people_enriched.jsonl (resumable, keyed by linkedin_url) + merged output/prospects.csv
"""
import csv, os, sys, json, time, urllib.request, urllib.error

BASE = os.path.join(os.path.dirname(__file__), "..")
PEOPLE = os.path.join(BASE, "output", "people.csv")
JL  = os.path.join(BASE, "output", "people_enriched.jsonl")
OUT = os.path.join(BASE, "output", "prospects.csv")
API = "https://app.fullenrich.com/api/v1"

def load_key(name):
    for p in ["/Users/jordan/Desktop/Blueprint-GTM-Skills/.env", os.path.join(BASE,"..",".env")]:
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                if line.startswith(name+"="):
                    v=line.split("=",1)[1].strip().strip("\"' ")
                    if v: return v
    sys.exit(f"missing {name}")
KEY = load_key("FULLENRICH_API_KEY")

def req(method, path, body=None):
    r = urllib.request.Request(API+path, data=json.dumps(body).encode() if body else None,
        method=method, headers={"Authorization": f"Bearer {KEY}", "content-type":"application/json"})
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_body": e.read().decode()[:200]}

def main(limit=None):
    people = list(csv.DictReader(open(PEOPLE, encoding="utf-8")))
    # dedupe by linkedin_url (a person can't repeat); keep those with a linkedin_url
    seen, targets = set(), []
    for r in people:
        li = r.get("linkedin_url","").strip()
        if not li or li in seen: continue
        seen.add(li)
        targets.append(r)
    done = {}
    if os.path.exists(JL):
        for ln in open(JL, encoding="utf-8"):
            try: d=json.loads(ln); done[d["linkedin_url"]]=d
            except Exception: pass
    todo = [t for t in targets if t["linkedin_url"] not in done]
    if limit: todo = todo[:limit]
    print(f"people: {len(targets)}  already enriched: {len(done)}  to enrich now: {len(todo)}")

    def em(e): return e.get("email") if isinstance(e,dict) else e
    def ph(p): return (p.get("number") or p.get("phone")) if isinstance(p,dict) else p
    def ph_type(p): return (p.get("type") or p.get("phone_type") or "") if isinstance(p,dict) else ""

    fh = open(JL, "a", encoding="utf-8")
    # 1) submit ALL batches up front, map enrichment_id -> the batch's linkedin urls
    jobs = {}  # eid -> set(linkedin_url)
    for i in range(0, len(todo), 100):
        batch = todo[i:i+100]
        datas = [{
            "firstname": t.get("first_name","") or (t.get("full_name","").split() or [""])[0],
            "lastname": t.get("last_name","") or " ".join(t.get("full_name","").split()[1:]),
            "domain": (t.get("resolved_domain") or t.get("domain") or "").strip(),
            "company_name": t.get("company_name",""),
            "linkedin_url": t["linkedin_url"],
            "enrich_fields": ["contact.emails","contact.phones"],
        } for t in batch]
        sub = req("POST", "/contact/enrich/bulk", {"name": f"cameron_{i//100}", "datas": datas})
        eid = sub.get("enrichment_id") or sub.get("id")
        if not eid:
            print("  submit failed:", json.dumps(sub)[:200]); continue
        jobs[eid] = {t["linkedin_url"] for t in batch}
        print(f"  submitted batch {i//100+1} ({len(batch)}) id={eid}", flush=True)
        time.sleep(1)
    # 2) poll all jobs until each is finished (or overall timeout ~30 min)
    pending = dict(jobs)
    for _ in range(120):
        if not pending: break
        time.sleep(15)
        for eid in list(pending.keys()):
            res = req("GET", f"/contact/enrich/bulk/{eid}")
            st = (res.get("status") or "").upper()
            if st not in ("FINISHED","COMPLETED","DONE"): continue
            for r in res.get("datas", res.get("results", [])):
                c = r.get("contact", r) or {}
                emails = c.get("emails") or []; phones = c.get("phones") or []
                inp = r.get("input", {}) or {}
                li = r.get("linkedin_url") or inp.get("linkedin_url") or ""
                rec = {"linkedin_url": li,
                       "fe_email": em(emails[0]) if emails else "",
                       "fe_all_emails": "; ".join(filter(None,(em(e) for e in emails))),
                       "fe_phone": ph(phones[0]) if phones else "",
                       "fe_all_phones": "; ".join(filter(None,(f"{ph(p)}({ph_type(p)})" for p in phones)))}
                fh.write(json.dumps(rec)+"\n"); done[li]=rec
            fh.flush(); del pending[eid]
            print(f"  job {eid} done; cumulative enriched {len(done)}; jobs left {len(pending)}", flush=True)
    fh.close()

    # merge -> prospects.csv (one row per person, best email + best phone)
    rows=[]
    for r in people:
        li=r.get("linkedin_url","").strip()
        e=done.get(li,{})
        best_email = e.get("fe_email") or r.get("blitz_email","")
        rows.append({**r,
            "best_email": best_email,
            "mobile_phone": e.get("fe_phone",""),
            "all_phones": e.get("fe_all_phones",""),
            "all_emails": e.get("fe_all_emails","") or r.get("blitz_email",""),
        })
    cols=["account_id","vertical","company_name","title","role_bucket","full_name",
          "best_email","mobile_phone","all_phones","all_emails","blitz_email",
          "linkedin_url","location","domain","company_score","company_evidence",
          "company_linkedin_url","resolved_domain","matched_tier","headline"]
    with open(OUT,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    we = sum(1 for x in rows if x["best_email"]); wp=sum(1 for x in rows if x["mobile_phone"])
    print(f"\nprospects: {len(rows)}  with email: {we}  with mobile phone: {wp}\n-> {OUT}")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv)>1 else None)
