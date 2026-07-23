#!/usr/bin/env python3
"""Channel B: Exa Agent API (POST /agent/runs) — async defense-tech list building.

create : kick off 5 agent runs (one per ICP domain) with a structured schema
poll   : check status, save completed outputs to checkpoints/exa_agent_runs.jsonl
more   : continue completed runs via previousRunId ("find 25 more")

Adapted from prospecting-ben/scripts/s2_exa_agent.py.
Usage: python3 s2_exa_agent.py create|poll|more
"""
import json
import sys
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
                    "funding_stage": {"type": "string"},
                    "funding_summary": {"type": "string"},
                    "domain_category": {
                        "type": "string",
                        "enum": ["mobile", "sensors", "data_collection",
                                 "ai_ml", "cyber", "other"]},
                    "dod_evidence": {"type": "string"},
                    "product_status": {
                        "type": "string",
                        "enum": ["prototype", "pilot", "fielded", "unknown"]},
                    "evidence_url": {"type": "string"}
                },
                "required": ["name", "website", "dod_evidence"]
            }
        }
    },
    "required": ["companies"]
}

COMMON = ("Exclude large defense primes (Lockheed, RTX, Boeing, Northrop, General "
          "Dynamics, L3Harris, BAE, Leidos, Booz Allen, SAIC, CACI), federal systems "
          "integrators, staffing agencies, and services-only consultancies. For each "
          "company: name, website, HQ city/state, employee estimate, funding stage, "
          "funding summary, domain category, one sentence of evidence they sell to "
          "DoD/military, product status (prototype/pilot/fielded), and one evidence URL.")

QUERIES = [
    ("ai-ml-isr",
     "List US-headquartered pre-seed, seed, or Series A defense technology startups "
     "applying AI/ML or computer vision to ISR, sensor data analytics, object/anomaly "
     "detection, or intelligence analysis, that have a working prototype or pilot and "
     "stated DoD/military customers, SBIR awards, or defense accelerator ties "
     "(AFWERX, DIU, SOFWERX, NSIN). " + COMMON),
    ("tactical-mobile-edge",
     "List US early-stage startups (pre-seed through Series A, or small bootstrapped "
     "firms under ~$20M revenue) building tactical mobile software, situational "
     "awareness apps, mission planning tools, ATAK/TAK-adjacent software, or edge "
     "computing for dismounted military operators and tactical units. " + COMMON),
    ("sensors-data-collection",
     "List US early-stage companies with sensor hardware+software prototypes or field "
     "data-collection products aimed at DoD or military users: unattended ground "
     "sensors, wearables for warfighters, RF/spectrum sensing, environmental sensing, "
     "drone-mounted sensors, or ISR payloads. Pre-seed through Series A preferred. "
     + COMMON),
    ("defense-cyber",
     "List US seed or Series A cybersecurity product companies whose stated market is "
     "DoD, the intelligence community, weapon systems, or the defense industrial base "
     "(not general enterprise security): tactical network security, cross-domain "
     "solutions, embedded/weapon-system security, OT security for military platforms. "
     + COMMON),
    ("sbir-graduates-raising",
     "List US companies that won a Department of Defense SBIR or STTR Phase II award "
     "since 2022 in AI/ML, sensors, mobile/edge software, data collection, or "
     "cybersecurity AND have raised venture funding (pre-seed to Series A), whose "
     "product is still pre-production — a prototype or pilot not yet a program of "
     "record. " + COMMON),
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
        if run.get("continued") or run["tag"].endswith("-more"):
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
