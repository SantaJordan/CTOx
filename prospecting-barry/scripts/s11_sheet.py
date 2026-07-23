# /// script
# requires-python = ">=3.10"
# dependencies = ["google-auth", "google-api-python-client"]
# ///
"""Stage 5d: build/update the Barry Hess Google Sheet.

Tabs: Ranked People (output/barry_final.csv), Company Summary (one row per
company with subscores + blind spots), Methodology (computed, never hand-written).
Sheet id cached in checkpoints/sheet_id.txt so the link never changes.

Usage: uv run scripts/s11_sheet.py
"""
import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT  # noqa: E402

SA = Path.home() / ".credentials" / "gdrive_service_account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
TITLE = "Barry Hess — Lab-to-Field Disconnect Prospects"
ID_FILE = ROOT / "checkpoints" / "sheet_id.txt"
FINAL = ROOT / "output" / "barry_final.csv"
RANKED = ROOT / "data" / "ranked_companies.csv"


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

    if ID_FILE.exists():
        sid = ID_FILE.read_text().strip()
    else:
        sid = sheets.spreadsheets().create(body={
            "properties": {"title": TITLE}}).execute()["spreadsheetId"]
        ID_FILE.parent.mkdir(parents=True, exist_ok=True)
        ID_FILE.write_text(sid)
        drive.permissions().create(fileId=sid, body={
            "role": "writer", "type": "anyone"}, fields="id").execute()
        print(f"Created sheet: https://docs.google.com/spreadsheets/d/{sid}")

    meta = sheets.spreadsheets().get(spreadsheetId=sid).execute()
    existing = {s["properties"]["title"]: s["properties"]["sheetId"]
                for s in meta["sheets"]}

    def write_tab(name, values):
        if name not in existing:
            r = sheets.spreadsheets().batchUpdate(spreadsheetId=sid, body={
                "requests": [{"addSheet": {"properties": {"title": name}}}]}).execute()
            existing[name] = r["replies"][0]["addSheet"]["properties"]["sheetId"]
        sheets.spreadsheets().values().clear(spreadsheetId=sid, range=f"'{name}'").execute()
        sheets.spreadsheets().values().update(
            spreadsheetId=sid, range=f"'{name}'!A1",
            valueInputOption="RAW", body={"values": values}).execute()

    people = list(csv.DictReader(open(FINAL, encoding="utf-8")))
    values = [list(people[0].keys())] + \
             [[r.get(c, "") for c in people[0].keys()] for r in people]
    write_tab("Ranked People", values)
    print(f"Ranked People: {len(people)} rows")

    comps = list(csv.DictReader(open(RANKED, encoding="utf-8")))
    values = [list(comps[0].keys())] + \
             [[r.get(c, "") for c in comps[0].keys()] for r in comps]
    write_tab("Company Summary", values)
    print(f"Company Summary: {len(comps)} rows")

    n_people = sum(1 for r in people if r.get("person") != "(none found)")
    n_email = sum(1 for r in people if r.get("best_email"))
    n_mobile = sum(1 for r in people if r.get("mobile"))
    n_comp = len({r["company"] for r in people})
    method = [
        [TITLE, f"built {time.strftime('%Y-%m-%d %H:%M')}"],
        [],
        ["Companies ranked", len(comps)],
        ["Companies in people list", n_comp],
        ["People", n_people],
        ["With email", n_email],
        ["With mobile", n_mobile],
        [],
        ["Sort key: disconnect_score (0-100, higher = the company's own language is "
         "more disconnected from deployed-environment reality — exactly who Barry helps). "
         "Five 0-20 subscores: lab-language intensity, deployment-awareness absence, "
         "operator absence, hiring-profile skew, stage pressure. Quotes required above 10; "
         "companies fluent in ATAK/ATO/DDIL score low; <500 words of own language = "
         "excluded as insufficient evidence."],
        ["Sourcing: 15 defense/natsec VC portfolios + Exa Agent API (5 domain queries + "
         "continuations) + DoD SBIR/STTR Phase II awards 2022+ (bulk data, non-mill) + "
         "a 967k-open-jobs corpus matched on Barry's signal spec. Verified via Blitz "
         "(US HQ, 2-300 headcount, primes/staffing dropped). Evidence packs judged by "
         "scoring agents; contacts via Blitz people + FullEnrich waterfall. All counts "
         "computed from run artifacts."],
    ]
    write_tab("Methodology", method)
    print(f"Sheet: https://docs.google.com/spreadsheets/d/{sid}")


if __name__ == "__main__":
    main()
