# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""s7 — FullEnrich waterfall for work email + mobile on every person from s6.

Submits all batches up front (<=100 rows each), polls until finished.
In : output/<cto>_people.csv        Out: checkpoints/enrich/<cto>.jsonl
Usage: python3 s7_fullenrich.py <cto-slug> [...]
"""
import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_common import OUTPUT, checkpoint_path, http_json, key, read_jsonl, say

API = "https://app.fullenrich.com/api/v1"


def req(method, path, body=None):
    try:
        return http_json(API + path, body,
                         {"Authorization": f"Bearer {key('FULLENRICH_API_KEY')}"},
                         method=method, retries=2)
    except RuntimeError as e:
        return {"_error": str(e)[:200]}


def em(e):
    return e.get("email") if isinstance(e, dict) else e


def ph(p):
    return (p.get("number") or p.get("phone")) if isinstance(p, dict) else p


def run_cto(slug):
    src = OUTPUT / f"{slug}_people.csv"
    if not src.exists():
        say(f"{slug}: no people file yet")
        return
    people = list(csv.DictReader(open(src)))
    jl = checkpoint_path("enrich", f"{slug}.jsonl")
    done = {r["linkedin_url"] for r in read_jsonl(jl)}
    seen = set()
    todo = []
    for p in people:
        li = p.get("linkedin_url", "").strip()
        if li and li not in done and li not in seen:
            seen.add(li)
            todo.append(p)
    say(f"{slug}: {len(people)} people, {len(done)} enriched, {len(todo)} to submit")
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
                  {"name": f"ctox_{slug}_{i // 100}", "datas": datas})
        eid = sub.get("enrichment_id") or sub.get("id")
        if not eid:
            say(f"  submit failed: {json.dumps(sub)[:200]}")
            continue
        jobs[eid] = True
        say(f"  submitted batch {i // 100 + 1} ({len(batch)} people)")
        time.sleep(1)

    pending = dict(jobs)
    with open(jl, "a") as fh:
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
                say(f"  batch {eid[:8]}… finished; {len(pending)} batches left")
    enriched = read_jsonl(jl)
    n_e = sum(1 for r in enriched if r.get("fe_email"))
    n_p = sum(1 for r in enriched if r.get("fe_phone"))
    say(f"{slug}: enriched {len(enriched)} people — {n_e} with email, {n_p} with mobile")


def main():
    for slug in sys.argv[1:]:
        run_cto(slug)


if __name__ == "__main__":
    main()
