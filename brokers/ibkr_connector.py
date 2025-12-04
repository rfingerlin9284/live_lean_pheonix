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
                parent_id = self.ib.placeOrder(contract, parent).orderId
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
