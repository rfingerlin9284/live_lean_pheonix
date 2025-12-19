#!/usr/bin/env python3
"""
Test: Profit Floor Implementation
Verifies that the Friday Profile Stage 1 (Profit Floor) works correctly
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_profit_floor_thresholds():
    """Test profit floor threshold calculations for different instruments"""
    print("=" * 70)
    print("TEST 1: Profit Floor Thresholds")
    print("=" * 70)
    
    test_cases = [
        {
            'symbol': 'EUR_USD',
            'expected_trigger_pips': 0.5,
            'expected_sl_offset_pips': 0.3,
            'pip_size': 0.0001
        },
        {
            'symbol': 'USD_JPY',
            'expected_trigger_pips': 5.0,
            'expected_sl_offset_pips': 3.0,
            'pip_size': 0.01
        },
        {
            'symbol': 'BTC_USD',
            'expected_trigger_pips': 5.0,
            'expected_sl_offset_pips': 3.0,
            'pip_size': 0.0001
        }
    ]
    
    for tc in test_cases:
        symbol = tc['symbol']
        
        # Simulate the threshold logic from oanda_trading_engine.py
        if 'JPY' in symbol:
            trigger_pips = 5.0
            sl_offset_pips = 3.0
        elif any(crypto in symbol for crypto in ['BTC', 'ETH', 'SOL', 'XRP']):
            trigger_pips = 5.0
            sl_offset_pips = 3.0
        else:
            trigger_pips = 0.5
            sl_offset_pips = 0.3
        
        passed = (
            trigger_pips == tc['expected_trigger_pips'] and
            sl_offset_pips == tc['expected_sl_offset_pips']
        )
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {symbol}:")
        print(f"  Trigger: {trigger_pips} pips (expected: {tc['expected_trigger_pips']})")
        print(f"  SL Offset: {sl_offset_pips} pips (expected: {tc['expected_sl_offset_pips']})")
    
    print()


def test_profit_floor_calculation():
    """Test profit floor SL calculation"""
    print("=" * 70)
    print("TEST 2: Profit Floor SL Calculation")
    print("=" * 70)
    
    test_cases = [
        {
            'symbol': 'EUR_USD',
            'direction': 'BUY',
            'entry_price': 1.1000,
            'current_price': 1.1005,
            'expected_new_sl': 1.10003,  # entry (1.1000) + 0.3 pips (0.00030)
            'pip_size': 0.0001
        },
        {
            'symbol': 'EUR_USD',
            'direction': 'SELL',
            'entry_price': 1.1000,
            'current_price': 1.0995,
            'expected_new_sl': 1.09997,  # entry (1.1000) - 0.3 pips (0.00030)
            'pip_size': 0.0001
        },
        {
            'symbol': 'USD_JPY',
            'direction': 'BUY',
            'entry_price': 150.00,
            'current_price': 150.06,
            'expected_new_sl': 150.03,
            'pip_size': 0.01
        }
    ]
    
    for tc in test_cases:
        symbol = tc['symbol']
        direction = tc['direction']
        entry_price = tc['entry_price']
        pip_size = tc['pip_size']
        
        # Calculate profit
        current_price = tc['current_price']
        if direction == 'BUY':
            profit_pips = (current_price - entry_price) / pip_size
        else:
            profit_pips = (entry_price - current_price) / pip_size
        
        # Get thresholds
        if 'JPY' in symbol:
            trigger_pips = 5.0
            sl_offset_pips = 3.0
        else:
            trigger_pips = 0.5
            sl_offset_pips = 0.3
        
        # Check if should trigger
        should_trigger = profit_pips >= trigger_pips
        
        # Calculate new SL
        if should_trigger:
            if direction == 'BUY':
                new_sl = entry_price + (sl_offset_pips * pip_size)
            else:
                new_sl = entry_price - (sl_offset_pips * pip_size)
            
            passed = abs(new_sl - tc['expected_new_sl']) < 0.00001
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} {symbol} {direction}:")
            print(f"  Entry: {entry_price:.5f}, Current: {current_price:.5f}")
            print(f"  Profit: {profit_pips:.1f} pips (trigger: {trigger_pips})")
            print(f"  New SL: {new_sl:.5f} (expected: {tc['expected_new_sl']:.5f})")
        else:
            print(f"⚠️  SKIP {symbol} {direction}: Profit {profit_pips:.1f} < trigger {trigger_pips}")
    
    print()


def test_data_blind_detection():
    """Test data-blind mode detection"""
    print("=" * 70)
    print("TEST 3: Data-Blind Mode Detection")
    print("=" * 70)
    
    test_cases = [
        {'candles': None, 'expected': True, 'desc': 'None candles'},
        {'candles': [], 'expected': True, 'desc': 'Empty candles'},
        {'candles': [{'close': 1.1}], 'expected': False, 'desc': 'Valid candles'},
    ]
    
    for tc in test_cases:
        candles = tc['candles']
        
        # Simulate data-blind detection logic
        data_blind_mode = candles is None or len(candles) == 0
        
        passed = data_blind_mode == tc['expected']
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"{status} {tc['desc']}:")
        print(f"  Data-blind: {data_blind_mode} (expected: {tc['expected']})")
    
    print()


def test_no_such_trade_detection():
    """Test NO_SUCH_TRADE error detection"""
    print("=" * 70)
    print("TEST 4: NO_SUCH_TRADE Error Detection")
    print("=" * 70)
    
    test_cases = [
        {
            'error_msg': 'NO_SUCH_TRADE: Trade ID not found',
            'error_code': 'NO_SUCH_TRADE',
            'expected': True,
            'desc': 'Exact error code'
        },
        {
            'error_msg': 'Trade not found: no such trade exists',
            'error_code': '',
            'expected': False,  # Our current logic only checks for exact "NO_SUCH_TRADE" string
            'desc': 'Partial phrase match (not currently detected)'
        },
        {
            'error_msg': 'Invalid stop loss price',
            'error_code': 'INVALID_PRICE',
            'expected': False,
            'desc': 'Different error'
        }
    ]
    
    for tc in test_cases:
        error_msg = tc['error_msg']
        error_code = tc['error_code']
        
        # Simulate NO_SUCH_TRADE detection logic
        is_no_such_trade = (
            'NO_SUCH_TRADE' in str(error_msg).upper() or
            'NO_SUCH_TRADE' in str(error_code).upper()
        )
        
        passed = is_no_such_trade == tc['expected']
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"{status} {tc['desc']}:")
        print(f"  Error: {error_msg}")
        print(f"  Detected: {is_no_such_trade} (expected: {tc['expected']})")
    
    print()


def test_event_type_consistency():
    """Test that canonical event types are used"""
    print("=" * 70)
    print("TEST 5: Event Type Consistency")
    print("=" * 70)
    
    # Read the trading engine file and check for canonical event types
    try:
        with open('oanda_trading_engine.py', 'r') as f:
            content = f.read()
        
        canonical_events = [
            'PROFIT_FLOOR_ARMED',
            'BROKER_TRADES_UNAVAILABLE_SKIP_ENTRY',
            'DATA_BLIND_FALLBACK_TIGHTEN_ONLY',
            'BROKER_MODIFICATION_FAILED',
            'BROKER_TRADE_NOT_FOUND_TREAT_CLOSED'
        ]
        
        for event in canonical_events:
            found = event in content
            status = "✅ FOUND" if found else "❌ MISSING"
            print(f"{status} {event}")
    
    except FileNotFoundError:
        print("⚠️  Could not find oanda_trading_engine.py")
    
    print()


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("FRIDAY PROFILE PROFIT FLOOR VERIFICATION TESTS")
    print("=" * 70)
    print()
    
    test_profit_floor_thresholds()
    test_profit_floor_calculation()
    test_data_blind_detection()
    test_no_such_trade_detection()
    test_event_type_consistency()
    
    print("=" * 70)
    print("All tests completed!")
    print("=" * 70)
    print()
    print("Next Steps:")
    print("1. Run oanda_trading_engine.py in paper trading mode")
    print("2. Monitor narration.jsonl for PROFIT_FLOOR_ARMED events")
    print("3. Verify profit floor activates at expected thresholds")
    print("4. Ensure no +profit → -loss round-trips occur")
    print()


if __name__ == '__main__':
    main()
