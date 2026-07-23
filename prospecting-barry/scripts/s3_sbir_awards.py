#!/usr/bin/env python3
"""Channel C: DoD SBIR/STTR Phase II awardees (2022+) from the SBIR.gov bulk CSV.

The SBIR.gov public API is offline ("The SBIR Public API is not available at this
time", checked 2026-07-23), so this reads the official bulk export instead:
  https://data.www.sbir.gov/awarddatapublic/award_data.csv  (~367MB, gitignored)

Phase II ≈ "has a working prototype, faces the valley of death" — Barry's exact EDP.
Filters: DoD agency, Phase II, award year >= 2022, title+abstract matched against
a domain lexicon derived from Barry's signal_spec. Flags SBIR mills (>8 awards in
window). Keeps abstracts — they are the company's own lab-language and prime
disconnect evidence for Stage-4 agents.

Output: checkpoints/sbir_awards.jsonl (one record per firm, awards nested).
Usage: python3 s3_sbir_awards.py
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, norm_domain  # noqa: E402

CSV_PATH = ROOT / "data" / "sbir_award_data.csv"
OUT = ROOT / "checkpoints" / "sbir_awards.jsonl"

MIN_YEAR = 2022
MILL_THRESHOLD = 8

# Domain lexicon from prospecting-ctox/dossiers/barry-hess/signal_spec.json
# (mobile / sensors / data collection / AI-ML / cyber). Word-boundary matched.
LEXICON = [
    "ATAK", "TAK server", "tactical edge", "edge computing", "edge AI",
    "mobile app", "Android", "situational awareness", "mission planning",
    "sensor", "unattended ground", "wearable", "RF sensing", "spectrum sensing",
    "data collection", "field data", "telemetry",
    "machine learning", "computer vision", "artificial intelligence",
    "deep learning", "neural network", "anomaly detection", "object detection",
    "ISR", "C2", "command and control", "geospatial", "GEOINT",
    "cybersecurity", "cyber security", "cross-domain", "zero trust",
    "network security", "UAS", "unmanned", "drone", "counter-UAS",
]
LEX_RE = [(t, re.compile(r"(?<![a-z0-9])" + re.escape(t.lower()) + r"(?![a-z0-9])"))
          for t in LEXICON]

RI_RE = re.compile(r"universit|college|institute of technology|\bstate u\b|research foundation",
                   re.I)


def lex_hits(text):
    t = (text or "").lower()
    return [term for term, rx in LEX_RE if rx.search(t)]


def main():
    if not CSV_PATH.exists():
        sys.exit(f"missing {CSV_PATH} — download the bulk CSV first (see docstring)")
    csv.field_size_limit(10_000_000)
    firms = defaultdict(lambda: {"awards": [], "all_award_count": 0})
    n_rows = 0
    with open(CSV_PATH, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        cols = {c.lower().strip(): c for c in reader.fieldnames}

        def col(row, *names):
            for n in names:
                c = cols.get(n)
                if c and row.get(c):
                    return row[c].strip()
            return ""

        for row in reader:
            n_rows += 1
            agency = col(row, "agency")
            if "defense" not in agency.lower() and agency.upper() != "DOD":
                continue
            company = col(row, "company")
            if not company or RI_RE.search(company):
                continue
            key = re.sub(r"[^a-z0-9]", "", company.lower())[:40]
            firms[key]["all_award_count"] += 1
            phase = col(row, "phase")
            if phase.strip().lower() not in ("phase ii", "ii", "2"):
                continue
            try:
                year = int(col(row, "award year", "award_year") or 0)
            except ValueError:
                year = 0
            if year < MIN_YEAR:
                continue
            title = col(row, "award title", "award_title")
            abstract = col(row, "abstract")
            hits = lex_hits(title + " " + abstract)
            if not hits:
                continue
            firms[key].setdefault("company", company)
            firms[key].setdefault("website", norm_domain(col(row, "company website", "company_website")))
            firms[key].setdefault("city", col(row, "city"))
            firms[key].setdefault("state", col(row, "state"))
            firms[key].setdefault("uei", col(row, "uei"))
            firms[key].setdefault("employees", col(row, "number employees", "number_employees"))
            firms[key]["awards"].append({
                "title": title, "phase": phase,
                "branch": col(row, "branch"), "year": year,
                "amount": col(row, "award amount", "award_amount"),
                "lexicon_hits": hits,
                "abstract": abstract[:4000],
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    kept = 0
    with open(OUT, "w", encoding="utf-8") as f:
        for key, rec in firms.items():
            if not rec["awards"]:
                continue
            rec["sbir_mill"] = rec["all_award_count"] > MILL_THRESHOLD
            rec["source"] = "sbir"
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            kept += 1
    mills = sum(1 for r in firms.values() if r["awards"] and r["all_award_count"] > MILL_THRESHOLD)
    print(f"rows scanned: {n_rows:,}; DoD PhII 2022+ lexicon-matched firms: {kept} "
          f"(of which {mills} flagged sbir_mill)")


if __name__ == "__main__":
    main()
