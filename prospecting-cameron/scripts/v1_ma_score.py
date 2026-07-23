#!/usr/bin/env python3
"""
V1 — Medicare Advantage "worst-situation" scorer for Cameron / BrassHelm.

Triangulation (all three gates must fire; score = G1 * G2 * G3):
  G1  Problem magnitude  -> enrollment (call-volume proxy)
  G2  In pain / pressure -> bad phone/customer-service Star measures + QBP-bonus jeopardy
  G3  Under-resourced     -> NOT a mega-carrier parent (they own this in-house = Twilio exclusion)

Inputs (CMS public, data.cms.gov):
  data/star2026/...Measure Stars...csv     (per-measure stars per contract)
  data/star2026/...Summary Ratings...csv   (overall/Part C/Part D summary stars + parent org)
  data/enroll0626/.../Monthly_Report_By_Contract_2026_06.csv  (enrollment per contract)

Output:
  output/v1_ma_scored.csv   (full scored, ranked)
  console preview of the top accounts
"""
import csv, sys, os, glob, re
csv.field_size_limit(sys.maxsize)

BASE = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(BASE, "data")
OUT  = os.path.join(BASE, "output", "v1_ma_scored.csv")

def find(pat):
    m = glob.glob(os.path.join(DATA, pat))
    if not m: sys.exit(f"missing: {pat}")
    return m[0]

MEASURE_STARS = find("star2026/*Measure Stars*.csv")
SUMMARY       = find("star2026/*Summary Ratings*.csv")
ENROLL        = find("enroll0626/**/Monthly_Report_By_Contract_*.csv")

# ---- Phone / member-access measures (the existential signals for Cameron) ----
# code -> (short label, weight). Higher weight = more "can't reach a human on the phone".
PHONE_MEASURES = {
    "C24": ("Customer Service", 3.0),
    "C33": ("Call Center (Interpreter/TTY)", 3.0),
    "D01": ("Drug Call Center (Interpreter/TTY)", 3.0),
    "C28": ("Complaints about the Health Plan", 2.5),
    "D02": ("Complaints about the Drug Plan", 2.0),
    "C29": ("Members Choosing to Leave the Plan", 2.5),
    "D03": ("Members Leaving (Drug)", 1.5),
    "C23": ("Getting Appointments & Care Quickly", 2.0),
    "C22": ("Getting Needed Care", 1.5),
    "C26": ("Rating of Health Plan", 1.0),
    "D05": ("Rating of Drug Plan", 1.0),
}

# ---- G3: mega-carrier parents who own voice eng in-house (EXCLUDE) ----
MEGA_PARENTS = [
    "unitedhealth", "humana", "cvs", "aetna", "centene", "wellcare", "elevance",
    "anthem", "cigna", "kaiser", "health care service corp", "hcsc", "highmark",
    "molina", "blue cross blue shield of", "bcbs", "guidewell", "florida blue",
    "carelon", "optum", "devoted health",  # devoted = heavily VC/tech-staffed
]
# Org types worth pursuing (member-facing call centers). CCP = Medicare Advantage.
GOOD_ORG_TYPES = ("local ccp", "regional ccp", "1876 cost", "msa", "pdp", "national pace")

def fnum(s):
    s = (s or "").strip().replace(",", "")
    try: return float(s)
    except: return None

def star(s):
    """Parse a measure/summary star cell -> float or None for non-numeric."""
    s = (s or "").strip()
    if not s: return None
    m = re.match(r"^([0-9](?:\.[0-9])?)", s)
    return float(m.group(1)) if m else None

# ---------- load Measure Stars (header: row1 names, row2 codes, data row4+) ----------
rows = list(csv.reader(open(MEASURE_STARS, encoding="utf-8-sig")))
codes = rows[2]
col_for = {}   # measure-code-prefix -> column index
for i, c in enumerate(codes):
    mm = re.match(r"\s*([CD]\d{2})\s*:", c or "")
    if mm: col_for[mm.group(1)] = i
measure_stars = {}   # contract -> {code: star}
for r in rows[4:]:
    cid = (r[0] or "").strip()
    if not cid: continue
    d = {}
    for code, idx in col_for.items():
        if code in PHONE_MEASURES:
            d[code] = star(r[idx]) if idx < len(r) else None
    measure_stars[cid] = d

# ---------- load Summary Ratings (overall stars + parent) ----------
srows = list(csv.reader(open(SUMMARY, encoding="utf-8-sig")))
shdr = srows[1]
def scol(name):
    for i, h in enumerate(shdr):
        if h.strip().lower() == name.lower(): return i
    return None
ci  = scol("Contract Number")
c_overall = scol("2026 Overall")
c_partc   = scol("2026 Part C Summary")
c_partd   = scol("2026 Part D Summary")
summary = {}
for r in srows[2:]:
    if ci is None or ci >= len(r): continue
    cid = (r[ci] or "").strip()
    if not cid: continue
    summary[cid] = {
        "overall": star(r[c_overall]) if c_overall is not None else None,
        "partc":   star(r[c_partc])   if c_partc   is not None else None,
        "partd":   star(r[c_partd])   if c_partd   is not None else None,
    }

# ---------- load enrollment (one row per contract) ----------
enroll = {}
er = csv.DictReader(open(ENROLL, encoding="utf-8-sig"))
for row in er:
    cid = (row.get("Contract Number") or "").strip()
    if not cid: continue
    enroll[cid] = {
        "n": fnum(row.get("Enrollment")) or 0,
        "org_type": (row.get("Organization Type") or "").strip(),
        "plan_type": (row.get("Plan Type") or "").strip(),
        "name": (row.get("Organization Marketing Name") or row.get("Organization Name") or "").strip(),
        "parent": (row.get("Parent Organization") or "").strip(),
    }

# ---------- score ----------
def g1_magnitude(n):
    # enrollment -> call-volume proxy. Need a real call center; cap so mega plans don't dominate.
    if n < 2000:   return 0
    if n < 5000:   return 1
    if n < 15000:  return 2
    if n < 50000:  return 3
    if n < 150000: return 4
    return 5

def g3_under_resourced(parent, org_type):
    p = parent.lower()
    if any(mp in p for mp in MEGA_PARENTS): return 0          # they own it in-house
    ot = org_type.lower()
    if not any(g in ot for g in GOOD_ORG_TYPES): return 1     # odd org type, keep low
    # provider-sponsored / regional independents score highest
    return 3

out = []
for cid, en in enroll.items():
    n = en["n"]
    g1 = g1_magnitude(n)
    if g1 == 0: continue
    g3 = g3_under_resourced(en["parent"], en["org_type"])
    if g3 == 0: continue

    ms = measure_stars.get(cid, {})
    sm = summary.get(cid, {})
    overall = sm.get("overall")

    # G2a: phone-measure pain. badness per measure = max(0, 3.5 - star) * weight
    pain = 0.0; bad_evidence = []
    for code, (label, w) in PHONE_MEASURES.items():
        s = ms.get(code)
        if s is None: continue
        if s <= 3.0:
            b = (3.5 - s) * w
            pain += b
            bad_evidence.append(f"{label}={s:g}★")
    # G2b: QBP-bonus jeopardy. <4.0 overall loses the rebate bonus; 2.5-3.5 = max pressure/turnaround zone.
    pressure = 0.0
    if overall is not None:
        if overall < 2.5:      pressure = 2.0      # crisis
        elif overall < 4.0:    pressure = 3.0      # just below the 4.0 bonus line = highest motivation
        else:                  pressure = 0.5      # already 4+, less urgent
    g2 = pain + pressure
    if g2 <= 0: continue   # no phone pain and no rating pressure -> not in motion

    score = round(g1 * g2 * g3, 1)
    out.append({
        "contract_id": cid,
        "plan_name": en["name"],
        "parent": en["parent"],
        "org_type": en["org_type"],
        "enrollment": int(n),
        "overall_star": overall if overall is not None else "",
        "g1_magnitude": g1,
        "g2_pain_pressure": round(g2, 1),
        "g3_under_resourced": g3,
        "score": score,
        "bad_phone_measures": "; ".join(bad_evidence),
    })

out.sort(key=lambda x: x["score"], reverse=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

print(f"contracts with enrollment      : {len(enroll)}")
print(f"qualified (all 3 gates fire)   : {len(out)}")
print(f"written: {OUT}\n")
print("=== TOP 30 (score | enroll | overall | plan | parent | pain) ===")
for x in out[:30]:
    print(f"{x['score']:6} | {x['enrollment']:>7} | {str(x['overall_star']):>4}★ | "
          f"{x['plan_name'][:30]:32}| {x['parent'][:22]:24}| {x['bad_phone_measures'][:60]}")
