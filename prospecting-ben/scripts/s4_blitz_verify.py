#!/usr/bin/env python3
"""Stage 2: verify candidates with Blitz — resolve LinkedIn, pull headcount/HQ.

Input : data/candidates_merged.csv  (name, domain, sources, notes)
Output: checkpoints/blitz_verify.jsonl ; data/universe_verified.csv

Filters applied downstream (soft): US HQ, employees_on_linkedin 15-170.
Blitz plan is flat-rate; 50-200 QPS. Resume-safe by domain.

Usage: python3 s4_blitz_verify.py
"""
import csv
import sys
import concurrent.futures as cf
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (ROOT, load_env, post_json, blitz_headers,  # noqa: E402
                    append_jsonl, read_jsonl, norm_domain)

IN = ROOT / "data" / "candidates_merged.csv"
OUT = ROOT / "checkpoints" / "blitz_verify.jsonl"
CSV_OUT = ROOT / "data" / "universe_verified.csv"
BASE = "https://api.blitz-api.ai/v2"


def verify_one(row):
    domain = norm_domain(row.get("domain", ""))
    rec = {"name": row["name"], "domain": domain, "sources": row.get("sources", ""),
           "notes": row.get("notes", ""), "linkedin_url": row.get("linkedin_url", "")}
    try:
        if not rec["linkedin_url"]:
            if not domain:
                rec["status"] = "no_domain"
                return rec
            r = post_json(f"{BASE}/enrichment/domain-to-linkedin",
                          {"domain": domain}, blitz_headers())
            if not r.get("found"):
                rec["status"] = "no_linkedin"
                return rec
            rec["linkedin_url"] = r.get("company_linkedin_url", "")
        r = post_json(f"{BASE}/enrichment/company",
                      {"company_linkedin_url": rec["linkedin_url"]}, blitz_headers())
        if not r.get("found"):
            rec["status"] = "enrich_miss"
            return rec
        c = r["company"]
        rec.update({
            "status": "ok",
            "blitz_name": c.get("name"),
            "employees_on_linkedin": c.get("employees_on_linkedin"),
            "size_band": c.get("size"),
            "industry": c.get("industry"),
            "founded_year": c.get("founded_year"),
            "hq_country": (c.get("hq") or {}).get("country_code"),
            "hq_city": (c.get("hq") or {}).get("city"),
            "hq_state": (c.get("hq") or {}).get("state"),
            "about": (c.get("about") or "")[:600],
            "blitz_domain": c.get("domain"),
            "specialties": ", ".join(c.get("specialties") or [])[:300],
        })
    except Exception as e:
        rec["status"] = f"err:{e}"
    return rec


def main():
    load_env()
    done = {r["domain"] or r["name"] for r in read_jsonl(OUT)}
    rows = [r for r in csv.DictReader(open(IN, encoding="utf-8"))
            if (norm_domain(r.get("domain", "")) or r["name"]) not in done]
    print(f"to verify: {len(rows)} (done {len(done)})")
    with cf.ThreadPoolExecutor(max_workers=20) as ex:
        for rec in ex.map(verify_one, rows):
            append_jsonl(OUT, rec)
    recs = read_jsonl(OUT)
    ok = [r for r in recs if r.get("status") == "ok"]
    keep = [r for r in ok
            if (r.get("hq_country") in ("US", None, ""))
            and (r.get("employees_on_linkedin") or 0) >= 12
            and (r.get("employees_on_linkedin") or 0) <= 200]
    cols = ["name", "blitz_name", "domain", "linkedin_url", "employees_on_linkedin",
            "size_band", "industry", "founded_year", "hq_city", "hq_state",
            "hq_country", "specialties", "sources", "notes", "about"]
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in sorted(keep, key=lambda x: -(x.get("employees_on_linkedin") or 0)):
            w.writerow(r)
    print(f"verified ok: {len(ok)}; in-band US keep: {len(keep)} -> {CSV_OUT}")


if __name__ == "__main__":
    main()
