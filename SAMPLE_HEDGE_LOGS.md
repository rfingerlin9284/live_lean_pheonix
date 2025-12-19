# Sample Hedge Recovery Logs

## Scenario: EUR_USD Long Position in Drawdown

### 1. Trade Entry (Normal OCO)
```json
{
  "timestamp": "2025-12-19T15:45:00.123Z",
  "event_type": "TRADE_SIGNAL",
  "symbol": "EUR_USD",
  "direction": "BUY",
  "entry": 1.08500,
  "stop_loss": 1.08300,
  "take_profit": 1.09140,
  "units": 14000,
  "notional": 15190.00,
  "rr_ratio": 3.2,
  "venue": "oanda"
}
```

### 2. Position Moves to -0.45R Drawdown (Hedge Triggers)
```json
{
  "timestamp": "2025-12-19T15:58:30.456Z",
  "event_type": "HEDGE_ARMED",
  "symbol": "EUR_USD",
  "parent_trade_id": "54321",
  "hedge_size_ratio": 0.35,
  "direction": "SELL",
  "units": 4900,
  "entry_price": 1.08410,
  "stop_loss": 1.08480,
  "take_profit": 1.08270,
  "sl_r": 0.35,
  "tp_r": 0.70,
  "venue": "oanda"
}
```

### 3. Hedge Order Placed Successfully
```json
{
  "timestamp": "2025-12-19T15:58:30.789Z",
  "event_type": "HEDGE_PLACED",
  "symbol": "EUR_USD",
  "parent_trade_id": "54321",
  "hedge_trade_id": "54322",
  "units": 4900,
  "direction": "SELL",
  "sl": 1.08480,
  "tp": 1.08270,
  "venue": "oanda"
}
```

### 4. OCO Linked to Hedge
```json
{
  "timestamp": "2025-12-19T15:58:30.890Z",
  "event_type": "HEDGE_OCO_LINKED",
  "symbol": "EUR_USD",
  "hedge_trade_id": "54322",
  "sl_r": 0.35,
  "tp_r": 0.70,
  "venue": "oanda"
}
```

### 5a. Hedge Exits (TP Hit) - Best Case
```json
{
  "timestamp": "2025-12-19T16:15:45.123Z",
  "event_type": "HEDGE_EXITED",
  "symbol": "EUR_USD",
  "hedge_trade_id": "54322",
  "parent_trade_id": "54321",
  "exit_type": "TP",
  "pnl": 68.60,
  "profit_r": 0.70,
  "venue": "oanda"
}
```

### 5b. Hedge Exits (SL Hit) - Loss Case
```json
{
  "timestamp": "2025-12-19T16:15:45.123Z",
  "event_type": "HEDGE_EXITED",
  "symbol": "EUR_USD",
  "hedge_trade_id": "54322",
  "parent_trade_id": "54321",
  "exit_type": "SL",
  "pnl": -34.30,
  "profit_r": -0.35,
  "venue": "oanda",
  "note": "No re-hedge (max layers reached)"
}
```

## Hedge Rejection Examples

### Rejected: Already Hedged
```json
{
  "timestamp": "2025-12-19T16:20:00.123Z",
  "event_type": "HEDGE_REJECTED",
  "symbol": "EUR_USD",
  "parent_trade_id": "54321",
  "reason": "Already hedged",
  "regime": "chop",
  "venue": "oanda"
}
```

### Rejected: Wrong Regime (Trend Breakout)
```json
{
  "timestamp": "2025-12-19T16:25:00.456Z",
  "event_type": "HEDGE_REJECTED",
  "symbol": "GBP_USD",
  "parent_trade_id": "54323",
  "reason": "Regime 'trend_breakout' not suitable for hedging (trend/breakout)",
  "regime": "trend_breakout",
  "venue": "oanda"
}
```

### Rejected: Max Concurrent Positions
```json
{
  "timestamp": "2025-12-19T16:30:00.789Z",
  "event_type": "HEDGE_REJECTED",
  "symbol": "USD_JPY",
  "parent_trade_id": "54324",
  "reason": "Max concurrent positions reached (12/12)",
  "regime": "chop",
  "venue": "oanda"
}
```

### Rejected: Max Margin Usage
```json
{
  "timestamp": "2025-12-19T16:35:00.012Z",
  "event_type": "HEDGE_REJECTED",
  "symbol": "AUD_USD",
  "parent_trade_id": "54325",
  "reason": "Max margin usage reached (25.3%/25.0%)",
  "regime": "mean_revert",
  "venue": "oanda"
}
```

### Rejected: Daily Loss Breaker
```json
{
  "timestamp": "2025-12-19T16:40:00.345Z",
  "event_type": "HEDGE_REJECTED",
  "symbol": "NZD_USD",
  "parent_trade_id": "54326",
  "reason": "Daily loss breaker active (-3.2%/-3.0%)",
  "regime": "chop",
  "venue": "oanda"
}
```

### Rejected: Drawdown Not in Range
```json
{
  "timestamp": "2025-12-19T16:45:00.678Z",
  "event_type": "HEDGE_REJECTED",
  "symbol": "EUR_GBP",
  "parent_trade_id": "54327",
  "reason": "Drawdown -0.20R not yet in trigger range (-0.35R)",
  "regime": "chop",
  "venue": "oanda"
}
```

## Cost Logging Examples

### Before Order Placement
```json
{
  "timestamp": "2025-12-19T15:45:00.100Z",
  "event_type": "COST_ANALYSIS",
  "symbol": "EUR_USD",
  "spread_pips": 0.8,
  "estimated_cost_usd": 11.20,
  "rr_ratio": 3.2,
  "expected_pnl_usd": 448.00,
  "notional_usd": 15190.00,
  "venue": "oanda"
}
```

## Spread Guard Examples

### Rejected: Spread Too Wide
```json
{
  "timestamp": "2025-12-19T16:50:00.123Z",
  "event_type": "GATE_REJECTION",
  "symbol": "GBP_JPY",
  "reason": "SPREAD_TOO_WIDE",
  "spread_pips": 2.4,
  "max_spread_pips": 1.8,
  "bid": 193.450,
  "ask": 193.474,
  "venue": "oanda"
}
```

## Regime Gate Examples

### Blocked: Low ML Confidence
```json
{
  "timestamp": "2025-12-19T16:55:00.456Z",
  "event_type": "REGIME_GATE_BLOCKED",
  "symbol": "USD_CAD",
  "regime": "sideways",
  "confidence": 0.58,
  "min_confidence": 0.65,
  "reason": "ML confidence below threshold",
  "venue": "ml_intelligence"
}
```

## Surgeon Exit Harmony Examples

### Exit Harmony: Letting SL Work
```
🛡️ EXIT HARMONY: EUR_USD RED 2.3h, but regime intact. Letting SL work.
```

### Exit Harmony: Trail Delayed
```
🛡️ EXIT HARMONY: GBP_USD at 0.52R profit, need 0.80R before trailing
```

### Trail Activated: Above +0.8R
```
🏛️ ARCHITECT TRAIL: EUR_USD moving SL 1.08300 -> 1.08520 (profit: 1.10R)
```

---

## 30 Lines of Sample Hedge Logs (Condensed)

```
2025-12-19 15:45:00.123 | TRADE_SIGNAL | EUR_USD | BUY | Entry: 1.08500 | SL: 1.08300 | TP: 1.09140 | RR: 3.2
2025-12-19 15:58:30.456 | HEDGE_ARMED | EUR_USD | Parent: 54321 | Hedge: SELL 4900 units | SL: 1.08480 | TP: 1.08270
2025-12-19 15:58:30.789 | HEDGE_PLACED | EUR_USD | Hedge ID: 54322 | Parent: 54321 | Direction: SELL
2025-12-19 15:58:30.890 | HEDGE_OCO_LINKED | EUR_USD | Hedge: 54322 | SL: 0.35R | TP: 0.70R
2025-12-19 16:15:45.123 | HEDGE_EXITED | EUR_USD | Hedge: 54322 | TP Hit | PnL: +$68.60 | Profit: 0.70R
2025-12-19 16:20:00.123 | HEDGE_REJECTED | EUR_USD | Parent: 54321 | Reason: Already hedged
2025-12-19 16:25:00.456 | TRADE_SIGNAL | GBP_USD | SELL | Entry: 1.26800 | SL: 1.27000 | TP: 1.26160 | RR: 3.2
2025-12-19 16:30:00.789 | COST_ANALYSIS | GBP_USD | Spread: 0.9 pips | Cost: $11.34 | Expected PnL: $453.60
2025-12-19 16:35:00.012 | HEDGE_REJECTED | AUD_USD | Reason: Max margin usage reached (25.3%/25.0%)
2025-12-19 16:40:00.345 | GATE_REJECTION | GBP_JPY | Reason: SPREAD_TOO_WIDE | Spread: 2.4 pips > 1.8 pips
2025-12-19 16:45:00.678 | REGIME_GATE_BLOCKED | USD_CAD | Regime: sideways | Confidence: 0.58 < 0.65
2025-12-19 16:50:00.123 | SURGEON | EUR_USD | EXIT HARMONY: RED 2.3h, regime intact. Letting SL work.
2025-12-19 16:55:00.456 | SURGEON | GBP_USD | EXIT HARMONY: At 0.52R profit, need 0.80R before trailing
2025-12-19 17:00:00.789 | TRADE_SIGNAL | USD_JPY | BUY | Entry: 151.250 | SL: 151.050 | TP: 151.890 | RR: 3.2
2025-12-19 17:05:00.012 | HEDGE_ARMED | USD_JPY | Parent: 54328 | Hedge: SELL 5250 units | Drawdown: -0.42R
2025-12-19 17:05:00.345 | HEDGE_PLACED | USD_JPY | Hedge ID: 54329 | Parent: 54328 | Direction: SELL
2025-12-19 17:10:00.678 | SURGEON | EUR_USD | ARCHITECT TRAIL: Moving SL 1.08300 -> 1.08520 (profit: 1.10R)
2025-12-19 17:15:00.123 | HEDGE_EXITED | USD_JPY | Hedge: 54329 | SL Hit | PnL: -$36.75 | Loss: -0.35R
2025-12-19 17:20:00.456 | HEDGE_REJECTED | NZD_USD | Reason: Daily loss breaker active (-3.2%/-3.0%)
2025-12-19 17:25:00.789 | COST_ANALYSIS | EUR_GBP | Spread: 1.2 pips | Cost: $16.80 | Expected PnL: $537.60
2025-12-19 17:30:00.012 | TRADE_SIGNAL | AUD_JPY | BUY | Entry: 97.450 | SL: 97.250 | TP: 98.090 | RR: 3.2
2025-12-19 17:35:00.345 | SURGEON | GBP_USD | EXIT HARMONY: At 0.95R profit, activating trail
2025-12-19 17:40:00.678 | SURGEON | AUD_JPY | ARCHITECT TRAIL: Moving SL 97.250 -> 97.550 (profit: 1.50R)
2025-12-19 17:45:00.123 | HEDGE_ARMED | EUR_USD | Parent: 54330 | Hedge: SELL 4550 units | Drawdown: -0.68R
2025-12-19 17:50:00.456 | HEDGE_PLACED | EUR_USD | Hedge ID: 54331 | Parent: 54330 | Direction: SELL
2025-12-19 17:55:00.789 | GATE_REJECTION | EUR_CHF | Reason: SPREAD_TOO_WIDE | Spread: 2.1 pips > 1.8 pips
2025-12-19 18:00:00.012 | REGIME_GATE_BLOCKED | USD_CHF | Regime: choppy | Confidence: 0.61 < 0.65
2025-12-19 18:05:00.345 | HEDGE_EXITED | EUR_USD | Hedge: 54331 | TP Hit | PnL: +$63.70 | Profit: 0.70R
2025-12-19 18:10:00.678 | SURGEON | EUR_USD | EXIT HARMONY: Parent recovered, back in profit
2025-12-19 18:15:00.123 | COST_ANALYSIS | NZD_USD | Spread: 1.5 pips | Cost: $9.00 | Expected PnL: $360.00
```

**Notes:**
- Hedges only trigger in drawdown range -0.35R to -0.9R
- Each hedge has its own OCO (SL + TP)
- No re-hedging after hedge SL hit
- Spread guard rejects orders with spread > 1.8 pips
- Regime gate blocks signals with confidence < 0.65
- Surgeon delays trailing until +0.8R profit
- All safety limits enforced (margin, positions, daily loss)
