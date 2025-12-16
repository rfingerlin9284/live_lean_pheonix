#!/usr/bin/env python3
"""RBZ toggle CLI (simple, safe).

Edits the JSON toggles file used by the engine.
Defaults to config/toggles.json unless PHX_TOGGLES_PATH/TOGGLES_PATH is set.

Examples:
  python3 tools/rbzctl.py status
  python3 tools/rbzctl.py get exit_mode
  python3 tools/rbzctl.py set exit_mode edge_hybrid
  python3 tools/rbzctl.py set aggressive_enabled false
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def _toggles_path() -> Path:
    env = os.getenv("PHX_TOGGLES_PATH") or os.getenv("TOGGLES_PATH")
    if env:
        return Path(env)
    return Path("config/toggles.json")


def _read_json(path: Path) -> dict:
    try:
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def _parse_value(raw: str) -> Any:
    # Try JSON parsing first (true/false/null/numbers/arrays/objects/strings)
    try:
        return json.loads(raw)
    except Exception:
        return raw


def main() -> int:
    ap = argparse.ArgumentParser(prog="rbzctl", description="RBOTZILLA toggles controller")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Print current toggles")

    g = sub.add_parser("get", help="Get one key")
    g.add_argument("key")

    s = sub.add_parser("set", help="Set one key")
    s.add_argument("key")
    s.add_argument("value")

    args = ap.parse_args()
    path = _toggles_path()
    data = _read_json(path)

    if args.cmd == "status":
        print(f"toggles_path: {path}")
        print(json.dumps(data, indent=2, sort_keys=False))
        return 0

    if args.cmd == "get":
        if args.key not in data:
            raise SystemExit(f"Key not found: {args.key}")
        print(json.dumps(data.get(args.key), indent=2, sort_keys=False))
        return 0

    if args.cmd == "set":
        val = _parse_value(args.value)
        data[args.key] = val
        _write_json(path, data)
        print(f"OK set {args.key} = {val!r} in {path}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
