#!/usr/bin/env python3
"""
OANDA Trading Engine - RBOTZILLA Consolidated Final (Single file)
This file contains the consolidated engine implementation for the OANDA connector.
It uses momentum-based signals, enforces the charter, and applies Tight SL and trailing stops.
PIN: 841921 | Consolidated: 2025-12-03
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import Dict, List

# Ensure repo root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from foundation.rick_charter import RickCharter
from brokers.oanda_connector import OandaConnector
from util.terminal_display import TerminalDisplay
from util.narration_logger import log_narration
from util.position_police import _rbz_force_min_notional_position_police
from systems.momentum_signals import generate_signal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('oanda_consolidated')


class OandaTradingEngine:
	def __init__(self, environment: str = 'practice'):
		if not getattr(RickCharter, 'PIN', None) == 841921:
			raise PermissionError('Invalid Charter PIN')

		self.display = TerminalDisplay()
		self.environment = environment
		self.oanda = OandaConnector(pin=841921, environment=environment)

		# Safety constants hard-coded
		self.MIN_CONFIDENCE = 0.55
		self.MAX_POSITIONS = 12
		self.STOP_LOSS_PIPS = 10
		self.TAKE_PROFIT_PIPS = 32
		self.TRAILING_START_PIPS = 3
		self.TRAILING_DIST_PIPS = 5
		self.TRADING_PAIRS = ['EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD', 'USD_CAD']

		self.running = False
		self.active_positions: Dict[str, dict] = {}

		self._announce()

	def _announce(self):
		self.display.clear_screen()
		self.display.header('RBOTZILLA Consolidated', f'Env: {self.environment} | PIN: {getattr(RickCharter, "PIN", "N/A")}')
		# Log the active profile and critical charter knobs for easier debugging
		try:
			log_narration(
				event_type="PROFILE_STATUS",
				details={
					"description": "Balanced profile applied",
					"min_expected_pnl_usd": getattr(RickCharter, 'MIN_EXPECTED_PNL_USD', None),
					"min_notional_usd": getattr(RickCharter, 'MIN_NOTIONAL_USD', None),
					"max_margin_utilization_pct": getattr(RickCharter, 'MAX_MARGIN_UTILIZATION_PCT', None),
				},
				symbol='SYSTEM',
				venue='oanda'
			)
		except Exception as e:
			logger.debug('Profile status narration failed: %s', e)

	def _run_police(self):
		try:
			_rbz_force_min_notional_position_police(account_id=self.oanda.account_id, token=self.oanda.api_token, api_base=self.oanda.api_base)
		except Exception as e:
			logger.warning('Position police error: %s', e)

	async def run(self):
		self.running = True
		while self.running:
			try:
				trades = self.oanda.get_trades() or []
				self.active_positions = {t['id']: t for t in trades}
				self.display.info('Active Positions', str(len(self.active_positions)))

				# Police enforcement
				self._run_police()

				# Place new trades if capacity allows
				if len(self.active_positions) < self.MAX_POSITIONS:
					for symbol in self.TRADING_PAIRS:
						if any((t.get('instrument') or t.get('symbol')) == symbol for t in trades):
							continue
						candles = self.oanda.get_historical_data(symbol, count=100, granularity='M15')
						sig, conf = generate_signal(symbol, candles)
						if sig and conf >= self.MIN_CONFIDENCE:
							await self._open_trade(symbol, sig, conf)
							await asyncio.sleep(1)

				# Manage open trades
				for trade in trades:
					await self._manage_trade(trade)

				await asyncio.sleep(30)
			except Exception as e:
				logger.error('Engine main loop error: %s', e)
				await asyncio.sleep(5)

	async def _open_trade(self, symbol: str, direction: str, confidence: float):
		prices = self.oanda.get_live_prices([symbol])
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

		result = self.oanda.place_oco_order(symbol, entry, sl, tp, units)
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
			current_sl = float(sl_order.get('price')) if sl_order and sl_order.get('price') is not None else None
			symbol = trade.get('instrument') or trade.get('symbol')
			prices = self.oanda.get_live_prices([symbol])
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
					self.oanda.set_trade_stop(trade.get('id'), new_sl)
		except Exception:
			pass


if __name__ == '__main__':
	engine = OandaTradingEngine(environment=os.getenv('RICK_ENV', 'practice'))
	try:
		asyncio.run(engine.run())
	except KeyboardInterrupt:
		print('\nStopped')
