# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""s6 — find 2-5 buyers per kept company via Blitz waterfall-ICP.

In : research/companies/<cto>/*.json  (Wave B agent verdicts; verdict=="keep")
Out: checkpoints/people/<cto>.jsonl (resumable) + output/<cto>_people.csv

Usage: python3 s6_blitz_people.py <cto-slug> [<cto-slug> ...]
"""
import csv
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_common import OUTPUT, RESEARCH, checkpoint_path, http_json, key, read_jsonl, say

BLITZ = "https://api.blitz-api.ai"
EXCL = ["fractional", "interim", "advisor", "assistant", "intern", "junior",
        "former", "consultant", "retired"]
DM_TIER = ["Chief Executive Officer", "CEO", "President", "Founder", "Co-Founder",
           "Owner", "Chief Operating Officer", "COO"]
PRODUCT_TIER = ["Chief Product Officer", "VP Product", "VP of Product",
                "Head of Product", "Chief Financial Officer", "CFO",
                "VP Engineering", "VP of Engineering", "Head of Engineering",
                "Director of Engineering"]


def post(path, body):
    try:
        return http_json(BLITZ + path, body,
                         {"x-api-key": key("BLITZ_API_KEY")}, retries=2, timeout=45)
    except RuntimeError as e:
        return {"_error": str(e)[:200]}


def resolve_company(name, domain):
    if domain:
        r = post("/v2/enrichment/domain-to-linkedin", {"domain": domain})
        if isinstance(r, dict) and r.get("company_linkedin_url"):
            return r["company_linkedin_url"]
    r = post("/v2/search/companies", {
        "company": {"name": {"include": [name]}, "hq": {"country_code": ["US"]}},
        "max_results": 3})
    res = (r or {}).get("results") or []
    return res[0].get("linkedin_url", "") if res else ""


def waterfall(url, tiers, n):
    return post("/v2/search/waterfall-icp-keyword", {
        "company_linkedin_url": url,
        "cascade": [{"include_title": t, "exclude_title": EXCL,
                     "location": ["WORLD"], "include_headline_search": True}
                    for t in tiers],
        "max_results": n})


def process_company(rec):
    comp = rec["company"]
    url = resolve_company(comp.get("name", ""), comp.get("domain", ""))
    people, seen = [], set()
    if url:
        spec_titles = [p for p in rec.get("people_spec", []) if isinstance(p, str)]
        tier1 = DM_TIER
        tier2 = (spec_titles or []) + PRODUCT_TIER
        for tiers, n, bucket in ((tier1, 2, "decision_maker"),
                                 ([tier2], 3, "tech_product")):
            resp = waterfall(url, [tiers] if bucket == "decision_maker" else tiers if isinstance(tiers[0], list) else [tiers], n)
            for x in (resp.get("results") or []):
                p = x.get("person", {})
                li = p.get("linkedin_url")
                if not li or li in seen:
                    continue
                seen.add(li)
                exps = p.get("experiences", []) or []
                cur = next((e for e in exps if e.get("job_is_current")),
                           exps[0] if exps else {})
                people.append({
                    "company_name": comp.get("name", ""),
                    "domain": comp.get("domain", ""),
                    "role_bucket": bucket,
                    "full_name": p.get("full_name", ""),
                    "first_name": p.get("first_name", "") or (p.get("full_name", "").split() or [""])[0],
                    "last_name": p.get("last_name", "") or " ".join(p.get("full_name", "").split()[1:]),
                    "title": cur.get("job_title") or p.get("headline", ""),
                    "headline": p.get("headline", ""),
                    "location": p.get("location", ""),
                    "linkedin_url": li,
                })
                if len(people) >= 5:
                    break
            if len(people) >= 5:
                break
    return {"_company": comp.get("name", ""), "company_linkedin_url": url,
            "people": people}


def run_cto(slug):
    keeps = []
    cdir = RESEARCH / slug
    for f in sorted(cdir.glob("*.json")):
        try:
            rec = json.loads(f.read_text())
        except Exception:
            continue
        if rec.get("verdict") == "keep":
            keeps.append(rec)
    if not keeps:
        say(f"{slug}: no kept companies yet")
        return

    jl = checkpoint_path("people", f"{slug}.jsonl")
    done = {r["_company"] for r in read_jsonl(jl)}
    todo = [r for r in keeps if r["company"].get("name", "") not in done]
    say(f"{slug}: {len(keeps)} kept companies, {len(done)} done, {len(todo)} to pull")

    lock = threading.Lock()
    with open(jl, "a") as fh, ThreadPoolExecutor(max_workers=10) as ex:
        futs = [ex.submit(process_company, r) for r in todo]
        for i, fut in enumerate(as_completed(futs), 1):
            rec = fut.result()
            with lock:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
            if i % 10 == 0:
                say(f"  …{i}/{len(todo)} companies processed")

    rows = []
    for rec in read_jsonl(jl):
        for p in rec["people"]:
            p["company_linkedin_url"] = rec.get("company_linkedin_url", "")
            rows.append(p)
    OUTPUT.mkdir(exist_ok=True)
    out = OUTPUT / f"{slug}_people.csv"
    if rows:
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
    say(f"{slug}: {len(rows)} people across {len(read_jsonl(jl))} companies -> {out.name}")


def main():
    for slug in sys.argv[1:]:
        run_cto(slug)


if __name__ == "__main__":
    main()
