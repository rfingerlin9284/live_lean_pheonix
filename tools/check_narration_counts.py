#!/usr/bin/env python3
"""Quick narration.jsonl stats.

Used by VS Code task: "Check Narration (tools)".

- Works with the default narration location used by util.narration_logger
- Safe to run while the file is being appended to
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check narration.jsonl event counts")
    parser.add_argument(
        "--file",
        default="narration.jsonl",
        help="Path to narration jsonl (default: narration.jsonl)",
    )
    parser.add_argument(
        "--last",
        type=int,
        default=2000,
        help="Only analyze last N lines (default: 2000)",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        # Common fallback
        alt = Path("logs/narration.jsonl")
        if alt.exists():
            path = alt
        else:
            print(f"narration file not found: {args.file} (also tried {alt})")
            return 2

    try:
        lines = path.read_text(errors="ignore").splitlines()
    except Exception as e:
        print(f"failed to read {path}: {e}")
        return 2

    if args.last > 0:
        lines = lines[-args.last :]

    total = 0
    bad = 0
    counts: Counter[str] = Counter()

    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        total += 1
        try:
            ev = json.loads(ln)
        except Exception:
            bad += 1
            continue
        counts[str(ev.get("event_type") or "UNKNOWN")] += 1

    print(f"File: {path}")
    print(f"Lines analyzed: {total}")
    if bad:
        print(f"Invalid JSON lines: {bad}")

    if not counts:
        print("No events found")
        return 1

    print("\nTop event types:")
    for k, v in counts.most_common(20):
        print(f"  {k:<28} {v}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
