#!/usr/bin/env python3
"""
V3b — Home-services "worst-situation" builder for Cameron / BrassHelm.
Source: OpenWebNinja Local Business Data (Google Maps).

Home services = high inbound-call dependency (every missed call = lost job), heavy
"after-hours / dispatch" phone load, and a wave of bolted-on cheap voice AI (Air.ai/Bland)
that breaks. Under-resourced on technical ownership = Cameron's wedge.
  G1 magnitude  -> review_count (+ multi-location operator bonus)
  G2 pain       -> volume of 1-2 star reviews + low rating
  G3 under-res. -> not a national franchise HQ brand (those have corporate IT)

Output: output/v3_homeservices_scored.csv
(V3a collections already built from CFPB -> output/v3_collections_candidates.csv)
"""
import os, sys, json, time, urllib.parse, urllib.request, csv, re
from collections import defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..")
RAW  = os.path.join(BASE, "data", "v3_homeservices_raw.jsonl")
OUT  = os.path.join(BASE, "output", "v3_homeservices_scored.csv")

def load_key():
    p = "/Users/jordan/Desktop/Blueprint-GTM-Skills/.env"
    for line in open(p):
        if line.startswith("OPENWEBNINJA_API_KEY="):
            return line.split("=",1)[1].strip().strip("\"' ")
    sys.exit("no key")
KEY = load_key()

SEGMENTS = [
    "HVAC company", "plumbing company", "roofing company",
    "water damage restoration", "pest control company", "garage door repair",
    "electrician company", "appliance repair service",
]
METROS = [
    "Houston TX", "Phoenix AZ", "Dallas TX", "Atlanta GA", "Tampa FL",
    "Las Vegas NV", "Charlotte NC", "Denver CO", "Orlando FL", "San Antonio TX",
]

def search(query, limit=20):
    url = "https://api.openwebninja.com/local-business-data/search?" + urllib.parse.urlencode(
        {"query": query, "limit": limit})
    req = urllib.request.Request(url, headers={"x-api-key": KEY})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def domain(url):
    if not url: return ""
    return re.sub(r"^https?://(www\.)?", "", url.strip().lower()).split("/")[0]

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
            rec = {"name": b.get("name") or "", "segment": seg, "rating": b.get("rating"),
                   "review_count": b.get("review_count") or 0, "neg_reviews": neg,
                   "phone": b.get("phone_number") or "", "website": b.get("website") or "",
                   "domain": domain(b.get("website")), "city": b.get("city") or "",
                   "state": b.get("state") or "", "full_address": b.get("full_address") or "",
                   "booking_link": b.get("booking_link") or ""}
            seen[pid] = rec
            rawf.write(json.dumps(rec) + "\n")
        print(f"{q:46} -> {len(d.get('data') or [])} (cum {len(seen)})")
        time.sleep(0.2)
rawf.close()

locs = defaultdict(int)
for r in seen.values():
    if r["domain"]: locs[r["domain"]] += 1

def g1(r):
    n = r["review_count"] or 0
    base = 5 if n>=2000 else 4 if n>=800 else 3 if n>=300 else 2 if n>=100 else 1 if n>=30 else 0
    multi = locs.get(r["domain"], 1)
    if multi >= 4: base = min(5, base+2)
    elif multi >= 2: base = min(5, base+1)
    return base, multi

def g2(r):
    pain = min(5, (r["neg_reviews"] or 0)/15.0)
    rt = r["rating"]
    if isinstance(rt,(int,float)):
        if rt<=3.5: pain+=3
        elif rt<=4.0: pain+=2
        elif rt<=4.4: pain+=1
    return round(pain,1)

rows=[]
for r in seen.values():
    g1s,multi=g1(r); g2s=g2(r)
    if g1s==0 or g2s==0: continue
    rows.append({**r,"multi_site":multi,"g1":g1s,"g2":g2s,"g3":3,
                 "score":round(g1s*g2s*3,1)})
rows.sort(key=lambda x:x["score"],reverse=True)
os.makedirs(os.path.dirname(OUT),exist_ok=True)
cols=["score","g1","g2","g3","multi_site","segment","name","rating","review_count",
      "neg_reviews","phone","website","domain","city","state","full_address","booking_link"]
with open(OUT,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore"); w.writeheader(); w.writerows(rows)
print(f"\nuniverse: {len(seen)}  qualified: {len(rows)}\nwritten: {OUT}\n=== TOP 25 ===")
for x in rows[:25]:
    print(f"{x['score']:6} | g1{x['g1']} g2{x['g2']} x{x['multi_site']} | ⭐{x['rating']} "
          f"({x['review_count']}rev,{x['neg_reviews']}neg) | {x['segment'][:16]:18}| "
          f"{x['name'][:28]:30}| {x['phone']}")
