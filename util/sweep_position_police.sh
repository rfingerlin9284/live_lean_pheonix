#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source .env 2>/dev/null || true
echo "=== STATUS: POSITION POLICE SWEEP (sub-15k auto-close) ==="
python3 - <<'PY'
from brokers.oanda_connector import OandaConnector
from util.position_police import _rbz_force_min_notional_position_police
try:
    c = OandaConnector(pin=841921, environment='practice')
    _rbz_force_min_notional_position_police(account_id=c.account_id, token=c.api_token, api_base=c.api_base)
    print('--- ACTION: Sweep executed ---')
except Exception as e:
    print('ERROR: sweep failed', e)
    raise
PY
