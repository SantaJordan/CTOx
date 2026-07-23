#!/usr/bin/env python3
"""Stage 5a: find CEO + CTO for the top-N ranked companies via Blitz waterfall-ICP.

In : data/ranked_companies.csv (top TOP_N by disconnect_score)
     checkpoints/blitz_verify.jsonl (company LinkedIn URLs already resolved)
Out: checkpoints/people.jsonl (resumable) + output/people.csv

Two buckets per company (max 2 each): CEO (CEO/Founder/President) and CTO
(CTO/VP Eng/Head of Eng/Technical Director). EXCL keeps fractional/interim/
advisors out — never hand Barry his competitors.

Usage: python3 s8_people.py [--top N]
"""
import csv
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (ROOT, load_env, post_json, blitz_headers,  # noqa: E402
                    read_jsonl, norm_domain)

IN = ROOT / "data" / "ranked_companies.csv"
VERIFY = ROOT / "checkpoints" / "blitz_verify.jsonl"
JL = ROOT / "checkpoints" / "people.jsonl"
OUT = ROOT / "output" / "people.csv"
BLITZ = "https://api.blitz-api.ai"
TOP_N = 100

EXCL = ["fractional", "interim", "advisor", "assistant", "intern", "junior",
        "former", "consultant", "retired", "board"]
CEO_TIER = ["Chief Executive Officer", "CEO", "Founder", "Co-Founder",
            "President", "Owner"]
CTO_TIER = ["Chief Technology Officer", "CTO", "VP of Engineering",
            "VP Engineering", "Head of Engineering", "Technical Director",
            "Chief Engineer", "Director of Engineering"]


def post(path, body):
    try:
        return post_json(BLITZ + path, body, blitz_headers(), timeout=60)
    except Exception as e:
        return {"_error": str(e)[:200]}


def resolve_company(name, domain, li_by_key):
    url = li_by_key.get(domain) or li_by_key.get(name.lower())
    if url:
        return url
    if domain:
        r = post("/v2/enrichment/domain-to-linkedin", {"domain": domain})
        if isinstance(r, dict) and r.get("company_linkedin_url"):
            return r["company_linkedin_url"]
    r = post("/v2/search/companies", {
        "company": {"name": {"include": [name]}, "hq": {"country_code": ["US"]}},
        "max_results": 3})
    res = (r or {}).get("results") or []
    return res[0].get("linkedin_url", "") if res else ""


def waterfall(url, titles, n):
    return post("/v2/search/waterfall-icp-keyword", {
        "company_linkedin_url": url,
        "cascade": [{"include_title": titles, "exclude_title": EXCL,
                     "location": ["WORLD"], "include_headline_search": True}],
        "max_results": n})


def process_company(row, li_by_key):
    name, domain = row["company"], norm_domain(row.get("domain", ""))
    url = resolve_company(name, domain, li_by_key)
    people, seen = [], set()
    if url:
        for titles, bucket in ((CEO_TIER, "ceo"), (CTO_TIER, "cto")):
            resp = waterfall(url, titles, 2)
            for x in (resp.get("results") or []):
                p = x.get("person", {})
                li = p.get("linkedin_url")
                if not li or li in seen:
                    continue
                seen.add(li)
                exps = p.get("experiences", []) or []
                cur = next((e for e in exps if e.get("job_is_current")),
                           exps[0] if exps else {})
                full = p.get("full_name", "")
                people.append({
                    "company_name": name, "slug": row.get("slug", ""),
                    "domain": domain, "role_bucket": bucket,
                    "full_name": full,
                    "first_name": p.get("first_name", "") or (full.split() or [""])[0],
                    "last_name": p.get("last_name", "") or " ".join(full.split()[1:]),
                    "title": cur.get("job_title") or p.get("headline", ""),
                    "headline": p.get("headline", ""),
                    "location": p.get("location", ""),
                    "linkedin_url": li,
                })
    return {"_company": name, "company_linkedin_url": url, "people": people}


def main():
    load_env()
    top_n = TOP_N
    if "--top" in sys.argv:
        top_n = int(sys.argv[sys.argv.index("--top") + 1])
    rows = list(csv.DictReader(open(IN, encoding="utf-8")))[:top_n]
    li_by_key = {}
    for r in read_jsonl(VERIFY):
        if r.get("linkedin_url"):
            if r.get("domain"):
                li_by_key[r["domain"]] = r["linkedin_url"]
            li_by_key[r.get("name", "").lower()] = r["linkedin_url"]

    done = {r["_company"] for r in read_jsonl(JL)}
    todo = [r for r in rows if r["company"] not in done]
    print(f"top {top_n} companies; {len(done)} done, {len(todo)} to pull")

    lock = threading.Lock()
    JL.parent.mkdir(parents=True, exist_ok=True)
    with open(JL, "a") as fh, ThreadPoolExecutor(max_workers=10) as ex:
        futs = [ex.submit(process_company, r, li_by_key) for r in todo]
        for i, fut in enumerate(as_completed(futs), 1):
            rec = fut.result()
            with lock:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
            if i % 10 == 0:
                print(f"  …{i}/{len(todo)}")

    wanted = {r["company"] for r in rows}
    out_rows = []
    for rec in read_jsonl(JL):
        if rec["_company"] not in wanted:
            continue
        for p in rec["people"]:
            p["company_linkedin_url"] = rec.get("company_linkedin_url", "")
            out_rows.append(p)
    OUT.parent.mkdir(exist_ok=True)
    if out_rows:
        with open(OUT, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()),
                               extrasaction="ignore")
            w.writeheader()
            w.writerows(out_rows)
    no_people = [rec["_company"] for rec in read_jsonl(JL)
                 if rec["_company"] in wanted and not rec["people"]]
    print(f"{len(out_rows)} people across {len(wanted) - len(no_people)} companies "
          f"-> {OUT}\ncompanies with none found ({len(no_people)}): "
          f"{', '.join(no_people[:15])}{'…' if len(no_people) > 15 else ''}")


if __name__ == "__main__":
    main()
