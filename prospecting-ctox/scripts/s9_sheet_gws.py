# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""s9 (gws variant) — build the cohort Google Sheet via the authenticated `gws` CLI.

Same output as s9_google_sheet.py but uses Jordan's existing gws credential
instead of Google ADC (which needs a browser reauth). Re-runnable: the sheet id
is cached in checkpoints/sheet_id.txt so the link stays stable.

Usage: python3 s9_sheet_gws.py
"""
import csv
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_common import CHECKPOINTS, DOSSIERS, OUTPUT, load_ctos, say

TITLE = "CTOx Cohort — Live-Signal Target Lists"
ID_FILE = CHECKPOINTS / "sheet_id.txt"


def gws(*args, params=None, body=None):
    cmd = ["gws", *args]
    if params is not None:
        cmd += ["--params", json.dumps(params)]
    if body is not None:
        cmd += ["--json", json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gws failed: {r.stderr[:400]}")
    out = r.stdout.strip()
    # gws prints a keyring notice line before the JSON body
    brace = out.find("{")
    return json.loads(out[brace:]) if brace >= 0 else {}


def main():
    ctos = load_ctos()

    if ID_FILE.exists():
        sid = ID_FILE.read_text().strip()
        say(f"Updating existing sheet {sid}")
    else:
        resp = gws("sheets", "spreadsheets", "create",
                   body={"properties": {"title": TITLE}})
        sid = resp["spreadsheetId"]
        ID_FILE.parent.mkdir(parents=True, exist_ok=True)
        ID_FILE.write_text(sid)
        say(f"Created sheet {sid}")

    meta = gws("sheets", "spreadsheets", "get", params={"spreadsheetId": sid})
    existing = {s["properties"]["title"] for s in meta.get("sheets", [])}

    summary = [["CTOx Cohort — Live-Signal Target Lists",
                f"built {time.strftime('%Y-%m-%d %H:%M')}"],
               [],
               ["CTO", "Niche", "Companies", "People", "With Email",
                "With Mobile", "Live-verified jobs", "Status"]]

    def write_tab(name, values):
        if name not in existing:
            gws("sheets", "spreadsheets", "batchUpdate",
                params={"spreadsheetId": sid},
                body={"requests": [{"addSheet": {"properties": {"title": name}}}]})
            existing.add(name)
        gws("sheets", "spreadsheets", "values", "clear",
            params={"spreadsheetId": sid, "range": f"'{name}'"}, body={})
        gws("sheets", "spreadsheets", "values", "update",
            params={"spreadsheetId": sid, "range": f"'{name}'!A1",
                    "valueInputOption": "RAW"},
            body={"values": values})

    for cto in ctos:
        slug, name = cto["slug"], cto["name"]
        final = OUTPUT / f"{slug}_final.csv"
        niche = ""
        spec_f = DOSSIERS / slug / "signal_spec.json"
        if spec_f.exists():
            try:
                niche = json.loads(spec_f.read_text()).get("niche_statement", "")
            except Exception:
                pass
        if not final.exists():
            summary.append([name, niche, 0, 0, 0, 0, 0, "no qualifying companies yet"])
            continue
        rows = list(csv.DictReader(open(final)))
        if not rows:
            summary.append([name, niche, 0, 0, 0, 0, 0, "no qualifying companies"])
            continue
        cols = list(rows[0].keys())
        summary.append([
            name, niche,
            len({r["Company"] for r in rows}), len(rows),
            sum(1 for r in rows if r["Best Email"]),
            sum(1 for r in rows if r["Mobile"]),
            sum(1 for r in rows if r["Live Job URL"]), "done"])
        write_tab(name, [cols] + [[r.get(c, "") for c in cols] for r in rows])
        say(f"tab written: {name} ({len(rows)} people rows)")

    summary += [[], [
        "Method: matched against the open-jobs dataset (~947k open postings across 16 hiring "
        "systems, CC0), gated to each person's vertical, scored on expertise-signal embeddings "
        "plus exact phrases; every listed job re-verified against the company's own live careers "
        "feed on the 'Job Verified' date; contacts via Blitz + FullEnrich. Every count above is "
        "computed from the run's own files, not typed by hand."]]
    write_tab("Summary", summary)
    say(f"Sheet: https://docs.google.com/spreadsheets/d/{sid}")


if __name__ == "__main__":
    main()
