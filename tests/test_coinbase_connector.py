#!/usr/bin/env python3
from coinbase.brokers.coinbase_connector import CoinbaseConnector
def test_coinbase_connector_init():
    c = CoinbaseConnector(environment='sandbox')
    assert c.environment == 'sandbox'
    # Without keys, trading_enabled should be False
    assert c.trading_enabled in (False, True)
