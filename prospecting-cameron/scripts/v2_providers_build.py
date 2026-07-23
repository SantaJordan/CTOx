#!/usr/bin/env python3
"""
V2 — Healthcare-provider "worst-situation" builder for Cameron / BrassHelm.
Source: OpenWebNinja Local Business Data (Google Maps) — Mimi is offline (tokens disabled).

Why these segments: phone-dependent, marketing-driven, missed-call-is-existential
(a missed admission/booking call = lost high-value patient), and typically under-resourced
on technical ownership. Google Maps gives the triangulation inputs directly:
  G1 magnitude  -> review_count (+ multi-location operator bonus)  = patient/call volume proxy
  G2 pain       -> volume of 1-2 star reviews + low rating         = documented dissatisfaction
  G3 under-res. -> not a mega hospital-system brand                = Twilio exclusion

Output: output/v2_providers_scored.csv
"""
import os, sys, json, time, urllib.parse, urllib.request, csv, re
from collections import defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..")
RAW  = os.path.join(BASE, "data", "v2_own_raw.jsonl")
OUT  = os.path.join(BASE, "output", "v2_providers_scored.csv")

def load_key():
    for p in ["/Users/jordan/Desktop/Blueprint-GTM-Skills/.env",
              os.path.join(BASE, "..", ".env")]:
        if os.path.exists(p):
            for line in open(p):
                if line.startswith("OPENWEBNINJA_API_KEY="):
                    return line.split("=",1)[1].strip().strip("\"' ")
    sys.exit("no OPENWEBNINJA_API_KEY")
KEY = load_key()

SEGMENTS = [
    "addiction treatment center", "fertility clinic", "dental group",
    "dermatology clinic", "plastic surgery center", "med spa", "urgent care",
]
METROS = [
    "Los Angeles CA", "Houston TX", "Phoenix AZ", "Chicago IL", "Dallas TX",
    "Atlanta GA", "Miami FL", "Philadelphia PA", "Las Vegas NV", "Tampa FL",
]
# G3: mega hospital-system / national brands that own tech in-house (EXCLUDE)
MEGA_BRANDS = [
    "hca ", "kaiser", "ascension", "commonspirit", "providence", "advent",
    "tenet", "mayo clinic", "cleveland clinic", "banner health", "sutter",
    "ucla", "cedars-sinai", "mount sinai", "nyu langone", "northwell",
    "baylor scott", "memorial hermann", "houston methodist", "northwestern medicine",
    "concentra", "carbon health", "citymd", "aspen dental", "heartland dental",
]

def search(query, limit=20):
    url = "https://api.openwebninja.com/local-business-data/search?" + urllib.parse.urlencode(
        {"query": query, "limit": limit})
    req = urllib.request.Request(url, headers={"x-api-key": KEY})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def domain(url):
    if not url: return ""
    m = re.sub(r"^https?://(www\.)?", "", url.strip().lower())
    return m.split("/")[0]

# ---- collect ----
seen = {}
rawf = open(RAW, "w")
for seg in SEGMENTS:
    for metro in METROS:
        q = f"{seg} {metro}"
        try:
            d = search(q)
        except Exception as e:
            print("ERR", q, e); time.sleep(1); continue
        for b in (d.get("data") or []):
            pid = b.get("place_id") or b.get("business_id")
            if not pid or pid in seen: continue
            rpr = b.get("reviews_per_rating") or {}
            neg = sum(int(rpr.get(str(s), 0) or 0) for s in (1, 2))
            rec = {
                "name": b.get("name") or "",
                "segment": seg,
                "rating": b.get("rating"),
                "review_count": b.get("review_count") or 0,
                "neg_reviews": neg,
                "phone": b.get("phone_number") or "",
                "website": b.get("website") or "",
                "domain": domain(b.get("website")),
                "city": b.get("city") or "", "state": b.get("state") or "",
                "full_address": b.get("full_address") or "",
                "booking_link": b.get("booking_link") or "",
            }
            seen[pid] = rec
            rawf.write(json.dumps(rec) + "\n")
        print(f"{q:48} -> {len(d.get('data') or [])} (cum {len(seen)})")
        time.sleep(0.2)
rawf.close()

# ---- multi-location operator detection (same domain across locations) ----
locs = defaultdict(int)
for r in seen.values():
    if r["domain"]: locs[r["domain"]] += 1

def g1(r):
    n = r["review_count"] or 0
    base = 0
    if n >= 1000: base = 5
    elif n >= 400: base = 4
    elif n >= 150: base = 3
    elif n >= 50: base = 2
    elif n >= 15: base = 1
    multi = locs.get(r["domain"], 1)
    if multi >= 4: base = min(5, base + 2)
    elif multi >= 2: base = min(5, base + 1)
    return base, multi

def g2(r):
    pain = 0.0
    pain += min(5, (r["neg_reviews"] or 0) / 10.0)          # absolute dissatisfaction volume
    rt = r["rating"]
    if isinstance(rt, (int, float)):
        if rt <= 3.0: pain += 3
        elif rt <= 3.7: pain += 2
        elif rt <= 4.2: pain += 1
    return round(pain, 1)

def g3(r):
    nl = (r["name"] + " " + r["domain"]).lower()
    if any(mb in nl for mb in MEGA_BRANDS): return 0
    return 3

rows = []
for r in seen.values():
    g1s, multi = g1(r)
    g3s = g3(r)
    if g3s == 0: continue
    g2s = g2(r)
    if g1s == 0 or g2s == 0: continue
    rows.append({**r, "multi_site": multi, "g1": g1s, "g2": g2s, "g3": g3s,
                 "score": round(g1s * g2s * g3s, 1)})

rows.sort(key=lambda x: x["score"], reverse=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
cols = ["score","g1","g2","g3","multi_site","segment","name","rating","review_count",
        "neg_reviews","phone","website","domain","city","state","full_address","booking_link"]
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

print(f"\nuniverse collected : {len(seen)}")
print(f"qualified (3 gates): {len(rows)}")
print(f"written: {OUT}\n=== TOP 30 ===")
for x in rows[:30]:
    print(f"{x['score']:6} | g1{x['g1']} g2{x['g2']} x{x['multi_site']} | ⭐{x['rating']} "
          f"({x['review_count']}rev,{x['neg_reviews']}neg) | {x['segment'][:18]:20}| "
          f"{x['name'][:30]:32}| {x['phone']}")
