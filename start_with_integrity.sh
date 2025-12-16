#!/bin/bash
set -euo pipefail

echo "🔍 Running integrity checks..."
python3 check_system_config.py || {
    echo "❌ INTEGRITY CHECK FAILED - Engine blocked from starting"
    exit 1
}

echo "✅ Integrity verified"
echo "🚀 Starting OANDA Practice Engine..."

# Load optional environment overrides (non-fatal)
source .env 2>/dev/null || true

# Default to practice unless overridden
export RICK_ENV="${RICK_ENV:-practice}"

# Default toggles path to workspace config unless overridden
export PHX_TOGGLES_PATH="${PHX_TOGGLES_PATH:-${TOGGLES_PATH:-config/toggles.json}}"

# Start canonical engine
exec python3 -u oanda/oanda_trading_engine.py
