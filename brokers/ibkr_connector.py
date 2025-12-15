#!/usr/bin/env python3
"""
Lightweight IBKR connector stub for paper-mode runs.
This connector provides local-safety stub methods for the IBKR engine and is intentionally minimal.
"""
from __future__ import annotations

import logging
from typing import List, Dict, Any, Optional
import os
import time
from dataclasses import dataclass
import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    from util.platform_breaker import is_platform_enabled
except Exception:
    def is_platform_enabled(platform: str) -> bool:
        return True

try:
    from ib_insync import IB, Stock, Forex, Order
    IB_INSYNC_AVAILABLE = True
except Exception:
    IB_INSYNC_AVAILABLE = False

logger = logging.getLogger('ibkr_connector')


class IBKRConnector:
    def __init__(self, pin: Optional[int] = None, environment: str = 'paper', host: str = '127.0.0.1', port: int = 7497):
        self.pin = pin
        self.environment = environment
        self.host = host
        self.port = port
        self.account_id = 'paper-ibkr'
        self.api_token = None
        self.api_base = 'https://api.ibkr.mock'
        self.ib = None
        if IB_INSYNC_AVAILABLE and self.environment == 'live':
            self._connect()

    def get_trades(self) -> List[Dict[str, Any]]:
        # Paper mode: no trades by default
        return []

    def get_historical_data(self, symbol: str, count: int = 100, granularity: str = 'M15'):
        return []

    def get_live_prices(self, symbols: List[str]):
        return {s: {'bid': 0.0, 'ask': 0.0} for s in symbols}

    def place_oco_order(self, symbol, entry, sl, tp, units):
        # Platform breaker: allow disabling IBKR only.
        if not is_platform_enabled('ibkr'):
            return {'success': False, 'error': 'IBKR_PLATFORM_BREAKER_OFF'}

        # Venue policy (non-secret): tune IBKR toward equities/ETFs, not crypto/forex.
        try:
            policy_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'venue_policies.json')
            with open(policy_path, 'r') as f:
                pol = (json.load(f) or {}).get('ibkr', {}) or {}
        except Exception:
            pol = {}

        # Optional live time window enforcement (equities RTH by default)
        try:
            if bool(pol.get('enforce_time_windows_live', False)) and self.environment == 'live':
                windows = pol.get('time_windows_newyork', []) or []
                if not self._is_now_in_ny_windows(windows):
                    return {'success': False, 'error': 'IBKR_BLOCKED_BY_TIME_WINDOW'}
        except Exception:
            pass

        sym = str(symbol or '').upper().strip()
        # Reject forex-style symbols first (those belong to OANDA).
        if pol.get('reject_forex_symbols', True):
            if '_' in sym or re.fullmatch(r'[A-Z]{6}', sym or ''):
                return {'success': False, 'error': f'IBKR_REJECTED_SYMBOL_FOREX:{sym}'}

        # Reject crypto-style symbols (those belong to Coinbase).
        if pol.get('reject_crypto_symbols', True):
            # Typical crypto product ids look like BTC-USD, ETH-USD, SOL-USD
            if re.fullmatch(r'[A-Z]{2,10}-USD', sym or ''):
                return {'success': False, 'error': f'IBKR_REJECTED_SYMBOL_CRYPTO:{sym}'}

        allowed = pol.get('allowed_symbols')
        if isinstance(allowed, list) and allowed:
            allowed_set = {str(x).upper().strip() for x in allowed if str(x).strip()}
            if sym not in allowed_set:
                return {'success': False, 'error': f'IBKR_SYMBOL_NOT_ALLOWED:{sym}'}

        # Optional max position notional (USD) for equities/ETFs
        try:
            max_pos = pol.get('max_position_usd', None)
            if max_pos is not None:
                max_pos = float(max_pos)
                notional = abs(float(units)) * abs(float(entry))
                if notional > max_pos:
                    return {'success': False, 'error': f'IBKR_MAX_POSITION_USD_EXCEEDED:{notional:.2f}>{max_pos:.2f}'}
        except Exception:
            pass

        # If ib_insync is present and connected, create OCO using IB API
        if IB_INSYNC_AVAILABLE and self.ib is not None:
            try:
                # Create a contract: assume stock for simplicity, fallback to Forex if JPY present
                contract = Stock(symbol, 'SMART', 'USD') if not any(s in symbol for s in ['USD', 'JPY']) else Forex(symbol)
                # Place parent limit order at entry
                parent = Order()
                parent.action = 'BUY' if units > 0 else 'SELL'
                parent.orderType = 'LMT'
                parent.totalQuantity = abs(int(units))
                parent.lmtPrice = float(entry)
                parent.transmit = False

                # Attach child TP and SL orders
                take_profit = Order()
                take_profit.action = 'SELL' if units > 0 else 'BUY'
                take_profit.orderType = 'LMT'
                take_profit.totalQuantity = abs(int(units))
                take_profit.lmtPrice = float(tp)
                take_profit.parentId = 0
                take_profit.transmit = False

                stop_loss = Order()
                stop_loss.action = 'SELL' if units > 0 else 'BUY'
                stop_loss.orderType = 'STP'
                stop_loss.totalQuantity = abs(int(units))
                stop_loss.auxPrice = float(sl)
                stop_loss.parentId = 0
                stop_loss.transmit = True

                # Place orders in ib_insync (parent first)
                trade = self.ib.placeOrder(contract, parent)
                parent_id = None
                try:
                    parent_id = getattr(getattr(trade, 'order', None), 'orderId', None)
                except Exception:
                    parent_id = None
                parent_id = parent_id if parent_id is not None else int(time.time())
                take_profit.parentId = parent_id
                stop_loss.parentId = parent_id
                self.ib.placeOrder(contract, take_profit)
                self.ib.placeOrder(contract, stop_loss)
                logger.info('IBKR: placed oco parent:%s', parent_id)
                return {'success': True, 'order_id': f'IBKR:{parent_id}'}
            except Exception as e:
                logger.error('IBKR OCO order failed: %s', e)
                return {'success': False, 'error': str(e)}
        else:
            # Fallback stub behavior
            logger.info('IBKR place_oco_order (paper stub): %s %s', symbol, units)
            return {'success': True, 'order_id': 'IBKR:PAPER:SIM'}

    def _is_now_in_ny_windows(self, windows: List[Dict]) -> bool:
        """Return True if current New York local time is inside any provided window."""
        ny = ZoneInfo("America/New_York")
        now_ny = datetime.now(tz=ny)
        dow = now_ny.weekday()  # 0=Mon
        day_map = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6}

        def parse_hhmm(s: str):
            parts = str(s).strip().split(':')
            return int(parts[0]), int(parts[1])

        for w in windows or []:
            try:
                days = w.get('days') or ['MON', 'TUE', 'WED', 'THU', 'FRI']
                days_int = {day_map.get(str(d).upper(), 0) for d in days}
                if dow not in days_int:
                    continue
                sh, sm = parse_hhmm(w.get('start', '00:00'))
                eh, em = parse_hhmm(w.get('end', '23:59'))
                start_min = sh * 60 + sm
                end_min = eh * 60 + em
                now_min = now_ny.hour * 60 + now_ny.minute
                if start_min <= now_min <= end_min:
                    return True
            except Exception:
                continue
        return False

    def set_trade_stop(self, trade_id, new_stop):
        # On IBKR, we would call IB.changeOrder; fallback prints
        if IB_INSYNC_AVAILABLE and self.ib is not None:
            try:
                # Minimal no-op for now
                logger.info('IBKR: set_trade_stop for %s -> %s (no-op in stub)', trade_id, new_stop)
                return True
            except Exception as e:
                logger.error('IBKR set trade stop failed: %s', e)
                return False
        logger.info('IBKR set_trade_stop (paper stub): %s %s', trade_id, new_stop)
        return True

    def _connect(self):
        try:
            self.ib = IB()
            self.ib.connect(self.host, int(self.port), clientId=int(time.time() % 10000))
            logger.info('IBKR: connected to TWS/Gateway at %s:%s', self.host, self.port)
        except Exception as e:
            logger.error('IBKR connect failed: %s', e)
            self.ib = None


__all__ = ["IBKRConnector"]
