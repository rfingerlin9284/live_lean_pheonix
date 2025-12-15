#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "=== STATUS: STOPPING ENGINE ==="
if pgrep -af "oanda_trading_engine.py" >/dev/null 2>&1; then
  echo "Found running engine"
  pkill -f "oanda_trading_engine.py" || true
  sleep 1
  pgrep -af "oanda_trading_engine.py" >/dev/null && echo "Engine still running" || echo "Engine stopped"
  echo "--- ACTION: Stop attempted ---"
else
  echo "No engine running"
  echo "--- ACTION: No-op (nothing to stop) ---"
fi
