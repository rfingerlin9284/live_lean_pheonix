# Wolfpack EdgePack Choice 1 - Implementation Complete

## Overview
The Wolfpack EdgePack Choice 1 system has been successfully implemented with all components integrated and verified.

## Verification Results

All invariant checks **PASSED** ✅:

```
✅ PASS: single instance lock works (lock file path)
✅ PASS: spread guard active (max spread shown)
✅ PASS: regime gate active (min confidence shown)
✅ PASS: hedge recovery enabled (max layers shown)
✅ PASS: OCO mandatory enforced for entries AND hedges
✅ PASS: surgeon harmony enabled (trail delay shown)
✅ PASS: Charter constants updated
```

## Hard Numbers (Updated)

### From oanda_trading_engine.py:
- `stop_loss_pips = 20` pips
- `take_profit_pips = 64` pips (3.2R ratio)
- Spread guard: **ACTIVE** (max 1.8 pips)
- Cost logging: **ACTIVE**
- Regime gating: **ACTIVE** (min confidence 0.65)

### From rick_charter.py:
- `MIN_RISK_REWARD_RATIO = 3.2`
- `MIN_NOTIONAL_USD = 15000` (updated for Wolfpack EdgePack)
- `MIN_EXPECTED_PNL_USD = 10.0` (updated for Wolfpack EdgePack)
- `MAX_CONCURRENT_POSITIONS = 12` (updated for Wolfpack EdgePack)
- `MAX_POSITIONS_PER_SYMBOL = 4`
- `DAILY_LOSS_BREAKER_PCT = 0.03` (3%, updated for Wolfpack EdgePack)
- `MAX_MARGIN_USAGE = 0.25` (25%)
- `MAX_SPREAD_PIPS = 1.8` (NEW - Wolfpack EdgePack)
- `WOLF_MIN_CONFIDENCE = 0.65` (NEW - Wolfpack EdgePack)
- `WOLF_MIN_TOP_SHARPE = 1.25` (NEW - Wolfpack EdgePack)

### From surgeon.py:
- `max_red_hold_hours = 2` (with smart regime-aware override)
- `trailing_activation_pct = 0.0005` (now overridden by +0.8R profit threshold)
- Trail delay: **+0.8R** minimum profit before trailing activates
- Exit harmony: Respects engine TP, doesn't sabotage 3.2R design

## Expected Hedge Log Examples

When the Quant Hedge Recovery module triggers, you'll see logs like:

```json
{
  "event_type": "HEDGE_ARMED",
  "symbol": "EUR_USD",
  "parent_trade_id": "12345",
  "hedge_size_ratio": 0.35,
  "direction": "SELL",
  "units": 4900,
  "sl_r": 0.35,
  "tp_r": 0.70
}

{
  "event_type": "HEDGE_PLACED",
  "symbol": "EUR_USD",
  "parent_trade_id": "12345",
  "hedge_trade_id": "12346",
  "units": 4900,
  "direction": "SELL",
  "sl": 1.08450,
  "tp": 1.08350
}

{
  "event_type": "HEDGE_OCO_LINKED",
  "hedge_trade_id": "12346",
  "sl_r": 0.35,
  "tp_r": 0.70
}
```

### Hedge Eligibility Criteria
Hedges are placed when:
- Parent trade is in drawdown between **-0.35R** and **-0.9R**
- Regime is mean-reversion/chop (NOT trend/breakout)
- Max concurrent positions not exceeded
- Max margin usage not exceeded
- Daily loss breaker not hit
- Max positions per symbol not exceeded
- Only **1 hedge layer** per parent (strict limit)

### Hedge Parameters
- Hedge size: **35%** of parent size
- Hedge SL: **0.35R**
- Hedge TP: **0.70R**
- Direction: **Opposite** of parent

## VSCode Task Dropdown

In VSCode, use the Command Palette (Ctrl+Shift+P) and select:
- **"Tasks: Run Task"** → **"RBOTzilla: Apply Wolfpack EdgePack Choice 1"**

You'll be prompted:
- **ON (recommended)** - Applies all upgrades with backup
- **OFF** - Does nothing

To rollback:
- **"Tasks: Run Task"** → **"RBOTzilla: Rollback Wolfpack EdgePack Choice 1"**

## Manual Commands

### Apply Choice 1
```bash
cd /home/runner/work/live_lean_pheonix/live_lean_pheonix
python3 tools/apply_wolfpack_edgepack_choice1.py
```

### Rollback Choice 1
```bash
cd /home/runner/work/live_lean_pheonix/live_lean_pheonix
python3 tools/rollback_wolfpack_edgepack_choice1.py
```

### View Latest Backup
```bash
ls -la backups/edgepack_choice1/
```

## Features Config (config/features.json)

All features are **ON** by default:
```json
{
  "wolfpack_edgepack_choice1": true,
  "regime_gate": true,
  "ml_confidence_gate": true,
  "spread_guard": true,
  "cost_logging": true,
  "single_instance_guard": true,
  "quant_hedge_recovery": true,
  "surgeon_exit_harmony": true
}
```

## Single Instance Guard

To wrap the engine with the instance guard:
```bash
./scripts/single_instance_guard.sh python3 oanda_trading_engine.py
```

This prevents duplicate engines from running simultaneously.

## Safety Mechanisms

### Spread Guard
- Checks spread in pips before placing order
- Rejects if spread > `MAX_SPREAD_PIPS` (1.8 pips)
- Logs rejection with spread details

### Regime Gate
- Requires ML confidence >= `WOLF_MIN_CONFIDENCE` (0.65)
- Rejects signals with low confidence
- Prevents trading when regime is uncertain

### Surgeon Exit Harmony
- Does NOT remove engine-placed TP orders
- Delays trailing until **+0.8R profit**
- Only cuts losers early if regime flipped AND confidence low
- Respects the 3.2R design

### Hedge Recovery Safety
- Max 1 hedge layer per parent
- Only in mean-reversion/chop regimes
- Strict eligibility checks (margin, positions, daily loss)
- Each hedge has own OCO (TP+SL)
- No re-hedging if hedge fails

## Next Steps

1. **Test in practice mode** with small positions
2. **Monitor narration logs** for hedge events
3. **Verify spread guard** is rejecting wide spreads
4. **Check regime gate** is blocking low-confidence signals
5. **Observe surgeon harmony** delaying trails until +0.8R

## Security Summary

✅ All upgrades implement strict safety caps
✅ No martingale or unlimited hedging
✅ Daily loss breaker enforced
✅ Margin usage limits enforced
✅ Position limits enforced
✅ OCO mandatory for all entries and hedges
✅ Single instance guard prevents duplicates
✅ Backup/rollback system in place

---

**Status**: ✅ Ready for deployment
**Mode**: Default ON
**Rollback**: Available via VSCode task or manual script
