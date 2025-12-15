#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source .env 2>/dev/null || true
echo "=== STATUS: STARTING OANDA PRACTICE ENGINE ==="
if pgrep -af "oanda_trading_engine.py" >/dev/null 2>&1; then
  echo "Engine already running"
  echo "--- ACTION: No-op (already running) ---"
  exit 0
fi
export RICK_ENV="${RICK_ENV:-practice}"
echo "Starting OANDA engine (env: ${RICK_ENV})"
(setsid nohup python3 -u oanda/oanda_trading_engine.py >/dev/null 2>&1 &)
sleep 2
if pgrep -af "oanda_trading_engine.py" >/dev/null 2>&1; then
  echo "Engine launched (background)"
  echo "--- ACTION: Engine started successfully ---"
else
  echo "Engine failed to start"
  exit 1
fi
