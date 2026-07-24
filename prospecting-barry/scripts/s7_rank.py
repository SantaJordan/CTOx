#!/usr/bin/env python3
"""Stage 4b: collect agent verdicts, validate, rank keeps by disconnect_score.
Output: data/ranked_companies.csv + sanity stats.
Usage: python3 s7_rank.py
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT  # noqa: E402

VERDICTS = ROOT / "research" / "verdicts"
OUT = ROOT / "data" / "ranked_companies.csv"

SUBS = ["lab_language_intensity", "deployment_awareness_absence",
        "operator_absence", "hiring_profile_skew", "stage_pressure"]
STAGE_ORDER = {"preseed_seed": 0, "series_a": 1, "revenue_stage": 2, "unknown": 3}


def main():
    rows, problems = [], []
    statuses = Counter()
    for p in sorted(VERDICTS.glob("*.json")):
        try:
            v = json.loads(p.read_text())
        except json.JSONDecodeError as e:
            problems.append(f"{p.name}: bad json ({e})")
            continue
        verdict = v.get("verdict")
        statuses[verdict or "missing"] += 1
        if verdict != "keep":
            continue
        subs = v.get("subscores") or {}
        total = sum(int(subs.get(k) or 0) for k in SUBS)
        declared = int(v.get("disconnect_score") or 0)
        if abs(total - declared) > 2:
            problems.append(f"{p.name}: score mismatch declared={declared} sum={total}")
        score = total
        for k in SUBS:
            s = int(subs.get(k) or 0)
            if not (0 <= s <= 20):
                problems.append(f"{p.name}: subscore {k}={s} out of range")
        bs = v.get("blind_spots") or []
        if len(bs) != 3:
            problems.append(f"{p.name}: {len(bs)} blind_spots (want 3)")
        if score > 50 and not any((b.get("evidence_quote") or "").strip() for b in bs):
            problems.append(f"{p.name}: score {score} with no evidence quotes")
        rows.append({
            "slug": v.get("slug") or p.stem, "company": v.get("company", ""),
            "domain": v.get("domain", ""), "disconnect_score": score,
            **{k: int(subs.get(k) or 0) for k in SUBS},
            "stage_band": v.get("stage_band", "unknown"),
            "confidence": v.get("confidence", ""),
            "what_they_do": v.get("what_they_do", ""),
            "dod_intent_evidence": v.get("dod_intent_evidence", ""),
            "blind_spot_1": json.dumps(bs[0], ensure_ascii=False) if len(bs) > 0 else "",
            "blind_spot_2": json.dumps(bs[1], ensure_ascii=False) if len(bs) > 1 else "",
            "blind_spot_3": json.dumps(bs[2], ensure_ascii=False) if len(bs) > 2 else "",
            "opener_hook": v.get("opener_hook", ""),
        })

    rows.sort(key=lambda r: (-r["disconnect_score"],
                             STAGE_ORDER.get(r["stage_band"], 3),
                             r["company"].lower()))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = ["rank", "disconnect_score", "company", "slug", "domain", "stage_band",
            "confidence", "what_they_do", "dod_intent_evidence"] + SUBS + \
           ["blind_spot_1", "blind_spot_2", "blind_spot_3", "opener_hook"]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    print(f"verdicts: {dict(statuses)}")
    if rows:
        scores = [r["disconnect_score"] for r in rows]
        print(f"keeps ranked: {len(rows)}; score min/med/max = "
              f"{min(scores)}/{sorted(scores)[len(scores)//2]}/{max(scores)}")
        hist = Counter(s // 10 * 10 for s in scores)
        print("histogram:", {f"{k}-{k+9}": hist[k] for k in sorted(hist)})
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems[:30]:
            print(" -", p)
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
