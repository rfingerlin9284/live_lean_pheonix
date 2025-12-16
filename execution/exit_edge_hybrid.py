"""execution.exit_edge_hybrid

Edge exits: ACD (BE/partial/full lock) -> Chandelier (ATR multiple)

Guarantee:
- The module only proposes *tightening* the stop-loss.
- Caller must enforce "only tighten" too (belt + suspenders).
"""

from __future__ import annotations

from typing import Dict, Any, Optional, List


def _pip(symbol: str) -> float:
    return 0.01 if "JPY" in (symbol or "") else 0.0001


def _is_long(trade: Dict[str, Any]) -> bool:
    try:
        return float(trade.get("currentUnits", trade.get("units", 0)) or 0) > 0
    except Exception:
        return False


def _cur_sl(trade: Dict[str, Any]) -> Optional[float]:
    try:
        sl_order = trade.get("stopLossOrder") or {}
        p = sl_order.get("price")
        return float(p) if p is not None else None
    except Exception:
        return None


def _atr(recent_candles: List[Dict[str, Any]], period: int = 14) -> float:
    """ATR in price units (not pips)."""
    if not recent_candles or len(recent_candles) < period + 2:
        return 0.0

    trs = []
    try:
        prev_c_raw = (recent_candles[-period - 1].get("mid") or {}).get("c")
        if prev_c_raw is None:
            return 0.0
        prev_close = float(prev_c_raw)
    except Exception:
        return 0.0

    for c in recent_candles[-period:]:
        try:
            mid = c.get("mid") or {}
            h_raw = mid.get("h")
            l_raw = mid.get("l")
            c_raw = mid.get("c")
            if h_raw is None or l_raw is None or c_raw is None:
                continue
            h = float(h_raw)
            l = float(l_raw)
            tr = max(h - l, abs(h - prev_close), abs(l - prev_close))
            trs.append(tr)
            prev_close = float(c_raw)
        except Exception:
            continue

    if not trs:
        return 0.0
    return sum(trs) / len(trs)


def apply(
    *,
    trade: Dict[str, Any],
    price_snap: Dict[str, Any],
    toggles: Dict[str, Any],
    recent_candles: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Return decision dict:

    {"action": "MOVE_SL", "new_sl": float, "reason": str, "meta": {...}}
    or
    {"action": "NONE", "reason": str}
    """

    sym = trade.get("instrument") or trade.get("symbol")
    if not sym:
        return {"action": "NONE", "reason": "no_symbol"}

    P = _pip(sym)
    long = _is_long(trade)

    try:
        entry = float(trade.get("price") or trade.get("entryPrice") or 0.0)
    except Exception:
        entry = 0.0

    cur_sl = _cur_sl(trade)

    try:
        v = price_snap.get("bid") if long else price_snap.get("ask")
        if v is None:
            curr = 0.0
        else:
            curr = float(v)
    except Exception:
        curr = 0.0

    if not entry or not curr:
        return {"action": "NONE", "reason": "no_price"}

    profit_pips = (curr - entry) / P if long else (entry - curr) / P

    # Gate
    if not bool(toggles.get("edge_exit_enabled", True)):
        return {"action": "NONE", "reason": "edge_exit_disabled"}

    def _int(key: str, default: int) -> int:
        try:
            return int(toggles.get(key, default))
        except Exception:
            return default

    def _flt(key: str, default: float) -> float:
        try:
            return float(toggles.get(key, default))
        except Exception:
            return default

    # ACD stages (pips)
    be_pips = _int("acd_be_pips", 6)
    part_pips = _int("acd_partial_pips", 12)
    full_pips = _int("acd_full_pips", 24)

    part_lock = _int("acd_partial_lock_pips", 4)
    full_lock = _int("acd_full_lock_pips", 2)

    # Step A: BE
    if profit_pips >= be_pips:
        new_sl = entry
        if cur_sl is None or (long and new_sl > cur_sl) or ((not long) and new_sl < cur_sl):
            return {"action": "MOVE_SL", "new_sl": float(new_sl), "reason": "ACD_BE", "meta": {"profit_pips": round(profit_pips, 2)}}

    # Step B: Partial lock
    if profit_pips >= part_pips:
        new_sl = (curr - part_lock * P) if long else (curr + part_lock * P)
        if cur_sl is None or (long and new_sl > cur_sl) or ((not long) and new_sl < cur_sl):
            return {"action": "MOVE_SL", "new_sl": float(new_sl), "reason": "ACD_PARTIAL", "meta": {"profit_pips": round(profit_pips, 2)}}

    # Step C: Full lock
    if profit_pips >= full_pips:
        new_sl = (curr - full_lock * P) if long else (curr + full_lock * P)
        if cur_sl is None or (long and new_sl > cur_sl) or ((not long) and new_sl < cur_sl):
            return {"action": "MOVE_SL", "new_sl": float(new_sl), "reason": "ACD_FULL", "meta": {"profit_pips": round(profit_pips, 2)}}

    # Step D: Chandelier (ATR)
    recent_candles = recent_candles or []
    atr_period = _int("chandelier_atr_period", 14)
    atr_mult = _flt("chandelier_atr_mult", 2.2)

    atr_val = _atr(recent_candles, period=max(2, atr_period))
    if atr_val > 0 and atr_mult > 0:
        dist = atr_mult * atr_val
        new_sl = (curr - dist) if long else (curr + dist)
        if cur_sl is None or (long and new_sl > cur_sl) or ((not long) and new_sl < cur_sl):
            return {
                "action": "MOVE_SL",
                "new_sl": float(new_sl),
                "reason": "CHAND",
                "meta": {
                    "profit_pips": round(profit_pips, 2),
                    "atr": atr_val,
                    "atr_mult": atr_mult,
                },
            }

    return {"action": "NONE", "reason": "hold", "meta": {"profit_pips": round(profit_pips, 2)}}
