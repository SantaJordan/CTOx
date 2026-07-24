#!/usr/bin/env python3
"""Stage 5b: FullEnrich bulk waterfall for work email + mobile on every s8 person.
In : output/people.csv        Out: checkpoints/enrich.jsonl
Usage: python3 s9_fullenrich.py
"""
import csv
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, load_env, read_jsonl  # noqa: E402

SRC = ROOT / "output" / "people.csv"
JL = ROOT / "checkpoints" / "enrich.jsonl"
API = "https://app.fullenrich.com/api/v1"


def req(method, path, body=None):
    headers = {"Authorization": f"Bearer {os.environ['FULLENRICH_API_KEY']}",
               "content-type": "application/json"}
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(r, timeout=90) as resp:
                return json.load(resp)
        except Exception as e:
            if attempt == 2:
                return {"_error": str(e)[:200]}
            time.sleep(5 * (attempt + 1))


def em(e):
    return e.get("email") if isinstance(e, dict) else e


def ph(p):
    return (p.get("number") or p.get("phone")) if isinstance(p, dict) else p


def main():
    load_env()
    if not SRC.exists():
        sys.exit("no output/people.csv yet — run s8 first")
    people = list(csv.DictReader(open(SRC)))
    done = {r["linkedin_url"] for r in read_jsonl(JL)}
    seen, todo = set(), []
    for p in people:
        li = p.get("linkedin_url", "").strip()
        if li and li not in done and li not in seen:
            seen.add(li)
            todo.append(p)
    print(f"{len(people)} people, {len(done)} enriched, {len(todo)} to submit")
    if not todo:
        return

    jobs = {}
    for i in range(0, len(todo), 100):
        batch = todo[i:i + 100]
        datas = [{
            "firstname": t.get("first_name", ""),
            "lastname": t.get("last_name", ""),
            "domain": (t.get("domain") or "").strip(),
            "company_name": t.get("company_name", ""),
            "linkedin_url": t["linkedin_url"],
            "enrich_fields": ["contact.emails", "contact.phones"],
        } for t in batch]
        sub = req("POST", "/contact/enrich/bulk",
                  {"name": f"barry_{i // 100}", "datas": datas})
        eid = sub.get("enrichment_id") or sub.get("id")
        if not eid:
            print(f"  submit failed: {json.dumps(sub)[:200]}")
            continue
        jobs[eid] = True
        print(f"  submitted batch {i // 100 + 1} ({len(batch)} people)")
        time.sleep(1)

    pending = dict(jobs)
    JL.parent.mkdir(parents=True, exist_ok=True)
    with open(JL, "a") as fh:
        for _ in range(120):
            if not pending:
                break
            time.sleep(15)
            for eid in list(pending):
                res = req("GET", f"/contact/enrich/bulk/{eid}")
                if (res.get("status") or "").upper() not in ("FINISHED", "COMPLETED", "DONE"):
                    continue
                for r in res.get("datas", res.get("results", [])):
                    c = r.get("contact", r) or {}
                    emails = c.get("emails") or []
                    phones = c.get("phones") or []
                    inp = r.get("input", {}) or {}
                    li = r.get("linkedin_url") or inp.get("linkedin_url") or ""
                    fh.write(json.dumps({
                        "linkedin_url": li,
                        "fe_email": em(emails[0]) if emails else "",
                        "fe_all_emails": "; ".join(filter(None, (em(e) for e in emails))),
                        "fe_phone": ph(phones[0]) if phones else "",
                    }, ensure_ascii=False) + "\n")
                fh.flush()
                del pending[eid]
                print(f"  batch {eid[:8]}… finished; {len(pending)} left")
    enriched = read_jsonl(JL)
    n_e = sum(1 for r in enriched if r.get("fe_email"))
    n_p = sum(1 for r in enriched if r.get("fe_phone"))
    print(f"enriched {len(enriched)} people — {n_e} with email, {n_p} with mobile "
          f"({n_e * 100 // max(len(enriched), 1)}% / {n_p * 100 // max(len(enriched), 1)}%)")


if __name__ == "__main__":
    main()
