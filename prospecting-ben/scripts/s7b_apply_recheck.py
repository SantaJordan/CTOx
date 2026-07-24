#!/usr/bin/env python3
"""Apply human-grade recheck verdicts to the ranked universe.

Adds a `verified` column to output/ben_universe_ranked.csv from
checkpoints/fit_recheck.jsonl. A studio whose flagship turns out to have
ALREADY SHIPPED is demoted to fit_verdict=caution and loses its launch-
proximity points, because the core ICP claim ("hasn't shipped") fails.

Re-runnable. Usage: python3 s7b_apply_recheck.py
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, read_jsonl  # noqa: E402

CSV = ROOT / "output" / "ben_universe_ranked.csv"
CONTACTS = ROOT / "output" / "contacts_ranked.csv"


def main():
    checks = {r["name"].lower(): r for r in
              read_jsonl(ROOT / "checkpoints" / "fit_recheck.jsonl")}
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    cols = list(rows[0].keys())
    if "verified" not in cols:
        cols.insert(cols.index("fit_verdict") + 1, "verified")

    for r in rows:
        c = checks.get(r["company"].lower())
        if not c:
            r.setdefault("verified", "")
            continue
        notes = []
        if c.get("headcount_note"):
            notes.append(c["headcount_note"])
        if c.get("status_note"):
            notes.append(c["status_note"])
        if c.get("recent_news"):
            notes.append(c["recent_news"])
        r["verified"] = f"[{c['still_fits'].upper()}] " + " | ".join(notes)[:700]

        # Demote a studio that has in fact already shipped its flagship.
        if c.get("launched") in ("yes", "partial") and c["still_fits"] != "yes":
            old = int(r["pain_score"])
            r["fit_verdict"] = "caution"
            r["pain_score"] = str(max(0, old - int(r["launch_score"] or 0)))
            r["launch_score"] = "0"
            r["launch_why"] = ("RECHECK: flagship already shipped commercially — "
                               + (c.get("status_note") or ""))[:400]

    rows.sort(key=lambda r: -int(r["pain_score"]))
    with open(CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    # keep contact pain scores in sync
    score = {r["company"]: r["pain_score"] for r in rows}
    crows = list(csv.DictReader(open(CONTACTS, encoding="utf-8")))
    for c in crows:
        c["pain_score"] = score.get(c["company"], c["pain_score"])
    crows.sort(key=lambda c: (-int(c["pain_score"]), c["company"]))
    with open(CONTACTS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(crows[0].keys()))
        w.writeheader()
        w.writerows(crows)

    for r in rows[:6]:
        print(f"{r['pain_score']:>3} {r['company']:<24} {r['fit_verdict']:<9} "
              f"{r['verified'][:60]}")
    print(f"\nrechecked+annotated: {sum(1 for r in rows if r['verified'])}")


if __name__ == "__main__":
    main()
