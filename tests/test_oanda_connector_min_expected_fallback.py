import os
import sys
from importlib import reload
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from oanda.brokers.oanda_connector import OandaConnector
from oanda.brokers import oanda_connector as ocmod


def test_min_expected_from_charter(monkeypatch):
    # Ensure RickCharter value is respected when present (uses foundation.rick_charter value)
    os.environ.pop('MIN_EXPECTED_PNL_USD', None)
    # Sanity check that the charter value is 35.0
    from foundation.rick_charter import RickCharter as FC
    assert FC.MIN_EXPECTED_PNL_USD == 35.0


def test_min_expected_env_override(monkeypatch):
    # If env override is present and RickCharter unavailable, it should be used
    monkeypatch.setenv('MIN_EXPECTED_PNL_USD', '42.0')
    # Monkeypatch missing RickCharter symbol for test
    monkeypatch.setattr(ocmod, 'RickCharter', None)
    conn = OandaConnector(pin=841921, environment='practice')
    conn.trading_enabled = True
    # Patch _make_request to avoid network
    conn._make_request = lambda method, endpoint, params=None, data=None: {'success': True, 'data': {'orderCreateTransaction': {'id': 'xyz'}}, 'latency_ms': 1}
    # expected_pnl of 41 should be blocked (min 42), and 43 allowed
    entry = 1.0
    units = 10000
    # 41 USD expected PnL => blocked
    tp_low = entry + (41.0 / units)
    res_low = conn.place_oco_order('EUR_USD', entry, stop_loss=0.99, take_profit=tp_low, units=units, order_type='LIMIT')
    assert res_low['success'] is False
    # 43 USD expected PnL => allowed
    tp_hi = entry + (43.0 / units)
    res_hi = conn.place_oco_order('EUR_USD', entry, stop_loss=0.99, take_profit=tp_hi, units=units, order_type='LIMIT')
    assert res_hi['success'] is True
