#!/usr/bin/env python3
"""Stage 5: assemble the final ranked universe.

Joins: universe_verified.csv + pain_signals.jsonl + briefs.jsonl (subagent
research) + contacts.jsonl + contact_emails.jsonl + fullenrich.jsonl.

Pain score (0-100):
  ops_gap        0-40  (Blitz team composition: senior eng present, no ops roles)
  hiring_signal  0-10  (open DevOps/build/IT reqs = acknowledged pain; eng scaling)
  milestone      0-30  (brief agents: funding cycle position, publisher milestones,
                        runway pressure)
  launch_prox    0-15  (brief agents: production phase / launch window)
  size_fit       0-5

Output: output/ben_universe_ranked.csv, output/contacts_ranked.csv

Usage: python3 s7_assemble.py
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, read_jsonl  # noqa: E402

CK = ROOT / "checkpoints"
OUTD = ROOT / "output"


def score_ops(sig):
    if not sig or sig.get("people_err"):
        return 10, "unknown team composition"
    senior, ops = sig.get("senior_eng_count", 0), sig.get("ops_people_count", 0)
    eng = sig.get("eng_people_found", 0)
    if eng == 0:
        return 10, "no engineers visible on LinkedIn"
    if ops == 0 and senior >= 2:
        return 40, f"{senior} senior eng leaders, ZERO dedicated ops roles"
    if ops == 0 and senior >= 1:
        return 32, f"{senior} senior eng leader(s), zero dedicated ops roles"
    if ops == 0:
        return 24, f"{eng} engineers, zero dedicated ops roles"
    if ops == 1:
        return 20, f"single point of failure: 1 ops person ({sig.get('ops_titles','')})"
    return 6, f"{ops} ops people present"


def score_hiring(sig):
    if not sig or sig.get("jobs_err"):
        return 0, ""
    s, why = 0, []
    if sig.get("ops_jobs", 0) > 0:
        s += 8
        why.append(f"hiring ops roles now: {sig.get('ops_job_titles','')}")
    if sig.get("eng_jobs", 0) >= 3:
        s += 2
        why.append(f"{sig['eng_jobs']} open eng reqs (scaling)")
    return min(s, 10), "; ".join(why)


def size_fit(n):
    if n is None:
        return 0
    if 20 <= n <= 150:
        return 5
    if 12 <= n < 20 or 150 < n <= 200:
        return 2
    return 0


def main():
    verified = {r["linkedin_url"]: r
                for r in csv.DictReader(open(ROOT / "data" / "universe_verified.csv",
                                             encoding="utf-8"))}
    sigs = {r["linkedin_url"]: r for r in read_jsonl(CK / "pain_signals.jsonl")}
    briefs = {}
    for r in read_jsonl(CK / "briefs.jsonl"):
        briefs[r.get("linkedin_url") or r.get("domain")] = r
    contacts = {r["linkedin_url"]: r for r in read_jsonl(CK / "contacts.jsonl")}
    emails = {r["person_linkedin"]: r for r in read_jsonl(CK / "contact_emails.jsonl")}
    fe = {r["linkedin_url"]: r for r in read_jsonl(CK / "fullenrich.jsonl")}

    rows, contact_rows = [], []
    for li, v in verified.items():
        b = briefs.get(li) or briefs.get(v["domain"]) or {}
        if b.get("fit_verdict") == "disqualify":
            continue
        sig = sigs.get(li)
        emp = int(v.get("employees_on_linkedin") or 0) or None
        ops_s, ops_why = score_ops(sig)
        hir_s, hir_why = score_hiring(sig)
        mil_s = int(b.get("milestone_pressure") or 0)
        lau_s = int(b.get("launch_proximity") or 0)
        siz_s = size_fit(emp)
        total = ops_s + hir_s + mil_s + lau_s + siz_s
        rows.append({
            "pain_score": total, "company": v["name"], "domain": v["domain"],
            "employees": emp, "hq": f"{v.get('hq_city','')}, {v.get('hq_state','')}",
            "founded": v.get("founded_year"),
            "ops_gap_score": ops_s, "ops_gap_why": ops_why,
            "hiring_score": hir_s, "hiring_why": hir_why,
            "milestone_score": mil_s, "milestone_why": b.get("milestone_why", ""),
            "launch_score": lau_s, "launch_why": b.get("launch_why", ""),
            "size_fit": siz_s,
            "fit_verdict": b.get("fit_verdict", "unresearched"),
            "game": b.get("game_title", ""), "game_status": b.get("game_status", ""),
            "total_raised": b.get("total_raised", ""),
            "last_round": b.get("last_round", ""),
            "investors": b.get("investors", ""),
            "senior_eng_titles": (sig or {}).get("senior_eng_titles", ""),
            "linkedin_url": li, "sources": v.get("sources", ""),
            "brief": b.get("brief_md", ""),
        })
        for p in (contacts.get(li) or {}).get("contacts") or []:
            pl = p.get("person_linkedin")
            em = (emails.get(pl) or {}).get("email") or ""
            if not em:
                fe_r = fe.get(pl) or {}
                em = next((e for e in (fe_r.get("emails") or []) if e), "")
            contact_rows.append({
                "pain_score": total, "company": v["name"], "domain": v["domain"],
                "full_name": p.get("full_name"), "title": p.get("title"),
                "email": em, "person_linkedin": pl,
                "tier": p.get("tier"), "location": str(p.get("location") or ""),
                "start_date": p.get("start_date", "")})

    rows.sort(key=lambda r: -r["pain_score"])
    contact_rows.sort(key=lambda r: (-r["pain_score"], r["company"]))
    OUTD.mkdir(parents=True, exist_ok=True)
    with open(OUTD / "ben_universe_ranked.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(OUTD / "contacts_ranked.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(contact_rows[0].keys()))
        w.writeheader()
        w.writerows(contact_rows)
    print(f"companies: {len(rows)}; contacts: {len(contact_rows)}; "
          f"emails: {sum(1 for c in contact_rows if c['email'])}")
    print(f"-> {OUTD}/ben_universe_ranked.csv, contacts_ranked.csv")


if __name__ == "__main__":
    main()
