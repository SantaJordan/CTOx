#!/usr/bin/env python3
"""Angle B: Exa Agent API (June 2026, POST /agent/runs) — async list building.

create : kick off N agent runs with a structured output schema
poll   : check status, save completed outputs to checkpoints/exa_agent_runs.jsonl
more   : continue completed runs via previousRunId ("find more")

Usage: python3 s2_exa_agent.py create|poll|more
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (ROOT, load_env, post_json, get_json, exa_headers,  # noqa: E402
                    append_jsonl, read_jsonl)

STATE = ROOT / "checkpoints" / "exa_agent_state.json"
OUT = ROOT / "checkpoints" / "exa_agent_runs.jsonl"

SCHEMA = {
    "type": "object",
    "properties": {
        "companies": {
            "type": "array",
            "maxItems": 25,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "website": {"type": "string", "format": "uri"},
                    "hq_location": {"type": "string"},
                    "employee_estimate": {"type": "string"},
                    "funding_summary": {"type": "string"},
                    "latest_round_date": {"type": "string"},
                    "investors": {"type": "string"},
                    "game_status": {"type": "string"},
                    "evidence_url": {"type": "string"}
                },
                "required": ["name", "website"]
            }
        }
    },
    "required": ["companies"]
}

QUERIES = [
    ("vc-funded-prelaunch",
     "List venture-funded video game development studios headquartered in the United "
     "States with roughly 20-150 employees that raised institutional funding (seed, "
     "Series A, Series B, or a strategic/publisher investment) since 2021 and have NOT "
     "yet launched their debut game (game still in development, pre-launch, in "
     "playtest/early access not counted as launched only if full release pending). "
     "For each: name, website, HQ city/state, employee estimate, funding summary with "
     "amounts, latest round date, investors, current game status, and one evidence URL."),
    ("aaa-veteran-studios",
     "List new game studios founded since 2019 by AAA industry veterans (ex-Blizzard, "
     "Bungie, Riot, Epic, Naughty Dog, 343, Respawn, etc.), headquartered in the United "
     "States, that raised $10M or more in venture or publisher funding and are still in "
     "development on their first title (nothing shipped yet). 20-150 employees. For "
     "each: name, website, HQ, employee estimate, funding summary, latest round date, "
     "investors, game status, evidence URL."),
    ("recent-round-2024-2026",
     "List US-headquartered game studios that announced funding rounds between January "
     "2024 and July 2026 specifically to fund development of an unreleased game "
     "(debut title or flagship title not yet launched). Exclude mobile-only hypercasual "
     "and gambling. Prefer studios with 20-150 employees. For each: name, website, HQ, "
     "employee estimate, funding summary, latest round date, investors, game status, "
     "evidence URL."),
]


def create():
    load_env()
    state = {"runs": []}
    for tag, q in QUERIES:
        body = {"query": q, "effort": "high", "outputSchema": SCHEMA}
        resp = post_json("https://api.exa.ai/agent/runs", body, exa_headers())
        run_id = resp.get("id") or resp.get("runId")
        print(f"created {tag}: {run_id} status={resp.get('status')}")
        state["runs"].append({"tag": tag, "id": run_id, "status": resp.get("status")})
    STATE.write_text(json.dumps(state, indent=2))


def poll():
    load_env()
    state = json.loads(STATE.read_text())
    done_ids = {r.get("run_id") for r in read_jsonl(OUT)}
    pending = 0
    for run in state["runs"]:
        if run["id"] in done_ids:
            continue
        resp = get_json(f"https://api.exa.ai/agent/runs/{run['id']}", exa_headers())
        status = resp.get("status")
        print(f"{run['tag']}: {status} (stop={resp.get('stopReason')})")
        if status in ("completed", "failed", "cancelled"):
            out = resp.get("output") or {}
            append_jsonl(OUT, {
                "run_id": run["id"], "tag": run["tag"], "status": status,
                "stop_reason": resp.get("stopReason"),
                "structured": out.get("structured"),
                "text": (out.get("text") or "")[:2000],
                "usage": resp.get("usage")})
        else:
            pending += 1
    print(f"pending: {pending}")
    return pending


def more():
    """Continue each completed run once to surface additional companies."""
    load_env()
    state = json.loads(STATE.read_text())
    new_runs = []
    for run in state["runs"]:
        if run.get("continued"):
            continue
        body = {"query": "Find 25 MORE companies matching the same criteria, excluding "
                         "every company already returned.",
                "effort": "high", "outputSchema": SCHEMA,
                "previousRunId": run["id"]}
        resp = post_json("https://api.exa.ai/agent/runs", body, exa_headers())
        run_id = resp.get("id") or resp.get("runId")
        print(f"continued {run['tag']}: {run_id}")
        run["continued"] = True
        new_runs.append({"tag": run["tag"] + "-more", "id": run_id,
                         "status": resp.get("status")})
    state["runs"] += new_runs
    STATE.write_text(json.dumps(state, indent=2))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "poll"
    {"create": create, "poll": poll, "more": more}[mode]()
