#!/usr/bin/env python3
"""Render output/BEN_LEADS.md — ranked, per-company research briefs + contacts.

Usage: python3 s8_report.py
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT  # noqa: E402

OUTD = ROOT / "output"


def main():
    rows = list(csv.DictReader(open(OUTD / "ben_universe_ranked.csv",
                                    encoding="utf-8")))
    contacts = list(csv.DictReader(open(OUTD / "contacts_ranked.csv",
                                        encoding="utf-8")))
    by_co = {}
    for c in contacts:
        by_co.setdefault(c["company"], []).append(c)

    L = []
    L.append("# Ben Cole — Funded, Unlaunched US Game Studios, Ranked by "
             "Operational Pain\n")
    L.append("**Thesis:** funded studio (20–150), debut/flagship game NOT "
             "launched, senior engineers carrying the ops layer (builds, cloud, "
             "security, access) instead of making the game — milestone and "
             "runway pressure make it acute.\n")
    L.append(f"**Universe:** {len(rows)} qualified studios "
             f"(from 490 discovered candidates across VC portfolios, funding "
             f"news, and Exa Agent sweeps; verified via Blitz). "
             f"{sum(1 for r in rows if r['fit_verdict']=='strong')} strong / "
             f"{sum(1 for r in rows if r['fit_verdict']=='medium')} medium / "
             f"{sum(1 for r in rows if r['fit_verdict']=='weak')} weak.\n")
    L.append("**Pain score** = ops-gap (0–40, LinkedIn team composition) + "
             "hiring signal (0–10) + milestone pressure (0–30) + launch "
             "proximity (0–15) + size fit (0–5).\n\n---\n")

    for i, r in enumerate(rows, 1):
        L.append(f"\n## {i}. {r['company']} — pain {r['pain_score']}/100 "
                 f"({r['fit_verdict']})\n")
        emp = r["employees"] or "?"
        L.append(f"**{emp} staff** · {r['hq']} · founded {r['founded'] or '?'} "
                 f"· {r['domain']} · [{r['linkedin_url']}]({r['linkedin_url']})\n")
        game = r["game"] or "unannounced"
        L.append(f"**Game:** {game} ({r['game_status'] or 'unknown'}) · "
                 f"**Raised:** {r['total_raised'] or 'unknown'} · "
                 f"**Last round:** {r['last_round'] or 'unknown'}\n")
        if r["investors"]:
            L.append(f"**Investors:** {r['investors']}\n")
        L.append(f"\n**Why now (pain breakdown):**\n")
        L.append(f"- Ops gap {r['ops_gap_score']}/40 — {r['ops_gap_why']}\n")
        if r["senior_eng_titles"]:
            L.append(f"  - Senior eng carrying it: {r['senior_eng_titles']}\n")
        if r["hiring_why"]:
            L.append(f"- Hiring {r['hiring_score']}/10 — {r['hiring_why']}\n")
        L.append(f"- Milestone pressure {r['milestone_score']}/30 — "
                 f"{r['milestone_why']}\n")
        L.append(f"- Launch proximity {r['launch_score']}/15 — {r['launch_why']}\n")
        if r["brief"]:
            L.append(f"\n**Research brief:** {r['brief']}\n")
        cs = by_co.get(r["company"]) or []
        if cs:
            L.append("\n**Contacts:**\n")
            L.append("| Name | Title | Email | LinkedIn |\n|---|---|---|---|\n")
            for c in cs:
                L.append(f"| {c['full_name']} | {(c['title'] or '')[:60]} | "
                         f"{c['email'] or '—'} | {c['person_linkedin']} |\n")
        L.append("\n---\n")

    out = OUTD / "BEN_LEADS.md"
    out.write_text("".join(L), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size//1024} KB)")


if __name__ == "__main__":
    main()
