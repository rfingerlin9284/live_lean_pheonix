#!/usr/bin/env python3
"""
Coinbase Trading Engine - RBOTZILLA
Safe crypto engine (sandbox mode by default)
"""
import os
import sys
import time
import logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from brokers.coinbase_connector import CoinbaseConnector
from util.narration_logger import log_narration
from util.trade_metrics import record_trade_event

def main():
    env = os.getenv('RICK_ENV', 'practice')
    coinbase = CoinbaseConnector(environment=env)
    symbols = ['BTC-USD', 'ETH-USD']
    max_positions = 1
    risk_per_trade = 0.01
    open_positions = 0
    for symbol in symbols:
        if open_positions >= max_positions:
            break
        price = 20000.0 if symbol == 'BTC-USD' else 1000.0
        entry = price
        sl = price * 0.97
        tp = price * 1.05
        size = 0.01
        result = coinbase.place_order(symbol, 'buy', size)
        if result:
            log_narration(event_type='TRADE_OPENED', details={'symbol': symbol, 'entry_price': entry, 'stop_loss': sl, 'take_profit': tp}, symbol=symbol, venue='coinbase')
            record_trade_event('coinbase', symbol, 'BUY', entry, sl, tp, size)
            open_positions += 1
        time.sleep(1)
    print('Coinbase engine run complete.')

if __name__ == '__main__':
    main()
