# Event Type Taxonomy - Canonical Event Names

**Generated:** 2025-12-19T00:00:25Z  
**Purpose:** Standardize event_type strings across all narration logging

## Canonical Event Types

All narration events MUST use these exact strings. No variants allowed.

### Entry & Signal Events

| Canonical Name | Description | Required Fields |
|----------------|-------------|-----------------|
| `SCAN_SIGNAL` | Signal detected by strategy scanner | `symbol`, `direction`, `confidence`, `strategy_name` |
| `WOLFPACK_VOTE` | Individual wolf pack member vote | `symbol`, `pack_name`, `direction`, `confidence` |
| `HIVE_ANALYSIS` | Aggregated Hive Mind consensus | `symbol`, `consensus`, `confidence`, `order_id`, `profit_atr` |
| `ENTRY_ALLOWED` | Entry passed all gates | `symbol`, `entry_price`, `units` |
| `OCO_PLACED` | Broker-level OCO bracket order created | `order_id`, `entry_price`, `stop_loss`, `take_profit`, `units`, `latency_ms` |
| `TRADE_OPENED` | Trade execution confirmed | `symbol`, `entry_price`, `stop_loss`, `take_profit` |

### Entry Block Events (Churn Guards)

| Canonical Name | Description | Required Fields |
|----------------|-------------|-----------------|
| `BROKER_TRADES_UNAVAILABLE_SKIP_ENTRY` | Broker state unknown (API/network failure) - skip entry | `symbol`, `reason` |
| `ENTRY_RATE_LIMIT_BLOCK` | Entry blocked by rate limiter | `symbol`, `seconds_remaining`, `last_entry_time` |
| `ENTRY_FLIP_CONFIDENCE_BLOCK` | Entry blocked by flip hysteresis | `symbol`, `last_direction`, `current_direction`, `confidence`, `required_confidence` |
| `ENTRY_SPREAD_BLOCK` | Entry blocked by spread gate | `symbol`, `current_spread_pips`, `max_spread_pips` |
| `ORDER_REJECTED_MIN_NOTIONAL` | Order rejected - below minimum notional | `units`, `notional`, `min_notional`, `entry_price`, `reason` |
| `CHARTER_VIOLATION` | Order blocked by charter constraint | `code`, `expected_pnl_usd`, `min_expected_pnl_usd`, `entry_price`, `take_profit`, `units` |

### Exit & Trade Management Events

| Canonical Name | Description | Required Fields |
|----------------|-------------|-----------------|
| `PROFIT_FLOOR_ARMED` | SL moved to profit floor (entry + buffer) | `symbol`, `order_id`, `original_sl`, `new_sl`, `profit_buffer_pips`, `profit_atr` |
| `SL_MOVED_TO_BREAKEVEN` | SL moved to breakeven (entry price) | `symbol`, `order_id`, `original_sl`, `new_sl`, `profit_atr` |
| `TP_REMOVED_MOMENTUM_DETECTED` | TP canceled due to strong momentum | `symbol`, `order_id`, `original_tp`, `momentum_strength`, `profit_atr` |
| `TP_RESTORED_WEAK_SIGNAL` | TP re-attached after signal weakened | `symbol`, `order_id`, `new_tp`, `confidence`, `profit_atr` |
| `TRAILING_STOP_TIGHTENED` | Trailing SL updated | `symbol`, `order_id`, `old_sl`, `new_sl`, `trail_distance`, `profit_atr` |
| `AGGRESSIVE_TIGHTEN` | SL tightened due to weak signal | `symbol`, `order_id`, `old_sl`, `new_sl`, `reason` |
| `DATA_BLIND_FALLBACK_TIGHTEN_ONLY` | Operating in data-blind mode (candles missing) | `symbol`, `order_id`, `action_taken`, `reason` |
| `TRADE_CLOSED` | Trade closed (manual or SL/TP hit) | `symbol`, `order_id`, `exit_price`, `pnl`, `outcome`, `duration_seconds` |

### Broker Error Events

| Canonical Name | Description | Required Fields |
|----------------|-------------|-----------------|
| `BROKER_TRADE_NOT_FOUND_TREAT_CLOSED` | NO_SUCH_TRADE error - treat as closed | `symbol`, `order_id`, `broker_response`, `action_taken` |
| `BROKER_MODIFICATION_FAILED` | SL/TP modification attempt failed | `symbol`, `order_id`, `modification_type`, `error_code`, `error_message` |
| `BROKER_STATE_REFRESH_FAILED` | Failed to fetch current broker state | `venue`, `error_code`, `error_message` |

### Profile & Configuration Events

| Canonical Name | Description | Required Fields |
|----------------|-------------|-----------------|
| `PROFILE_STATUS` | Trading profile applied | `description`, `min_expected_pnl_usd`, `min_notional_usd`, `max_margin_utilization_pct` |
| `REGIME_DETECTED` | Market regime classification | `regime`, `confidence`, `indicators` |

### System Events

| Canonical Name | Description | Required Fields |
|----------------|-------------|-----------------|
| `ENGINE_STARTED` | Trading engine started | `environment`, `version`, `config_loaded` |
| `ENGINE_STOPPED` | Trading engine stopped | `reason`, `uptime_seconds` |
| `POSITION_POLICE_ALERT` | Position police flagged anomaly | `alert_type`, `symbols_affected`, `action_taken` |

---

## Deprecated / Near-Miss Variants (DO NOT USE)

These variants have been found in the codebase and MUST be replaced with canonical names:

| ❌ Deprecated | ✅ Use This Instead | Status |
|--------------|---------------------|--------|
| `BROKER_TRADES_UNAVAILABLE` | `BROKER_TRADES_UNAVAILABLE_SKIP_ENTRY` | Needs standardization |
| `ENTRY_BLOCKED_RATE_LIMIT` | `ENTRY_RATE_LIMIT_BLOCK` | Needs standardization |
| `TP_CANCELLED` | `TP_REMOVED_MOMENTUM_DETECTED` | Needs standardization |
| `SL_UPDATED` | `TRAILING_STOP_TIGHTENED` or `SL_MOVED_TO_BREAKEVEN` | Needs context |
| `TRADE_EXIT` | `TRADE_CLOSED` | Needs standardization |

---

## JSON Event Structure (Standard Format)

All narration events MUST follow this schema:

```json
{
  "timestamp": "2025-12-19T00:00:00.000000+00:00",  // ISO 8601 with timezone
  "event_type": "CANONICAL_EVENT_NAME",              // From taxonomy above
  "symbol": "EUR_USD",                                // Trading symbol (or "SYSTEM")
  "venue": "oanda",                                   // Broker/venue (or null)
  "details": {                                        // Event-specific fields
    "field1": "value1",
    "field2": 123.45,
    "field3": true
  }
}
```

### Required Top-Level Fields
- `timestamp` (string, ISO 8601 with timezone)
- `event_type` (string, must be from canonical list)
- `symbol` (string or null)
- `venue` (string or null)
- `details` (object, event-specific fields)

### Details Field Requirements

Each event type has specific required fields in `details`. See table above.

---

## Grep Verification Commands

To verify event type usage across the codebase:

```bash
# Find all BROKER_TRADES_UNAVAILABLE variants
grep -r "BROKER_TRADES_UNAVAILABLE" --include="*.py" .

# Find all event_type assignments
grep -r 'event_type.*=' --include="*.py" . | grep -v ".pyc"

# Find all log_narration calls
grep -r 'log_narration(' --include="*.py" .

# Check narration.jsonl for event types
jq -r '.event_type' narration.jsonl | sort | uniq -c | sort -rn
```

---

## Migration Plan

### Phase 1: Audit (Completed)
- [x] Scan codebase for all event_type strings
- [x] Identify variants and near-misses
- [x] Create canonical taxonomy

### Phase 2: Standardization (Next)
- [ ] Replace all deprecated variants with canonical names
- [ ] Add new canonical events for Friday Profile stages
- [ ] Update all `log_narration()` calls

### Phase 3: Enforcement (Future)
- [ ] Add event_type validation to `log_narration()`
- [ ] Create enum or constant file with canonical names
- [ ] Add linter rule to block non-canonical event types

---

## Usage Examples

### ✅ Correct Usage

```python
from util.narration_logger import log_narration

# Entry block example
log_narration(
    event_type='ENTRY_RATE_LIMIT_BLOCK',
    details={
        'seconds_remaining': 45,
        'last_entry_time': '2025-12-19T00:00:00Z'
    },
    symbol='EUR_USD',
    venue='oanda'
)

# Profit floor example
log_narration(
    event_type='PROFIT_FLOOR_ARMED',
    details={
        'order_id': '12345',
        'original_sl': 1.0995,
        'new_sl': 1.1003,
        'profit_buffer_pips': 0.5,
        'profit_atr': 1.2
    },
    symbol='EUR_USD',
    venue='oanda'
)

# Data-blind fallback example
log_narration(
    event_type='DATA_BLIND_FALLBACK_TIGHTEN_ONLY',
    details={
        'order_id': '12345',
        'action_taken': 'profit_floor_only',
        'reason': 'recent_candles_empty'
    },
    symbol='EUR_USD',
    venue='oanda'
)
```

### ❌ Incorrect Usage

```python
# DON'T use custom event types
log_narration(
    event_type='MY_CUSTOM_EVENT',  # ❌ Not in taxonomy
    details={'foo': 'bar'},
    symbol='EUR_USD'
)

# DON'T use deprecated variants
log_narration(
    event_type='SL_UPDATED',  # ❌ Use TRAILING_STOP_TIGHTENED
    details={'new_sl': 1.1010},
    symbol='EUR_USD'
)

# DON'T omit required fields
log_narration(
    event_type='PROFIT_FLOOR_ARMED',
    details={'new_sl': 1.1003},  # ❌ Missing order_id, original_sl, etc.
    symbol='EUR_USD'
)
```

---

## Maintenance Notes

**Last Updated:** 2025-12-19  
**Maintainer:** Automated Friday Profile Recovery  
**Review Frequency:** After any new event type addition

**Change Log:**
- 2025-12-19: Initial taxonomy created
- 2025-12-19: Added Friday Profile stage events
- 2025-12-19: Added broker error events
