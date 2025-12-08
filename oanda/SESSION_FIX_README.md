# OANDA Connector Session Fix

## Problem
The OANDA trading engine was showing:
- `Session: off_hours | Active: False | Strategies: []`
- Trading was not occurring during certain hours

## Solution
Updated `/oanda/oanda_trading_engine.py` to:

1. **Always show active session for practice mode**: Practice/paper trading should not be restricted by market hours
2. **Display session status**: Shows current session state, active status, and loaded strategies
3. **Display ATR trailing stops**: Shows current trailing stop levels for active positions
4. **Market hours check only for live mode**: Live trading respects Forex market hours (Sunday 5pm EST - Friday 5pm EST)

## Changes Made

### File: `/oanda/oanda_trading_engine.py`

#### Added Session Status Display
```python
# Display session status - always active for practice mode
session_status = "active" if self.environment == 'practice' else self._check_market_hours()
is_active = True if self.environment == 'practice' else session_status == "active"
active_strategies = self.TRADING_PAIRS if is_active else []
self.display.info('Session', f'{session_status} | Active: {is_active} | Strategies: {active_strategies}')
```

#### Added Market Hours Check Method
```python
def _check_market_hours(self):
    """Check if Forex market is currently open (for live mode only)"""
    try:
        from util.market_hours_manager import MarketHoursManager
        manager = MarketHoursManager()
        is_open = manager.is_forex_open()
        return "active" if is_open else "off_hours"
    except (ImportError, AttributeError) as e:
        # If market hours manager not available, default to off_hours for safety
        logger.debug(f"Market hours manager not available: {e}")
        return "off_hours"
```

#### Added ATR Trail Display (with rate limiting)
```python
# Display ATR trailing updates for active positions (only when values change)
for trade in trades:
    symbol = trade.get('instrument') or trade.get('symbol')
    sl_order = trade.get('stopLossOrder') or {}
    current_sl = sl_order.get('price')
    if current_sl and symbol:
        try:
            current_sl_float = float(current_sl)
            # Only display if value changed significantly
            last_value = self._last_atr_trail_values.get(symbol)
            if last_value is None or abs(current_sl_float - last_value) > self.TRAIL_DISPLAY_THRESHOLD:
                self.display.info('ATR Trail', f'{symbol}: {current_sl}')
                self._last_atr_trail_values[symbol] = current_sl_float
        except (ValueError, TypeError):
            pass
```

## Expected Output

After the fix, when running in practice mode, you should see:

```
=== RBOTZILLA Consolidated ===
Env: practice | PIN: 841921

  • Active Positions    : 1
  • Session             : active | Active: True | Strategies: ['EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD', 'USD_CAD']
  • ATR Trail           : USD_CAD: 1.38372
```

## Testing

Run the test script to verify the fix:
```bash
python3 test_oanda_session_fix.py
```

## Usage

### Practice Mode (Paper Trading)
```bash
RICK_ENV=practice python3 oanda/oanda_trading_engine.py
```
- Session: Always "active"
- Active: Always True
- Trading: Not restricted by market hours

### Live Mode (Real Money)
```bash
RICK_ENV=live python3 oanda/oanda_trading_engine.py
```
- Session: "active" or "off_hours" based on Forex market hours
- Active: True only during market hours (Sunday 5pm EST - Friday 5pm EST)
- Trading: Respects market hours

## Notes

- The fix ensures paper trading can occur 24/7 for testing purposes
- Live trading still respects Forex market hours for safety
- The session status display matches the format expected by monitoring systems
- ATR trailing stop levels are displayed for transparency
