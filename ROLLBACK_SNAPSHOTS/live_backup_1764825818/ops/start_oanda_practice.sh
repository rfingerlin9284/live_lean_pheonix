#!/usr/bin/env bash
set -euo pipefail

# Start OANDA engine in practice mode (explicit gating required)
export RICK_ENV=${RICK_ENV:-practice}
export ALLOW_PRACTICE_ORDERS=${ALLOW_PRACTICE_ORDERS:-0}
export CONFIRM_PRACTICE_ORDER=${CONFIRM_PRACTICE_ORDER:-0}
export PRACTICE_PIN=${PRACTICE_PIN:-841921}
export OANDA_FORCE_ENV=${OANDA_FORCE_ENV:-practice}
export OANDA_LOAD_ENV_FILE=${OANDA_LOAD_ENV_FILE:-1}

echo "Starting OANDA engine in practice mode..."
PYTHONPATH=$PWD .venv/bin/python oanda/oanda_trading_engine.py
