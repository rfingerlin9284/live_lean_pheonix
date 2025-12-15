#!/usr/bin/env python3
"""IBKR Equities Smoke Check (no trades)

- Confirms: platform breaker status, allowed symbols, time-window policy.
- Confirms: ib_insync presence (needed for live headless connectivity).
- Does NOT place orders.

Run:
  python3 tools/ibkr_equities_smoke_check.py
"""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    from util.platform_breaker import load_breakers

    br = load_breakers()
    st = br.get('ibkr')
    print('IBKR breaker:', 'ENABLED' if (st is None or st.enabled) else 'DISABLED', getattr(st, 'reason', ''))

    pol_path = Path('config/venue_policies.json')
    pol = {}
    if pol_path.exists():
        pol = json.loads(pol_path.read_text()).get('ibkr', {}) or {}

    print('IBKR market:', pol.get('market'))
    print('IBKR allowed_symbols:', pol.get('allowed_symbols'))
    print('IBKR max_position_usd:', pol.get('max_position_usd'))
    print('IBKR enforce_time_windows_live:', pol.get('enforce_time_windows_live'))
    print('IBKR time_windows_newyork:', pol.get('time_windows_newyork'))

    # Connector capability / dependency check
    from brokers import ibkr_connector
    print('ib_insync available:', bool(getattr(ibkr_connector, 'IB_INSYNC_AVAILABLE', False)))

    # Instantiate in paper mode (always safe)
    from brokers.ibkr_connector import IBKRConnector
    ic = IBKRConnector(pin=None, environment='paper')
    print('paper connector ok:', True)

    print('NOTE: For true headless LIVE equities trading, you need IB Gateway/TWS running + ib_insync installed,')
    print('and then run a venue-specific runner loop (not yet present in this repo snapshot).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
