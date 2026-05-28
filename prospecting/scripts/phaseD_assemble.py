#!/usr/bin/env python3
"""
Phase C+D — join Stage1 scores + Phase A (contacts/team) + Phase B (jobs),
compute composite PAIN score, keep/drop, write evidence-grounded opener +
"why I believed" (message = redescription of the targeting), and emit:
  prospecting/output/companies_by_pain.csv  (sorted by pain)
  prospecting/output/people.csv             (CEO/COO + top technical contacts)
"""
import csv, os, json, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def p(*a): return os.path.join(ROOT, *a)
os.makedirs(p("output"), exist_ok=True)

stage1 = {r["Domain"]: r for r in csv.DictReader(open(p("data", "stage1_top_candidates.csv"), encoding="utf-8"))}
A = {}
for ln in open(p("checkpoints", "phaseA.jsonl"), encoding="utf-8"):
    try:
        r = json.loads(ln); A[r.get("domain")] = r
    except Exception: pass
B = {}
if os.path.exists(p("checkpoints", "phaseB.jsonl")):
    for ln in open(p("checkpoints", "phaseB.jsonl"), encoding="utf-8"):
        try:
            r = json.loads(ln); B[r.get("domain")] = r
        except Exception: pass
B2 = {}  # Apify LinkedIn-jobs pass (no-ATS companies)
if os.path.exists(p("checkpoints", "phaseB_apify.jsonl")):
    for ln in open(p("checkpoints", "phaseB_apify.jsonl"), encoding="utf-8"):
        try:
            r = json.loads(ln); B2[r.get("domain")] = r
        except Exception: pass
FE = {}  # FullEnrich email/phone fill, keyed by person linkedin_url
if os.path.exists(p("checkpoints", "phaseA2_fullenrich.jsonl")):
    for ln in open(p("checkpoints", "phaseA2_fullenrich.jsonl"), encoding="utf-8"):
        try:
            r = json.loads(ln); FE[r.get("linkedin_url")] = r
        except Exception: pass

def fill_contact(person):
    """Fill missing email/phone from FullEnrich by the person's LinkedIn URL."""
    li = person.get("linkedin")
    if li and li in FE:
        if not person.get("email"): person["email"] = FE[li].get("email", "") or ""
        if not person.get("phone"): person["phone"] = FE[li].get("phone", "") or ""
    return person

# readable label for the integration opportunity from named SoR hits
SOR_LABEL = [
    (("epic", "athenahealth", "cerner", "hl7", "fhir", "interoperability", "emr", "ehr"), "EHR/clinical-data integration (Epic/athena/HL7-FHIR)"),
    (("edi", "x12", "837", "835", "clearinghouse", "claims"), "claims/EDI integration"),
    (("workday", "hris"), "Workday/HRIS integration"),
    (("salesforce", "appexchange", "health cloud"), "Salesforce integration"),
    (("netsuite", "sap", "dynamics 365", "microsoft dynamics", "erp"), "ERP integration (NetSuite/SAP/Dynamics)"),
    (("servicenow",), "ServiceNow integration"),
    (("snowflake", "databricks"), "data-warehouse integration (Snowflake/Databricks)"),
    (("veeva",), "Veeva Vault integration"),
    (("guidewire", "duck creek"), "insurance-core integration"),
    (("procore",), "Procore/construction integration"),
]
def opportunity(sor_hits):
    h = (sor_hits or "").lower()
    for keys, label in SOR_LABEL:
        if any(k in h for k in keys):
            return label
    return "system-to-system integration"

def first_name(n): return (n or "").split()[0] if n else ""

def build():
    companies, people = [], []
    kept = dropped = 0
    for dom, s in stage1.items():
        a = A.get(dom, {}); b = B.get(dom, {}); b2 = B2.get(dom, {})
        try: a1 = int(s.get("axis1_key_integration") or 0)
        except: a1 = 0
        try: a2 = int(s.get("axis2_complexity") or 0)
        except: a2 = 0
        # take the stronger of the free-ATS signal and the Apify signal
        jobs_pain = max(int(b.get("jobs_pain_score") or 0), int(b2.get("jobs_pain_score") or 0))
        integ_jobs = max(int(b.get("integration_jobs") or 0), int(b2.get("integration_jobs") or 0))
        silo_jobs = max(int(b.get("silo_jobs") or 0), int(b2.get("silo_jobs") or 0))
        if not b.get("integration_titles") and b2.get("integration_titles"):
            b = {**b, "integration_titles": b2.get("integration_titles"), "ats": "linkedin(apify)"}
        ft_cto = a.get("has_full_time_cto", "")
        no_cto = (ft_cto == "no")
        # keep/drop: require SOME integration relevance or silo/jobs pain
        if a1 == 0 and a2 <= 1 and jobs_pain == 0:
            dropped += 1; continue
        kept += 1
        # composite pain (leadership gap is a booster)
        pain = round(2.0*a1 + 1.5*a2 + 1.0*jobs_pain + 0.5*min(integ_jobs,4) + (3.0 if no_cto else 0.0), 2)
        opp = opportunity(s.get("axis1_sor_hits"))
        ceo = fill_contact(a.get("ceo") or {}); coo = fill_contact(a.get("coo") or {})
        dm = ceo if ceo.get("name") else coo
        fn = first_name(dm.get("name"))
        tech_ratio = a.get("technical_ratio", ""); tech_count = a.get("tech_count", "")
        total_emp = a.get("total_employees", "")
        # why I believed (evidence)
        ev = []
        if s.get("axis1_sor_hits"): ev.append(f"depends on {s['axis1_sor_hits'].replace('|', ', ')}")
        if a2 >= 3: ev.append("multi-platform / high integration surface")
        if integ_jobs: ev.append(f"hiring {integ_jobs} integration/API role(s)" + (f" ({b.get('integration_titles','')[:80]})" if b.get('integration_titles') else ""))
        if silo_jobs: ev.append(f"{silo_jobs} ops/data-entry role(s) = silo pain")
        if no_cto: ev.append("no full-time CTO detected")
        if tech_count and total_emp: ev.append(f"{tech_count} technical of ~{total_emp} staff (ratio {tech_ratio})")
        why = "; ".join(ev)
        # opener (message = redescription of the targeting)
        hook = []
        if no_cto: hook.append("you've got engineers but no full-time technical lead")
        if integ_jobs: hook.append("you're hiring for integration work")
        elif a1 >= 3: hook.append(f"{opp} looks central to your growth")
        hook_txt = " and ".join(hook) if hook else f"{opp} looks central to your roadmap"
        greeting = f"Hi {fn}," if fn else "Hi there,"
        opener = (f"{greeting} I work as a fractional CTO on exactly your situation — "
                  f"{s.get('Company Name','your company')} where {hook_txt}. I led {opp.split('(')[0].strip()} "
                  f"work at Veeva for a decade; I'd love to show how I'd ship it without stalling your roadmap.")
        companies.append({
            "rank": 0, "pain_score": pain, "company": s.get("Company Name", ""), "domain": dom,
            "linkedin_company": a.get("linkedin_company", s.get("LinkedIn Company URL", "")),
            "integration_opportunity": opp, "axis1_key_integration": a1, "axis2_complexity": a2,
            "sor_hits": s.get("axis1_sor_hits", ""), "jobs_pain_score": jobs_pain,
            "integration_jobs": integ_jobs, "integration_job_titles": b.get("integration_titles", ""),
            "silo_jobs": silo_jobs, "silo_job_titles": b.get("silo_titles", ""), "ats": b.get("ats", ""),
            "has_full_time_cto": ft_cto, "leadership_count": a.get("leadership_count", ""),
            "tech_count": tech_count, "total_employees": total_emp, "technical_ratio": tech_ratio,
            "funding_range": s.get("Total Funding Range", ""), "industry": s.get("Industry", ""),
            "decision_maker": dm.get("name", ""), "dm_title": dm.get("title", ""),
            "dm_email": dm.get("email", ""), "dm_email_domain_ok": dm.get("email_domain_ok", ""),
            "dm_phone": dm.get("phone", ""), "why_i_believed": why, "opener": opener,
        })
        # people rows: CEO, COO, top technical
        for role, person in (("CEO", ceo), ("COO", coo)):
            if person.get("name"):
                people.append({"company": s.get("Company Name", ""), "domain": dom, "role_type": role,
                               "name": person.get("name", ""), "title": person.get("title", ""),
                               "email": person.get("email", ""), "email_domain_ok": person.get("email_domain_ok", ""),
                               "phone": person.get("phone", ""), "linkedin": person.get("linkedin", "")})
        for t in (a.get("top_technical") or [])[:8]:
            if t.get("name"):
                people.append({"company": s.get("Company Name", ""), "domain": dom, "role_type": "technical",
                               "name": t.get("name", ""), "title": t.get("title", ""), "email": "",
                               "email_domain_ok": "", "phone": "", "linkedin": t.get("linkedin", "")})
    companies.sort(key=lambda x: x["pain_score"], reverse=True)
    for i, c in enumerate(companies, 1): c["rank"] = i
    with open(p("output", "companies_by_pain.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(companies[0].keys())); w.writeheader(); w.writerows(companies)
    with open(p("output", "people.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(people[0].keys())); w.writeheader(); w.writerows(people)
    print(f"kept={kept} dropped={dropped}")
    print(f"companies_by_pain.csv = {len(companies)} rows ; people.csv = {len(people)} rows")
    print(f"with decision-maker email: {sum(1 for c in companies if c['dm_email'])}")
    print(f"with decision-maker phone: {sum(1 for c in companies if c['dm_phone'])}")
    print("\n=== TOP 15 BY PAIN ===")
    for c in companies[:15]:
        print(f" #{c['rank']:<3} pain={c['pain_score']:<5} {c['company'][:26]:27} | {c['integration_opportunity'][:34]:35} | CTO={c['has_full_time_cto']:3} | DM={c['decision_maker'][:18]:19} {c['dm_phone']}")

if __name__ == "__main__":
    build()
