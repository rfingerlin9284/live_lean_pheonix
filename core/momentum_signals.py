"""Momentum-based signal generator for RICK system
Charter-compliant: M15 candles, trend + momentum confirmation
PIN: 841921 - No random entries allowed

LOWERED THRESHOLDS FOR DATA VERIFICATION - Will log all scan activity
"""
import logging

logger = logging.getLogger('momentum_signals')

def _sma(seq, n):
    """Simple Moving Average"""
    return sum(seq[-n:]) / n if len(seq) >= n else sum(seq)/max(len(seq),1)

def _mom(seq, n=10):
    """Momentum (rate of change over n periods)"""
    if len(seq) <= n: 
        return 0.0
    a, b = float(seq[-n-1]), float(seq[-1])
    return (b-a)/max(abs(a),1e-9) * 100.0

def _rsi(closes, period=14):
    """Relative Strength Index"""
    if len(closes) < period + 1:
        return 50.0  # neutral
    gains = []
    losses = []
    for i in range(-period, 0):
        change = closes[i] - closes[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def _ema(seq, n):
    """Exponential Moving Average"""
    if len(seq) < n:
        return sum(seq) / max(len(seq), 1)
    multiplier = 2 / (n + 1)
    ema = sum(seq[:n]) / n
    for price in seq[n:]:
        ema = (price - ema) * multiplier + ema
    return ema

def generate_signal(symbol, candles):
    """Generate BUY/SELL signal with confidence
    
    Args:
        symbol: Trading pair (e.g., "EUR_USD")
        candles: List of OANDA candle dicts with 'mid': {'c': close_price}
        
    Returns:
        (signal, confidence) where:
            signal: "BUY", "SELL", or None
            confidence: 0.0 to 1.0
    """
    # Narration import for verbose logging
    try:
        from util.narration_logger import log_narration
    except ImportError:
        def log_narration(*args, **kwargs): pass
    
    # Extract OHLC from candle format
    closes = []
    highs = []
    lows = []
    for c in candles:
        if isinstance(c, dict):
            if 'mid' in c:
                mid = c['mid']
                if 'c' in mid:
                    closes.append(float(mid['c']))
                if 'h' in mid:
                    highs.append(float(mid['h']))
                if 'l' in mid:
                    lows.append(float(mid['l']))
            elif 'close' in c:
                closes.append(float(c['close']))
                highs.append(float(c.get('high', c['close'])))
                lows.append(float(c.get('low', c['close'])))
    
    closes = [x for x in closes if x > 0][-100:]
    highs = [x for x in highs if x > 0][-100:]
    lows = [x for x in lows if x > 0][-100:]
    
    # Log data receipt confirmation
    logger.info(f"📊 SCAN [{symbol}]: Received {len(candles)} candles, extracted {len(closes)} valid closes")
    
    if len(closes) < 30:
        logger.warning(f"⚠️ [{symbol}]: Insufficient data ({len(closes)} closes, need 30)")
        log_narration(
            event_type="SCAN_INSUFFICIENT_DATA",
            details={"candles_received": len(candles), "closes_extracted": len(closes), "required": 30},
            symbol=symbol,
            venue="oanda"
        )
        meta = {"source": "momentum_signals", "reason": "insufficient_data"}
        return (None, 0.0, meta)
    
    # Calculate indicators
    s20 = _sma(closes, 20)
    s50 = _sma(closes, 50)
    e9 = _ema(closes, 9)
    e21 = _ema(closes, 21)
    m10 = _mom(closes, 10)
    rsi = _rsi(closes, 14)
    current_price = closes[-1]
    
    # Calculate ATR for volatility context
    atr = 0
    if len(highs) >= 14 and len(lows) >= 14:
        trs = []
        for i in range(-14, 0):
            tr = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
            trs.append(tr)
        atr = sum(trs) / 14
    
    # Log detailed scan metrics
    scan_metrics = {
        "price": round(current_price, 5),
        "sma20": round(s20, 5),
        "sma50": round(s50, 5),
        "ema9": round(e9, 5),
        "ema21": round(e21, 5),
        "momentum_10": round(m10, 4),
        "rsi_14": round(rsi, 2),
        "atr_14": round(atr, 6),
        "trend": "BULL" if s20 > s50 else "BEAR" if s20 < s50 else "FLAT"
    }
    
    logger.info(f"📈 [{symbol}] Indicators: SMA20={s20:.5f} SMA50={s50:.5f} MOM={m10:.3f}% RSI={rsi:.1f}")
    
    # Log scan activity to narration
    log_narration(
        event_type="SCAN_METRICS",
        details=scan_metrics,
        symbol=symbol,
        venue="oanda"
    )
    
    # ===== LOWERED THRESHOLDS FOR DATA VERIFICATION =====
    # Original: m10 > 0.15 / m10 < -0.15
    # Lowered:  m10 > 0.05 / m10 < -0.05  (3x more sensitive)
    
    MOMENTUM_THRESHOLD = 0.05  # Was 0.15, now 0.05 for testing
    
    signal = None
    confidence = 0.0
    reason = "no_signal"
    
    # Multi-factor scoring
    bull_score = 0
    bear_score = 0
    
    # Factor 1: SMA Trend
    if s20 > s50:
        bull_score += 1
    elif s20 < s50:
        bear_score += 1
    
    # Factor 2: EMA Trend
    if e9 > e21:
        bull_score += 1
    elif e9 < e21:
        bear_score += 1
    
    # Factor 3: Momentum
    if m10 > MOMENTUM_THRESHOLD:
        bull_score += 1
    elif m10 < -MOMENTUM_THRESHOLD:
        bear_score += 1
    
    # Factor 4: RSI
    if 30 < rsi < 50:  # Oversold bounce potential
        bull_score += 0.5
    elif 50 < rsi < 70:  # Overbought fade potential
        bear_score += 0.5
    
    # Factor 5: Price vs EMAs
    if current_price > e21:
        bull_score += 0.5
    elif current_price < e21:
        bear_score += 0.5
    
    # Generate signal based on scores (need 2+ factors agreeing)
    if bull_score >= 2 and bull_score > bear_score:
        signal = "BUY"
        confidence = min(bull_score / 4, 1.0)  # Normalize to 0-1
        reason = f"bull_factors={bull_score:.1f}"
    elif bear_score >= 2 and bear_score > bull_score:
        signal = "SELL"
        confidence = min(bear_score / 4, 1.0)
        reason = f"bear_factors={bear_score:.1f}"
    else:
        reason = f"neutral (bull={bull_score:.1f}, bear={bear_score:.1f})"
    
    # Log signal decision
    log_narration(
        event_type="SCAN_SIGNAL" if signal else "SCAN_NO_SIGNAL",
        details={
            "signal": signal,
            "confidence": round(confidence, 3),
            "reason": reason,
            "bull_score": bull_score,
            "bear_score": bear_score,
            "momentum": round(m10, 4),
            "rsi": round(rsi, 2)
        },
        symbol=symbol,
        venue="oanda"
    )
    
    if signal:
        logger.info(f"🎯 [{symbol}] SIGNAL: {signal} @ {confidence:.2f} confidence ({reason})")
    else:
        logger.debug(f"⏸️ [{symbol}] No signal: {reason}")
    
    # Map strategy name to family
    chosen_strategy_name = "momentum_signal"
    lower_name = chosen_strategy_name.lower()
    if any(k in lower_name for k in ["bollinger", "range", "sideways", "rsi"]):
        family = "mean_reversion"
    elif "fvg" in lower_name or "gap" in lower_name or "liquidity" in lower_name:
        family = "fvg"
    elif "scalp" in lower_name or "scalping" in lower_name or "momentum" in lower_name:
        family = "scalping"
    elif "trend" in lower_name or "breakout" in lower_name:
        family = "trend"
    else:
        family = "other"

    meta = {
        "family": family,
        "strategy_name": chosen_strategy_name,
        "reason": reason,
    }
    return (signal, confidence, meta)

# Backward-compatible wrapper
def generate_signal_simple(symbol, candles):
    signal, confidence, _ = generate_signal(symbol, candles)
    return signal, confidence
