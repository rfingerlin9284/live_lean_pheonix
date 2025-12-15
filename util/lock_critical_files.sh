#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "=== STATUS: LOCKING CRITICAL FILES ==="
chmod a-w brokers/oanda_connector.py foundation/rick_charter.py oanda/oanda_trading_engine.py .vscode/tasks.json 2>/dev/null || true
echo "Checking locks:"
ls -la brokers/oanda_connector.py foundation/rick_charter.py oanda/oanda_trading_engine.py .vscode/tasks.json 2>/dev/null | awk '{print $1, $9}'
echo "--- ACTION: Files locked read-only (idempotent) ---"
