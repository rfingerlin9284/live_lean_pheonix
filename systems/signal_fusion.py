"""systems.signal_fusion

Signal fusion layer (additive):
- Keeps your existing momentum engine as the primary brain.
- Adds a lightweight "wolfpack proxy" score.
- Adds an ADR/volatility sanity gate.

Returns: (direction, confidence, confluence, meta)
"""

from __future__ import annotations

from typing import Dict, List, Tuple, Any, Optional
import math

# Primary entry brain (Dec 5th profitable logic path)
try:
    from core.momentum_signals import generate_signal as momentum_signal
except Exception:
    def momentum_signal(symbol: str, candles: List[Dict[str, Any]]):
        return (None, 0.0)


def _wolfpack_proxy(closes: List[float]) -> float:
    """Return 0..1."""
    if len(closes) < 20:
        return 0.0

    # Simple EMA-ish slope proxy + zscore on last return
    ema = sum(closes[-10:]) / 10.0
    slope = (closes[-1] - ema) / max(abs(ema), 1e-9)

    rets = []
    start = max(1, len(closes) - 50)
    for i in range(start, len(closes)):
        prev = closes[i - 1]
        if prev == 0:
            continue
        rets.append((closes[i] - prev) / max(abs(prev), 1e-9))

    if not rets:
        return 0.0

    mu = sum(rets) / len(rets)
    var = sum((r - mu) ** 2 for r in rets) / max(len(rets), 1)
    z = (rets[-1] - mu) / math.sqrt(var + 1e-12)

    score = 0.5 * slope + 0.5 * max(min(z / 3.0, 1.0), -1.0)
    # squash to 0..1
    return max(0.0, min(1.0, 0.5 + score / 2.0))


def _pip(symbol: str) -> float:
    return 0.01 if "JPY" in (symbol or "") else 0.0001


def _adr_pips(symbol: str, candles: List[Dict[str, Any]], lookback: int = 14) -> Optional[float]:
    if len(candles) < lookback + 2:
        return None
    P = _pip(symbol)
    rng = []
    for c in candles[-lookback:]:
        try:
            mid = c.get("mid") or {}
            h_raw = mid.get("h")
            l_raw = mid.get("l")
            if h_raw is None or l_raw is None:
                continue
            h = float(h_raw)
            l = float(l_raw)
            rng.append((h - l) / P)
        except Exception:
            continue
    if not rng:
        return None
    return sum(rng) / len(rng)


def fuse(
    symbol: str,
    candles: List[Dict[str, Any]],
    toggles: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[str], float, float, Dict[str, Any]]:
    """Returns (direction, confidence, confluence, meta)."""

    toggles = toggles or {}

    # Primary signal (supports 2-tuple or 3-tuple)
    result = momentum_signal(symbol, candles)
    if isinstance(result, tuple):
        direction = result[0]
        confidence = float(result[1]) if len(result) > 1 else 0.0
        meta = result[2] if len(result) > 2 and isinstance(result[2], dict) else {}
    else:
        direction, confidence, meta = result, 0.0, {}

    # Extract closes
    closes: List[float] = []
    for c in candles:
        try:
            mid = c.get("mid") or {}
            if "c" in mid:
                closes.append(float(mid["c"]))
        except Exception:
            continue

    wolf = _wolfpack_proxy(closes)
    adr = _adr_pips(symbol, candles, lookback=int(toggles.get("vol_adr_lookback", 14)))

    # Vol gate: default generous cap; operator can tighten
    try:
        adr_cap = float(toggles.get("vol_adr_cap_pips", 400))
    except Exception:
        adr_cap = 400.0

    if adr is not None and adr_cap > 0 and adr > adr_cap:
        return None, 0.0, 0.0, {"vol_gate": True, "adr_pips": round(adr, 1), "adr_cap_pips": adr_cap}

    if direction:
        confluence = max(0.0, min(1.0, 0.65 * float(confidence) + 0.35 * float(wolf)))
    else:
        confluence = 0.0

    out_meta = {
        **(meta or {}),
        "wolf_proxy": round(wolf, 3),
        "adr_pips": round(adr, 1) if adr is not None else None,
        "adr_cap_pips": adr_cap,
    }

    return direction, float(confidence), float(confluence), out_meta
