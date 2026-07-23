#!/usr/bin/env python3
"""Angle C: Exa funding-news sweep — game-studio funding announcements 2023-2026.

Runs a battery of Exa searches (auto type, cheap) across funding-news phrasings
and games-press domains; saves raw hits for downstream extraction.

Output: checkpoints/funding_news_hits.jsonl
Usage: python3 s3_funding_news.py
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (ROOT, load_env, post_json, exa_headers,  # noqa: E402
                    append_jsonl, read_jsonl)

OUT = ROOT / "checkpoints" / "funding_news_hits.jsonl"

NEWS_DOMAINS = ["gamesindustry.biz", "gamedeveloper.com", "venturebeat.com",
                "vgc.videogameschronicle.com", "gamesbeat.com", "techcrunch.com",
                "gamespress.com", "prnewswire.com", "businesswire.com",
                "investgame.net", "naavik.co", "pocketgamer.biz"]

QUERIES = [
    "game studio raises Series A funding to develop debut title",
    "game studio raises seed round new studio founded by veterans first game",
    "game studio announces funding round game in development unannounced title",
    "video game developer raises millions Series B upcoming game pre-launch",
    "new AAA game studio funding round ex-Blizzard ex-Bungie ex-Riot founders",
    "game studio publisher investment milestone funding development agreement",
    "indie game studio raises funding PC console game in production",
    "game studio funding round 2025 debut game early development",
    "game studio funding round 2026 first title in development",
    "US game developer closes funding round to expand team ahead of launch",
]


def main():
    load_env()
    seen_urls = {h["url"] for h in read_jsonl(OUT)}
    total = 0
    for i, q in enumerate(QUERIES):
        for domains in (NEWS_DOMAINS, None):   # domain-scoped + open web
            body = {"query": q, "type": "auto", "numResults": 25,
                    "startPublishedDate": "2023-01-01T00:00:00.000Z",
                    "contents": {"text": {"maxCharacters": 2500}}}
            if domains:
                body["includeDomains"] = domains
            try:
                resp = post_json("https://api.exa.ai/search", body, exa_headers())
            except Exception as e:
                print(f"  query {i} err: {e}")
                continue
            for r in resp.get("results", []):
                url = r.get("url")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                append_jsonl(OUT, {
                    "query": q, "scoped": bool(domains), "url": url,
                    "title": r.get("title"),
                    "published": r.get("publishedDate"),
                    "text": (r.get("text") or "")[:2500]})
                total += 1
        print(f"query {i+1}/{len(QUERIES)} done; total new hits {total}")
        time.sleep(0.3)
    print(f"TOTAL new hits: {total}; file now {len(read_jsonl(OUT))}")


if __name__ == "__main__":
    main()
