#!/usr/bin/env python3
"""Merge all discovery angles into data/candidates_merged.csv.

Inputs (checkpoints/): portco_extract_batch1/2.jsonl, portco_extract_missing.jsonl
(game_studio rows), news_extract_batch1/2.jsonl (non-released rows),
exa_agent_runs.jsonl (structured companies).
Dedupe by domain first, then normalized name.

Usage: python3 s3b_merge_candidates.py
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, read_jsonl, norm_domain  # noqa: E402

CK = ROOT / "checkpoints"
OUT = ROOT / "data" / "candidates_merged.csv"


def nname(s):
    s = re.sub(r"[^a-z0-9 ]", "", (s or "").lower())
    s = re.sub(r"\b(games|game|studios|studio|interactive|entertainment|inc|llc"
               r"|co|corp|the)\b", "", s)
    return re.sub(r"\s+", "", s)


def main():
    merged = {}   # key -> rec

    def add(name, domain, source, note):
        name = (name or "").strip()
        if not name or len(name) < 2:
            return
        domain = norm_domain(domain)
        key = domain or ("n:" + nname(name))
        if not key or key == "n:":
            return
        # if a name-key rec later gains a domain, prefer domain key
        if key in merged:
            r = merged[key]
            if source not in r["sources"]:
                r["sources"] += f"|{source}"
            if note and note not in r["notes"]:
                r["notes"] = (r["notes"] + " || " + note)[:900]
        else:
            # check name-key duplicate when adding domain-key rec
            nk = "n:" + nname(name)
            if domain and nk in merged:
                r = merged.pop(nk)
                r["domain"] = domain
                if source not in r["sources"]:
                    r["sources"] += f"|{source}"
                if note and note not in r["notes"]:
                    r["notes"] = (r["notes"] + " || " + note)[:900]
                merged[key] = r
            else:
                merged[key] = {"name": name, "domain": domain,
                               "sources": source, "notes": (note or "")[:900]}

    # VC portfolios — game studios only
    for f in ["portco_extract_batch1.jsonl", "portco_extract_batch2.jsonl",
              "portco_extract_missing.jsonl"]:
        for r in read_jsonl(CK / f):
            if r.get("category_guess") == "game_studio":
                add(r.get("name"), r.get("domain"), f"vc:{r.get('fund_id')}",
                    r.get("evidence", ""))

    # News events — skip released/live
    for f in ["news_extract_batch1.jsonl", "news_extract_batch2.jsonl"]:
        for r in read_jsonl(CK / f):
            if r.get("game_status") in ("released", "live-game"):
                continue
            note = (f"{r.get('amount','')} {r.get('round','')} {r.get('date','')} "
                    f"inv: {r.get('investors','')} status: {r.get('game_status','')} "
                    f"src: {r.get('source_url','')}").strip()
            add(r.get("name"), r.get("domain"), "news", note)
            if r.get("hq"):
                merged_key = norm_domain(r.get("domain")) or ("n:" + nname(r.get("name", "")))
                if merged_key in merged and "hq:" not in merged[merged_key]["notes"]:
                    merged[merged_key]["notes"] += f" || hq: {r['hq']}"

    # Exa agent structured output
    for run in read_jsonl(CK / "exa_agent_runs.jsonl"):
        st = run.get("structured") or {}
        for c in (st.get("companies") or []):
            note = (f"{c.get('funding_summary','')} {c.get('latest_round_date','')} "
                    f"inv: {c.get('investors','')} status: {c.get('game_status','')} "
                    f"hq: {c.get('hq_location','')} emp: {c.get('employee_estimate','')} "
                    f"src: {c.get('evidence_url','')}").strip()
            add(c.get("name"), c.get("website"), f"exa-agent:{run.get('tag')}", note)

    rows = sorted(merged.values(), key=lambda r: (-len(r["sources"].split("|")),
                                                  r["name"].lower()))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["name", "domain", "sources", "notes",
                                          "linkedin_url"])
        w.writeheader()
        for r in rows:
            r["linkedin_url"] = ""
            w.writerow(r)
    multi = sum(1 for r in rows if "|" in r["sources"])
    print(f"merged candidates: {len(rows)} ({multi} multi-source) -> {OUT}")


if __name__ == "__main__":
    main()
