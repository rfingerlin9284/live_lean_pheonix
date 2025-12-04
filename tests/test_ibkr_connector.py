#!/usr/bin/env python3
from ibkr.brokers.ibkr_connector import IBKRConnector
def test_ibkr_connector_init():
    c = IBKRConnector(environment='paper')
    assert c.environment == 'paper'
    assert c.trading_enabled in (False, True)
