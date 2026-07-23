"""Shared helpers for the prospecting-ctox pipeline.

Env loading (never prints values), HTTP with retries, JSONL checkpoints,
plain-English progress. No hardcoded home paths — everything resolves from
this file's location or $HOME.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # prospecting-ctox/
REPO = ROOT.parent                                      # CTOx repo root
CHECKPOINTS = ROOT / "checkpoints"
DATA = ROOT / "data"
OUTPUT = ROOT / "output"
DOSSIERS = ROOT / "dossiers"
RESEARCH = ROOT / "research" / "companies"

_ENV_CACHE = {}


def load_env():
    """Load keys from CTOx .env, falling back to the Blueprint master .env.

    Returns a dict. NEVER print these values — the audience is watching.
    """
    if _ENV_CACHE:
        return _ENV_CACHE
    candidates = [
        REPO / ".env",
        Path.home() / "Desktop" / "Blueprint-GTM-Skills" / ".env",
    ]
    for path in candidates:
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            _ENV_CACHE.setdefault(k.strip(), v.strip())
    return _ENV_CACHE


def key(name):
    val = load_env().get(name) or os.environ.get(name)
    if not val:
        sys.exit(f"MISSING KEY: {name} (checked project .env and Blueprint .env)")
    return val


def http_json(url, payload=None, headers=None, method=None, retries=4, timeout=60):
    """POST/GET JSON with exponential backoff. Returns parsed JSON or raises."""
    headers = dict(headers or {})
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers.setdefault("Content-Type", "application/json")
    last_err = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers=headers,
                                     method=method or ("POST" if data else "GET"))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")[:500]
            last_err = f"HTTP {e.code}: {body}"
            if e.code == 429:
                time.sleep(60)          # documented Blitz cool-off
                continue
            if e.code >= 500:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"{url} -> {last_err}") from None
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = str(e)
            time.sleep(2 ** attempt)
    raise RuntimeError(f"{url} failed after {retries} tries: {last_err}")


def checkpoint_path(stage, name):
    p = CHECKPOINTS / stage
    p.mkdir(parents=True, exist_ok=True)
    return p / name


def read_jsonl(path):
    if not Path(path).exists():
        return []
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def append_jsonl(path, obj):
    with open(path, "a") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def done_ids(path, id_field="id"):
    return {r.get(id_field) for r in read_jsonl(path)}


def say(msg):
    """Plain-English progress line, flushed immediately."""
    print(msg, flush=True)


def load_ctos():
    return json.loads((ROOT / "ctos.json").read_text())["ctos"]
