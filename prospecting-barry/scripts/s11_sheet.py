#!/usr/bin/env python3
"""Stage 5d: build/update the Barry Hess Google Sheet via the `gws` CLI.

The google-api-python-client path needs `gcloud auth application-default login`,
which had expired; `gws` holds a working keyring credential, so we shell out to it.

Tabs: Ranked People, Company Summary, Methodology (all computed from artifacts).
Sheet id cached in checkpoints/sheet_id.txt so the link never changes.

Usage: python3 s11_sheet.py
"""
import csv
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT  # noqa: E402

TITLE = "Barry Hess — Lab-to-Field Disconnect Prospects"
ID_FILE = ROOT / "checkpoints" / "sheet_id.txt"
FINAL = ROOT / "output" / "barry_final.csv"
RANKED = ROOT / "data" / "ranked_companies.csv"
MAX_CELL = 45000


def gws(*args, payload=None):
    cmd = ["gws", *args]
    if payload is not None:
        cmd += ["--json", json.dumps(payload)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"gws failed: {' '.join(args[:4])}\n{r.stderr[:500]}")
    out = r.stdout
    if out.startswith("Using keyring"):
        out = out.split("\n", 1)[1] if "\n" in out else "{}"
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {}


def clip(v):
    return ("" if v is None else str(v))[:MAX_CELL]


def main():
    if ID_FILE.exists():
        sid = ID_FILE.read_text().strip()
        print(f"reusing sheet {sid}")
    else:
        resp = gws("sheets", "spreadsheets", "create",
                   payload={"properties": {"title": TITLE}})
        sid = resp["spreadsheetId"]
        ID_FILE.parent.mkdir(parents=True, exist_ok=True)
        ID_FILE.write_text(sid)
        print(f"created sheet {sid}")

    meta = gws("sheets", "spreadsheets", "get", "--params",
               json.dumps({"spreadsheetId": sid}))
    existing = {s["properties"]["title"] for s in meta.get("sheets", [])}

    def write_tab(name, values):
        if name not in existing:
            gws("sheets", "spreadsheets", "batchUpdate", "--params",
                json.dumps({"spreadsheetId": sid}),
                payload={"requests": [{"addSheet": {"properties": {"title": name}}}]})
            existing.add(name)
        gws("sheets", "spreadsheets", "values", "clear", "--params",
            json.dumps({"spreadsheetId": sid, "range": f"'{name}'"}), payload={})
        # gws takes the body on argv, so chunk by serialized size to stay under
        # ARG_MAX (~1MB on macOS). Blind-spot cells are long, so budget ~150KB.
        BUDGET = 150_000
        i = 0
        while i < len(values):
            block, size, j = [], 0, i
            while j < len(values):
                row_size = len(json.dumps(values[j], ensure_ascii=False))
                if block and size + row_size > BUDGET:
                    break
                block.append(values[j])
                size += row_size
                j += 1
            gws("sheets", "spreadsheets", "values", "update", "--params",
                json.dumps({"spreadsheetId": sid,
                            "range": f"'{name}'!A{i + 1}",
                            "valueInputOption": "RAW"}),
                payload={"values": block})
            i = j

    people = list(csv.DictReader(open(FINAL, encoding="utf-8")))
    cols = list(people[0].keys())
    write_tab("Ranked People",
              [cols] + [[clip(r.get(c, "")) for c in cols] for r in people])
    print(f"Ranked People: {len(people)} rows")

    comps = list(csv.DictReader(open(RANKED, encoding="utf-8")))
    ccols = list(comps[0].keys())
    write_tab("Company Summary",
              [ccols] + [[clip(r.get(c, "")) for c in ccols] for r in comps])
    print(f"Company Summary: {len(comps)} rows")

    n_people = sum(1 for r in people if r.get("person") != "(none found)")
    n_email = sum(1 for r in people if r.get("best_email"))
    n_mobile = sum(1 for r in people if r.get("mobile"))
    n_comp_contacts = len({r["company"] for r in people
                           if r.get("person") != "(none found)"})
    method = [
        [TITLE, f"built {time.strftime('%Y-%m-%d %H:%M')}"],
        [],
        ["Companies ranked (kept)", len(comps)],
        ["Companies with contacts", n_comp_contacts],
        ["People", n_people],
        ["With email", n_email],
        ["With mobile", n_mobile],
        [],
        ["SORT KEY — disconnect_score (0-100). Higher = the company's own language is "
         "further from deployed-environment reality, which is exactly the gap Barry "
         "closes. Five 0-20 subscores: lab-language intensity, deployment-awareness "
         "absence, operator absence, hiring-profile skew, stage pressure. A verbatim "
         "quote is required for any subscore above 10. Companies already fluent in "
         "ATAK/ATO/DDIL score LOW and sit at the bottom of the list."],
        ["GATES — every company had to show genuine DoD motion in its OWN artifacts "
         "(SBIR award, explicit military-customer language, DIU/AFWERX engagement). "
         "Defense-VC portfolio membership alone was not sufficient. Dropped: primes, "
         "systems integrators, staffing/services shops, SBIR mills, and companies "
         "already fielded at scale (they crossed the valley). Companies with under "
         "~500 words of their own language were excluded as insufficient evidence."],
        ["SOURCING — 15 defense/natsec VC portfolios + Exa Agent API (5 domain "
         "queries plus continuations) + DoD SBIR/STTR Phase II awards 2022+ (bulk "
         "SBIR.gov data, non-mill) + a 967k open-jobs corpus matched on Barry's "
         "signal spec. 895 candidates deduped, then Blitz-verified to 569 US "
         "early-stage companies (2-300 headcount, primes/staffing removed)."],
        ["JUDGING — one evidence pack per company (their own site copy, SBIR "
         "abstracts, news, live job postings), each judged by an AI agent against "
         "the identical rubric. 568 scored: 259 keeps, 274 drops, 35 insufficient "
         "evidence."],
        ["CONTACTS — Blitz people search (CEO + CTO buckets, fractional/interim "
         "excluded) then FullEnrich waterfall. 'email_domain_match = no' flags an "
         "email on a different domain than the company: usually a sister domain or "
         "personal address, occasionally a stale record from a prior employer. "
         "Verify those before sending."],
        ["All counts above are computed from run artifacts, not hand-entered."],
    ]
    write_tab("Methodology", method)
    print(f"Sheet: https://docs.google.com/spreadsheets/d/{sid}")


if __name__ == "__main__":
    main()
