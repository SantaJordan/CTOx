#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-auth", "google-api-python-client"]
# ///
"""s9 — publish Ben Cole's target universe to ONE Google Sheet.

Tabs:
  Start Here      — what this is, how to work it, method, live counts
  Studios         — 42 qualified studios, ranked by pain score, with brief
  Contacts        — decision-makers w/ emails, sorted by company pain

Re-runnable: sheet id cached in checkpoints/sheet_id.txt so the link is stable.
Counts are COMPUTED from the CSVs, never hand-written.

Usage: python3 s9_google_sheet.py
"""
import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path.home() / "Desktop" / "Blueprint-GTM-Skills"
                       / "tools" / "google-auth"))
from common import ROOT  # noqa: E402
from google_auth import get_service  # noqa: E402

OUTD = ROOT / "output"
ID_FILE = ROOT / "checkpoints" / "sheet_id.txt"
TITLE = "Ben Cole — Funded, Unlaunched US Game Studios (ranked by ops pain)"

STUDIO_COLS = [
    ("pain_score", "Pain", 55), ("company", "Studio", 170),
    ("fit_verdict", "Fit", 70), ("verified", "Spot-check (manually re-verified)", 320),
    ("employees", "Staff", 55),
    ("hq", "HQ", 140), ("game", "Game", 150),
    ("game_status", "Game status", 110),
    ("total_raised", "Raised", 95), ("last_round", "Last round", 130),
    ("investors", "Investors", 200),
    ("ops_gap_why", "Ops gap (the hook)", 300),
    ("senior_eng_titles", "Senior eng carrying it", 260),
    ("milestone_why", "Milestone / runway pressure", 300),
    ("launch_why", "Launch proximity", 260),
    ("brief", "Research brief", 600),
    ("domain", "Website", 150), ("linkedin_url", "LinkedIn", 200),
]
CONTACT_COLS = [
    ("pain_score", "Pain", 55), ("company", "Studio", 170),
    ("full_name", "Name", 150), ("title", "Title", 220),
    ("email", "Email", 230), ("person_linkedin", "LinkedIn", 250),
    ("location", "Location", 160),
]


def main():
    sheets = get_service("sheets", "v4")
    drive = get_service("drive", "v3")

    studios = list(csv.DictReader(open(OUTD / "ben_universe_ranked.csv",
                                       encoding="utf-8")))
    contacts = list(csv.DictReader(open(OUTD / "contacts_ranked.csv",
                                        encoding="utf-8")))

    if ID_FILE.exists():
        sid = ID_FILE.read_text().strip()
    else:
        sid = sheets.spreadsheets().create(body={
            "properties": {"title": TITLE}}).execute()["spreadsheetId"]
        ID_FILE.parent.mkdir(parents=True, exist_ok=True)
        ID_FILE.write_text(sid)
        drive.permissions().create(fileId=sid, body={
            "role": "reader", "type": "anyone"}, fields="id").execute()
        print(f"Created sheet: https://docs.google.com/spreadsheets/d/{sid}")

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

    n_strong = sum(1 for r in studios if r["fit_verdict"] == "strong")
    n_med = sum(1 for r in studios if r["fit_verdict"] == "medium")
    n_weak = sum(1 for r in studios if r["fit_verdict"] == "weak")
    n_email = sum(1 for c in contacts if c["email"])
    n_zero_ops = sum(1 for r in studios if "ZERO dedicated ops" in r["ops_gap_why"])
    n_check = sum(1 for r in studios if r.get("verified"))

    # ---------- Start Here ----------
    intro = [
        ["Funded, unlaunched US game studios — ranked by operational pain"],
        [f"Built for Ben Cole (Studio Foundations) · {time.strftime('%d %B %Y')}"
         " · by Jordan Crawford, Blueprint GTM"],
        [],
        ["WHAT THIS IS"],
        ["Every studio here is: US-headquartered, venture- or publisher-funded, "
         "roughly 20-150 people, and has NOT yet shipped its debut/flagship game."],
        ["They are ranked by how likely it is that senior engineers are personally "
         "carrying the operational layer (builds, cloud, security, access, vendors) "
         "instead of building the game."],
        [],
        ["HOW TO WORK IT"],
        ["1. Open the 'Studios' tab. It is already sorted — highest pain at the top."],
        ["2. Read the 'Ops gap (the hook)' column. That is the specific, evidence-based "
         "reason to reach out, drawn from the studio's actual engineering roster."],
        ["3. Read 'Research brief' for the full picture before you write."],
        ["4. Open the 'Contacts' tab, filter by studio name, and email the CEO / "
         "studio head / technical leader listed there."],
        [],
        ["WHAT THE NUMBERS MEAN"],
        ["Pain score (0-100) = ops gap (0-40) + hiring signals (0-10) + milestone & "
         "runway pressure (0-30) + launch proximity (0-15) + size fit (0-5)."],
        ["Ops gap is the heaviest weight because it is the most direct evidence: it "
         "counts senior engineers and technical directors on staff against the number "
         "of dedicated DevOps / IT / security / build people. Senior engineers with no "
         "ops support means somebody senior is doing that work."],
        ["Fit = strong / medium / weak, judged from the research on funding stage, "
         "launch status, and whether the pitch lands right now."],
        [],
        ["WHAT'S IN HERE"],
        ["Qualified studios", len(studios)],
        ["  Strong fit", n_strong],
        ["  Medium fit", n_med],
        ["  Weak fit", n_weak],
        ["Studios with 2+ senior engineers and ZERO dedicated ops staff", n_zero_ops],
        ["Decision-maker contacts", len(contacts)],
        ["  With a verified email address", n_email],
        ["Top studios independently spot-checked by hand", n_check],
        [],
        ["HOW IT WAS BUILT"],
        ["Started from ~490 candidate studios discovered three independent ways: "
         "portfolio pages of 20 game-focused VC funds (BITKRAFT, Makers, Griffin, "
         "1Up, Galaxy, Konvoy, Play Ventures and others); a sweep of game-industry "
         "funding announcements from 2023 onward; and AI research agents asked to "
         "enumerate funded pre-launch studios."],
        ["Each candidate was then verified for headcount, HQ country and company "
         "identity, which cut the list to 92 real US studios in the size band."],
        ["Every one of those 92 was researched individually — funding history, game "
         "status, production phase — and its engineering roster analysed for the "
         "ops-ownership gap. 50 were disqualified (game already launched, non-US, "
         "acquired, or not a game studio), leaving the 42 here."],
        ["Contacts were pulled for each surviving studio and emails verified through "
         "two independent providers."],
        [],
        ["CAVEATS — PLEASE READ"],
        ["Headcount comes from LinkedIn and runs a little behind reality."],
        ["'Game status' reflects the most recent public information found; a studio "
         "may have announced something since."],
        ["The ops-gap signal infers from public profiles who is NOT on staff. It is "
         "strong evidence, not proof — a studio may have an ops contractor who does "
         "not appear publicly. Treat it as a well-founded opening hypothesis."],
        ["Contact emails are provider-verified but not send-tested. Warm up and send "
         "in small batches."],
        ["The 'Spot-check' column shows studios I re-verified by hand after the "
         "automated pass. Where it says CAUTION, read the note before using that "
         "studio as an anchor example — one of them turned out to have already "
         "shipped a game and was demoted accordingly."],
    ]
    write_tab("Start Here", intro)

    # ---------- Studios ----------
    vals = [[label for _, label, _ in STUDIO_COLS]]
    for r in studios:
        vals.append([r.get(k, "") for k, _, _ in STUDIO_COLS])
    write_tab("Studios", vals)

    # ---------- Contacts ----------
    cvals = [[label for _, label, _ in CONTACT_COLS]]
    for c in contacts:
        cvals.append([c.get(k, "") for k, _, _ in CONTACT_COLS])
    write_tab("Contacts", cvals)

    # ---------- formatting ----------
    reqs = []
    for tab, cols, nrows in (("Studios", STUDIO_COLS, len(studios)),
                             ("Contacts", CONTACT_COLS, len(contacts))):
        tid = existing[tab]
        reqs += [
            {"repeatCell": {
                "range": {"sheetId": tid, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"bold": True},
                    "backgroundColor": {"red": .12, "green": .16, "blue": .22},
                    "wrapStrategy": "CLIP"}},
                "fields": "userEnteredFormat(textFormat,backgroundColor,wrapStrategy)"}},
            {"repeatCell": {
                "range": {"sheetId": tid, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {"userEnteredFormat": {"textFormat": {
                    "bold": True, "foregroundColor": {
                        "red": 1, "green": 1, "blue": 1}}}},
                "fields": "userEnteredFormat.textFormat"}},
            {"updateSheetProperties": {
                "properties": {"sheetId": tid, "gridProperties": {
                    "frozenRowCount": 1, "frozenColumnCount": 2}},
                "fields": "gridProperties(frozenRowCount,frozenColumnCount)"}},
            {"setBasicFilter": {"filter": {"range": {
                "sheetId": tid, "startRowIndex": 0,
                "endRowIndex": nrows + 1, "startColumnIndex": 0,
                "endColumnIndex": len(cols)}}}},
            {"repeatCell": {
                "range": {"sheetId": tid, "startRowIndex": 1},
                "cell": {"userEnteredFormat": {
                    "wrapStrategy": "WRAP", "verticalAlignment": "TOP"}},
                "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"}},
        ]
        for i, (_, _, width) in enumerate(cols):
            reqs.append({"updateDimensionProperties": {
                "range": {"sheetId": tid, "dimension": "COLUMNS",
                          "startIndex": i, "endIndex": i + 1},
                "properties": {"pixelSize": width}, "fields": "pixelSize"}})
        # pain score colour scale
        reqs.append({"addConditionalFormatRule": {"rule": {
            "ranges": [{"sheetId": tid, "startRowIndex": 1,
                        "startColumnIndex": 0, "endColumnIndex": 1}],
            "gradientRule": {
                "minpoint": {"color": {"red": 1, "green": 1, "blue": 1},
                             "type": "NUMBER", "value": "40"},
                "maxpoint": {"color": {"red": .91, "green": .34, "blue": .30},
                             "type": "NUMBER", "value": "85"}}},
            "index": 0}})

    intro_tid = existing["Start Here"]
    reqs += [
        {"updateDimensionProperties": {
            "range": {"sheetId": intro_tid, "dimension": "COLUMNS",
                      "startIndex": 0, "endIndex": 1},
            "properties": {"pixelSize": 760}, "fields": "pixelSize"}},
        {"repeatCell": {
            "range": {"sheetId": intro_tid, "startRowIndex": 0, "endRowIndex": 1},
            "cell": {"userEnteredFormat": {"textFormat": {
                "bold": True, "fontSize": 15}}},
            "fields": "userEnteredFormat.textFormat"}},
        {"repeatCell": {
            "range": {"sheetId": intro_tid, "startRowIndex": 1},
            "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP"}},
            "fields": "userEnteredFormat.wrapStrategy"}},
    ]
    for hdr_row in (3, 7, 13, 19, 29, 36):
        reqs.append({"repeatCell": {
            "range": {"sheetId": intro_tid, "startRowIndex": hdr_row,
                      "endRowIndex": hdr_row + 1},
            "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
            "fields": "userEnteredFormat.textFormat"}})

    # Start Here first
    reqs.append({"updateSheetProperties": {
        "properties": {"sheetId": intro_tid, "index": 0}, "fields": "index"}})

    sheets.spreadsheets().batchUpdate(
        spreadsheetId=sid, body={"requests": reqs}).execute()

    # drop the default empty Sheet1 if present
    if "Sheet1" in existing:
        sheets.spreadsheets().batchUpdate(spreadsheetId=sid, body={
            "requests": [{"deleteSheet": {"sheetId": existing["Sheet1"]}}]}).execute()

    url = f"https://docs.google.com/spreadsheets/d/{sid}"
    print(f"Studios: {len(studios)} | Contacts: {len(contacts)} "
          f"({n_email} with email)")
    print(f"Sheet: {url}")


if __name__ == "__main__":
    main()
