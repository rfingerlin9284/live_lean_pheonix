#!/usr/bin/env python3
"""Headless Platform Sentinel

Goal:
- Periodically health-check each venue.
- If a venue fails N times in a row, flip ONLY that venue's breaker OFF.

This does not place orders.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Dict, Any

from util.platform_breaker import set_platform_enabled, load_breakers


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def check_oanda() -> Dict[str, Any]:
    try:
        from brokers.oanda_connector import OandaConnector
        env = (__import__('os').environ.get('RICK_ENV') or 'practice')
        oc = OandaConnector(pin=841921, environment=env)
        ok, msg = oc.check_authorization()
        return {'ok': bool(ok), 'msg': str(msg)}
    except Exception as e:
        return {'ok': False, 'msg': f'exception:{e}'}


def check_coinbase() -> Dict[str, Any]:
    # Prefer advanced connector if present; it supports a health_check method.
    try:
        from brokers.coinbase_advanced_connector import CoinbaseAdvancedConnector
        cc = CoinbaseAdvancedConnector(pin=None)
        res = cc.health_check()
        ok = (res.get('status') == 'healthy')
        return {'ok': bool(ok), 'msg': str(res)}
    except Exception as e:
        return {'ok': False, 'msg': f'exception:{e}'}


def check_ibkr() -> Dict[str, Any]:
    try:
        from brokers.ibkr_connector import IBKRConnector
        ic = IBKRConnector(pin=None, environment='paper')
        # Paper stub is considered healthy.
        return {'ok': True, 'msg': 'paper_stub_ok'}
    except Exception as e:
        return {'ok': False, 'msg': f'exception:{e}'}


def main() -> int:
    interval_s = 15
    max_failures = 3

    fails = {'oanda': 0, 'coinbase': 0, 'ibkr': 0}

    print(f'[{_utc_now_iso()}] Platform Sentinel starting (interval={interval_s}s, max_failures={max_failures})')

    while True:
        checks = {
            'oanda': check_oanda,
            'coinbase': check_coinbase,
            'ibkr': check_ibkr,
        }

        for platform, fn in checks.items():
            # If breaker already off, skip checks (operator has intentionally disabled)
            st = load_breakers().get(platform)
            if st is not None and not st.enabled:
                continue

            res = fn()
            ok = bool(res.get('ok'))
            msg = res.get('msg')
            if ok:
                fails[platform] = 0
            else:
                fails[platform] += 1

            print(f'[{_utc_now_iso()}] {platform}: ok={ok} fails={fails[platform]} msg={str(msg)[:200]}')

            if not ok and fails[platform] >= max_failures:
                set_platform_enabled(platform, False, reason=f'auto_disabled_after_{fails[platform]}_failures')
                print(f'[{_utc_now_iso()}] {platform}: BREAKER OFF (auto)')

        time.sleep(interval_s)


if __name__ == '__main__':
    raise SystemExit(main())
