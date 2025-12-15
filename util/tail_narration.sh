#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "=== STATUS: NARRATION MONITOR ==="
echo "Press Ctrl+C to stop"
pgrep -af "oanda_trading_engine.py" >/dev/null && echo "Engine running" || echo "WARNING: Engine not running"
echo ""
echo "--- ACTION: Attaching to narration stream ---"
[ -f narration.jsonl ] && tail -f narration.jsonl || ([ -f logs/narration.jsonl ] && tail -f logs/narration.jsonl) || echo "No narration log found yet"
