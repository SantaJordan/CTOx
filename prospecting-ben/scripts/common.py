#!/usr/bin/env python3
"""Shared helpers for the Ben Cole (Studio Foundations) prospecting pipeline."""
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # prospecting-ben/
REPO = ROOT.parent                                     # CTOx/


def load_env():
    # Repo .env is authoritative and OVERRIDES inherited shell exports (a stale
    # EXA_API_KEY in the shell profile broke /agent/runs with 401).
    loaded = set()
    for envfile in [REPO / ".env", Path.home() / "Desktop/Blueprint-GTM-Skills/.env"]:
        if envfile.exists():
            try:
                for line in envfile.read_text().splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        k, v = k.strip(), v.strip().strip('"').strip("'")
                        if k and v and k not in loaded:
                            os.environ[k] = v
                            loaded.add(k)
            except PermissionError:
                pass


def post_json(url, body, headers, timeout=90):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def get_json(url, headers, timeout=60):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def exa_headers():
    return {"x-api-key": os.environ["EXA_API_KEY"]}


def blitz_headers():
    return {"x-api-key": os.environ["BLITZ_API_KEY"]}


def norm_domain(url_or_domain):
    if not url_or_domain:
        return ""
    d = re.sub(r"^https?://", "", url_or_domain.strip().lower())
    d = d.split("/")[0].split("?")[0]
    return d[4:] if d.startswith("www.") else d


def append_jsonl(path, rec):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def read_jsonl(path):
    out = []
    p = Path(path)
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out
