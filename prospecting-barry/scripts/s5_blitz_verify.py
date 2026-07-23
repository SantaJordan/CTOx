#!/usr/bin/env python3
"""Stage 2: verify candidates with Blitz — resolve LinkedIn, pull headcount/HQ,
apply Barry's firmographic gates.

Input : data/candidates_merged.csv
Output: checkpoints/blitz_verify.jsonl ; data/universe_verified.csv

Gates (from Barry's signal_spec disqualifiers + Jordan's loose either/or stage
decision): US HQ; headcount 2-300 (2-150 core, 151-300 flagged stage=late);
drop primes/major SIs and staffing/recruiting shops. stage_band derived from
channel notes (funding stage if Exa saw one, sbir, else unknown).

Usage: python3 s5_blitz_verify.py
"""
import csv
import re
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

PRIME_RE = re.compile(
    r"lockheed|raytheon|\brtx\b|boeing|northrop|general dynamics|l3harris"
    r"|bae systems|leidos|booz allen|\bsaic\b|\bcaci\b|mantech|peraton"
    r"|accenture|deloitte|kbr\b|jacobs|amentum|maximus|mitre|aerospace corp",
    re.I)
STAFFING_RE = re.compile(
    r"staffing|recruiting|recruitment|talent (acquisition|solutions)"
    r"|workforce solutions|placement (firm|agency)|body.?shop|cleared jobs",
    re.I)


def stage_band(sources, notes):
    t = (notes or "").lower()
    if re.search(r"pre.?seed", t):
        return "preseed_seed"
    if re.search(r"\bseed\b", t):
        return "preseed_seed"
    if re.search(r"series a\b", t):
        return "series_a"
    if re.search(r"series [b-d]\b", t):
        return "late_round"
    if "sbir" in (sources or ""):
        return "revenue_stage"
    return "unknown"


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
    drops = {"prime": 0, "staffing": 0, "non_us": 0, "too_big": 0, "too_small": 0}
    keep = []
    for r in ok:
        blob = " ".join(str(r.get(k) or "") for k in
                        ("name", "blitz_name", "industry", "about", "specialties"))
        emp = r.get("employees_on_linkedin") or 0
        if PRIME_RE.search(blob):
            drops["prime"] += 1
            continue
        if STAFFING_RE.search(blob):
            drops["staffing"] += 1
            continue
        if r.get("hq_country") not in ("US", None, ""):
            drops["non_us"] += 1
            continue
        if emp > 300:
            drops["too_big"] += 1
            continue
        if emp < 2:
            drops["too_small"] += 1
            continue
        r["late_flag"] = emp > 150
        r["stage_band"] = stage_band(r.get("sources"), r.get("notes"))
        keep.append(r)

    cols = ["name", "blitz_name", "domain", "blitz_domain", "linkedin_url",
            "employees_on_linkedin", "late_flag", "stage_band", "size_band",
            "industry", "founded_year", "hq_city", "hq_state", "hq_country",
            "specialties", "sources", "notes", "about"]
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in sorted(keep, key=lambda x: -(x.get("employees_on_linkedin") or 0)):
            w.writerow(r)
    print(f"verified ok: {len(ok)}; drops: {drops}; keep: {len(keep)} -> {CSV_OUT}")


if __name__ == "__main__":
    main()
