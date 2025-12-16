"""
Aggressive leverage & scaling plan (PIN protected).
Computes units additively based on a confluence score.

Safety notes:
- Default is DISABLED.
- Hard-capped by leverage_max.
- Does not bypass Charter or broker-side notional guards.
"""

from __future__ import annotations

import os
from typing import Dict, Tuple, Any

PIN = 841921


def _pin_ok(pin: int) -> bool:
    try:
        return int(pin) == PIN
    except Exception:
        return False


def compute_units(
    *,
    pin: int,
    price: float,
    side: str,
    base_units_at_1x: int,
    toggles: Dict[str, Any],
) -> Tuple[int, Dict[str, Any]]:
    """Return (signed_units, meta).

    side: BUY/SELL
    base_units_at_1x: already-calculated charter-min sizing base (before aggressiveness)

    The engine/broker still enforce:
    - stop-loss required
    - Charter min-notional (broker-side enforcement)
    - any position police / margin gates elsewhere
    """

    # Defaults are conservative; operator must explicitly enable.
    enabled = bool(toggles.get("aggressive_enabled", False))
    if os.getenv("RICK_AGGRESSIVE_PLAN", "0").lower() in ("1", "true", "yes"):
        enabled = True

    try:
        max_leverage = float(os.getenv("RICK_LEVERAGE_MAX", toggles.get("leverage_max", 3.0)))
    except Exception:
        max_leverage = 3.0

    try:
        base_mult = float(os.getenv("RICK_AGGRESSIVE_LEVERAGE", toggles.get("base_leverage", 1.5)))
    except Exception:
        base_mult = 1.5

    try:
        aggress = float(os.getenv("RICK_LEVERAGE_AGGRESSIVENESS", toggles.get("leverage_aggressiveness", 1.0)))
    except Exception:
        aggress = 1.0

    # Confluence is expected in [0..1]
    try:
        confluence = float(toggles.get("entry_confluence", 0.0))
    except Exception:
        confluence = 0.0
    confluence = max(0.0, min(1.0, confluence))

    if (not enabled) or (not _pin_ok(pin)):
        mult = 1.0
    else:
        # approval score = confluence * aggressiveness
        approval = confluence * max(0.0, aggress)
        mult = base_mult * (1.0 + approval)

    # Hard caps
    mult = max(1.0, min(float(mult), float(max_leverage)))

    units_abs = int(round(abs(int(base_units_at_1x)) * mult))
    # Keep at least 1 unit
    units_abs = max(1, units_abs)

    side_u = (side or "").upper()
    sign = 1 if side_u == "BUY" else -1

    meta = {
        "enabled": bool(enabled and _pin_ok(pin)),
        "confluence": round(confluence, 3),
        "base_units_1x": int(base_units_at_1x),
        "multiplier": round(mult, 3),
        "est_notional": round(float(units_abs) * float(price), 2) if price else None,
        "leverage_max": max_leverage,
        "base_leverage": base_mult,
        "leverage_aggressiveness": aggress,
    }

    return units_abs * sign, meta
