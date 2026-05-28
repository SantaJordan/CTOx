#!/usr/bin/env python3
"""
Phase A2 — FullEnrich forward enrichment to FILL missing email/phone for
CEO/COO that Blitz couldn't fully resolve. Writes prospecting/checkpoints/
phaseA2_fullenrich.jsonl keyed by person linkedin_url. (PII — local only.)
Usage: python3 phaseA2_fullenrich.py [LIMIT] [--dry]
"""
import os, sys, json, time, urllib.request, urllib.error

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def p(*a): return os.path.join(ROOT, *a)
KEY = None
for line in open(p("..", ".env"), encoding="utf-8"):
    if line.startswith("FULLENRICH_API_KEY="):
        KEY = line.strip().split("=", 1)[1]
assert KEY, "FULLENRICH_API_KEY missing"
BASE = "https://app.fullenrich.com/api/v1"
OUT = p("checkpoints", "phaseA2_fullenrich.jsonl")

def req(method, path, body=None):
    r = urllib.request.Request(BASE + path, data=json.dumps(body).encode() if body else None,
        method=method, headers={"Authorization": f"Bearer {KEY}", "content-type": "application/json"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.load(resp)

def split_name(full):
    parts = (full or "").split()
    return (parts[0] if parts else ""), (" ".join(parts[1:]) if len(parts) > 1 else "")

def collect_targets():
    """CEO/COO with a linkedin_url but missing email or phone."""
    tgts = []
    for ln in open(p("checkpoints", "phaseA.jsonl"), encoding="utf-8"):
        try: r = json.loads(ln)
        except Exception: continue
        dom = r.get("domain", "")
        for role in ("ceo", "coo"):
            person = r.get(role) or {}
            li = person.get("linkedin")
            if li and (not person.get("email") or not person.get("phone")):
                fn, lnm = split_name(person.get("name"))
                tgts.append({"firstname": fn, "lastname": lnm, "domain": dom,
                             "company_name": r.get("company", ""), "linkedin_url": li,
                             "enrich_fields": ["contact.emails", "contact.phones"]})
    # dedup by linkedin
    seen, out = set(), []
    for t in tgts:
        if t["linkedin_url"] not in seen:
            seen.add(t["linkedin_url"]); out.append(t)
    return out

def main(limit=None, dry=False):
    tgts = collect_targets()
    if limit: tgts = tgts[:limit]
    print(f"contacts needing fill: {len(tgts)}")
    if dry:
        sub = req("POST", "/contact/enrich/bulk", {"name": "carl_fill_test", "datas": tgts[:2]})
        print("submit response:", json.dumps(sub)[:300]); return
    done = {}
    if os.path.exists(OUT):
        for ln in open(OUT, encoding="utf-8"):
            try: d = json.loads(ln); done[d["linkedin_url"]] = 1
            except Exception: pass
    tgts = [t for t in tgts if t["linkedin_url"] not in done]
    fh = open(OUT, "a", encoding="utf-8")
    for i in range(0, len(tgts), 100):
        batch = tgts[i:i+100]
        sub = req("POST", "/contact/enrich/bulk", {"name": f"carl_fill_{i}", "datas": batch})
        eid = sub.get("enrichment_id") or sub.get("id")
        if not eid:
            print("no enrichment_id; resp:", json.dumps(sub)[:200]); break
        for _ in range(40):
            time.sleep(15)
            res = req("GET", f"/contact/enrich/bulk/{eid}")
            if res.get("status") in ("FINISHED", "COMPLETED", "DONE"): break
        for r in res.get("datas", res.get("results", [])):
            c = r.get("contact", r) or {}
            emails = c.get("emails") or []
            phones = c.get("phones") or []
            li = (r.get("linkedin_url") or (r.get("input", {}) or {}).get("linkedin_url") or "")
            fh.write(json.dumps({"linkedin_url": li,
                "email": (emails[0].get("email") if emails and isinstance(emails[0], dict) else (emails[0] if emails else "")),
                "phone": (phones[0].get("number") if phones and isinstance(phones[0], dict) else (phones[0] if phones else ""))}) + "\n")
        fh.flush()
        print(f"  batch {i//100+1}: {len(batch)} submitted, {res.get('status')}")
    print("done ->", OUT)

if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "--dry" in args
    lim = next((int(a) for a in args if a.isdigit()), None)
    main(lim, dry)
