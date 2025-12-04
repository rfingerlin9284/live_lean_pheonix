#!/usr/bin/env bash
# Start OANDA trading engine in practice mode

cd /home/ing/RICK/RICK_PHOENIX

echo "Starting OANDA Trading Engine in PRACTICE mode..."
echo "Press Ctrl+C to stop"
echo ""

export RICK_ENV=practice
exec python3 oanda/oanda_trading_engine.py
