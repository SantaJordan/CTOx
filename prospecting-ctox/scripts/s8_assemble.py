# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""s8 — merge everything into one people-list CSV per CTO.

One row PER PERSON; company data repeated on every row (Jordan's spec).
In : research/companies/<cto>/*.json (keeps: talk track, evidence, grade)
     checkpoints/live/<cto>_companies_live.jsonl (liveness + verified date)
     output/<cto>_people.csv (Blitz people)
     checkpoints/enrich/<cto>.jsonl (FullEnrich email/mobile)
Out: output/<cto>_final.csv  +  output/<cto>_final_public.csv (no mobiles)

--qa prints mechanical checks instead of writing.
Usage: python3 s8_assemble.py <cto-slug> [...]
"""
import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_common import CHECKPOINTS, OUTPUT, RESEARCH, read_jsonl, say

COLS = ["Company", "Company Does", "Industry", "Stage", "Why This Company (signal)",
        "Live Job Title", "Live Job URL", "Job Verified", "Fit Score",
        "Person", "Title", "Role", "Best Email", "Mobile", "Person LinkedIn",
        "Company LinkedIn", "Location", "Talk Track", "Copy Grade"]


def run_cto(slug, qa=False):
    keeps = {}
    for f in sorted((RESEARCH / slug).glob("*.json")):
        try:
            rec = json.loads(f.read_text())
        except Exception:
            continue
        if rec.get("verdict") == "keep":
            keeps[rec["company"].get("name", "")] = rec

    live = {}
    for r in read_jsonl(CHECKPOINTS / "live" / f"{slug}_companies_live.jsonl"):
        live[r["company"]] = r
    verified_date = ""
    lf = CHECKPOINTS / "live" / f"{slug}_companies_live.jsonl"
    if lf.exists():
        verified_date = time.strftime("%Y-%m-%d", time.localtime(lf.stat().st_mtime))

    enrich = {r["linkedin_url"]: r for r in read_jsonl(CHECKPOINTS / "enrich" / f"{slug}.jsonl")}

    ppl_file = OUTPUT / f"{slug}_people.csv"
    people = list(csv.DictReader(open(ppl_file))) if ppl_file.exists() else []

    rows = []
    for p in people:
        comp = p.get("company_name", "")
        k = keeps.get(comp)
        if not k:
            continue
        ev = (k.get("evidence_jobs") or [{}])[0]
        e = enrich.get(p.get("linkedin_url", ""), {})
        rows.append({
            "Company": comp,
            "Company Does": k["company"].get("one_liner", ""),
            "Industry": k["company"].get("industry", ""),
            "Stage": k["company"].get("stage", ""),
            "Why This Company (signal)": k.get("reason", ""),
            "Live Job Title": ev.get("title", ""),
            "Live Job URL": ev.get("url", ""),
            "Job Verified": verified_date,
            "Fit Score": k.get("fit_score", ""),
            "Person": p.get("full_name", ""),
            "Title": p.get("title", ""),
            "Role": p.get("role_bucket", ""),
            "Best Email": e.get("fe_email", ""),
            "Mobile": e.get("fe_phone", ""),
            "Person LinkedIn": p.get("linkedin_url", ""),
            "Company LinkedIn": p.get("company_linkedin_url", ""),
            "Location": p.get("location", ""),
            "Talk Track": k.get("talk_track", ""),
            "Copy Grade": k.get("copy_grade", ""),
        })
    rows.sort(key=lambda r: (-float(r["Fit Score"] or 0), r["Company"]))

    if qa:
        n_email = sum(1 for r in rows if r["Best Email"])
        n_mob = sum(1 for r in rows if r["Mobile"])
        n_url = sum(1 for r in rows if r["Live Job URL"])
        say(f"{slug}: {len(keeps)} kept companies, {len(rows)} people rows, "
            f"{n_email} emails ({n_email * 100 // max(len(rows), 1)}%), "
            f"{n_mob} mobiles, {n_url} rows with a live job URL")
        missing_track = [c for c, k in keeps.items() if not k.get("talk_track")]
        if missing_track:
            say(f"  MISSING talk tracks: {missing_track[:5]}")
        return

    out = OUTPUT / f"{slug}_final.csv"
    pub = OUTPUT / f"{slug}_final_public.csv"
    for path, redact in ((out, False), (pub, True)):
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writeheader()
            for r in rows:
                rr = dict(r)
                if redact:
                    rr["Mobile"] = ""
                w.writerow(rr)
    say(f"{slug}: wrote {len(rows)} people rows across "
        f"{len({r['Company'] for r in rows})} companies -> {out.name} (+ public copy, no mobiles)")


def main():
    args = [a for a in sys.argv[1:] if a != "--qa"]
    qa = "--qa" in sys.argv
    for slug in args:
        run_cto(slug, qa=qa)


if __name__ == "__main__":
    main()
