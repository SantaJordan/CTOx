#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-auth", "google-api-python-client"]
# ///
"""
C4 — Publish the Cameron / BrassHelm prospect sheet to Google Sheets.
Tabs: Prospects (people + contacts) | Target Accounts | Methodology.
Auth: service account (~/.credentials/gdrive_service_account.json) else gcloud ADC.
"""
import csv, os, sys, json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PROSPECTS = BASE/"output"/"prospects.csv"
ACCOUNTS  = BASE/"output"/"accounts.csv"
SA = Path.home()/".credentials"/"gdrive_service_account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

def creds():
    if SA.exists():
        from google.oauth2 import service_account
        return service_account.Credentials.from_service_account_file(str(SA), scopes=SCOPES)
    import google.auth
    c,_ = google.auth.default(scopes=SCOPES); return c

def opener(p):
    v=p["vertical"]
    if v=="medicare_advantage":
        return ("Saw your CMS Star Ratings — the member-facing phone measures are where the "
                "rebate dollars are leaking. I rebuilt exactly this for a health plan doing 10-20k "
                "calls/day (found 67% of 'successful transfers' were actually voicemails).")
    if v=="provider":
        return ("Your Google reviews show a booking/phone bottleneck at real volume. Every missed "
                "call is a lost high-value patient. I own voice-AI deployments end-to-end so the "
                "phone actually converts instead of dropping to voicemail.")
    if v=="collections":
        return ("You run a large outbound dialer operation and it's generating CFPB communication "
                "complaints. I build compliant, verified voice-AI calling (right-party contact, "
                "voicemail detection) — and I prove the numbers are real.")
    return ("High inbound call volume and every missed call is a lost job. I deploy voice AI that "
            "books the call instead of dropping it, bridged into the phone system you already run.")

def rows_csv(path):
    return list(csv.DictReader(open(path, encoding="utf-8"))) if path.exists() else []

def main():
    pros = rows_csv(PROSPECTS); accts = rows_csv(ACCOUNTS)
    if not pros: sys.exit("no prospects.csv — run c3 first")
    from googleapiclient.discovery import build
    cr = creds()
    sheets = build("sheets","v4",credentials=cr,cache_discovery=False)
    drive  = build("drive","v3",credentials=cr,cache_discovery=False)

    p_hdr = ["Account","Vertical","Company","Person","Title","Role","Best Email","Mobile Phone",
             "All Phones","All Emails","LinkedIn","Location","Why Target (evidence)","Suggested Opener"]
    p_rows = [[p["account_id"],p["vertical"],p["company_name"],p["full_name"],p["title"],
               p["role_bucket"],p.get("best_email",""),p.get("mobile_phone",""),
               p.get("all_phones",""),p.get("all_emails",""),p["linkedin_url"],p["location"],
               p["company_evidence"],opener(p)] for p in pros]

    a_hdr = ["Account","Vertical","Company","Parent","Domain","Main Phone","Location",
             "Segment","Score","Why Target (evidence)"]
    a_rows = [[a["account_id"],a["vertical"],a["company_name"],a.get("parent",""),a.get("domain",""),
               a.get("main_phone",""),a.get("location",""),a.get("segment",""),a.get("score",""),
               a["evidence"]] for a in accts]

    m_rows = [
      ["Cameron / BrassHelm — Triangulated 'Worst-Situation' Voice-AI Prospects"],
      [f"Built {datetime.now(timezone.utc).strftime('%Y-%m-%d')} • {len(accts)} accounts • {len(pros)} people"],
      [""],
      ["Thesis","Find companies where voice/telephony is revenue- or compliance-critical, "
       "the phone is measurably broken, AND nobody owns the technical side (Cameron's wedge)."],
      ["Gate 1 — Real problem","Voice/phone critical at volume (call-volume proxy)."],
      ["Gate 2 — In pain / pressure","Public evidence the phone is broken + financial/regulatory pressure."],
      ["Gate 3 — Under-resourced","Not a mega-carrier / health-system / CPaaS that owns voice in-house."],
      [""],
      ["Vertical","Universe source","Pain signal"],
      ["Medicare Advantage","CMS 2026 Star Ratings + enrollment","Low Customer Service / Call Center / "
       "Complaints stars + sub-4★ QBP-bonus jeopardy (real rebate $)."],
      ["Healthcare providers","Google Maps (OpenWebNinja)","Volume of 1-2★ reviews at high review counts; "
       "missed booking call = lost high-value patient. Fertility / plastic surgery / med spa / rehab."],
      ["Collections","CFPB Consumer Complaint DB","Phone communication-tactics complaints = large outbound "
       "dialer under pressure (mega players excluded)."],
      ["Home services","Google Maps (OpenWebNinja)","High call volume + negative-review volume; every missed "
       "call = lost job (weakest fit — third priority)."],
      [""],
      ["People","Blitz waterfall-ICP: decision-maker (CEO/COO/President/Founder) + tech/ops owner "
       "(CTO/CIO/VP-Tech, then VP Ops / Member Experience / Patient Access / Contact Center / Growth)."],
      ["Contacts","FullEnrich waterfall (email + mobile) with Blitz email as baseline."],
    ]

    title = f"BrassHelm Voice-AI Prospects — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
    resp = sheets.spreadsheets().create(body={"properties":{"title":title},
        "sheets":[{"properties":{"title":t,"index":i}} for i,t in
                  enumerate(["Prospects","Target Accounts","Methodology"])]},
        fields="spreadsheetId").execute()
    ss=resp["spreadsheetId"]
    sheets.spreadsheets().values().batchUpdate(spreadsheetId=ss, body={"valueInputOption":"RAW",
        "data":[{"range":"Prospects!A1","values":[p_hdr]+p_rows},
                {"range":"Target Accounts!A1","values":[a_hdr]+a_rows},
                {"range":"Methodology!A1","values":m_rows}]}).execute()
    # bold header rows + freeze
    reqs=[]
    for sh in resp.get("sheets",[]): pass
    meta = sheets.spreadsheets().get(spreadsheetId=ss).execute()
    for s in meta["sheets"]:
        sid=s["properties"]["sheetId"]
        reqs.append({"repeatCell":{"range":{"sheetId":sid,"startRowIndex":0,"endRowIndex":1},
            "cell":{"userEnteredFormat":{"textFormat":{"bold":True}}},"fields":"userEnteredFormat.textFormat.bold"}})
        reqs.append({"updateSheetProperties":{"properties":{"sheetId":sid,"gridProperties":{"frozenRowCount":1}},
            "fields":"gridProperties.frozenRowCount"}})
    sheets.spreadsheets().batchUpdate(spreadsheetId=ss, body={"requests":reqs}).execute()
    try:
        drive.permissions().create(fileId=ss, body={"type":"anyone","role":"reader"}, fields="id").execute()
    except Exception as e:
        print("share warn:", e, file=sys.stderr)
    url=f"https://docs.google.com/spreadsheets/d/{ss}"
    print(url)
    open(BASE/"output"/"SHEET_URL.txt","w").write(url+"\n")

if __name__ == "__main__":
    main()
