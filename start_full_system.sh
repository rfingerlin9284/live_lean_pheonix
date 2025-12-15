#!/bin/bash
# RICK PHOENIX Full System Startup - 4 Terminal Layout
# Exactly as used Friday 5PM
set -e

cd "$(dirname "$0")"

echo "=== RICK PHOENIX FULL SYSTEM STARTUP ==="
echo "PIN: 841921 | Environment: Practice"

# Kill any existing instances
pkill -f "oanda/oanda_trading_engine.py" || true
pkill -f "oanda_trading_engine.py" || true
pkill -f "oanda\.oanda_trading_engine" || true
pkill -f active_trade_monitor.py || true
pkill -f system_watchdog.py || true
pkill -f proactive_trade_guide.py || true

# Ensure two-step SL settings are in .env
if ! grep -q "TWO_STEP_SL_MODE" .env 2>/dev/null; then
    echo "" >> .env
    echo "# Two-Step SL Protocol (Friday 5PM settings)" >> .env
    echo "TWO_STEP_SL_MODE=ON" >> .env
    echo "STEP2_TRIGGER_PIPS=8" >> .env
    echo "STEP2_LOCK_PCT=70" >> .env
    echo "STEP2_MIN_TRAIL_PIPS=3" >> .env
    echo "RBZ_STEP2_ENABLED=1" >> .env
fi

# Source environment
source .env 2>/dev/null || true

echo "✅ Two-Step SL: ON (trigger: 8 pips, lock: 70%, trail: 3 pips)"
echo ""
echo "Starting 4-terminal layout:"
echo "  Terminal 1: Brain/Hive/Agent with Narration"
echo "  Terminal 2: Sentinel + Watchdog"
echo "  Terminal 3: Proactive Trade Guide"
echo "  Terminal 4: OANDA Engine (Practice)"
echo ""

# Check if running in tmux
if [ -n "$TMUX" ]; then
    # Split into 4 panes
    tmux split-window -h
    tmux split-window -v
    tmux select-pane -t 0
    tmux split-window -v
    
    # Pane 0: Brain/Hive with Narration
    tmux select-pane -t 0
    tmux send-keys "cd $(pwd) && tail -f narration.jsonl | grep -E '(TRADE_OPENED|TRADE_CLOSED|ORDER_PLACED|CONSENSUS|WOLFPACK)'" C-m
    
    # Pane 1: Sentinel + Watchdog
    tmux select-pane -t 1
    tmux send-keys "cd $(pwd) && python3 active_trade_monitor.py 2>&1 | tee /tmp/sentinel.log" C-m
    
    # Pane 2: Proactive Trade Guide
    tmux select-pane -t 2
    tmux send-keys "cd $(pwd) && python3 util/proactive_trade_guide.py" C-m
    
    # Pane 3: OANDA Engine
    tmux select-pane -t 3
    tmux send-keys "cd $(pwd) && RICK_ENV=practice python3 -u oanda/oanda_trading_engine.py" C-m
    
    echo "✅ All 4 terminals started in tmux"
else
    # Not in tmux - start in background with logs
    echo "Not in tmux - starting processes in background..."
    
    # Terminal 1: Narration viewer
    tail -f narration.jsonl | grep -E '(TRADE_OPENED|TRADE_CLOSED|ORDER_PLACED|CONSENSUS|WOLFPACK)' > /tmp/narration_live.log 2>&1 &
    
    # Terminal 2: Sentinel + Watchdog
    python3 active_trade_monitor.py > /tmp/sentinel.log 2>&1 &
    python3 system_watchdog.py > /tmp/watchdog.log 2>&1 &
    
    # Terminal 3: Proactive Trade Guide
    python3 util/proactive_trade_guide.py > /tmp/trade_guide.log 2>&1 &
    
    # Terminal 4: OANDA Engine (foreground)
    echo "✅ Background processes started"
    echo "✅ Logs: /tmp/sentinel.log, /tmp/watchdog.log, /tmp/trade_guide.log"
    echo ""
    echo "Starting OANDA Engine..."
    RICK_ENV=practice python3 -u oanda/oanda_trading_engine.py
fi
