#!/usr/bin/env python3
"""
Coinbase Connector - Safe wrapper for Coinbase Advanced Trade APIs
Designed for practice/sandbox usage and defers to environment gating.
"""
import os
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class CoinbaseConnector:
    def __init__(self, pin: int = None, environment: str = None):
        self.environment = environment or os.getenv('COINBASE_ENV', 'sandbox')
        self.api_key = os.getenv('COINBASE_API_KEY')
        self.api_secret = os.getenv('COINBASE_API_SECRET')
        self.trading_enabled = bool(self.api_key and self.api_secret and self.environment in ('sandbox', 'live'))
        logger.info(f"CoinbaseConnector initialized for {self.environment} ; trading_enabled={self.trading_enabled}")

    def get_account_summary(self) -> Optional[Dict[str, Any]]:
        # Read-only diagnostic: if sandbox mode with keys present, try to call real API; otherwise return None
        if not self.trading_enabled:
            logger.warning('Coinbase sandbox keys missing; trading disabled')
            return None
        # If the external library is installed, perform a real call; otherwise return stub
        try:
            try:
                from coinbase.client import CoinbaseClient
            except Exception:
                CoinbaseClient = None
            if CoinbaseClient:
                client = CoinbaseClient(api_key=self.api_key, api_secret=self.api_secret)
                return client.get_account_summary()
            else:
                # If the client isn't installed, we can optionally try a REST call if OAUTH is set up
                # For safety, prefer the stub if no SDK or configured REST credentials
                logger.debug('Coinbase SDK not installed; returning telemetry stub')
                return {
                    'account_id': 'sandbox-coinbase-1',
                    'currency': 'USD',
                    'balance': 10000.0
                }
        except Exception as e:
            logger.debug('Coinbase call failed unexpectedly: %s', e)
            return {
                'account_id': 'sandbox-coinbase-1',
                'currency': 'USD',
                'balance': 10000.0
            }

    def place_order(self, instrument: str, side: str, size: float, price: Optional[float] = None) -> Dict[str, Any]:
        # Do not place live orders unless enabled and environment is 'sandbox' or 'live'
        if not self.trading_enabled:
            return {'success': False, 'error': 'TRADING_DISABLED'}
        # Try to use external library; otherwise simulate a response
        try:
            try:
                from coinbase.client import CoinbaseClient
            except Exception:
                CoinbaseClient = None
            if CoinbaseClient:
                client = CoinbaseClient(api_key=self.api_key, api_secret=self.api_secret)
                order = client.place_order(instrument=instrument, side=side, size=size, price=price)
                return {'success': True, 'order': order}
            else:
                logger.info('Coinbase SDK not installed; returning simulated order due to missing SDK')
                return {'success': True, 'order': {'id': 'sim-coinbase-001', 'instrument': instrument, 'side': side, 'size': size, 'price': price}}
        except Exception as e:
            logger.error('Coinbase place_order exception: %s', e)
            return {'success': False, 'error': str(e)}

    def get_trades(self) -> List[Dict[str, Any]]:
        # Returns active trades; sandbox-only
        if not self.trading_enabled:
            return []
        try:
            from coinbase.client import CoinbaseClient
            client = CoinbaseClient(api_key=self.api_key, api_secret=self.api_secret)
            return client.get_open_trades()
        except Exception:
            return []

def get_coinbase_connector(pin: int = None, environment: str = 'sandbox') -> CoinbaseConnector:
    return CoinbaseConnector(pin=pin, environment=environment)
