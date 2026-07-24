#!/usr/bin/env python3
"""Stage 5c: assemble the final deliverable — one row per person, companies sorted
by disconnect_score (most lab-blind first).
Out: output/barry_final.csv (with mobiles) + output/barry_final_public.csv (without)
Usage: python3 s10_assemble.py [--qa]
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, read_jsonl  # noqa: E402

RANKED = ROOT / "data" / "ranked_companies.csv"
PEOPLE = ROOT / "output" / "people.csv"
ENRICH = ROOT / "checkpoints" / "enrich.jsonl"
OUT = ROOT / "output" / "barry_final.csv"
OUT_PUB = ROOT / "output" / "barry_final_public.csv"


def bs_text(raw):
    try:
        b = json.loads(raw)
        return f"{b.get('blind_spot','')} — {b.get('operator_reality','')} " \
               f"[quote: \"{b.get('evidence_quote','')}\" ({b.get('quote_source','')})]"
    except Exception:
        return raw or ""


def main():
    qa = "--qa" in sys.argv
    ranked = list(csv.DictReader(open(RANKED, encoding="utf-8")))
    people = list(csv.DictReader(open(PEOPLE, encoding="utf-8"))) if PEOPLE.exists() else []
    fe = {r["linkedin_url"]: r for r in read_jsonl(ENRICH)}

    by_company = {}
    for p in people:
        by_company.setdefault(p["company_name"], []).append(p)

    rows = []
    for c in ranked:
        plist = by_company.get(c["company"], [])
        base = {
            "rank": c["rank"], "disconnect_score": c["disconnect_score"],
            "company": c["company"], "domain": c["domain"],
            "what_they_do": c["what_they_do"], "stage_band": c["stage_band"],
            "confidence": c["confidence"],
            "dod_evidence": c["dod_intent_evidence"],
            "blind_spot_1": bs_text(c.get("blind_spot_1")),
            "blind_spot_2": bs_text(c.get("blind_spot_2")),
            "blind_spot_3": bs_text(c.get("blind_spot_3")),
            "opener_hook": c.get("opener_hook", ""),
        }
        if not plist:
            rows.append({**base, "person": "(none found)", "role": "", "title": "",
                         "best_email": "", "all_emails": "", "mobile": "",
                         "email_domain_match": "",
                         "person_linkedin": "", "location": ""})
        for p in plist:
            e = fe.get(p["linkedin_url"], {})
            rows.append({**base,
                         "person": p["full_name"], "role": p["role_bucket"],
                         "title": p["title"],
                         "best_email": e.get("fe_email", ""),
                         "all_emails": e.get("fe_all_emails", ""),
                         "mobile": e.get("fe_phone", ""),
                         "email_domain_match": e.get("email_domain_match", ""),
                         "person_linkedin": p["linkedin_url"],
                         "location": p.get("location", "")})

    cols = ["rank", "disconnect_score", "company", "domain", "what_they_do",
            "stage_band", "confidence", "dod_evidence", "person", "role", "title",
            "best_email", "all_emails", "mobile", "email_domain_match",
            "person_linkedin", "location",
            "blind_spot_1", "blind_spot_2", "blind_spot_3", "opener_hook"]
    OUT.parent.mkdir(exist_ok=True)
    for path, strip in ((OUT, False), (OUT_PUB, True)):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=[c for c in cols
                                              if not (strip and c in ("mobile",))],
                               extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow({k: v for k, v in r.items()
                            if not (strip and k == "mobile")})
    n_people = sum(1 for r in rows if r["person"] != "(none found)")
    n_email = sum(1 for r in rows if r.get("best_email"))
    n_mobile = sum(1 for r in rows if r.get("mobile"))
    print(f"{len(ranked)} companies, {n_people} people, {n_email} emails "
          f"({n_email * 100 // max(n_people, 1)}%), {n_mobile} mobiles "
          f"({n_mobile * 100 // max(n_people, 1)}%) -> {OUT}")

    if qa:
        problems = []
        seen = set()
        for r in rows:
            k = (r["company"], r["person"])
            if k in seen:
                problems.append(f"dup row: {k}")
            seen.add(k)
            if r.get("best_email") and r.get("domain"):
                dom = r["best_email"].split("@")[-1].lower()
                if dom and r["domain"] not in dom and dom not in r["domain"]:
                    problems.append(f"email-domain mismatch: {r['person']} "
                                    f"{r['best_email']} vs {r['domain']}")
            if int(r["disconnect_score"]) > 50 and not any(
                    r.get(f"blind_spot_{i}") for i in (1, 2, 3)):
                problems.append(f"{r['company']}: high score, no blind spots")
        top100 = {c["company"] for c in ranked[:100]}
        no_person = {r["company"] for r in rows
                     if r["person"] == "(none found)" and r["company"] in top100}
        print(f"QA: {len(problems)} problems; top-100 companies without any person: "
              f"{len(no_person)}")
        for p in problems[:20]:
            print(" -", p)


if __name__ == "__main__":
    main()
