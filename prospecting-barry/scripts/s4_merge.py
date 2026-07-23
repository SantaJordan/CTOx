#!/usr/bin/env python3
"""Merge all four discovery channels into data/candidates_merged.csv.

Inputs (checkpoints/): portco_extract_A/B/C.jsonl (defense VC portfolios),
exa_agent_runs.jsonl (structured companies), sbir_awards.jsonl (DoD Phase II,
non-mill), plus ../prospecting-ctox/checkpoints/match/barry-hess_companies.csv
(jobs-are-confessions channel).
Dedupe by domain first, then normalized name. Sources kept as provenance list.

Usage: python3 s4_merge.py
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, REPO, read_jsonl, norm_domain  # noqa: E402

CK = ROOT / "checkpoints"
OUT = ROOT / "data" / "candidates_merged.csv"
JOBS_CSV = REPO / "prospecting-ctox" / "checkpoints" / "match" / "barry-hess_companies.csv"


def nname(s):
    s = re.sub(r"[^a-z0-9 ]", "", (s or "").lower())
    s = re.sub(r"\b(technologies|technology|tech|systems|system|solutions|labs|lab"
               r"|defense|industries|inc|llc|co|corp|corporation|the)\b", "", s)
    return re.sub(r"\s+", "", s)


def main():
    merged = {}

    def add(name, domain, source, note):
        name = (name or "").strip()
        if not name or len(name) < 2:
            return
        domain = norm_domain(domain)
        key = domain or ("n:" + nname(name))
        if not key or key == "n:":
            return
        if key in merged:
            r = merged[key]
            if source not in r["sources"]:
                r["sources"] += f"|{source}"
            if note and note not in r["notes"]:
                r["notes"] = (r["notes"] + " || " + note)[:900]
        else:
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

    # A/B/C: defense VC portfolios
    n_large = 0
    for f in ["portco_extract_A.jsonl", "portco_extract_B.jsonl",
              "portco_extract_C.jsonl"]:
        for r in read_jsonl(CK / f):
            if r.get("skip_large"):
                n_large += 1
                continue
            add(r.get("name"), r.get("domain"), f"vc:{r.get('fund')}",
                r.get("note", ""))

    # Exa agent structured output
    for run in read_jsonl(CK / "exa_agent_runs.jsonl"):
        st = run.get("structured") or {}
        for c in (st.get("companies") or []):
            note = (f"{c.get('funding_stage','')} {c.get('funding_summary','')} "
                    f"dom: {c.get('domain_category','')} status: {c.get('product_status','')} "
                    f"dod: {c.get('dod_evidence','')} hq: {c.get('hq_location','')} "
                    f"emp: {c.get('employee_estimate','')} src: {c.get('evidence_url','')}").strip()
            add(c.get("name"), c.get("website"), f"exa-agent:{run.get('tag')}", note)

    # SBIR DoD Phase II (non-mill only — mills are research houses, not product cos)
    n_mill = 0
    for r in read_jsonl(CK / "sbir_awards.jsonl"):
        if r.get("sbir_mill"):
            n_mill += 1
            continue
        aw = r.get("awards") or []
        years = sorted({a["year"] for a in aw})
        branches = sorted({a.get("branch") or "" for a in aw if a.get("branch")})
        latest = max(aw, key=lambda a: a["year"]) if aw else {}
        note = (f"SBIR PhII x{len(aw)} {years} {'/'.join(branches)} "
                f"latest: {latest.get('title','')[:120]} "
                f"hq: {r.get('city','')},{r.get('state','')} emp: {r.get('employees','')}").strip()
        add(r.get("company"), r.get("website"), "sbir", note)

    # Jobs-are-confessions channel (ctox match for barry-hess)
    if JOBS_CSV.exists():
        for r in csv.DictReader(open(JOBS_CSV, encoding="utf-8")):
            slug = r.get("company", "")
            domain = slug if "." in slug else ""
            note = (f"jobs fit={r.get('fit_score','')} n={r.get('n_matched_jobs','')} "
                    f"open={r.get('company_open_jobs','')} does: {r.get('company_does','')} "
                    f"stage: {r.get('company_stage','')} best: {r.get('best_job_title','')}").strip()
            add(slug, domain, f"jobs:{r.get('ats','')}", note)

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
    print(f"merged candidates: {len(rows)} ({multi} multi-source; "
          f"excluded {n_mill} sbir mills, {n_large} known-large) -> {OUT}")


if __name__ == "__main__":
    main()
