#!/usr/bin/env python3
"""
Coinbase Trading Engine - Canary mode aware clone of the OANDA engine
This engine enforces the AgentCharter and reads sector config; Canary mode avoids live orders
PIN: 841921
"""
import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import Dict

# Ensure repo root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from foundation.rick_charter import RickCharter
from foundation.agent_charter import AgentCharter
from util.sector_loader import load_sectors
CoinbaseConnector = None
from util.terminal_display import TerminalDisplay
from util.narration_logger import log_narration
from util.position_police import _rbz_force_min_notional_position_police
from systems.momentum_signals import generate_signal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('coinbase_consolidated')


class CoinbaseTradingEngine:
    def __init__(self, environment: str = 'practice'):
        # Enforce Agent Charter at startup
        AgentCharter.enforce()
        if not getattr(RickCharter, 'PIN', None) == 841921:
            raise PermissionError('Invalid Charter PIN')

        self.sectors = load_sectors()
        self.cfg = self.sectors.get('coinbase', {})
        self.mode = self.cfg.get('mode', 'disabled')

        self.display = TerminalDisplay()
        self.environment = environment
        # Initialize connector instance; CoinbaseAdvancedConnector has a slightly different API
        # Lazy import connector to avoid hard import-time dependency failures (e.g., coinbase libs)
        try:
            from brokers.coinbase_advanced_connector import CoinbaseAdvancedConnector as CoinbaseConnector
            self.coinbase = CoinbaseConnector(pin=841921)
        except Exception as e:
            logger.warning('Coinbase connector could not be imported: %s; using minimal stub', e)
            class _Stub:
                def __init__(self):
                    self.account_id = 'paper-coinbase'
                    self.api_token = None
                    self.api_base = None
                def get_current_positions(self):
                    return []
                def place_market_order(self, *a, **k):
                    return {'success': True, 'order_id': 'COINBASE:PAPER:SIM'}
            self.coinbase = _Stub()

        # Safety constants hard-coded; maintain Balanced profile defaults
        self.MIN_CONFIDENCE = 0.55
        self.MAX_POSITIONS = 12
        self.STOP_LOSS_PIPS = 10
        self.TAKE_PROFIT_PIPS = 32
        self.TRAILING_START_PIPS = 3
        self.TRAILING_DIST_PIPS = 5
        self.TRADING_PAIRS = ['BTC_USD', 'ETH_USD', 'ADA_USD']

        self.running = False
        self.active_positions: Dict[str, dict] = {}

        self._announce()

    def _announce(self):
        self.display.clear_screen()
        self.display.header('RICK COINBASE Canary', f'Mode: {self.mode} | PIN: {getattr(RickCharter, "PIN", "N/A")}')
        try:
            log_narration(
                event_type="PROFILE_STATUS",
                details={
                    "description": "Balanced profile applied (Coinbase Canary)",
                    "min_expected_pnl_usd": getattr(RickCharter, 'MIN_EXPECTED_PNL_USD', None),
                    "min_notional_usd": getattr(RickCharter, 'MIN_NOTIONAL_USD', None),
                },
                symbol='SYSTEM',
                venue='coinbase'
            )
        except Exception as e:
            logger.debug('Profile status narration failed: %s', e)

    def _run_police(self):
        try:
            account_id = getattr(self.coinbase, 'account_id', getattr(self.coinbase, 'client', None))
            api_token = getattr(self.coinbase, 'api_token', None)
            api_base = getattr(self.coinbase, 'api_base', None)
            _rbz_force_min_notional_position_police(account_id=account_id, token=api_token, api_base=api_base)
        except Exception as e:
            logger.warning('Position police error: %s', e)

    async def run(self):
        self.running = True
        while self.running:
            try:
                trades = []
                if hasattr(self.coinbase, 'get_trades'):
                    trades = self.coinbase.get_trades() or []
                elif hasattr(self.coinbase, 'get_current_positions'):
                    # Convert positions to simplified trades
                    trades = [{
                        'id': f"pos_{i}",
                        'instrument': p.get('symbol') if isinstance(p, dict) else None,
                        'units': p.get('size') if isinstance(p, dict) else 0,
                        'price': p.get('price', 0) if isinstance(p, dict) else 0
                    } for i, p in enumerate(self.coinbase.get_current_positions() or [])]
                self.active_positions = {t['id']: t for t in trades}
                self.display.info('Active Positions', str(len(self.active_positions)))

                self._run_police()

                if len(self.active_positions) < self.MAX_POSITIONS:
                    for symbol in self.TRADING_PAIRS:
                        if any((t.get('instrument') or t.get('symbol')) == symbol for t in trades):
                            continue
                        if hasattr(self.coinbase, 'get_historical_data'):
                            candles = self.coinbase.get_historical_data(symbol, count=100, granularity='M15')
                        else:
                            candles = []
                        sig, conf = generate_signal(symbol, candles)
                        if sig and conf >= self.MIN_CONFIDENCE:
                            await self._open_trade(symbol, sig, conf)
                            await asyncio.sleep(1)

                for trade in trades:
                    await self._manage_trade(trade)

                await asyncio.sleep(30)
            except Exception as e:
                logger.error('Engine main loop error: %s', e)
                await asyncio.sleep(5)

    async def _open_trade(self, symbol: str, direction: str, confidence: float):
        if hasattr(self.coinbase, 'get_live_prices'):
            prices = self.coinbase.get_live_prices([symbol])
        else:
            prices = {symbol: {'bid': None, 'ask': None}}
        if not prices or symbol not in prices:
            return
        snap = prices[symbol]
        bid = snap.get('bid')
        ask = snap.get('ask')
        entry = ask if direction == 'BUY' else bid
        if entry is None:
            return
        try:
            entry = float(entry)
        except Exception:
            return

        pip = 0.01 if 'JPY' in symbol else 0.0001
        sl = entry - (self.STOP_LOSS_PIPS * pip) if direction == 'BUY' else entry + (self.STOP_LOSS_PIPS * pip)
        tp = entry + (self.TAKE_PROFIT_PIPS * pip) if direction == 'BUY' else entry - (self.TAKE_PROFIT_PIPS * pip)

        units = int(getattr(RickCharter, 'MIN_NOTIONAL_USD', 15000) / max(entry, 1e-9))
        units = units if direction == 'BUY' else -units
        risk_usd = abs(entry - sl) * abs(units)
        reward_usd = abs(tp - entry) * abs(units)

        self.display.info('Placing', f"{symbol} {direction} | SL: {sl:.5f} (-${risk_usd:.2f}) | TP: {tp:.5f} (+${reward_usd:.2f})")
        log_narration(event_type='TRADE_SIGNAL', details={'symbol': symbol, 'direction': direction, 'confidence': confidence})

        # Canary mode: do not submit orders, just log
        if self.mode == 'canary':
            log_narration(event_type='CANARY_SIGNAL', details={'symbol': symbol, 'direction': direction, 'confidence': confidence}, symbol=symbol, venue='coinbase')
            self.display.info('Canary', f'CANARY: Not executing orders for {symbol} in canary mode')
            return {'success': True, 'order_id': 'CANARY:SIM'}

        result = None
        if hasattr(self.coinbase, 'place_oco_order'):
            result = self.coinbase.place_oco_order(symbol, entry, sl, tp, units)
        elif hasattr(self.coinbase, 'place_market_order'):
            # Fallback to market order for connectors that do not support OCO; 'size_usd' approximates notional
            size_usd = round(abs(units) * entry, 2)
            result = self.coinbase.place_market_order(symbol, 'BUY' if units > 0 else 'SELL', size_usd)
        else:
            result = {'success': False, 'error': 'Connector does not support order submission'}
        if result.get('success'):
            order_id = result.get('order_id')
            self.display.alert(f"✅ OCO order placed! Order ID: {order_id}", 'SUCCESS')
            self.display.trade_open(symbol, direction, entry, f"Stop: {sl:.5f} | Target: {tp:.5f} | Size: {abs(units):,} units | Notional: ${abs(units)*entry:,.0f}")
            log_narration(event_type='TRADE_OPENED', details={'symbol': symbol, 'entry_price': entry, 'stop_loss': sl, 'take_profit': tp, 'stop_loss_usd': round(risk_usd, 2), 'take_profit_usd': round(reward_usd, 2)})
        else:
            self.display.error('Order failed: ' + str(result.get('error')))

    async def _manage_trade(self, trade):
        try:
            is_long = float(trade.get('currentUnits', trade.get('units', 0))) > 0
            entry = float(trade.get('price') or trade.get('entryPrice') or 0)
            sl_order = trade.get('stopLossOrder') or {}
            price_val = sl_order.get('price') if sl_order else None
            current_sl = float(price_val) if price_val is not None else None
            symbol = trade.get('instrument') or trade.get('symbol')
            if hasattr(self.coinbase, 'get_live_prices'):
                prices = self.coinbase.get_live_prices([symbol])
            else:
                prices = {symbol: {'bid': None, 'ask': None}}
            if not prices or symbol not in prices:
                return
            snap = prices[symbol]
            curr = snap.get('bid') if is_long else snap.get('ask')
            if curr is None:
                return
            curr = float(curr)
            pip = 0.01 if 'JPY' in symbol else 0.0001
            profit_pips = (curr - entry) / pip if is_long else (entry - curr) / pip
            if profit_pips > self.TRAILING_START_PIPS and current_sl is not None:
                new_sl = curr - (self.TRAILING_DIST_PIPS * pip) if is_long else curr + (self.TRAILING_DIST_PIPS * pip)
                if (is_long and new_sl > current_sl) or (not is_long and new_sl < current_sl):
                    self.display.info('Trailing', f"{symbol}: {current_sl:.5f} -> {new_sl:.5f}")
                    if hasattr(self.coinbase, 'set_trade_stop'):
                        self.coinbase.set_trade_stop(trade.get('id'), new_sl)
        except Exception:
            pass


if __name__ == '__main__':
    engine = CoinbaseTradingEngine(environment=os.getenv('RICK_ENV', 'practice'))
    try:
        asyncio.run(engine.run())
    except KeyboardInterrupt:
        print('\nStopped')
