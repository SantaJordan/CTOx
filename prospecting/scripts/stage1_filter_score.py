#!/usr/bin/env python3
"""
Stage 1 — Filter Eric's SaaS TAM to a Series-A cohort and score axes 1 & 2
(missing key integration; integration complexity) from CSV text only.
Axis 3 (silo pain) and gap-signal confirmation happen in Stage 2 (website scrape).

Input : prospecting/data/us-software-saas-companies-cleaned.csv
Output: prospecting/data/stage1_scored.csv         (full scored cohort)
        prospecting/data/stage1_top_candidates.csv  (top N for website enrichment)
Rubrics: prospecting/research/axis{1,2}_*.md
"""
import csv, sys, re
csv.field_size_limit(sys.maxsize)

IN = "prospecting/data/us-software-saas-companies-cleaned.csv"
OUT_ALL = "prospecting/data/stage1_scored.csv"
OUT_TOP = "prospecting/data/stage1_top_candidates.csv"

# ---- Series A proxy: US + known funding in the A band ----
FUNDING_A = {"$1M - $5M", "$5M - $10M", "$10M - $25M"}
FUNDING_EDGE = {"Under $1M", "$25M - $50M"}  # kept, down-weighted
SIZE_OK = {"2-10 employees", "11-50 employees", "51-200 employees", "201-500 employees"}

# ---- Axis 1: named systems-of-record (high value) ----
A1_SOR_HIGH = [
    "epic", "epic ehr", "app orchard", "athenahealth", "athenaone", "athena marketplace",
    "cerner", "oracle health", "veradigm", "allscripts", "powerchart",
    "workday", "veeva", "veeva vault", "netsuite", "suiteapp", "sap", "s/4hana",
    "servicenow", "guidewire", "duck creek", "epic integration", "ehr integration",
    "emr integration", "erp integration", "hris integration",
    "hl7", "fhir", "smart on fhir", "interoperability", "carequality", "commonwell",
    "edi", "x12", "837", "835", "270", "271", "clearinghouse", "claims integration",
    "salesforce", "appexchange", "health cloud", "dynamics 365", "microsoft dynamics",
    "procore", "snowflake", "databricks",
]
A1_SOR_COMMODITY = ["stripe", "twilio", "quickbooks", "xero", "plaid", "shopify", "hubspot"]
A1_GAP = [
    "request an integration", "request integration", "integration roadmap",
    "coming soon", "no api", "manual upload", "csv import", "csv export",
    "flat file", "sftp", "manual data entry", "double entry", "limited integrations",
    "custom integration", "manual export", "manual import",
]

# ---- Axis 2: integration complexity ----
A2_STRONG = [
    "integration marketplace", "app marketplace", "integrations directory",
    "two-way sync", "bi-directional sync", "bidirectional sync", "real-time sync",
    "real time sync", "api-first", "api first", "developer portal", "developer platform",
    "webhooks", "sdk", "embedded", "white-label", "white label", "ipaas", "etl",
    "reverse etl", "data pipeline", "middleware", "change data capture",
    "single source of truth", "integrates with", "connects with", "syncs with",
    "unify your data", "unify data", "disparate systems",
]
A2_MEDIUM = [
    "product suite", "all-in-one platform", "workflow automation", "triggers and actions",
    "partner program", "technology partners", "omnichannel", "multi-channel", "sso",
    "saml", "scim", "oauth", "data warehouse", "modernize legacy", "legacy systems",
    "connect your apps", "connect your tools", "existing stack",
]
A2_WEAK = ["seamless integration", "open api", "rest api", "api available", "cloud-based", "integration"]

# ---- Integration-vendor demotion (they ARE the cure) ----
VENDOR_PATTERNS = [
    "ipaas", "integration platform", "integration-platform-as-a-service",
    "unified api", "etl tool", "elt tool", "data integration platform",
    "embedded integration", "embedded ipaas", "no-code integration",
    "reverse etl", "data pipeline platform", "connect any app", "any-to-any integration",
    "mulesoft", "workato", "boomi", "celigo", "tray.io", "fivetran", "merge.dev",
    "integration-as-a-service", "we connect your", "connect all your tools",
]
# service firms / agencies (sellers of integration labor, not buyers)
SERVICE_INDUSTRIES = [
    "it services and it consulting", "business consulting and services",
    "information technology and services", "advertising services", "marketing services",
    "design services", "staffing and recruiting", "it system custom software development",
]

_RX = {}
def _rx(t):
    r = _RX.get(t)
    if r is None:
        # match whole token only: not preceded/followed by another alphanumeric
        r = re.compile(r'(?<![a-z0-9])' + re.escape(t) + r'(?![a-z0-9])')
        _RX[t] = r
    return r

def hits(text, terms):
    return [t for t in terms if _rx(t).search(text)]

def axis1_score(text):
    sor = hits(text, A1_SOR_HIGH)
    comm = hits(text, A1_SOR_COMMODITY)
    gap = hits(text, A1_GAP)
    if not sor and not comm:
        return 0, sor, gap
    base = 0
    if sor:
        base = 3 if len(sor) >= 1 else 0
        if len(sor) >= 3:
            base = 4
    elif comm:
        base = 2  # commodity SoR only
    if gap:
        base = min(5, base + 1)
    return base, sor, gap

def axis2_score(text):
    s = len(hits(text, A2_STRONG))
    m = len(hits(text, A2_MEDIUM))
    w = min(2, len(hits(text, A2_WEAK)))
    raw = s * 2 + m * 1 + w * 0.5
    if raw == 0:
        sc = 0
    elif raw <= 1.5:
        sc = 1
    elif raw <= 3:
        sc = 2
    elif raw <= 5:
        sc = 3
    elif raw <= 7:
        sc = 4
    else:
        sc = 5
    if sc >= 3 and s == 0:   # require a STRONG signal to clear 3
        sc = 2
    return sc, s, m

def main():
    n = kept = 0
    rows_out = []
    with open(IN, newline="", encoding="utf-8", errors="replace") as f:
        r = csv.DictReader(f)
        for row in r:
            n += 1
            if row.get("Country", "") != "United States":
                continue
            fund = row.get("Total Funding Range", "")
            size = row.get("Employee Size Range", "")
            in_band = fund in FUNDING_A
            edge = fund in FUNDING_EDGE
            if not (in_band or edge):
                continue
            if size and size not in SIZE_OK and "Self-employed" not in size:
                # allow blank size; drop clearly-too-big
                if any(b in size for b in ["501-1,000", "1,001-5,000", "5,001-10,000", "10,001+"]):
                    continue
            text = " ".join([
                row.get("Industry", ""), row.get("SubIndustry", ""),
                row.get("Description", ""), row.get("Specialties", ""),
                row.get("Derived Description", ""),
            ]).lower()
            ind = row.get("Industry", "").lower()

            a1, sor, gap = axis1_score(text)
            a2, strong, med = axis2_score(text)
            if a1 == 0 and a2 == 0:
                continue

            vendor = bool(hits(text, VENDOR_PATTERNS))
            service = any(si in ind for si in SERVICE_INDUSTRIES)

            funding_w = 1.0 if in_band else 0.4
            composite = a1 * 2.0 + a2 * 1.0 + funding_w
            if vendor:
                composite -= 4.0
            if service:
                composite -= 1.5

            kept += 1
            rows_out.append({
                "Domain": row.get("Domain", ""),
                "Company Name": row.get("Company Name", ""),
                "LinkedIn Company URL": row.get("LinkedIn Company URL", ""),
                "Industry": row.get("Industry", ""),
                "SubIndustry": row.get("SubIndustry", ""),
                "Employee Size Range": size,
                "Total Funding Range": fund,
                "Founded": row.get("Founded", ""),
                "Locality": row.get("Locality", ""),
                "axis1_key_integration": a1,
                "axis1_sor_hits": "|".join(sor)[:200],
                "axis1_gap_hits": "|".join(gap)[:200],
                "axis2_complexity": a2,
                "axis2_strong_hits": strong,
                "is_integration_vendor": int(vendor),
                "is_service_firm": int(service),
                "composite_stage1": round(composite, 2),
                "Description": (row.get("Description", "") or "")[:500].replace("\n", " "),
            })
    rows_out.sort(key=lambda x: x["composite_stage1"], reverse=True)
    cols = list(rows_out[0].keys())
    with open(OUT_ALL, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows_out)
    # top candidates = not a vendor, not a service firm, composite>=6
    top = [x for x in rows_out if not x["is_integration_vendor"] and not x["is_service_firm"]
           and x["composite_stage1"] >= 6][:1200]
    with open(OUT_TOP, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(top)

    print(f"scanned rows           : {n}")
    print(f"US + Series-A-band cohort scored (a1 or a2 >0): {kept}")
    print(f"integration vendors flagged: {sum(x['is_integration_vendor'] for x in rows_out)}")
    print(f"service firms flagged      : {sum(x['is_service_firm'] for x in rows_out)}")
    print(f"top candidates (clean, composite>=6): {len(top)}")
    print("\n=== TOP 25 PREVIEW ===")
    for x in top[:25]:
        print(f"  {x['composite_stage1']:5} a1={x['axis1_key_integration']} a2={x['axis2_complexity']} "
              f"| {x['Company Name'][:32]:34} | {x['Industry'][:26]:28} | {x['axis1_sor_hits'][:40]}")

if __name__ == "__main__":
    main()
