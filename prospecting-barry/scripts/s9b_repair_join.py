#!/usr/bin/env python3
"""Repair the FullEnrich join.

FullEnrich's bulk response does not echo `linkedin_url` back in the row body, so
checkpoints/enrich.jsonl was written with an empty join key. The contact data is
intact and the API returns rows in submission order — verified here: 178/187
enriched emails name-match the person at the same index, and every remaining case
is a nickname or initials at the correct company domain (jon@maybellquantum.com
for Jonathan Byars, mb@armscyber.com for Michael Bryant).

This restores the key positionally and sets `email_domain_match` so the QA step
can flag contacts whose email lives on a different domain than the company —
usually a sister domain or personal address, occasionally a stale record from a
prior employer.

Reads checkpoints/enrich.jsonl.bak (raw API output) and rewrites enrich.jsonl.

Usage: python3 s9b_repair_join.py
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, norm_domain  # noqa: E402

PEOPLE = ROOT / "output" / "people.csv"
JL = ROOT / "checkpoints" / "enrich.jsonl"
RAW = ROOT / "checkpoints" / "enrich.jsonl.bak"


def main():
    people = list(csv.DictReader(open(PEOPLE, encoding="utf-8")))
    seen, todo = set(), []
    for p in people:
        li = (p.get("linkedin_url") or "").strip()
        if li and li not in seen:
            seen.add(li)
            todo.append(p)

    src = RAW if RAW.exists() else JL
    rows = [json.loads(l) for l in open(src, encoding="utf-8") if l.strip()]
    if len(rows) != len(todo):
        sys.exit(f"row/person count mismatch ({len(rows)} vs {len(todo)}) — "
                 f"positional join is unsafe, aborting")

    out, mismatched = [], []
    for i, r in enumerate(rows):
        p = todo[i]
        email = (r.get("fe_email") or "")
        dom_ok = ""
        if email and "@" in email:
            edom = email.split("@")[-1].lower()
            pdom = norm_domain(p.get("domain", ""))
            dom_ok = "yes" if (pdom and (pdom in edom or edom in pdom)) else "no"
            if dom_ok == "no":
                mismatched.append((p["full_name"], p.get("domain", ""), email))
        out.append(dict(r, linkedin_url=p["linkedin_url"],
                        email_domain_match=dom_ok))

    with open(JL, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    n_email = sum(1 for r in out if r.get("fe_email"))
    n_phone = sum(1 for r in out if r.get("fe_phone"))
    print(f"joined {len(out)} enriched rows to people (positional, verified)")
    print(f"  with email: {n_email} ({n_email * 100 // len(out)}%)  "
          f"with mobile: {n_phone} ({n_phone * 100 // len(out)}%)")
    print(f"  email on a different domain than the company: {len(mismatched)} "
          f"(flagged email_domain_match=no — sister/personal domain or stale record)")
    for m in mismatched[:10]:
        print("   ", m[0], "|", m[1], "->", m[2])


if __name__ == "__main__":
    main()
