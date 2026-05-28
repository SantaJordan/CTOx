#!/usr/bin/env python3
"""
Phase A — deterministic Blitz enrichment over the Stage-1 candidate set.
Per company: tech-team count + ratio + top technical contacts, leadership count,
has_full_time_cto, CEO + COO decision-makers with email + phone (domain-guarded).

Resumable: appends one JSON line per company to prospecting/checkpoints/phaseA.jsonl.
Usage: python3 phaseA_enrich.py [LIMIT]   (no LIMIT = all)
"""
import csv, os, sys, json, time, threading, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV = os.path.join(ROOT, "..", ".env")
IN = os.path.join(ROOT, "data", "stage1_top_candidates.csv")
CKPT = os.path.join(ROOT, "checkpoints", "phaseA.jsonl")
OUT = os.path.join(ROOT, "data", "phaseA_enriched.csv")
BASE = "https://api.blitz-api.ai"

KEY = None
for line in open(ENV, encoding="utf-8"):
    if line.startswith("BLITZ_API_KEY="):
        KEY = line.strip().split("=", 1)[1]
assert KEY, "BLITZ_API_KEY missing"

_lock = threading.Lock()

def post(path, body, tries=3):
    data = json.dumps(body).encode()
    for i in range(tries):
        req = urllib.request.Request(BASE + path, data=data,
            headers={"x-api-key": KEY, "content-type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < tries - 1:
                time.sleep(1.5 * (i + 1)); continue
            return {"_error": e.code}
        except Exception:
            if i < tries - 1:
                time.sleep(1.0); continue
            return {"_error": "timeout"}
    return {"_error": "exhausted"}

def empfind(url, funcs, levels=None, n=25):
    b = {"company_linkedin_url": url, "max_results": n, "page": 1,
         "country_code": ["US"], "job_function": funcs}
    if levels:
        b["job_level"] = levels
    return post("/v2/search/employee-finder", b)

def waterfall(url, titles, n=1):
    return post("/v2/search/waterfall-icp-keyword", {
        "company_linkedin_url": url,
        "cascade": [{"include_title": titles, "exclude_title": ["assistant", "intern"],
                     "location": ["WORLD"], "include_headline_search": True}],
        "max_results": n})

def cur_title(person):
    for e in person.get("experiences", []):
        if e.get("job_is_current"):
            return (e.get("job_title") or "").strip()
    return (person.get("headline") or "").strip()

def contact(person, company_domain):
    pl = person.get("linkedin_url", "")
    email = phone = ""; dom_ok = ""
    if pl:
        em = post("/v2/enrichment/email", {"person_linkedin_url": pl})
        if isinstance(em, dict) and "_error" not in em:
            email = em.get("email") or (em.get("all_emails") or [""])[0] or ""
        ph = post("/v2/enrichment/phone", {"person_linkedin_url": pl})
        if isinstance(ph, dict) and "_error" not in ph:
            phone = ph.get("phone") or ""
    if email and company_domain:
        dom_ok = "yes" if email.split("@")[-1].lower().endswith(company_domain.lower()) else "no"
    return {"name": person.get("full_name", ""), "title": cur_title(person),
            "linkedin": pl, "email": email, "email_domain_ok": dom_ok, "phone": phone}

LEAD_TITLES = ["chief technology officer", "cto", "vp engineering", "vp of engineering",
               "head of engineering", "chief technical officer", "vp technology"]

def enrich(row):
    dom = (row.get("Domain") or "").strip()
    url = (row.get("LinkedIn Company URL") or "").strip()
    rec = {"domain": dom, "company": row.get("Company Name", ""),
           "linkedin_company": url, "size_range": row.get("Employee Size Range", ""),
           "funding": row.get("Total Funding Range", ""),
           "axis1": row.get("axis1_key_integration", ""), "axis2": row.get("axis2_complexity", ""),
           "sor_hits": row.get("axis1_sor_hits", ""), "industry": row.get("Industry", "")}
    if not url and dom:
        r = post("/v2/enrichment/domain-to-linkedin", {"domain": dom})
        url = r.get("company_linkedin_url", "") if isinstance(r, dict) else ""
        rec["linkedin_company"] = url
    if not url:
        rec["status"] = "no_linkedin"; return rec

    co = post("/v2/enrichment/company", {"company_linkedin_url": url})
    total_emp = (co.get("company", {}) or {}).get("employees_on_linkedin") if isinstance(co, dict) else None
    rec["total_employees"] = total_emp or ""

    PAGE = 10
    tech = empfind(url, ["Engineering", "Information Technology"], n=PAGE)
    tech_people, tech_count = [], ""
    if isinstance(tech, dict) and "_error" not in tech:
        tp = tech.get("total_pages", 0) or 0
        rl = tech.get("results_length", 0) or 0
        tech_count = tp * PAGE if tp and tp > 1 else rl   # estimate (total_pages*page_size)
        for x in tech.get("results", []):
            p = x.get("person", {})
            tech_people.append({"name": p.get("full_name", ""), "title": cur_title(p),
                                "linkedin": p.get("linkedin_url", "")})
    rec["tech_count"] = tech_count
    try:
        rec["technical_ratio"] = round(int(tech_count) / int(total_emp), 3) if tech_count and total_emp else ""
    except Exception:
        rec["technical_ratio"] = ""

    # leadership + CTO detection via waterfall (reliable on small companies; employee-finder is sparse)
    lead = waterfall(url, ["Chief Technology Officer", "CTO", "VP Engineering", "VP of Engineering",
                           "Head of Engineering", "Chief Technical Officer", "Director of Engineering",
                           "Engineering Manager", "Lead Engineer"], 8)
    leads, has_cto = [], "no"
    if isinstance(lead, dict) and "_error" not in lead:
        rec["leadership_count"] = lead.get("results_length", "")
        for x in lead.get("results", []):
            p = x.get("person", {}); t = cur_title(p).lower()
            leads.append({"name": p.get("full_name", ""), "title": cur_title(p),
                          "linkedin": p.get("linkedin_url", "")})
            if any(k in t for k in LEAD_TITLES):
                has_cto = "yes"
    rec["has_full_time_cto"] = has_cto
    # top ~8 technical contacts: leadership first, then ICs, dedup by linkedin
    seen, top = set(), []
    for p in leads + tech_people:
        k = p["linkedin"] or p["name"]
        if k and k not in seen:
            seen.add(k); top.append(p)
        if len(top) >= 8:
            break
    rec["top_technical"] = top

    ceo = waterfall(url, ["CEO", "Chief Executive Officer", "Founder", "Co-Founder", "President"], 1)
    coo = waterfall(url, ["COO", "Chief Operating Officer", "VP Operations", "Head of Operations"], 1)
    rec["ceo"] = contact(ceo["results"][0]["person"], dom) if (isinstance(ceo, dict) and ceo.get("results")) else {}
    rec["coo"] = contact(coo["results"][0]["person"], dom) if (isinstance(coo, dict) and coo.get("results")) else {}
    rec["status"] = "ok"
    return rec

def main(limit=None):
    rows = list(csv.DictReader(open(IN, encoding="utf-8")))
    if limit:
        rows = rows[:limit]
    done = set()
    if os.path.exists(CKPT):
        for ln in open(CKPT, encoding="utf-8"):
            try:
                done.add(json.loads(ln).get("domain"))
            except Exception:
                pass
    todo = [r for r in rows if (r.get("Domain") or "").strip() not in done]
    print(f"total={len(rows)} done={len(done)} todo={len(todo)}")
    n = 0
    with ThreadPoolExecutor(max_workers=20) as ex:
        futs = {ex.submit(enrich, r): r for r in todo}
        for f in as_completed(futs):
            rec = f.result()
            with _lock:
                with open(CKPT, "a", encoding="utf-8") as ck:
                    ck.write(json.dumps(rec) + "\n")
            n += 1
            if n % 25 == 0:
                print(f"  {n}/{len(todo)} done", flush=True)
    print(f"enriched {n} new companies -> {CKPT}")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
