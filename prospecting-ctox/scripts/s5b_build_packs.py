# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""s5b — build one evidence-pack file per (cto, company) for the Wave B agents.

Packs combine: the CTO's niche summary, the matched jobs (scores + JD excerpts,
4-week-old snapshot), the liveness verdict, and the company's FRESH full job
list pulled from the cached live ATS feed (titles only). Agents judge identical
evidence instead of each re-searching the world.

Out: research/packs/<cto>/<company_slug>.md
Usage: python3 s5b_build_packs.py <cto-slug> [...]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_common import CHECKPOINTS, DATA, DOSSIERS, ROOT, read_jsonl, say

PACKS = ROOT / "research" / "packs"


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60] or "unknown"


def fresh_titles(ats, feed_slug):
    if not feed_slug:
        return []
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", f"{ats}_{feed_slug}")
    f = DATA / "ats_cache" / f"{safe}.json"
    if not f.exists():
        return []
    text = f.read_text()
    if text.startswith('{"_fetch_error"'):
        return []
    titles = re.findall(r'"(?:title|text|name)"\s*:\s*"([^"]{4,90})"', text)
    seen, out = set(), []
    for t in titles:
        if t not in seen and not t.startswith("http"):
            seen.add(t)
            out.append(t)
    return out[:40]


def run_cto(slug):
    spec = json.loads((DOSSIERS / slug / "signal_spec.json").read_text())
    live = read_jsonl(CHECKPOINTS / "live" / f"{slug}_companies_live.jsonl")
    outdir = PACKS / slug
    outdir.mkdir(parents=True, exist_ok=True)
    n = 0
    for comp in live:
        if comp["liveness"] == "dead":
            continue
        cslug = slugify(comp["company"])
        jobs = comp["live_jobs"] or comp["jobs"]
        lines = [
            f"# Evidence pack — {comp['company']} (for CTO {slug})",
            f"ATS: {comp['ats']} | liveness: {comp['liveness']} | feed slug: {comp.get('feed_slug')}",
            "",
            f"## CTO niche\n{spec.get('niche_statement', '')}",
            f"EDP: {spec.get('edp', '')}",
            "",
            "## Matched jobs (from the 2026-06-25 snapshot; 'live' = re-verified today)",
        ]
        for j in jobs[:4]:
            lines += [
                f"### {j['title']}  [score {j['score']}, live={j.get('live')}]",
                f"apply: {j['url']}",
                f"posted: {j.get('posted_at', '?')} | company_does: {j.get('company_does', '')} | "
                f"industry: {j.get('industry', '')} | stage: {j.get('company_stage', '')}",
                f"signals: strong_title={j['hit_strong']} gap={j['hit_gap']} jd_lexicon={j['hit_jdlex']}",
                "JD excerpt (snapshot):",
                "```",
                (j.get("jd_head") or "")[:1200],
                "```",
            ]
        ft = fresh_titles(comp["ats"], comp.get("feed_slug"))
        if ft:
            lines += ["", "## Company's FULL current job list (fresh, from today's ATS feed)",
                      *[f"- {t}" for t in ft]]
        (outdir / f"{cslug}.md").write_text("\n".join(lines))
        n += 1
    say(f"{slug}: {n} evidence packs -> research/packs/{slug}/")


def main():
    for slug in sys.argv[1:]:
        run_cto(slug)


if __name__ == "__main__":
    main()
