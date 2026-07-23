#!/usr/bin/env python3
"""Recovery pass: resolve LinkedIn company URLs for promising unresolved
candidates via Exa (linkedin.com/company keyword search), then Blitz-verify
and append to universe.

Usage: python3 s4b_recover.py
"""
import re
import sys
import csv
import concurrent.futures as cf
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (ROOT, load_env, post_json, exa_headers,  # noqa: E402
                    append_jsonl, read_jsonl, norm_domain)
import s4_blitz_verify as s4  # noqa: E402

CK = ROOT / "checkpoints"
OUT = CK / "blitz_verify.jsonl"

LI_RE = re.compile(r"linkedin\.com/company/([A-Za-z0-9\-_%\.]+)", re.I)


def find_linkedin(name, notes):
    q = f"{name} game studio"
    body = {"query": q, "type": "keyword", "numResults": 5,
            "includeDomains": ["linkedin.com"]}
    try:
        resp = post_json("https://api.exa.ai/search", body, exa_headers())
        for r in resp.get("results", []):
            m = LI_RE.search(r.get("url") or "")
            if m:
                slug = m.group(1).rstrip("/").lower()
                if slug in ("linkedin", "company"):
                    continue
                # crude name check: half the name tokens appear in slug/title
                toks = [t for t in re.split(r"\W+", name.lower())
                        if len(t) > 2 and t not in ("the", "games", "game",
                                                    "studios", "studio")]
                hay = (slug + " " + (r.get("title") or "")).lower()
                if not toks or sum(t in hay for t in toks) >= max(1, len(toks)//2):
                    return f"https://www.linkedin.com/company/{slug}"
    except Exception:
        pass
    return ""


def main():
    load_env()
    recs = read_jsonl(OUT)
    resolved_names = {r["name"] for r in recs if r.get("status") == "ok"}
    targets = [r for r in recs
               if r.get("status") in ("no_domain", "no_linkedin", "enrich_miss")
               and r["name"] not in resolved_names
               and ("|" in r.get("sources", "") or "news" in r.get("sources", "")
                    or "exa-agent" in r.get("sources", ""))]
    # dedupe by name
    seen, tgts = set(), []
    for r in targets:
        if r["name"].lower() not in seen:
            seen.add(r["name"].lower())
            tgts.append(r)
    print(f"recovery targets: {len(tgts)}")

    def one(r):
        li = find_linkedin(r["name"], r.get("notes", ""))
        if not li:
            return {"name": r["name"], "status": "recover_failed"}
        row = {"name": r["name"], "domain": r.get("domain", ""),
               "sources": r.get("sources", ""), "notes": r.get("notes", ""),
               "linkedin_url": li}
        rec = s4.verify_one(row)
        rec["recovered_via"] = "exa-linkedin"
        return rec

    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        n_ok = 0
        for rec in ex.map(one, tgts):
            append_jsonl(OUT, rec)
            if rec.get("status") == "ok":
                n_ok += 1
    print(f"recovered ok: {n_ok}")

    # regenerate universe_verified.csv (same filter as s4)
    recs = read_jsonl(OUT)
    best = {}
    for r in recs:
        if r.get("status") != "ok":
            continue
        key = r.get("linkedin_url") or r["name"].lower()
        best[key] = r
    keep = [r for r in best.values()
            if (r.get("hq_country") in ("US", None, ""))
            and 12 <= (r.get("employees_on_linkedin") or 0) <= 200]
    cols = ["name", "blitz_name", "domain", "linkedin_url", "employees_on_linkedin",
            "size_band", "industry", "founded_year", "hq_city", "hq_state",
            "hq_country", "specialties", "sources", "notes", "about"]
    with open(s4.CSV_OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in sorted(keep, key=lambda x: -(x.get("employees_on_linkedin") or 0)):
            if not r.get("domain"):
                r["domain"] = norm_domain(r.get("blitz_domain", ""))
            w.writerow(r)
    print(f"universe now: {len(keep)} -> {s4.CSV_OUT}")


if __name__ == "__main__":
    main()
