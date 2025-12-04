#!/usr/bin/env python3
import os
import sys
from unittest import mock

import pytest


def run_tool(argv, env=None):
    # Run the script by invoking its `main` with monkeypatched sys.argv
    from importlib import reload
    import tools.place_practice_market_order as tool_module
    reload(tool_module)
    old_argv = sys.argv[:]
    sys.argv = [old_argv[0]] + argv
    if env:
        old_env = os.environ.copy()
        os.environ.update(env)
    try:
        return tool_module.main()
    finally:
        sys.argv = old_argv
        if env:
            os.environ.clear()
            os.environ.update(old_env)


def test_blocked_without_allow_env():
    rc = run_tool(["EUR_USD", "1000", "--confirm", "--stop-loss", "1.0", "--take-profit", "1.05"], env={})
    assert rc == 3


def test_requires_confirm():
    rc = run_tool(["EUR_USD", "1000", "--stop-loss", "1.0", "--take-profit", "1.05"], env={"ALLOW_PRACTICE_ORDERS":"1", "PRACTICE_PIN":"841921"})
    assert rc == 4


def test_successful_call(monkeypatch, tmp_path):
    # Enable practice orders
    env = {
        "ALLOW_PRACTICE_ORDERS": "1",
        "CONFIRM_PRACTICE_ORDER": "1",
        "PRACTICE_PIN": "841921",
        "OANDA_PRACTICE_TOKEN": "token",
        "OANDA_PRACTICE_ACCOUNT_ID": "1234-5678"
    }

    # Monkeypatch OandaConnector to make it return success without network
    class DummyConnector:
        def __init__(self, pin=None, environment=None):
            self.environment = environment
            self.trading_enabled = True

        def place_oco_order(self, instrument, entry_price, stop_loss, take_profit, units, ttl_hours, order_type):
            return {"success": True, "order_id": "practice_001"}

    monkeypatch.setattr('oanda.brokers.oanda_connector.OandaConnector', DummyConnector)
    rc = run_tool([
        "EUR_USD", "1000", "--confirm", "--stop-loss", "1.0", "--take-profit", "1.05", "--pin", "841921"
    ], env=env)
    assert rc == 0
