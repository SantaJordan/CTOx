#!/usr/bin/env python3
"""
C1 — Assemble the cross-vertical TARGET ACCOUNT shortlist for Cameron / BrassHelm.
Reads the four scored CSVs, dedupes providers/home-services to the operator (by domain),
attaches a Texada-clean evidence string per account, and writes a unified accounts.csv.

Output: output/accounts.csv  (the list of companies Cameron should target)
"""
import csv, os, re, hashlib
from collections import defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT  = os.path.join(BASE, "output", "accounts.csv")

# Full high-fit universe. Home services held back (weakest fit) -> set 0; raise to enrich later.
CAP = {"medicare_advantage": 999, "provider": 9999, "collections": 999, "home_services": 9999}

def stable_id(vertical, name, domain):
    h = hashlib.md5(f"{vertical}|{name.strip().lower()}|{domain.strip().lower()}".encode()).hexdigest()[:8]
    return "AC" + h

def rd(path):
    p = os.path.join(BASE, "output", path)
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []

accounts = []

# ---- V1 Medicare Advantage ----
for r in rd("v1_ma_scored.csv")[:CAP["medicare_advantage"]]:
    accounts.append({
        "vertical": "medicare_advantage",
        "company_name": r["plan_name"],
        "parent": r["parent"],
        "domain": "",
        "main_phone": "",
        "location": "",
        "score": r["score"],
        "evidence": f"{int(float(r['enrollment'])):,} members; overall {r['overall_star']}★ "
                    f"(QBP-bonus pressure); CMS phone measures: {r['bad_phone_measures']}",
        "segment": r["org_type"],
    })

# ---- V2 providers: dedupe to operator by domain, keep highest-score rep ----
def operator_dedupe(rows, vertical, cap):
    by_dom = defaultdict(list)
    nodom = []
    for r in rows:
        d = (r.get("domain") or "").strip().lower()
        (by_dom[d] if d else nodom).append(r)
    reps = []
    for d, grp in by_dom.items():
        grp.sort(key=lambda x: float(x["score"]), reverse=True)
        rep = grp[0]
        rep["_locations"] = len(grp)
        reps.append(rep)
    # include domainless singletons too (less useful, lower priority)
    for r in nodom:
        r["_locations"] = 1
        reps.append(r)
    reps.sort(key=lambda x: float(x["score"]), reverse=True)
    return reps[:cap]

def clean_brand(name):
    # strip trailing location/branch descriptors after a dash/pipe/paren
    return re.split(r"\s+[-|(]", name)[0].strip()

for r in operator_dedupe(rd("v2_providers_scored.csv"), "provider", CAP["provider"]):
    accounts.append({
        "vertical": "provider",
        "company_name": clean_brand(r["name"]),
        "parent": "",
        "domain": r.get("domain",""),
        "main_phone": r.get("phone",""),
        "location": f"{r.get('city','')}, {r.get('state','')}",
        "score": r["score"],
        "evidence": f"{r['segment']}; {r['review_count']} Google reviews "
                    f"({r['neg_reviews']} at 1-2★, {r['rating']}★); ~{r.get('_locations',1)} locations seen",
        "segment": r["segment"],
    })

# ---- V3 collections (CFPB) ----
for r in rd("v3_collections_candidates.csv")[:CAP["collections"]]:
    accounts.append({
        "vertical": "collections",
        "company_name": r["company"],
        "parent": "",
        "domain": "",
        "main_phone": "",
        "location": "",
        "score": r["comm_tactics_complaints_18mo"],
        "evidence": f"{r['comm_tactics_complaints_18mo']} CFPB phone-communication-tactics "
                    f"complaints (18mo) → large outbound dialer operation under pressure",
        "segment": "debt-collection",
    })

# ---- V3 home services ----
for r in operator_dedupe(rd("v3_homeservices_scored.csv"), "home_services", CAP["home_services"]):
    accounts.append({
        "vertical": "home_services",
        "company_name": clean_brand(r["name"]),
        "parent": "",
        "domain": r.get("domain",""),
        "main_phone": r.get("phone",""),
        "location": f"{r.get('city','')}, {r.get('state','')}",
        "score": r["score"],
        "evidence": f"{r['segment']}; {r['review_count']} reviews ({r['neg_reviews']} negative, "
                    f"{r['rating']}★); every missed call = lost job",
        "segment": r["segment"],
    })

for a in accounts:
    a["account_id"] = stable_id(a["vertical"], a["company_name"], a.get("domain",""))
# de-dup any id collisions (same brand+domain appearing twice)
_seen=set(); accounts=[a for a in accounts if not (a["account_id"] in _seen or _seen.add(a["account_id"]))]

cols = ["account_id","vertical","company_name","parent","domain","main_phone",
        "location","segment","score","evidence"]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(accounts)

from collections import Counter
print("accounts by vertical:", dict(Counter(a["vertical"] for a in accounts)))
print(f"total accounts: {len(accounts)}  ->  {OUT}")
print("\n=== sample ===")
for a in accounts[:6] + accounts[30:34]:
    print(f"{a['account_id']} [{a['vertical'][:12]:12}] {a['company_name'][:34]:36} dom={a['domain'][:24]:25} {a['evidence'][:70]}")
