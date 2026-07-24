#!/usr/bin/env python3
"""Stage 3: build one evidence pack per verified company so the disconnect-scoring
agents judge identical evidence instead of each re-searching the world.
Output : research/packs/<slug>.md  + checkpoints/packs_manifest.jsonl (resume-safe)
Usage: python3 s6_build_packs.py [--limit N]
"""
import csv
import json
import re
import sys
import concurrent.futures as cf
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (ROOT, REPO, load_env, post_json, exa_headers,  # noqa: E402
                    blitz_headers, append_jsonl, read_jsonl, norm_domain)

IN = ROOT / "data" / "universe_verified.csv"
PACKS = ROOT / "research" / "packs"
MANIFEST = ROOT / "checkpoints" / "packs_manifest.jsonl"
SBIR = ROOT / "checkpoints" / "sbir_awards.jsonl"
JOBS_JSONL = REPO / "prospecting-ctox" / "checkpoints" / "match" / "barry-hess_jobs.jsonl"
BLITZ = "https://api.blitz-api.ai/v2"

MAX_SITE_CHARS = 6000
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)")


def slugify(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")[:60]


def scrub(text):
    return PHONE_RE.sub("[phone]", EMAIL_RE.sub("[email]", text or ""))


def nkey(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())[:40]


def fetch_site(domain):
    try:
        r = post_json("https://api.exa.ai/contents",
                      {"urls": [f"https://{domain}"],
                       "text": {"maxCharacters": MAX_SITE_CHARS},
                       "livecrawl": "preferred",
                       "subpages": 3,
                       "subpageTarget": ["product", "technology", "solutions", "about"]},
                      exa_headers(), timeout=90)
        chunks = []
        for res in r.get("results") or []:
            if res.get("text"):
                chunks.append(f"URL: {res.get('url')}\n{res['text']}")
            for sp in res.get("subpages") or []:
                if sp.get("text"):
                    chunks.append(f"URL: {sp.get('url')}\n{sp['text'][:2500]}")
        return "\n\n".join(chunks)[:MAX_SITE_CHARS + 4000]
    except Exception as e:
        return f"(site fetch failed: {e})"


def fetch_news(name):
    try:
        r = post_json("https://api.exa.ai/search",
                      {"query": f"{name} defense funding contract award",
                       "numResults": 3, "type": "auto", "category": "news",
                       "contents": {"text": {"maxCharacters": 700}}},
                      exa_headers(), timeout=60)
        out = []
        for res in r.get("results") or []:
            out.append(f"- {res.get('title','')} ({res.get('publishedDate','')[:10]}) "
                       f"{res.get('url','')}\n  {(res.get('text') or '')[:500]}")
        return "\n".join(out)
    except Exception as e:
        return f"(news fetch failed: {e})"


def fetch_jobs(li_url):
    if not li_url:
        return []
    try:
        r = post_json(f"{BLITZ}/jobs/company",
                      {"company_linkedin_url": li_url, "job": {}},
                      blitz_headers(), timeout=120)
        jobs = r.get("results") or r.get("jobs") or []
        return [{"title": j.get("title") or j.get("job_title") or "",
                 "location": j.get("location") or ""} for j in jobs][:40]
    except Exception:
        return []


def load_context():
    spec = json.loads((REPO / "prospecting-ctox" / "dossiers" / "barry-hess"
                       / "signal_spec.json").read_text())
    doctrine = (REPO / "prospecting-ctox" / "dossiers" / "DOCTRINE-BRIEF.md").read_text()
    sbir_by_key = {}
    for r in read_jsonl(SBIR):
        sbir_by_key[nkey(r.get("company"))] = r
        if r.get("website"):
            sbir_by_key[norm_domain(r["website"])] = r
    jd_by_slug = {}
    for r in read_jsonl(JOBS_JSONL):
        jd_by_slug.setdefault(r.get("company"), []).append(r)
    return spec, doctrine, sbir_by_key, jd_by_slug


CHECKLIST = """## Deployed-reality checklist (score absence against this)
- **DDIL**: denied/disconnected/intermittent/low-bandwidth comms. Canonical example: an AI
  crowd-detection startup streamed 30fps video; the contested environment had bandwidth for
  1 frame every 5 seconds. One architecture change (frame-rate decoupling) saved the project.
- **SWaP-C**: size, weight, power, cost on the platform actually carried/mounted.
- **ATO/RMF**: Authority to Operate on government networks; STIGs, POA&Ms, IL4/IL5.
- **CMMC / NIST 800-171**: company-level compliance before the contract dies.
- **ITAR/export**: controlled data handling.
- **Operator training & sustainment**: who trains the E-5, who fixes it in the field, spares,
  battery logistics, GFE integration.
- **Advocacy chain**: a champion above the operator level; operators loving it is not adoption.
- **Prime/flow-down mechanics**: subcontract structure, government back-end integration.
- **TAK ecosystem**: if it touches situational awareness and never mentions ATAK/TAK, ask why.
"""


def build_pack(row, spec, doctrine, sbir_by_key, jd_by_slug):
    name = row["name"]
    domain = norm_domain(row.get("blitz_domain") or row.get("domain"))
    slug = slugify(name)
    out = PACKS / f"{slug}.md"
    rec = {"slug": slug, "name": name, "domain": domain}
    try:
        site = fetch_site(domain) if domain else "(no domain known)"
        news = fetch_news(name)
        jobs = fetch_jobs(row.get("linkedin_url"))
        sbir = sbir_by_key.get(domain) or sbir_by_key.get(nkey(name))
        jds = jd_by_slug.get(row.get("name")) or jd_by_slug.get(domain) or []

        own_words = len((site or "").split()) + \
            sum(len((a.get("abstract") or "").split()) for a in (sbir or {}).get("awards", []))

        parts = [f"# Evidence pack: {name}",
                 f"slug: {slug} | domain: {domain} | HQ: {row.get('hq_city','')}, "
                 f"{row.get('hq_state','')} {row.get('hq_country','')} | "
                 f"employees(LI): {row.get('employees_on_linkedin','')} | "
                 f"founded: {row.get('founded_year','')} | stage_band: {row.get('stage_band','')}"
                 f"{' | LATE(151-300)' if row.get('late_flag') in ('True', True) else ''}",
                 f"sources: {row.get('sources','')}",
                 f"industry(LI): {row.get('industry','')} | specialties: {row.get('specialties','')}",
                 f"channel notes: {row.get('notes','')}",
                 f"own-language word count: ~{own_words}",
                 "\n## Their own words (website via Exa, livecrawl-preferred)\n",
                 scrub(site),
                 "\n## LinkedIn about\n", scrub(row.get("about", "")),
                 ]
        if sbir:
            parts.append("\n## SBIR/STTR record (their own abstracts)\n")
            for a in sbir["awards"][:4]:
                parts.append(f"### {a['title']} — {a.get('branch','')} {a['year']} "
                             f"(${a.get('amount','')})\n{scrub(a.get('abstract',''))[:3000]}")
        if news:
            parts.append("\n## News (Exa, top 3)\n" + scrub(news))
        if jobs:
            parts.append("\n## Open roles (Blitz, live)\n" +
                         "\n".join(f"- {j['title']} ({j['location']})" for j in jobs))
        else:
            parts.append("\n## Open roles\n(no jobs data found)")
        if jds:
            parts.append("\n## Matched JDs from jobs corpus (barry-hess signal match)\n")
            for j in jds[:4]:
                parts.append(f"### {j.get('title','')} (score {j.get('score','')})\n"
                             f"{scrub((j.get('jd_head') or j.get('jd_markdown') or '')[:800])}")
        parts += ["\n---\n# Context for the scoring agent (do not re-search)",
                  f"\n## Barry Hess niche\n{spec['niche_statement']}\n\n**EDP:** {spec['edp']}",
                  "\n" + CHECKLIST,
                  "\n## Doctrine\n" + doctrine]
        out.write_text("\n".join(parts), encoding="utf-8")
        rec.update({"status": "ok", "own_words": own_words,
                    "has_sbir": bool(sbir), "n_jobs": len(jobs), "n_jds": len(jds)})
    except Exception as e:
        rec["status"] = f"err:{e}"
    return rec


def main():
    load_env()
    limit = 0
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    PACKS.mkdir(parents=True, exist_ok=True)
    spec, doctrine, sbir_by_key, jd_by_slug = load_context()
    done = {r["slug"] for r in read_jsonl(MANIFEST) if r.get("status") == "ok"}
    rows = [r for r in csv.DictReader(open(IN, encoding="utf-8"))
            if slugify(r["name"]) not in done]
    if limit:
        rows = rows[:limit]
    print(f"packs to build: {len(rows)} (done {len(done)})")
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(build_pack, r, spec, doctrine, sbir_by_key, jd_by_slug)
                for r in rows]
        for fut in cf.as_completed(futs):
            rec = fut.result()
            append_jsonl(MANIFEST, rec)
    ok = [r for r in read_jsonl(MANIFEST) if r.get("status") == "ok"]
    print(f"packs ok: {len(ok)} -> {PACKS}")


if __name__ == "__main__":
    main()
