#!/usr/bin/env python3
"""Stage 4: pull decision-maker contacts per studio (Blitz), then emails.

pull    : waterfall-icp-keyword per company -> CEO / studio head / CTO /
          tech leadership contacts -> checkpoints/contacts.jsonl
emails  : Blitz email enrichment per contact -> checkpoints/contact_emails.jsonl
fullenrich : FullEnrich bulk top-up for contacts Blitz missed ->
          checkpoints/fullenrich.jsonl

Usage: python3 s6_contacts.py pull|emails|fullenrich
"""
import csv
import json
import sys
import time
import concurrent.futures as cf
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (ROOT, load_env, post_json, blitz_headers,  # noqa: E402
                    append_jsonl, read_jsonl)

IN = ROOT / "data" / "universe_verified.csv"
CONTACTS = ROOT / "checkpoints" / "contacts.jsonl"
EMAILS = ROOT / "checkpoints" / "contact_emails.jsonl"
FE_OUT = ROOT / "checkpoints" / "fullenrich.jsonl"
BASE = "https://api.blitz-api.ai/v2"

CASCADE = [
    {"include_title": ["Chief Executive Officer", "CEO", "Co-Founder", "Founder",
                       "Studio Head", "Studio Director", "General Manager"],
     "exclude_title": ["assistant", "advisor", "board", "investor"],
     "location": ["WORLD"], "include_headline_search": True},
    {"include_title": ["Chief Technology Officer", "CTO", "Technical Director",
                       "Tech Director", "VP Engineering", "VP of Engineering",
                       "Head of Engineering", "Director of Engineering",
                       "Chief Operating Officer", "COO", "Head of Production",
                       "Executive Producer"],
     "exclude_title": ["assistant", "advisor", "board"],
     "location": ["WORLD"], "include_headline_search": True},
]


def pull_one(row):
    li = row["linkedin_url"]
    out = {"name": row["name"], "domain": row["domain"], "linkedin_url": li,
           "contacts": []}
    try:
        r = post_json(f"{BASE}/search/waterfall-icp-keyword",
                      {"company_linkedin_url": li, "cascade": CASCADE,
                       "max_results": 8}, blitz_headers(), timeout=120)
        for res in r.get("results") or []:
            p = res.get("person") or {}
            exps = p.get("experiences") or []
            cur = next((e for e in exps
                        if e.get("job_is_current")
                        and (e.get("company_linkedin_url") or "").rstrip("/")
                        .endswith(li.rstrip("/").split("/")[-1])), None)
            title = (cur or {}).get("job_title") or p.get("headline") or ""
            out["contacts"].append({
                "full_name": p.get("full_name"),
                "first_name": p.get("first_name"),
                "last_name": p.get("last_name"),
                "title": title,
                "headline": p.get("headline"),
                "person_linkedin": p.get("linkedin_url"),
                "location": p.get("location"),
                "tier": res.get("icp"),
                "start_date": (cur or {}).get("job_start_date"),
            })
    except Exception as e:
        out["err"] = str(e)[:150]
    return out


def pull():
    load_env()
    done = {r["linkedin_url"] for r in read_jsonl(CONTACTS)}
    rows = [r for r in csv.DictReader(open(IN, encoding="utf-8"))
            if r.get("linkedin_url") and r["linkedin_url"] not in done]
    print(f"companies to pull contacts for: {len(rows)} (done {len(done)})")
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        n = 0
        for rec in ex.map(pull_one, rows):
            append_jsonl(CONTACTS, rec)
            n += 1
            if n % 10 == 0:
                print(f"  {n}/{len(rows)}")
    print("done")


def emails():
    load_env()
    done = {r["person_linkedin"] for r in read_jsonl(EMAILS)}
    targets = []
    for c in read_jsonl(CONTACTS):
        for p in c.get("contacts") or []:
            pl = p.get("person_linkedin")
            if pl and pl not in done:
                targets.append((c["name"], c["domain"], p))
    print(f"contacts needing email: {len(targets)}")

    def one(t):
        comp, dom, p = t
        rec = {"company": comp, "domain": dom,
               "person_linkedin": p["person_linkedin"],
               "full_name": p.get("full_name"), "title": p.get("title")}
        try:
            r = post_json(f"{BASE}/enrichment/email",
                          {"person_linkedin_url": p["person_linkedin"]},
                          blitz_headers(), timeout=90)
            rec["email"] = r.get("email") or ""
            rec["email_status"] = "found" if r.get("found") else "not_found"
            rec["all_emails"] = "; ".join(e.get("email", "") for e in
                                          (r.get("all_emails") or []))[:200]
        except Exception as e:
            rec["err"] = str(e)[:120]
        return rec

    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        n = 0
        for rec in ex.map(one, targets):
            append_jsonl(EMAILS, rec)
            n += 1
            if n % 20 == 0:
                print(f"  {n}/{len(targets)}")
    got = sum(1 for r in read_jsonl(EMAILS) if r.get("email"))
    print(f"emails found: {got}/{len(read_jsonl(EMAILS))}")


def fullenrich():
    load_env()
    import os
    key = os.environ["FULLENRICH_API_KEY"]
    fe_base = "https://app.fullenrich.com/api/v1"

    def fe_req(method, path, body=None):
        import urllib.request
        req = urllib.request.Request(fe_base + path,
                                     data=json.dumps(body).encode() if body else None,
                                     method=method,
                                     headers={"Authorization": f"Bearer {key}",
                                              "content-type": "application/json"})
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)

    have = {r["person_linkedin"]: r for r in read_jsonl(EMAILS)}
    fe_done = {r.get("linkedin_url") for r in read_jsonl(FE_OUT)}
    targets = []
    for c in read_jsonl(CONTACTS):
        for p in c.get("contacts") or []:
            pl = p.get("person_linkedin")
            if not pl or pl in fe_done:
                continue
            if have.get(pl, {}).get("email"):
                continue
            targets.append({"firstname": p.get("first_name") or "",
                            "lastname": p.get("last_name") or "",
                            "domain": c["domain"], "company_name": c["name"],
                            "linkedin_url": pl,
                            "enrich_fields": ["contact.emails"]})
    print(f"FullEnrich targets: {len(targets)}")
    for i in range(0, len(targets), 100):
        batch = targets[i:i + 100]
        sub = fe_req("POST", "/contact/enrich/bulk",
                     {"name": f"ben_studios_{i}", "datas": batch})
        eid = sub.get("enrichment_id") or sub.get("id")
        if not eid:
            print("no enrichment_id:", json.dumps(sub)[:200])
            break
        res = {}
        for _ in range(60):
            time.sleep(15)
            res = fe_req("GET", f"/contact/enrich/bulk/{eid}")
            if res.get("status") in ("FINISHED", "COMPLETED", "DONE"):
                break
        for r in res.get("datas", res.get("results", [])):
            c = r.get("contact", r) or {}
            emails_l = c.get("emails") or []
            li = (r.get("linkedin_url")
                  or (r.get("input", {}) or {}).get("linkedin_url") or "")
            append_jsonl(FE_OUT, {
                "linkedin_url": li,
                "emails": [e.get("email") if isinstance(e, dict) else e
                           for e in emails_l],
                "raw_status": r.get("status") or res.get("status")})
        print(f"  batch {i}: {len(batch)} submitted")


if __name__ == "__main__":
    {"pull": pull, "emails": emails, "fullenrich": fullenrich}[sys.argv[1]]()
