#!/usr/bin/env bash
# Stop all running OANDA trading engine instances

echo "Stopping all OANDA trading engine processes..."
pkill -f "python3.*oanda/oanda_trading_engine.py" || echo "No processes found"
sleep 2
echo "Verifying processes stopped..."
if pgrep -f "oanda/oanda_trading_engine.py" > /dev/null; then
    echo "⚠️  Some processes still running. Force killing..."
    pkill -9 -f "oanda/oanda_trading_engine.py"
    sleep 1
fi

remaining=$(pgrep -f "oanda/oanda_trading_engine.py" | wc -l)
if [ "$remaining" -eq 0 ]; then
    echo "✅ All OANDA processes stopped successfully"
else
    echo "❌ Warning: $remaining processes still running"
    ps aux | grep "oanda/oanda_trading_engine.py" | grep -v grep
fi
