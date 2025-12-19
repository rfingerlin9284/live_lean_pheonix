# Friday Profile - Exit & Trade Management Behavior

**Generated:** 2025-12-19T00:00:25Z  
**Purpose:** Document the exact "Friday Profile" behavior for SL/TP/trailing logic that prevents +80 pip → -10 pip round-trips

## Executive Summary

The "Friday Profile" represents the working trade management behavior that:
1. **Immediately** moves SL to profit floor when trade shows ANY profit buffer
2. **Never** allows a profitable trade to round-trip back into full loss
3. Uses **tight trailing** (1-2 pips FX / ticks futures / bps crypto) when signal remains strong
4. Removes or effectively ignores TP in strong momentum conditions
5. **Only tightens** stops, never widens them

---

## Timeline Analysis from Logs

### Current System State (from narration.jsonl)

**Recent Activity Pattern:**
- **HIVE_ANALYSIS events**: Continuous wolfpack voting with confidence scores
  - Example: `"consensus": "buy", "confidence": 0.8375, "profit_atr": -0.84`
  - Shows system IS tracking profit in ATR multiples (negative = unrealized loss)
- **CHARTER_VIOLATION events**: Frequent MIN_EXPECTED_PNL_USD blocks
  - System enforcing minimum profit thresholds (35-100 USD)
- **OCO_PLACED events**: Initial bracket orders with SL/TP
- **TRADE_OPENED events**: Entry confirmations

**Missing Events (The Problem):**
- ❌ **No SL_MOVED_TO_BREAKEVEN** events
- ❌ **No TP_REMOVED** events  
- ❌ **No TRAILING_STOP_TIGHTENED** events
- ❌ **No PROFIT_FLOOR_ARMED** events

This explains the +80 → -10 round-trip: **The profit protection logic isn't executing**

---

## Friday Profile Requirements (What We Must Build)

### A. Entry: Broker-Level OCO (Initial SL + TP)

**Current Implementation:** ✅ Working  
**Evidence:** `OCO_PLACED` events in narration.jsonl  
**Location:** `oanda_trading_engine.py`, `brokers/oanda_connector.py`

```json
{
  "event_type": "OCO_PLACED",
  "details": {
    "entry_price": 1.1,
    "stop_loss": 1.099,
    "take_profit": 1.1036,
    "units": 10000
  }
}
```

### B. Stage 1: Profit Floor (IMMEDIATE on ANY profit buffer)

**Current Implementation:** ❌ **MISSING - THIS IS THE CRITICAL FAILURE**  
**Required Threshold:**
- **FX (non-JPY):** +0.5 pips profit → move SL to entry + 0.3 pips
- **FX (JPY pairs):** +5 pips profit → move SL to entry + 3 pips  
- **Crypto:** +5 bps profit → move SL to entry + 3 bps
- **Futures:** +1 tick profit → move SL to entry + 0.5 ticks

**Action Required:**
1. Monitor current profit vs entry continuously
2. As SOON as profit buffer hit → modify SL at broker
3. Log event: `PROFIT_FLOOR_ARMED`
4. **NEVER** let trade go from +buffer back to -full_loss

### C. Stage 2: TP Removal on Strong Signal

**Current Implementation:** ⚠️ Partially exists in `util/momentum_trailing.py`  
**Criteria for "Strong Signal":**
- Wolfpack confidence >= min_conf + 0.10 (e.g., 0.70 baseline + 0.10 = 0.80)
- Profit >= 2x ATR
- Trend strength > 0.65 (from `MomentumDetector`)
- Market cycle contains 'STRONG' OR volatility > 1.2

**Action Required:**
1. After profit floor armed, check signal strength
2. If strong → cancel TP (or set to astronomical level)
3. Log event: `TP_REMOVED_MOMENTUM_DETECTED`

### D. Stage 3: Tight Trailing (1-2 pips/ticks/bps)

**Current Implementation:** ✅ Exists in `util/momentum_trailing.py`  
**From Code:** `SmartTrailingSystem.calculate_dynamic_trailing_distance()`

**Progressive Tightening Schedule:**

| Profit Range | Trail Distance | Notes |
|--------------|----------------|-------|
| 0-1x ATR | 1.2x ATR | Charter standard |
| 1-2x ATR | 1.0x ATR | Start tightening |
| 2-3x ATR | 0.8x ATR | Tight |
| 3-4x ATR | 0.6x ATR | Very tight |
| 4-5x ATR | 0.5x ATR | Lock profit |
| 5+x ATR | 0.4x ATR | Ultra tight |

**Momentum Loosening:** If momentum active, apply 1.15x factor to let it run

**Action Required:**
1. Calculate trailing distance based on profit_atr_multiple
2. Update SL at broker every N seconds (recommended: 15-30s)
3. Log event: `TRAILING_STOP_TIGHTENED`

### E. Stage 4: Weak Signal Mode (Re-attach TP or Tighten Aggressively)

**Current Implementation:** ❌ **MISSING**  
**Trigger:** Confidence drops below threshold OR consensus flips

**Action Required:**
1. If TP was removed, re-attach at conservative level (1.5x ATR)
2. OR tighten trailing more aggressively (reduce multiplier by 0.2x)
3. Log event: `WEAK_SIGNAL_TP_RESTORED` or `AGGRESSIVE_TIGHTEN`

### F. Stage 5: Data-Blind Failsafe

**Current Implementation:** ❌ **MISSING**  
**Trigger:** Missing candle context OR ATR returns None/0

**Constraints:**
- **ALLOW ONLY:** 
  - Tighten loser-kill (if trade negative)
  - Stage 1 profit floor (if profit buffer exists)
  - Stage 2 breakeven move (if already in profit)
- **DO NOT APPLY:**
  - ATR chandelier stops
  - Structure pivots
  - FVG/Fib tightening
  - Choke mode logic

**Action Required:**
1. Detect: `recent_candles == []` OR `atr is None or atr == 0`
2. Return early with reason: `data_blind_fallback`
3. Log event: `DATA_BLIND_FALLBACK_TIGHTEN_ONLY`

---

## Instrument-Specific Thresholds

### FX (Forex via OANDA)

**Non-JPY Pairs (EUR_USD, GBP_USD, etc.):**
- Pip size: 0.0001
- Profit floor trigger: +0.0005 (0.5 pips)
- Profit floor SL: entry + 0.0003 (0.3 pips)
- Tight trailing: 0.0001 to 0.0002 (1-2 pips)

**JPY Pairs (USD_JPY, EUR_JPY, etc.):**
- Pip size: 0.01
- Profit floor trigger: +0.05 (5 pips)
- Profit floor SL: entry + 0.03 (3 pips)
- Tight trailing: 0.01 to 0.02 (1-2 pips)

### Crypto (via Coinbase)

**Spot (BTC, ETH, etc.):**
- Basis points: 0.01% = 1 bp
- Profit floor trigger: +0.0005 (5 bps, 0.05%)
- Profit floor SL: entry + 0.0003 (3 bps)
- Tight trailing: 0.0001 to 0.0002 (1-2 bps)

### Futures (if enabled)

**Micros (ES, NQ, etc.):**
- Tick size: varies by contract (e.g., 0.25 for ES)
- Profit floor trigger: +1 tick
- Profit floor SL: entry + 0.5 ticks
- Tight trailing: 1-2 ticks

---

## Failure Mode Analysis: +80 → -10 Round-Trip

### Root Cause
**The profit floor logic (Stage 1) is NOT executing**

### Evidence
1. No `PROFIT_FLOOR_ARMED` events in logs
2. No `SL_MOVED_TO_BREAKEVEN` events
3. HIVE_ANALYSIS shows negative profit_atr (unrealized loss) persisting

### Why This Happens
**Possible Causes:**
1. **BE trigger never checked:** Exit daemon not running or not wired to engine
2. **Broker modification fails silently:** SL update returns error but not logged
3. **Trade ID stale:** Broker state refresh fails, engine can't find trade to modify
4. **Timing issue:** Profit buffer hit between polling intervals, then reversed

### Fix Strategy
1. ✅ **Add continuous profit monitoring** (every loop iteration, not just on signals)
2. ✅ **Log ALL broker modification attempts** (success + failure)
3. ✅ **Retry broker state refresh** on modification failure (max 1 retry)
4. ✅ **Emit canonical events** for every stage transition

---

## Implementation Checklist

### Phase 1: Profit Floor (HIGHEST PRIORITY)
- [ ] Add profit buffer check to main trading loop
- [ ] Implement `move_sl_to_profit_floor()` in connector
- [ ] Add `PROFIT_FLOOR_ARMED` event emission
- [ ] Test: Entry @ 1.1000, profit @ 1.1005 → SL moves to 1.1003

### Phase 2: TP Removal on Momentum
- [ ] Wire `MomentumDetector` to main engine
- [ ] Add logic to cancel TP when momentum detected
- [ ] Add `TP_REMOVED_MOMENTUM_DETECTED` event
- [ ] Test: 2x ATR profit + strong signal → TP canceled

### Phase 3: Progressive Trailing
- [ ] Wire `SmartTrailingSystem` to main engine
- [ ] Add periodic SL update loop (every 15-30s)
- [ ] Add `TRAILING_STOP_TIGHTENED` event
- [ ] Test: 3x ATR profit → SL trails at 0.8x ATR

### Phase 4: Weak Signal Handling
- [ ] Add confidence drop detection
- [ ] Implement TP re-attach logic
- [ ] Add `WEAK_SIGNAL_TP_RESTORED` event
- [ ] Test: Confidence 0.80 → 0.65 → TP re-attached

### Phase 5: Data-Blind Failsafe
- [ ] Add candle context validation
- [ ] Add `data_blind_fallback` return path
- [ ] Add `DATA_BLIND_FALLBACK_TIGHTEN_ONLY` event
- [ ] Test: Empty candles → only allow tighten ops

---

## Current System Gaps

### What Exists ✅
- OCO bracket orders (initial SL/TP)
- Momentum detection (`MomentumDetector`)
- Progressive trailing calculation (`SmartTrailingSystem`)
- Narration logger (`util/narration_logger.py`)
- Wolfpack consensus (`HIVE_ANALYSIS` events)

### What's Missing ❌
- **Profit floor execution** (Stage 1) - **CRITICAL**
- **Active TP removal** (Stage 2)
- **Periodic SL updates** (Stage 3 continuous trailing)
- **Weak signal detection** (Stage 4)
- **Data-blind guard rails** (Stage 5)
- **Broker error handling** (NO_SUCH_TRADE, etc.)

---

## Next Steps

1. **Implement Stage 1 (Profit Floor)** in `oanda_trading_engine.py`
2. **Add continuous monitoring loop** for open positions
3. **Wire momentum detector** to engine decision flow
4. **Add all canonical events** to narration logger
5. **Test end-to-end** with paper trading account

---

## References

**Code Locations:**
- Main Engine: `/home/runner/work/live_lean_pheonix/live_lean_pheonix/oanda_trading_engine.py`
- Momentum/Trailing: `/home/runner/work/live_lean_pheonix/live_lean_pheonix/util/momentum_trailing.py`
- Narration Logger: `/home/runner/work/live_lean_pheonix/live_lean_pheonix/util/narration_logger.py`
- OANDA Connector: `/home/runner/work/live_lean_pheonix/live_lean_pheonix/oanda/brokers/oanda_connector.py`

**Log Files:**
- Narration: `/home/runner/work/live_lean_pheonix/live_lean_pheonix/narration.jsonl`

**Configs:**
- Wolfpack: `/home/runner/work/live_lean_pheonix/live_lean_pheonix/configs/wolfpack_config.json`
- Paper Trading: `/home/runner/work/live_lean_pheonix/live_lean_pheonix/configs/paper_trading_config.json`
