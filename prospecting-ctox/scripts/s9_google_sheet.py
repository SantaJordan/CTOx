# /// script
# requires-python = ">=3.10"
# dependencies = ["google-auth", "google-api-python-client"]
# ///
"""s9 — build/update the ONE cohort Google Sheet: Summary tab + one tab per CTO.

Each CTO tab is a people list (one row per person, company columns repeated).
Summary numbers are COMPUTED from the run artifacts, never hand-written.
Re-runnable: updates tabs in place as more CTOs finish. Sheet id cached in
checkpoints/sheet_id.txt so the link never changes.

Usage: python3 s9_google_sheet.py            (all finished CTOs)
       python3 s9_google_sheet.py <slug> ... (just these tabs)
"""
import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_common import CHECKPOINTS, DOSSIERS, OUTPUT, load_ctos, say

SA = Path.home() / ".credentials" / "gdrive_service_account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
TITLE = "CTOx Cohort — Live-Signal Target Lists"
ID_FILE = CHECKPOINTS / "sheet_id.txt"


def creds():
    if SA.exists():
        from google.oauth2 import service_account
        return service_account.Credentials.from_service_account_file(str(SA), scopes=SCOPES)
    import google.auth
    c, _ = google.auth.default(scopes=SCOPES)
    return c


def main():
    from googleapiclient.discovery import build
    cr = creds()
    sheets = build("sheets", "v4", credentials=cr, cache_discovery=False)
    drive = build("drive", "v3", credentials=cr, cache_discovery=False)

    ctos = load_ctos()
    only = set(sys.argv[1:])

    if ID_FILE.exists():
        sid = ID_FILE.read_text().strip()
    else:
        sid = sheets.spreadsheets().create(body={
            "properties": {"title": TITLE}}).execute()["spreadsheetId"]
        ID_FILE.parent.mkdir(parents=True, exist_ok=True)
        ID_FILE.write_text(sid)
        drive.permissions().create(fileId=sid, body={
            "role": "writer", "type": "anyone"}, fields="id").execute()
        say(f"Created sheet: https://docs.google.com/spreadsheets/d/{sid}")

    meta = sheets.spreadsheets().get(spreadsheetId=sid).execute()
    existing = {s["properties"]["title"]: s["properties"]["sheetId"]
                for s in meta["sheets"]}

    def ensure_tab(name):
        if name in existing:
            return existing[name]
        r = sheets.spreadsheets().batchUpdate(spreadsheetId=sid, body={
            "requests": [{"addSheet": {"properties": {"title": name}}}]}).execute()
        tid = r["replies"][0]["addSheet"]["properties"]["sheetId"]
        existing[name] = tid
        return tid

    def write_tab(name, values):
        ensure_tab(name)
        sheets.spreadsheets().values().clear(
            spreadsheetId=sid, range=f"'{name}'").execute()
        sheets.spreadsheets().values().update(
            spreadsheetId=sid, range=f"'{name}'!A1",
            valueInputOption="RAW", body={"values": values}).execute()

    summary = [["CTOx Cohort — Live-Signal Target Lists",
                f"built {time.strftime('%Y-%m-%d %H:%M')}"],
               [],
               ["CTO", "Niche", "Companies", "People", "With Email", "With Mobile",
                "Live-verified jobs", "Status"]]

    for cto in ctos:
        slug, name = cto["slug"], cto["name"]
        final = OUTPUT / f"{slug}_final.csv"
        spec_f = DOSSIERS / slug / "signal_spec.json"
        niche = ""
        if spec_f.exists():
            try:
                niche = json.loads(spec_f.read_text()).get("niche_statement", "")
            except Exception:
                pass
        if not final.exists():
            summary.append([name, niche, "", "", "", "", "", "in progress"])
            continue
        rows = list(csv.DictReader(open(final)))
        n_comp = len({r["Company"] for r in rows})
        n_email = sum(1 for r in rows if r["Best Email"])
        n_mob = sum(1 for r in rows if r["Mobile"])
        n_live = sum(1 for r in rows if r["Live Job URL"])
        summary.append([name, niche, n_comp, len(rows), n_email, n_mob,
                        n_live, "done"])
        if only and slug not in only and name not in only:
            continue
        values = [list(rows[0].keys())] if rows else [["(no rows)"]]
        values += [[r.get(c, "") for c in rows[0].keys()] for r in rows]
        write_tab(name, values)
        say(f"tab written: {name} ({len(rows)} people rows)")

    summary += [[],
                ["Method: sourced from the open-jobs dataset (~967k open postings, 16 hiring"
                 " systems, CC0); matched by expertise-signal embeddings + exact phrases;"
                 " every listed job re-verified against the company's live ATS feed on the"
                 " 'Job Verified' date; contacts via Blitz + FullEnrich. Counts above are"
                 " computed from run artifacts."]]
    write_tab("Summary", summary)
    say(f"Sheet: https://docs.google.com/spreadsheets/d/{sid}")


if __name__ == "__main__":
    main()
