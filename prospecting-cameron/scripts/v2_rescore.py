#!/usr/bin/env python3
"""Re-score V2 from raw with a tightened Gate-3 (health-system / HCA / PE-rollup owned = excluded)
and a segment-fit weight (independent, phone/marketing-driven specialties rank highest).
Reads data/v2_own_raw.jsonl -> output/v2_providers_scored.csv (overwrites)."""
import os, json, csv, re
from collections import defaultdict
BASE = os.path.join(os.path.dirname(__file__), "..")
RAW  = os.path.join(BASE, "data", "v2_own_raw.jsonl")
OUT  = os.path.join(BASE, "output", "v2_providers_scored.csv")

# Health systems + HCA/Optum/PE urgent-care rollups + national dental/derm chains (own IT in-house).
OWNED = [
 "hca","carenow","md now","banner","honorhealth","baycare","tgh","patient first",
 "physicians immediate care","nextcare","gohealth","medexpress","concentra","citymd",
 "carbon health","fastmed","afc urgent","wellnow","exer","dignity","intermountain","atrium",
 "novant","wellstar","piedmont","emory","ucla","usc ","jefferson","temple","adventhealth",
 "orlando health","advent","scripps","sharp ","sutter","providence","ascension","commonspirit",
 "methodist","memorial hermann","baptist","mercy","st joseph","kaiser","mayo","cleveland clinic",
 "mount sinai","nyu","northwell","northwestern","baylor scott","tenet","steward","optum",
 "aspen dental","heartland dental","pacific dental","western dental","forward dermatology",
 "u.s. dermatology","schweiger","american addiction","acadia",
]
# segment fit: independent, marketing/phone-booking specialties = strongest Cameron fit
SEG_FIT = {
 "fertility clinic": 1.3, "plastic surgery center": 1.25, "med spa": 1.2,
 "addiction treatment center": 1.15, "dermatology clinic": 1.1, "dental group": 1.1,
 "urgent care": 0.7,  # skews health-system owned
}

def owned(name, domain):
    s = (name + " " + domain).lower()
    return any(b in s for b in OWNED)

rows = [json.loads(l) for l in open(RAW)]
locs = defaultdict(int)
for r in rows:
    if r.get("domain"): locs[r["domain"]] += 1

def g1(r):
    n = r["review_count"] or 0
    base = 5 if n>=1000 else 4 if n>=400 else 3 if n>=150 else 2 if n>=50 else 1 if n>=15 else 0
    multi = locs.get(r["domain"],1)
    if multi>=4: base=min(5,base+2)
    elif multi>=2: base=min(5,base+1)
    return base, multi

def g2(r):
    pain = min(5,(r["neg_reviews"] or 0)/10.0)
    rt = r["rating"]
    if isinstance(rt,(int,float)):
        if rt<=3.0: pain+=3
        elif rt<=3.7: pain+=2
        elif rt<=4.2: pain+=1
    return round(pain,1)

out=[]
for r in rows:
    if owned(r["name"], r.get("domain","")): continue
    g1s,multi=g1(r); g2s=g2(r)
    if g1s==0 or g2s==0: continue
    fit=SEG_FIT.get(r["segment"],1.0)
    score=round(g1s*g2s*3*fit,1)
    out.append({**r,"multi_site":multi,"g1":g1s,"g2":g2s,"g3":3,"seg_fit":fit,"score":score})
out.sort(key=lambda x:x["score"],reverse=True)
cols=["score","g1","g2","g3","seg_fit","multi_site","segment","name","rating","review_count",
      "neg_reviews","phone","website","domain","city","state","full_address","booking_link"]
with open(OUT,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore"); w.writeheader(); w.writerows(out)
print(f"qualified after tightened G3: {len(out)}  (was {len(rows)} raw)\nwritten {OUT}\n=== TOP 30 (independent specialty providers) ===")
for x in out[:30]:
    print(f"{x['score']:6} | x{x['multi_site']:>2} | ⭐{x['rating']} ({x['review_count']}rev,{x['neg_reviews']}neg) | "
          f"{x['segment'][:16]:18}| {x['name'][:32]:34}| {x['city']},{x['state']} | {x['phone']}")
