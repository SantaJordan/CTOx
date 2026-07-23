"""s1 — pull each CTO's full profile from FullEnrich (LinkedIn URL as data).

Writes checkpoints/cto_enrich/<slug>.json with the raw API response.
Resumable: skips slugs that already have a file. Never prints key values.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_common import key, http_json, checkpoint_path, load_ctos, say

BASE = "https://app.fullenrich.com/api/v2"


def fetch_profile(headers, linkedin_url):
    # Preferred: direct lookup by LinkedIn URL.
    for body in (
        {"person_professional_network_url": linkedin_url},
        {"professional_network_url": linkedin_url},
        {"linkedin_url": linkedin_url},
    ):
        try:
            resp = http_json(f"{BASE}/people/lookup", body, headers, retries=1)
            if resp and (resp.get("person") or resp.get("full_name") or resp.get("id")):
                return {"source": "people/lookup", "response": resp}
        except RuntimeError:
            continue
    # Fallback: search with the live-verified filter shape.
    resp = http_json(f"{BASE}/people/search", {
        "person_professional_network_urls": [{"value": linkedin_url}],
        "limit": 1,
    }, headers)
    return {"source": "people/search", "response": resp}


def main():
    headers = {"Authorization": f"Bearer {key('FULLENRICH_API_KEY')}"}
    ok, failed = 0, []
    for cto in load_ctos():
        out = checkpoint_path("cto_enrich", f"{cto['slug']}.json")
        if out.exists():
            say(f"{cto['name']}: already pulled, skipping")
            ok += 1
            continue
        say(f"{cto['name']}: pulling profile from FullEnrich…")
        try:
            result = fetch_profile(headers, cto["linkedin_url"])
            result["cto"] = cto
            out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
            n_jobs = "?"
            try:
                persons = result["response"].get("persons") or [result["response"].get("person") or result["response"]]
                n_jobs = len((persons[0].get("employment") or {}).get("all") or [])
            except Exception:
                pass
            say(f"{cto['name']}: saved ({n_jobs} career positions found)")
            ok += 1
        except Exception as e:
            failed.append(cto["slug"])
            say(f"{cto['name']}: FAILED — {e}")
    say(f"Done: {ok}/{len(load_ctos())} profiles saved" + (f"; failed: {', '.join(failed)}" if failed else ""))


if __name__ == "__main__":
    main()
