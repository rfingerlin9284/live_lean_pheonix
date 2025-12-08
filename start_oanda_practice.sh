#!/usr/bin/env bash
#
# Start OANDA Trading Engine in Practice Mode
# Session is always active for paper trading (24/7 operation)
#

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

echo "🤖 Starting OANDA Trading Engine in PRACTICE mode"
echo "=================================================="
echo ""
echo "Environment: PRACTICE (Paper Trading)"
echo "Session: Always Active (24/7)"
echo "Market Hours: Not enforced"
echo ""
echo "Press Ctrl+C to stop"
echo ""

export RICK_ENV=practice
exec python3 oanda/oanda_trading_engine.py
