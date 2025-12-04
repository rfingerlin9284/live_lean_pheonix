#!/usr/bin/env python3
"""
Position Police utility
Provides `_rbz_force_min_notional_position_police()` as a single source of truth
for enforcing the Charter MIN_NOTIONAL_USD requirement across modules.
"""
from typing import Optional
import os
import json
import requests
from datetime import datetime, timezone

try:
    from foundation.rick_charter import RickCharter
except Exception:
    class RickCharter:
        MIN_NOTIONAL_USD = 10000

try:
    from util.narration_logger import log_narration
except Exception:
    def log_narration(*args, **kwargs):
        # no-op if narration logger not available
        return


def _rbz_usd_notional(instrument: str, units: float, price: float) -> float:
    try:
        base, quote = instrument.split("_", 1)
        u = abs(float(units))
        p = float(price)
        if quote == "USD":
            return u * p
        if base == "USD":
            return u * 1.0
        return 0.0
    except Exception:
        return 0.0


def _rbz_fetch_price(sess, acct: str, inst: str, tok: str):
    try:
        r = sess.get(
            f"https://api-fxpractice.oanda.com/v3/accounts/{acct}/pricing",
            headers={"Authorization": f"Bearer {tok}"},
            params={"instruments": inst}, timeout=5,
        )
        j = r.json()
        # Prefer closeoutAsk/closeoutBid - fallback to mid-price
        if j and 'prices' in j and len(j['prices']) > 0:
            p = j['prices'][0]
            return float(p.get('closeoutAsk') or p.get('closeoutBid') or p.get('mid') or 0.0)
    except Exception:
        pass
    return None


def _rbz_force_min_notional_position_police(account_id: Optional[str] = None, token: Optional[str] = None, api_base: Optional[str] = None) -> bool:
    """
    Enforce minimum notional for OANDA positions. Returns True if executed without raising.
    If not credentials present, function prints a skip message and returns False.
    """
    MIN_NOTIONAL = getattr(RickCharter, 'MIN_NOTIONAL_USD', 10000)
    acct = account_id or os.environ.get('OANDA_PRACTICE_ACCOUNT_ID') or os.environ.get('OANDA_ACCOUNT_ID')
    tok = token or os.environ.get('OANDA_PRACTICE_TOKEN') or os.environ.get('OANDA_TOKEN')
    apibase = api_base or os.environ.get('OANDA_PRACTICE_API') or os.environ.get('OANDA_API') or 'https://api-fxpractice.oanda.com'
    if not acct or not tok:
        print('[RBZ_POLICE] skipped (no creds)')
        return False

    s = requests.Session()
    violations_found = 0
    violations_closed = 0

    try:
        r = s.get(f"{apibase}/v3/accounts/{acct}/openPositions", headers={"Authorization": f"Bearer {tok}"}, timeout=7)
        positions = r.json().get('positions', [])
    except Exception as e:
        print('[RBZ_POLICE] error fetching positions:', e)
        return False

    timestamp = datetime.now(timezone.utc).isoformat()
    for pos in positions:
        inst = pos.get('instrument')
        long_u = float(pos.get('long', {}).get('units', '0'))
        short_u = float(pos.get('short', {}).get('units', '0'))
        net = long_u + short_u
        if net == 0:
            continue
        avg = pos.get('long', {}).get('averagePrice') or pos.get('short', {}).get('averagePrice')
        price = float(avg) if avg else (_rbz_fetch_price(s, acct, inst, tok) or 0.0)
        notional = _rbz_usd_notional(inst, net, price)
        if 0 < notional < MIN_NOTIONAL:
            violations_found += 1
            violation_data = {
                "timestamp": timestamp,
                "event_type": "CHARTER_VIOLATION",
                "action": "POSITION_POLICE_AUTO_CLOSE",
                "details": {
                    "violation": "POSITION_BELOW_MIN_NOTIONAL",
                    "instrument": inst,
                    "net_units": net,
                    "side": "long" if net > 0 else "short",
                    "avg_price": price,
                    "notional_usd": round(notional, 2),
                    "min_required_usd": MIN_NOTIONAL,
                    "account": acct,
                    "enforcement": "GATED_LOGIC_AUTOMATIC"
                },
                "symbol": inst,
                "venue": "oanda"
            }
            print(json.dumps(violation_data))
            try:
                log_narration(**violation_data)
            except Exception:
                pass
            # Close side
            side = 'long' if net > 0 else 'short'
            payload = {'longUnits': 'ALL'} if side == 'long' else {'shortUnits': 'ALL'}
            try:
                close_response = s.put(f"{apibase}/v3/accounts/{acct}/positions/{inst}/close", headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}, data=json.dumps(payload), timeout=7)
                if close_response.status_code == 200:
                    violations_closed += 1
                    close_data = {
                        "timestamp": timestamp,
                        "event_type": "POSITION_CLOSED",
                        "action": "CHARTER_ENFORCEMENT_SUCCESS",
                        "details": {"instrument": inst, "reason": "BELOW_MIN_NOTIONAL", "status": "CLOSED_BY_POSITION_POLICE"},
                        "symbol": inst,
                        "venue": "oanda"
                    }
                    print(json.dumps(close_data))
                    try:
                        log_narration(**close_data)
                    except Exception:
                        pass
            except Exception:
                pass

    if violations_found > 0:
        summary = {
            "timestamp": timestamp,
            "event_type": "POSITION_POLICE_SUMMARY",
            "details": {
                "violations_found": violations_found,
                "violations_closed": violations_closed,
                "enforcement": "GATED_LOGIC_AUTOMATIC",
                "min_notional_usd": MIN_NOTIONAL
            }
        }
        print(json.dumps(summary))
        try:
            log_narration(**summary)
        except Exception:
            pass
    return True
