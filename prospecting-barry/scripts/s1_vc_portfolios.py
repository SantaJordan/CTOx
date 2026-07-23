#!/usr/bin/env python3
"""Channel A: fetch portfolio pages for defense/natsec VC funds into a local cache.

Adapted from prospecting-ben/scripts/s1_vc_portfolio_gather.py (URL templates
+ sitemap + Exa site-search fallback). Output: data/page_cache/<fund>/<n>.html
+ checkpoints/vc_gather_manifest.jsonl. Resume-safe.

Broad funds (a16z, Lux, 8VC, IQT) are flagged broad=True so the extraction
agent applies a strict defense-only filter.

Usage: uv run --with aiohttp python3 s1_vc_portfolios.py
"""
import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, load_env  # noqa: E402

try:
    import aiohttp
except ImportError:
    print("run with: uv run --with aiohttp python3 ...")
    sys.exit(1)

CACHE = ROOT / "data" / "page_cache"
MANIFEST = ROOT / "checkpoints" / "vc_gather_manifest.jsonl"
AS_OF = time.strftime("%Y-%m-%d")

# (fund_id, name, domain, broad) — broad funds need strict defense-only extraction.
FUNDS = [
    ("shield", "Shield Capital", "shieldcap.com", False),
    ("decisive-point", "Decisive Point", "decisivepoint.com", False),
    ("razors-edge", "Razor's Edge Ventures", "razorsvc.com", False),
    ("marque", "Marque Ventures", "marque.vc", False),
    ("booz-ventures", "Booz Allen Ventures", "boozallen.com", False),
    ("aei-horizonx", "AEI HorizonX", "aeindustrial.com", False),
    ("silent", "Silent Ventures", "silent.vc", False),
    ("harpoon", "Harpoon Ventures", "harpoonvc.com", False),
    ("red-cell", "Red Cell Partners", "redcellpartners.com", False),
    ("scout", "Scout Ventures", "scoutventures.com", False),
    ("new-north", "New North Ventures", "newnorthventures.com", False),
    ("iqt", "In-Q-Tel", "iqt.org", True),
    ("a16z-ad", "a16z American Dynamism", "a16z.com", True),
    ("lux", "Lux Capital", "luxcapital.com", True),
    ("8vc", "8VC", "8vc.com", True),
]

PATHS = ["/portfolio", "/companies", "/investments", "/portfolio-companies",
         "/our-companies", "/ventures", "/portfolio/", "/companies/", "/fund"]
SITEMAP_RE = re.compile(r"<loc>([^<]*(?:portfolio|companies|investments|ventures)[^<]*)</loc>", re.I)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
CONCURRENCY = 10


def text_len(html):
    return len(re.sub(r"\s+", " ", re.sub(
        r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>", " ", html)))


async def get(session, url, timeout=25):
    try:
        async with session.get(url, headers=UA,
                               timeout=aiohttp.ClientTimeout(total=timeout),
                               allow_redirects=True, ssl=False) as r:
            if r.status != 200:
                return None, r.status
            return await r.text(errors="replace"), 200
    except Exception:
        return None, "err"


async def exa_portfolio(session, domain, name):
    body = {"query": f"{name} portfolio companies defense national security",
            "numResults": 4, "type": "keyword", "includeDomains": [domain]}
    try:
        async with session.post("https://api.exa.ai/search", json=body, headers={
                "x-api-key": os.environ["EXA_API_KEY"],
                "Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=30)) as r:
            if r.status != 200:
                return []
            data = await r.json()
            return [x.get("url") for x in data.get("results", []) if x.get("url")]
    except Exception:
        return []


async def gather(session, sem, fund_id, name, domain, broad, done):
    if fund_id in done:
        return None
    async with sem:
        rec = {"fund_id": fund_id, "fund_name": name, "domain": domain,
               "broad": broad, "as_of": AS_OF, "pages": [], "status": "no_page_found"}
        base = f"https://{domain}"
        candidates = [base + p for p in PATHS]
        sm, _ = await get(session, base + "/sitemap.xml", timeout=15)
        if sm:
            candidates += SITEMAP_RE.findall(sm)[:8]
        candidates += await exa_portfolio(session, domain, name)
        seen, saved = set(), 0
        outdir = CACHE / fund_id
        for url in candidates:
            u = (url or "").rstrip("/")
            if not u or u in seen or saved >= 4:
                continue
            seen.add(u)
            html, status = await get(session, url)
            if not html:
                continue
            tl = text_len(html)
            outdir.mkdir(parents=True, exist_ok=True)
            fname = f"{saved}.html"
            (outdir / fname).write_text(html, errors="replace")
            rec["pages"].append({"url": url, "file": f"{fund_id}/{fname}",
                                 "text_len": tl, "js_heavy": tl < 800})
            saved += 1
        if saved:
            rec["status"] = ("ok" if any(not p["js_heavy"] for p in rec["pages"])
                             else "js_heavy_only")
        return rec


async def main():
    load_env()
    CACHE.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if MANIFEST.exists():
        for line in MANIFEST.read_text().splitlines():
            try:
                done.add(json.loads(line)["fund_id"])
            except json.JSONDecodeError:
                pass
    print(f"{len(FUNDS)} funds; {len(done)} already gathered")
    sem = asyncio.Semaphore(CONCURRENCY)
    async with aiohttp.ClientSession() as session:
        tasks = [gather(session, sem, fid, n, d, b, done) for fid, n, d, b in FUNDS]
        with open(MANIFEST, "a") as out:
            for coro in asyncio.as_completed(tasks):
                rec = await coro
                if rec:
                    out.write(json.dumps(rec) + "\n")
                    out.flush()
                    print(f"  {rec['fund_id']}: {rec['status']} "
                          f"({len(rec['pages'])} pages)")


if __name__ == "__main__":
    asyncio.run(main())
