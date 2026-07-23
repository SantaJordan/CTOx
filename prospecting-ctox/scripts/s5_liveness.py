# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""s5 — verify matched jobs are still open against each company's live ATS feed.

Feeds are cached (data/ats_cache/) and deduped across CTOs — one fetch serves all.
A job is LIVE iff its apply URL (or id) appears in the current feed.
Companies on ATSes without a free feed are marked liveness=unverified.
The cached feed is also the freshness upgrade: it holds the company's ENTIRE
current job list, which Wave B quotes instead of the 4-week-old snapshot.

Usage: python3 s5_liveness.py [slug ...]   (default: every slug with a match file)
"""
import json
import re
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_common import CHECKPOINTS, DATA, checkpoint_path, read_jsonl, say

CACHE = DATA / "ats_cache"
UA = {"User-Agent": "Mozilla/5.0 (research; contact: blueprintgtm.com)"}

# slug extractors keyed by the dataset's `ats` value; each returns (slug, feed_url)
PATTERNS = {
    "greenhouse": (r"greenhouse\.io/(?:embed/job_app\?for=)?([A-Za-z0-9_-]+)",
                   "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"),
    "lever": (r"lever\.co/([A-Za-z0-9_-]+)",
              "https://api.lever.co/v0/postings/{slug}?mode=json"),
    "ashby": (r"ashbyhq\.com/(?:posting-api/job-board/)?([A-Za-z0-9_.%-]+)",
              "https://api.ashbyhq.com/posting-api/job-board/{slug}"),
    "smartrecruiters": (r"smartrecruiters\.com/([A-Za-z0-9_-]+)",
                        "https://api.smartrecruiters.com/v1/companies/{slug}/postings"),
    "workable": (r"workable\.com/(?:j/)?([A-Za-z0-9_-]+)",
                 "https://apply.workable.com/api/v1/widget/accounts/{slug}"),
    "bamboohr": (r"https?://([A-Za-z0-9-]+)\.bamboohr\.com",
                 "https://{slug}.bamboohr.com/careers/list"),
    "recruitee": (r"https?://([A-Za-z0-9-]+)\.recruitee\.com",
                  "https://{slug}.recruitee.com/api/offers/"),
}


def feed_for(ats, url):
    pat = PATTERNS.get(ats.lower())
    if not pat:
        return None, None
    m = re.search(pat[0], url)
    if not m:
        return None, None
    slug = m.group(1)
    return slug, pat[1].format(slug=slug)


def fetch_feed(ats, slug, feed_url):
    CACHE.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", f"{ats}_{slug}")
    cached = CACHE / f"{safe}.json"
    if cached.exists() and time.time() - cached.stat().st_mtime < 86400:
        return cached.read_text()
    req = urllib.request.Request(feed_url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode(errors="replace")
        cached.write_text(body)
        time.sleep(0.15)
        return body
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        cached.write_text(json.dumps({"_fetch_error": str(e)}))
        return cached.read_text()


def job_live_in_feed(job, feed_text):
    if not feed_text or feed_text.startswith('{"_fetch_error"'):
        return None  # unverifiable
    url = job["url"]
    # normalize: match on the unique posting id portion of the url when present
    tail = url.rstrip("/").split("/")[-1]
    tail = tail.split("?")[0]
    if tail and len(tail) >= 6 and tail in feed_text:
        return True
    if url in feed_text:
        return True
    # fallback: exact title match still in feed (weaker)
    if job["title"] and json.dumps(job["title"])[1:-1] in feed_text:
        return True
    return False


def process_slug(slug):
    jobs = read_jsonl(CHECKPOINTS / "match" / f"{slug}_jobs.jsonl")
    if not jobs:
        say(f"{slug}: no matched jobs file, skipping")
        return
    companies = {}
    for j in jobs:
        companies.setdefault((j["ats"], j["company"]), []).append(j)

    say(f"{slug}: checking {len(companies)} companies against live ATS feeds…")
    results = []

    def check(item):
        (ats, company), cjobs = item
        cslug, feed_url = feed_for(ats, cjobs[0]["url"])
        if not feed_url:
            return {"ats": ats, "company": company, "liveness": "unverified",
                    "live_jobs": [], "jobs": cjobs, "feed_slug": None}
        feed = fetch_feed(ats, cslug, feed_url)
        live = []
        for j in cjobs:
            v = job_live_in_feed(j, feed)
            j["live"] = v
            if v:
                live.append(j)
        status = "live" if live else ("unverified" if any(
            j["live"] is None for j in cjobs) else "dead")
        return {"ats": ats, "company": company, "liveness": status,
                "live_jobs": live, "jobs": cjobs, "feed_slug": cslug}

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(check, companies.items()))

    out = checkpoint_path("live", f"{slug}_companies_live.jsonl")
    out.write_text("")
    n_live = n_dead = n_unv = 0
    with open(out, "a") as f:
        for r in results:
            n_live += r["liveness"] == "live"
            n_dead += r["liveness"] == "dead"
            n_unv += r["liveness"] == "unverified"
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    say(f"{slug}: {n_live} companies still hiring, {n_dead} went dead, "
        f"{n_unv} unverifiable — verified {time.strftime('%Y-%m-%d %H:%M')}")


def main():
    slugs = sys.argv[1:]
    if not slugs:
        slugs = sorted(p.stem.replace("_jobs", "") for p in
                       (CHECKPOINTS / "match").glob("*_jobs.jsonl"))
    for slug in slugs:
        process_slug(slug)


if __name__ == "__main__":
    main()
