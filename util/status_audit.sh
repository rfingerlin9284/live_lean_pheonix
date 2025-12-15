#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "=== STATUS: SYSTEM HEALTH CHECK ==="
echo ""
echo "Engine:"
pgrep -af "oanda_trading_engine.py" >/dev/null && echo "Running" || echo "Stopped"
echo ""
echo "Connector Gates:"
grep -q "EXPECTED_PNL_BELOW_MIN" brokers/oanda_connector.py && echo "TP-PnL floor active" || echo "Missing"
grep -q "MIN_NOTIONAL" brokers/oanda_connector.py && echo "Notional floor active" || echo "Missing"
echo ""
echo "Position Police:"
grep -q "_rbz_force_min_notional_position_police" oanda/oanda_trading_engine.py && echo "Armed" || echo "Missing"
echo ""
echo "Charter Constants:"
python3 - <<'PY'
from foundation.rick_charter import RickCharter as R
print(f"MIN_NOTIONAL={getattr(R, 'MIN_NOTIONAL_USD', '?')} MIN_PNL={getattr(R, 'MIN_EXPECTED_PNL_USD', '?')}")
PY
echo ""
echo "--- ACTION: Audit complete ---"
