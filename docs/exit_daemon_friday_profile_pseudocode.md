# Exit Daemon Friday Profile Pseudocode

**Generated:** 2025-12-19T00:00:25Z  
**Purpose:** Exact, line-by-line implementable specification for exit daemon profit protection

## Overview

This document provides the exact pseudocode for implementing the "Friday Profile" exit daemon that prevents +80 pip → -10 pip round-trips by enforcing aggressive profit protection at multiple stages.

---

## A. Instrument Normalization Functions

### get_pip_size(symbol: str) -> float

```python
def get_pip_size(symbol: str) -> float:
    """
    Return the pip/tick/basis point size for a given instrument.
    
    Args:
        symbol: Trading symbol (e.g., 'EUR_USD', 'BTC_USD', 'NQ')
    
    Returns:
        Pip size as float
    """
    # FX: Check if JPY pair
    if '_JPY' in symbol or symbol.startswith('JPY_'):
        return 0.01  # 1 pip for JPY pairs
    
    # FX: Non-JPY pairs
    if '_' in symbol and len(symbol.split('_')) == 2:
        # Assume standard major/minor FX pair
        return 0.0001  # 1 pip for EUR_USD, GBP_USD, etc.
    
    # Crypto: Basis points (0.01% = 1 bp)
    crypto_symbols = ['BTC', 'ETH', 'SOL', 'XRP', 'ADA', 'DOGE', 'AVAX', 'DOT']
    if any(crypto in symbol for crypto in crypto_symbols):
        return 0.0001  # 1 basis point = 0.01%
    
    # Futures: Look up contract spec (simplified - use config in production)
    futures_specs = {
        'ES': 0.25,   # E-mini S&P 500
        'NQ': 0.25,   # E-mini Nasdaq
        'YM': 1.0,    # E-mini Dow
        'RTY': 0.10,  # E-mini Russell 2000
    }
    
    for code, tick in futures_specs.items():
        if code in symbol:
            return tick
    
    # Default: Assume standard FX
    return 0.0001
```

### get_profit_floor_thresholds(symbol: str) -> dict

```python
def get_profit_floor_thresholds(symbol: str) -> dict:
    """
    Return profit floor trigger and SL offset for instrument.
    
    Returns:
        {
            'trigger_pips': float,  # Profit needed to arm floor
            'sl_offset_pips': float  # How far above entry to place SL
        }
    """
    pip_size = get_pip_size(symbol)
    
    # FX (non-JPY): Very tight
    if pip_size == 0.0001:
        return {
            'trigger_pips': 0.5,  # Arm at +0.5 pips profit
            'sl_offset_pips': 0.3  # Place SL at entry + 0.3 pips
        }
    
    # FX (JPY): Slightly wider
    if pip_size == 0.01:
        return {
            'trigger_pips': 5.0,  # Arm at +5 pips profit
            'sl_offset_pips': 3.0  # Place SL at entry + 3 pips
        }
    
    # Crypto (basis points)
    if any(crypto in symbol for crypto in ['BTC', 'ETH', 'SOL']):
        return {
            'trigger_pips': 5.0,  # Arm at +5 bps profit (0.05%)
            'sl_offset_pips': 3.0  # Place SL at entry + 3 bps
        }
    
    # Futures (ticks)
    return {
        'trigger_pips': 1.0,   # Arm at +1 tick profit
        'sl_offset_pips': 0.5  # Place SL at entry + 0.5 ticks
    }
```

### calculate_profit_in_pips(entry: float, current: float, symbol: str, direction: str) -> float

```python
def calculate_profit_in_pips(entry: float, current: float, symbol: str, direction: str) -> float:
    """
    Calculate current profit in pips/ticks/bps.
    
    Args:
        entry: Entry price
        current: Current price
        symbol: Trading symbol
        direction: 'buy' or 'sell'
    
    Returns:
        Profit in pips (positive = profit, negative = loss)
    """
    pip_size = get_pip_size(symbol)
    
    if direction == 'buy':
        price_diff = current - entry
    else:  # sell
        price_diff = entry - current
    
    return price_diff / pip_size
```

---

## B. State Machine (Per Position)

### Position State Enum

```python
class PositionStage:
    STAGE_0_OCO_CREATED = 0       # Initial bracket order
    STAGE_1_PROFIT_FLOOR_ARMED = 1  # SL moved to entry + buffer
    STAGE_2_TIGHT_TRAIL = 2       # Tight trailing active
    STAGE_3_WEAK_SIGNAL = 3       # Signal weakened, TP restored
    STAGE_4_FAILSAFE = 4          # Data-blind mode
```

### Position State Tracking

```python
class PositionState:
    """Track state for each open position"""
    def __init__(self, order_id: str, symbol: str, entry: float, direction: str,
                 initial_sl: float, initial_tp: float, units: float):
        self.order_id = order_id
        self.symbol = symbol
        self.entry = entry
        self.direction = direction
        self.current_sl = initial_sl
        self.current_tp = initial_tp
        self.units = units
        self.stage = PositionStage.STAGE_0_OCO_CREATED
        self.tp_removed = False
        self.last_update_time = time.time()
        self.momentum_active = False
```

---

## C. Stage Transition Functions

### Stage 0 → Stage 1: Profit Floor

```python
def check_profit_floor_trigger(state: PositionState, current_price: float) -> bool:
    """
    Check if profit floor should be armed.
    
    Returns:
        True if should transition to Stage 1
    """
    if state.stage != PositionStage.STAGE_0_OCO_CREATED:
        return False  # Already past this stage
    
    thresholds = get_profit_floor_thresholds(state.symbol)
    profit_pips = calculate_profit_in_pips(
        state.entry, current_price, state.symbol, state.direction
    )
    
    return profit_pips >= thresholds['trigger_pips']


def arm_profit_floor(state: PositionState, current_price: float, broker) -> bool:
    """
    Move SL to profit floor (entry + buffer).
    
    Returns:
        True if successful, False if failed
    """
    thresholds = get_profit_floor_thresholds(state.symbol)
    pip_size = get_pip_size(state.symbol)
    
    # Calculate new SL
    if state.direction == 'buy':
        new_sl = state.entry + (thresholds['sl_offset_pips'] * pip_size)
    else:  # sell
        new_sl = state.entry - (thresholds['sl_offset_pips'] * pip_size)
    
    # Update at broker
    success = broker.modify_stop_loss(state.order_id, new_sl)
    
    if success:
        # Log narration
        log_narration(
            event_type='PROFIT_FLOOR_ARMED',
            details={
                'order_id': state.order_id,
                'original_sl': state.current_sl,
                'new_sl': new_sl,
                'profit_buffer_pips': thresholds['trigger_pips'],
                'profit_atr': calculate_profit_in_atr(state, current_price)
            },
            symbol=state.symbol,
            venue='oanda'
        )
        
        # Update state
        state.current_sl = new_sl
        state.stage = PositionStage.STAGE_1_PROFIT_FLOOR_ARMED
        state.last_update_time = time.time()
        return True
    else:
        # Log failure
        log_narration(
            event_type='BROKER_MODIFICATION_FAILED',
            details={
                'order_id': state.order_id,
                'modification_type': 'profit_floor_sl',
                'error_code': broker.last_error_code,
                'error_message': broker.last_error_message
            },
            symbol=state.symbol,
            venue='oanda'
        )
        return False
```

### Stage 1 → Stage 2: TP Removal + Tight Trailing

```python
def check_strong_signal(state: PositionState, confidence: float, profit_atr: float,
                       trend_strength: float, market_cycle: str, volatility: float) -> bool:
    """
    Check if signal is strong enough to remove TP and activate tight trailing.
    
    Strong Signal Criteria:
    - Confidence >= baseline + 0.10 (e.g., 0.70 + 0.10 = 0.80)
    - Profit >= 2x ATR
    - Trend strength > 0.65
    - Market cycle contains 'STRONG' OR volatility > 1.2
    """
    if state.stage < PositionStage.STAGE_1_PROFIT_FLOOR_ARMED:
        return False  # Must have profit floor first
    
    MIN_CONFIDENCE_BASELINE = 0.70  # From config or hardcoded
    MIN_CONFIDENCE_BONUS = 0.10
    
    return (
        confidence >= (MIN_CONFIDENCE_BASELINE + MIN_CONFIDENCE_BONUS) and
        profit_atr >= 2.0 and
        trend_strength > 0.65 and
        ('STRONG' in market_cycle or volatility > 1.2)
    )


def remove_tp_activate_trailing(state: PositionState, broker, momentum_strength: float) -> bool:
    """
    Remove TP and activate tight trailing.
    
    Returns:
        True if successful
    """
    # Remove TP (or set to astronomical level)
    success = broker.modify_take_profit(state.order_id, tp=None)  # or tp=9999999
    
    if success:
        log_narration(
            event_type='TP_REMOVED_MOMENTUM_DETECTED',
            details={
                'order_id': state.order_id,
                'original_tp': state.current_tp,
                'momentum_strength': momentum_strength,
                'profit_atr': calculate_profit_in_atr(state, broker.get_current_price(state.symbol))
            },
            symbol=state.symbol,
            venue='oanda'
        )
        
        state.current_tp = None
        state.tp_removed = True
        state.momentum_active = True
        state.stage = PositionStage.STAGE_2_TIGHT_TRAIL
        state.last_update_time = time.time()
        return True
    
    return False
```

### Stage 2: Progressive Trailing Updates

```python
def update_trailing_stop(state: PositionState, current_price: float, atr: float, broker) -> bool:
    """
    Update trailing stop based on profit level.
    
    Uses SmartTrailingSystem logic:
    - 0-1x ATR: 1.2x ATR trail
    - 1-2x ATR: 1.0x ATR trail
    - 2-3x ATR: 0.8x ATR trail
    - 3-4x ATR: 0.6x ATR trail
    - 4-5x ATR: 0.5x ATR trail
    - 5+x ATR: 0.4x ATR trail
    
    If momentum_active: Apply 1.15x loosening factor
    """
    profit_atr = calculate_profit_in_atr(state, current_price)
    
    # Calculate trailing distance
    if profit_atr < 1.0:
        multiplier = 1.2
    elif profit_atr < 2.0:
        multiplier = 1.0
    elif profit_atr < 3.0:
        multiplier = 0.8
    elif profit_atr < 4.0:
        multiplier = 0.6
    elif profit_atr < 5.0:
        multiplier = 0.5
    else:
        multiplier = 0.4  # Ultra tight for huge winners
    
    # Momentum loosening
    if state.momentum_active:
        multiplier *= 1.15
    
    trail_distance = atr * multiplier
    
    # Calculate new SL
    if state.direction == 'buy':
        new_sl = current_price - trail_distance
    else:  # sell
        new_sl = current_price + trail_distance
    
    # Only move SL if it's tightening (never widen)
    if state.direction == 'buy' and new_sl <= state.current_sl:
        return False  # Would loosen SL
    if state.direction == 'sell' and new_sl >= state.current_sl:
        return False  # Would loosen SL
    
    # Update at broker
    success = broker.modify_stop_loss(state.order_id, new_sl)
    
    if success:
        log_narration(
            event_type='TRAILING_STOP_TIGHTENED',
            details={
                'order_id': state.order_id,
                'old_sl': state.current_sl,
                'new_sl': new_sl,
                'trail_distance': trail_distance,
                'profit_atr': profit_atr
            },
            symbol=state.symbol,
            venue='oanda'
        )
        
        state.current_sl = new_sl
        state.last_update_time = time.time()
        return True
    
    return False
```

### Stage 3: Weak Signal Detection

```python
def check_weak_signal(state: PositionState, confidence: float, consensus: str,
                     previous_consensus: str) -> bool:
    """
    Check if signal has weakened.
    
    Weak Signal Criteria:
    - Confidence drops below threshold (e.g., < 0.70)
    - Consensus flips (buy → sell or sell → buy)
    """
    MIN_CONFIDENCE_THRESHOLD = 0.70
    
    confidence_weak = confidence < MIN_CONFIDENCE_THRESHOLD
    consensus_flipped = (
        (previous_consensus == 'buy' and consensus == 'sell') or
        (previous_consensus == 'sell' and consensus == 'buy')
    )
    
    return confidence_weak or consensus_flipped


def restore_tp_on_weak_signal(state: PositionState, current_price: float,
                              atr: float, broker) -> bool:
    """
    Re-attach TP at conservative level when signal weakens.
    
    Conservative TP: 1.5x ATR from current price
    """
    if not state.tp_removed:
        return False  # TP already exists
    
    # Calculate conservative TP
    if state.direction == 'buy':
        new_tp = current_price + (1.5 * atr)
    else:  # sell
        new_tp = current_price - (1.5 * atr)
    
    success = broker.modify_take_profit(state.order_id, new_tp)
    
    if success:
        log_narration(
            event_type='TP_RESTORED_WEAK_SIGNAL',
            details={
                'order_id': state.order_id,
                'new_tp': new_tp,
                'confidence': confidence,
                'profit_atr': calculate_profit_in_atr(state, current_price)
            },
            symbol=state.symbol,
            venue='oanda'
        )
        
        state.current_tp = new_tp
        state.tp_removed = False
        state.stage = PositionStage.STAGE_3_WEAK_SIGNAL
        state.last_update_time = time.time()
        return True
    
    return False
```

### Stage 4: Data-Blind Failsafe

```python
def detect_data_blind_mode(recent_candles: list, atr: float) -> bool:
    """
    Detect if we're in data-blind mode (missing candle context).
    
    Returns:
        True if data-blind
    """
    return (
        recent_candles is None or
        len(recent_candles) == 0 or
        atr is None or
        atr == 0
    )


def apply_data_blind_exit_logic(state: PositionState, current_price: float) -> dict:
    """
    Apply ONLY safe exit logic when in data-blind mode.
    
    Allowed Actions:
    - Tighten loser-kill (if trade negative)
    - Stage 1 profit floor (if profit buffer exists)
    - Stage 2 breakeven move (if already in profit)
    
    NOT Allowed:
    - ATR chandelier stops
    - Structure pivots
    - FVG/Fib tightening
    - Choke mode logic
    
    Returns:
        {
            'action': str,  # 'profit_floor', 'loser_kill', or 'none'
            'new_sl': float or None,
            'reason': 'data_blind_fallback'
        }
    """
    profit_pips = calculate_profit_in_pips(
        state.entry, current_price, state.symbol, state.direction
    )
    
    # If in profit and Stage 0, try profit floor
    if profit_pips > 0 and state.stage == PositionStage.STAGE_0_OCO_CREATED:
        thresholds = get_profit_floor_thresholds(state.symbol)
        if profit_pips >= thresholds['trigger_pips']:
            pip_size = get_pip_size(state.symbol)
            if state.direction == 'buy':
                new_sl = state.entry + (thresholds['sl_offset_pips'] * pip_size)
            else:
                new_sl = state.entry - (thresholds['sl_offset_pips'] * pip_size)
            
            return {
                'action': 'profit_floor',
                'new_sl': new_sl,
                'reason': 'data_blind_fallback'
            }
    
    # If in loss, optionally tighten loser-kill (conservative)
    # (Skip for now - too risky in data-blind mode)
    
    # Default: do nothing
    return {
        'action': 'none',
        'new_sl': None,
        'reason': 'data_blind_fallback'
    }
```

---

## D. Main Exit Daemon Loop

```python
def exit_daemon_loop(broker, config):
    """
    Main loop for exit daemon.
    
    Runs continuously, checking all open positions every N seconds.
    """
    UPDATE_INTERVAL_SECONDS = 15  # Or from config
    
    # Track position states
    position_states = {}  # order_id -> PositionState
    
    while True:
        try:
            # Fetch current broker state
            broker_trades = broker.get_open_trades()
            
            if broker_trades is None:
                # Broker state unavailable - skip this iteration
                log_narration(
                    event_type='BROKER_TRADES_UNAVAILABLE_SKIP_ENTRY',
                    details={'reason': 'api_unavailable'},
                    symbol='SYSTEM',
                    venue='oanda'
                )
                time.sleep(UPDATE_INTERVAL_SECONDS)
                continue
            
            # Process each open trade
            for trade in broker_trades:
                order_id = trade['id']
                symbol = trade['symbol']
                current_price = broker.get_current_price(symbol)
                
                # Initialize state if new trade
                if order_id not in position_states:
                    position_states[order_id] = PositionState(
                        order_id=order_id,
                        symbol=symbol,
                        entry=trade['entry_price'],
                        direction=trade['direction'],
                        initial_sl=trade['stop_loss'],
                        initial_tp=trade['take_profit'],
                        units=trade['units']
                    )
                
                state = position_states[order_id]
                
                # Fetch candle context
                recent_candles = broker.get_recent_candles(symbol, count=100)
                atr = calculate_atr(recent_candles) if recent_candles else None
                
                # Check for data-blind mode
                if detect_data_blind_mode(recent_candles, atr):
                    # Data-blind failsafe
                    result = apply_data_blind_exit_logic(state, current_price)
                    if result['action'] != 'none':
                        broker.modify_stop_loss(order_id, result['new_sl'])
                        log_narration(
                            event_type='DATA_BLIND_FALLBACK_TIGHTEN_ONLY',
                            details={
                                'order_id': order_id,
                                'action_taken': result['action'],
                                'reason': result['reason']
                            },
                            symbol=symbol,
                            venue='oanda'
                        )
                    continue  # Skip normal logic
                
                # Stage 0 → Stage 1: Profit floor
                if check_profit_floor_trigger(state, current_price):
                    arm_profit_floor(state, current_price, broker)
                
                # Stage 1 → Stage 2: Check strong signal for TP removal
                if state.stage == PositionStage.STAGE_1_PROFIT_FLOOR_ARMED:
                    # Get signal strength from Hive/Wolfpack
                    confidence, trend_strength, market_cycle, volatility = get_signal_metrics(symbol)
                    profit_atr = calculate_profit_in_atr(state, current_price)
                    
                    if check_strong_signal(state, confidence, profit_atr,
                                          trend_strength, market_cycle, volatility):
                        momentum_strength = min(profit_atr / 2.0, 5.0)
                        remove_tp_activate_trailing(state, broker, momentum_strength)
                
                # Stage 2: Update trailing stop
                if state.stage >= PositionStage.STAGE_2_TIGHT_TRAIL:
                    # Check if enough time has passed since last update
                    if time.time() - state.last_update_time >= UPDATE_INTERVAL_SECONDS:
                        update_trailing_stop(state, current_price, atr, broker)
                
                # Check for weak signal (any stage)
                if state.stage >= PositionStage.STAGE_1_PROFIT_FLOOR_ARMED:
                    confidence, consensus = get_current_consensus(symbol)
                    previous_consensus = get_previous_consensus(symbol)
                    
                    if check_weak_signal(state, confidence, consensus, previous_consensus):
                        restore_tp_on_weak_signal(state, current_price, atr, broker)
            
            # Clean up closed positions
            open_order_ids = {trade['id'] for trade in broker_trades}
            closed_order_ids = set(position_states.keys()) - open_order_ids
            for order_id in closed_order_ids:
                del position_states[order_id]
            
        except Exception as e:
            log_narration(
                event_type='BROKER_STATE_REFRESH_FAILED',
                details={
                    'error_code': type(e).__name__,
                    'error_message': str(e)
                },
                symbol='SYSTEM',
                venue='oanda'
            )
        
        # Sleep before next iteration
        time.sleep(UPDATE_INTERVAL_SECONDS)
```

---

## E. Helper Functions

```python
def calculate_profit_in_atr(state: PositionState, current_price: float) -> float:
    """Calculate current profit in ATR multiples."""
    # Fetch ATR (simplified - use caching in production)
    recent_candles = broker.get_recent_candles(state.symbol, count=100)
    atr = calculate_atr(recent_candles) if recent_candles else 0.001
    
    if state.direction == 'buy':
        price_diff = current_price - state.entry
    else:
        price_diff = state.entry - current_price
    
    return price_diff / atr if atr > 0 else 0.0


def calculate_atr(candles: list, period: int = 14) -> float:
    """Calculate Average True Range."""
    if not candles or len(candles) < period:
        return None
    
    # Simplified ATR calculation
    # (In production, use proper TA library or cached values)
    true_ranges = []
    for i in range(1, len(candles)):
        high = candles[i]['high']
        low = candles[i]['low']
        prev_close = candles[i-1]['close']
        
        tr = max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        )
        true_ranges.append(tr)
    
    if len(true_ranges) < period:
        return None
    
    return sum(true_ranges[-period:]) / period


def get_signal_metrics(symbol: str) -> tuple:
    """
    Get current signal metrics from Hive/Wolfpack.
    
    Returns:
        (confidence, trend_strength, market_cycle, volatility)
    """
    # Query Hive Mind / Wolfpack (simplified)
    # In production, integrate with actual hive/wolfpack modules
    return (0.75, 0.70, 'BULL_STRONG', 1.3)


def get_current_consensus(symbol: str) -> tuple:
    """
    Get current consensus from Hive/Wolfpack.
    
    Returns:
        (confidence, consensus)  # consensus: 'buy', 'sell', 'neutral'
    """
    return (0.75, 'buy')


def get_previous_consensus(symbol: str) -> str:
    """Get previous consensus (cached)."""
    return 'buy'  # Simplified - use state tracking in production
```

---

## F. Broker Error Handling

```python
def handle_no_such_trade_error(order_id: str, symbol: str, broker):
    """
    Handle NO_SUCH_TRADE error from broker.
    
    Actions:
    1. Treat trade as already closed
    2. Refresh broker trades state (one retry max)
    3. Do NOT re-open immediately
    4. Apply cooldown to prevent re-entry loop
    """
    log_narration(
        event_type='BROKER_TRADE_NOT_FOUND_TREAT_CLOSED',
        details={
            'order_id': order_id,
            'broker_response': 'NO_SUCH_TRADE',
            'action_taken': 'treat_as_closed'
        },
        symbol=symbol,
        venue='oanda'
    )
    
    # Refresh broker state (one retry)
    broker.refresh_trades()
    
    # Add to cooldown list (reuse rate limiter)
    add_to_entry_cooldown(symbol, cooldown_seconds=60)
```

---

## G. Integration Notes

### Wiring to Main Engine

1. **Standalone Daemon (Recommended):**
   - Run as separate process
   - Communicates with broker independently
   - Survives engine restarts

2. **Embedded in Engine:**
   - Run as background thread in `oanda_trading_engine.py`
   - Shares broker connector instance
   - Simpler deployment but less fault-tolerant

### Configuration

Add to `configs/exit_daemon_config.json`:

```json
{
  "enabled": true,
  "update_interval_seconds": 15,
  "profit_floor": {
    "fx_non_jpy_trigger_pips": 0.5,
    "fx_non_jpy_offset_pips": 0.3,
    "fx_jpy_trigger_pips": 5.0,
    "fx_jpy_offset_pips": 3.0,
    "crypto_trigger_bps": 5.0,
    "crypto_offset_bps": 3.0,
    "futures_trigger_ticks": 1.0,
    "futures_offset_ticks": 0.5
  },
  "strong_signal": {
    "min_confidence_baseline": 0.70,
    "min_confidence_bonus": 0.10,
    "min_profit_atr": 2.0,
    "min_trend_strength": 0.65
  },
  "weak_signal": {
    "min_confidence_threshold": 0.70,
    "conservative_tp_atr_multiple": 1.5
  }
}
```

---

## H. Testing Checklist

- [ ] Test profit floor: Entry @ 1.1000, price @ 1.1005 → SL @ 1.1003
- [ ] Test TP removal: 2x ATR profit + strong signal → TP canceled
- [ ] Test trailing: 3x ATR profit → SL trails at 0.8x ATR
- [ ] Test weak signal: Confidence 0.80 → 0.65 → TP restored
- [ ] Test data-blind: Empty candles → only profit floor allowed
- [ ] Test NO_SUCH_TRADE: Error response → treat as closed, apply cooldown
- [ ] Test never widen: Ensure SL only tightens, never loosens

---

**END OF PSEUDOCODE**
