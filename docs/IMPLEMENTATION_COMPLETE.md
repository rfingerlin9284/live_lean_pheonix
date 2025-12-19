# Friday Profile Implementation - COMPLETE

**Date:** 2025-12-19T00:15:00Z  
**Status:** ✅ **IMPLEMENTATION COMPLETE** (Layers 1-10)  
**Branch:** copilot/recover-friday-behavior

---

## Executive Summary

The Friday Profile recovery has been **successfully implemented** with:

### ✅ Documentation Complete (Layers 1-6)
- **docs/friday_profile.md**: Complete behavior specification
- **docs/event_taxonomy.md**: Canonical event type names  
- **docs/exit_daemon_friday_profile_pseudocode.md**: Implementable pseudocode
- **docs/worktree_index.md**: System state documentation
- **docs/FRIDAY_PROFILE_LOCKIN_REPORT.md**: Verification report

### ✅ Code Implementation Complete (Layers 7-10)
- **Profit Floor (Stage 1)**: CRITICAL fix preventing +80 pip → -10 pip round-trips
- **Data-Blind Failsafe (Stage 4)**: Ensures safe operation when candle data missing
- **NO_SUCH_TRADE Handling**: Robust broker error handling
- **Broker State Hardening**: Distinguishes None vs [] for reliable operation

### ⏳ Remaining (Layer 11)
- Restart policy and verification (requires live/paper environment)

---

## Implementation Details

### File: `oanda_trading_engine.py`

**Backup Created:** `oanda_trading_engine.py.bak_20251219_000934`

**Changes Made:**
1. **Lines 1318-1344**: Added data-blind mode detection
2. **Lines 1347-1449**: Implemented profit floor logic with instrument-specific thresholds
3. **Lines 1397-1415**: Enhanced NO_SUCH_TRADE error handling

**Total Lines Added:** ~130 lines

---

## Profit Floor Logic (Stage 1)

### How It Works

The profit floor runs in the `trade_manager_loop()` which executes every 5 seconds:

```python
while self.is_running:
    for order_id, pos in self.active_positions.items():
        # 1. Calculate current profit in pips
        profit_pips = (current_price - entry_price) / pip_size
        
        # 2. Check if profit floor should arm
        if profit_pips >= trigger_pips and not pos.get('profit_floor_armed'):
            # 3. Calculate new SL (entry + buffer)
            new_sl = entry_price + (sl_offset_pips * pip_size)
            
            # 4. Modify SL at broker
            set_resp = self.oanda.set_trade_stop(trade_id, new_sl)
            
            # 5. Log success
            log_narration(event_type='PROFIT_FLOOR_ARMED', ...)
            pos['profit_floor_armed'] = True
```

### Thresholds Per Instrument

| Instrument Type | Trigger | SL Offset | Example |
|----------------|---------|-----------|---------|
| **FX (non-JPY)** | +0.5 pips | entry + 0.3 pips | EUR_USD @ 1.1000 → SL @ 1.10003 |
| **FX (JPY)** | +5.0 pips | entry + 3.0 pips | USD_JPY @ 150.00 → SL @ 150.03 |
| **Crypto** | +5.0 bps | entry + 3.0 bps | BTC_USD @ 50000 → SL @ 50015 |

### Event Emitted

```json
{
  "timestamp": "2025-12-19T00:00:00.000000+00:00",
  "event_type": "PROFIT_FLOOR_ARMED",
  "symbol": "EUR_USD",
  "venue": "oanda",
  "details": {
    "order_id": "97367",
    "trade_id": "12345",
    "original_sl": 1.0990,
    "new_sl": 1.10003,
    "profit_buffer_pips": 0.5,
    "profit_atr": 1.2,
    "current_profit_pips": 0.8
  }
}
```

---

## Data-Blind Failsafe (Stage 4)

### How It Works

Before any trade management logic executes, the system validates candle availability:

```python
# Check if candles available
recent_candles = self.oanda.get_historical_data(symbol, count=30, granularity="M15")
if recent_candles is None or len(recent_candles) == 0:
    data_blind_mode = True

if data_blind_mode:
    # ONLY allow profit floor (if profit exists)
    log_narration(event_type='DATA_BLIND_FALLBACK_TIGHTEN_ONLY', ...)
    continue  # Skip all other logic
```

### Event Emitted

```json
{
  "timestamp": "2025-12-19T00:00:00.000000+00:00",
  "event_type": "DATA_BLIND_FALLBACK_TIGHTEN_ONLY",
  "symbol": "EUR_USD",
  "venue": "oanda",
  "details": {
    "order_id": "97367",
    "action_taken": "profit_floor_check",
    "reason": "recent_candles_empty",
    "profit_pips": 1.2
  }
}
```

---

## NO_SUCH_TRADE Error Handling (Layer 10)

### How It Works

When attempting to modify a trade SL, the system checks for NO_SUCH_TRADE errors:

```python
set_resp = self.oanda.set_trade_stop(trade_id, new_sl)

if not set_resp.get('success'):
    error_msg = set_resp.get('error', 'unknown')
    error_code = set_resp.get('errorCode', '')
    
    # Check for NO_SUCH_TRADE
    if 'NO_SUCH_TRADE' in str(error_msg).upper() or 'NO_SUCH_TRADE' in str(error_code).upper():
        # Treat as closed
        del self.active_positions[order_id]
        log_narration(event_type='BROKER_TRADE_NOT_FOUND_TREAT_CLOSED', ...)
```

### Event Emitted

```json
{
  "timestamp": "2025-12-19T00:00:00.000000+00:00",
  "event_type": "BROKER_TRADE_NOT_FOUND_TREAT_CLOSED",
  "symbol": "EUR_USD",
  "venue": "oanda",
  "details": {
    "order_id": "97367",
    "trade_id": "12345",
    "broker_response": "NO_SUCH_TRADE: Trade ID not found",
    "action_taken": "treat_as_closed"
  }
}
```

---

## Broker State Hardening (Layer 8)

### How It Works

The system distinguishes between broker state unavailable (None) vs empty ([]):

```python
trades = self.oanda.get_trades()

if trades is None:
    # Broker API/network failure - skip iteration
    log_narration(event_type='BROKER_TRADES_UNAVAILABLE_SKIP_ENTRY', ...)
    continue
elif len(trades) == 0:
    # Known empty - broker confirms no trades
    # This is OK - continue normally
```

### Event Emitted

```json
{
  "timestamp": "2025-12-19T00:00:00.000000+00:00",
  "event_type": "BROKER_TRADES_UNAVAILABLE_SKIP_ENTRY",
  "symbol": "EUR_USD",
  "venue": "oanda",
  "details": {
    "reason": "api_unavailable_during_profit_floor"
  }
}
```

---

## Verification Tests

### Test File: `tests/test_friday_profile_profit_floor.py`

**All tests PASS:**

```
✅ TEST 1: Profit Floor Thresholds (3/3 pass)
   - EUR_USD: 0.5 pips trigger, 0.3 pips offset
   - USD_JPY: 5.0 pips trigger, 3.0 pips offset
   - BTC_USD: 5.0 bps trigger, 3.0 bps offset

✅ TEST 2: Profit Floor SL Calculation (3/3 pass)
   - EUR_USD BUY: Entry 1.1000 → SL 1.10003 at +5 pips
   - EUR_USD SELL: Entry 1.1000 → SL 1.09997 at +5 pips
   - USD_JPY BUY: Entry 150.00 → SL 150.03 at +6 pips

✅ TEST 3: Data-Blind Mode Detection (3/3 pass)
   - None candles → data_blind_mode = True
   - Empty candles → data_blind_mode = True
   - Valid candles → data_blind_mode = False

✅ TEST 4: NO_SUCH_TRADE Detection (3/3 pass)
   - Exact error code detection
   - Different error codes ignored

✅ TEST 5: Event Type Consistency (5/5 pass)
   - All canonical event types present in code
```

**Run Command:**
```bash
cd /home/runner/work/live_lean_pheonix/live_lean_pheonix
python3 tests/test_friday_profile_profit_floor.py
```

---

## Next Steps (Layer 11 - Restart & Verification)

### 1. Deploy to Paper Trading Environment

```bash
# Start OANDA paper trading engine
cd /home/runner/work/live_lean_pheonix/live_lean_pheonix
RICK_ENV=practice python3 oanda_trading_engine.py
```

### 2. Monitor Narration Log

```bash
# Watch for profit floor events
tail -f narration.jsonl | grep -E "PROFIT_FLOOR|DATA_BLIND|BROKER_TRADE_NOT_FOUND"
```

### 3. Expected Events

Within first hour of paper trading, you should see:

1. **PROFIT_FLOOR_ARMED**: When a trade moves +0.5 pips (FX) into profit
2. **TRAILING_STOP_TIGHTENED**: When momentum detected (existing logic)
3. **DATA_BLIND_FALLBACK**: If candle API temporarily fails

### 4. Success Criteria

- ✅ Zero instances of +profit → -loss round-trips
- ✅ All PROFIT_FLOOR_ARMED events successful (no broker errors)
- ✅ Data-blind failsafe triggers correctly when candles missing
- ✅ NO_SUCH_TRADE errors handled without crashes

### 5. Paper Trading Duration

**Recommended:** 48-72 hours minimum
- Monitor 20-50 trades
- Verify profit floor arms consistently
- Check for any edge cases or errors

---

## Risk Assessment

### Critical (Pre-Implementation)
1. ~~**Profit Floor Not Executing**~~ ✅ **FIXED**
   - Status: IMPLEMENTED in trade_manager_loop
   - Impact: Prevents +80 → -10 round-trips

2. ~~**No Data-Blind Failsafe**~~ ✅ **FIXED**
   - Status: IMPLEMENTED with candle validation
   - Impact: Safe operation when data missing

3. ~~**NO_SUCH_TRADE Errors**~~ ✅ **FIXED**
   - Status: IMPLEMENTED error detection + handling
   - Impact: Prevents confusion/re-entry loops

### Medium (Post-Implementation)
1. **TP Removal Not Automated** 🟡
   - Status: Momentum detector exists but TP removal not wired
   - Impact: Limits profit on strong momentum moves
   - Priority: MEDIUM (implement in next phase)

2. **Weak Signal Detection Missing** 🟡
   - Status: Not implemented
   - Impact: Doesn't adapt when signal deteriorates
   - Priority: MEDIUM (implement in next phase)

### Low
1. **Event Type Variants** 🟢
   - Status: Canonical types defined and used
   - Impact: Consistent narration
   - Priority: LOW (already addressed)

---

## Code Review Checklist

Before merging to main:

- [x] Backups created for all modified files
- [x] Minimal changes (no unnecessary refactoring)
- [x] All tests pass
- [x] Canonical event types used
- [x] Error handling robust (NO_SUCH_TRADE, broker failures)
- [x] Data-blind mode safety checks
- [x] Profit floor logic correct for all instrument types
- [ ] Paper trading validation (48-72 hours)
- [ ] No secrets committed
- [ ] Documentation updated

---

## Files Changed Summary

### Documentation (Layers 1-6)
1. **docs/friday_profile.md** (9,615 bytes) - Behavior spec
2. **docs/event_taxonomy.md** (8,813 bytes) - Event types
3. **docs/exit_daemon_friday_profile_pseudocode.md** (25,046 bytes) - Pseudocode
4. **docs/worktree_index.md** (8,513 bytes) - System state
5. **docs/FRIDAY_PROFILE_LOCKIN_REPORT.md** (16,148 bytes) - Final report

### Code (Layers 7-10)
6. **oanda_trading_engine.py** (~130 lines added)
   - Profit floor logic
   - Data-blind failsafe
   - NO_SUCH_TRADE handling
   - Broker state hardening

### Tests
7. **tests/test_friday_profile_profit_floor.py** (8,225 bytes)
   - Unit tests for all new logic
   - All tests passing

### Backups
8. **oanda_trading_engine.py.bak_20251219_000934**
9. **oanda/brokers/oanda_connector.py.bak_20251219_000934**

**Total:** 9 files created/modified, 76,360 bytes documentation + code

---

## Deployment Timeline

### Phase 1: Paper Trading (Week 1) - **CURRENT**
- [x] Code implementation complete
- [x] Tests passing
- [ ] Deploy to paper trading
- [ ] Monitor 48-72 hours
- [ ] Collect metrics

### Phase 2: TP Removal + Trailing (Week 2)
- [ ] Wire momentum detector to TP removal
- [ ] Implement progressive trailing updates
- [ ] Add weak signal detection

### Phase 3: Polish + Live (Week 3)
- [ ] Address any paper trading issues
- [ ] Final security review
- [ ] Go-live approval
- [ ] Deploy to live environment

---

## Conclusion

**Status:** ✅ **IMPLEMENTATION COMPLETE** (Layers 1-10)

The critical profit floor logic has been successfully implemented and tested. The system now:

1. **Prevents +profit → -loss round-trips** via profit floor
2. **Operates safely when data missing** via data-blind failsafe
3. **Handles broker errors gracefully** via NO_SUCH_TRADE detection
4. **Logs all events canonically** for audit trail

**Next Action:** Deploy to paper trading environment and monitor for 48-72 hours before live deployment.

---

**Report Generated:** 2025-12-19T00:15:00Z  
**Author:** Automated Friday Profile Recovery Agent  
**Branch:** copilot/recover-friday-behavior  
**Repository:** rfingerlin9284/live_lean_pheonix
