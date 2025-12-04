#!/usr/bin/env python3
import os
import json
from pathlib import Path
from datetime import datetime, timezone
import time

from oanda.oanda_trading_engine import OandaTradingEngine


class FakeOanda:
    def __init__(self):
        self.account_id = 'FAKE'
        self.api_base = 'https://api-fxpractice.oanda.com'
    def get_account_info(self):
        return {'NAV': 5000, 'balance': 5000, 'marginUsed': 0}
    def get_historical_data(self, inst, count=120, granularity='M15'):
        return [{'time': 't', 'open': 1.2, 'close': 1.2, 'high': 1.2002, 'low': 1.1998, 'volume': 1} for _ in range(count)]
    def place_oco_order(self, instrument=None, entry_price=None, stop_loss=None, take_profit=None, units=0, ttl_hours=6.0, explanation=None):
        order_id = f'F_{int(datetime.now(timezone.utc).timestamp())}'
        try:
            from util.narration_logger import log_narration
            details = {
                'broker': 'OANDA',
                'order_id': order_id,
                'instrument': instrument,
                'units': units,
                'entry_price': entry_price,
                'environment': 'PRACTICE'
            }
            if explanation:
                details['explanation'] = explanation
            log_narration('BROKER_ORDER_CREATED', details)
        except Exception:
            pass
        return {'success': True, 'order_id': order_id, 'latency_ms': 10}
    def get_trades(self):
        return []
    def cancel_order(self, order_id):
        return {'success': True}
    def set_trade_stop(self, trade_id, stop):
        return {'success': True}


def test_trade_confidence_decomposition(tmp_path):
    tmpfile = tmp_path / 'test_narration_conf.jsonl'
    os.environ['NARRATION_FILE_OVERRIDE'] = str(tmpfile)
    os.environ['RICK_AGGRESSIVE_PLAN'] = '1'
    os.environ['RICK_AGGRESSIVE_LEVERAGE'] = '3'

    engine = OandaTradingEngine(environment='practice')
    engine.min_notional_usd = 1
    engine.oanda = FakeOanda()
    # Ensure no registry collision
    try:
        from util.positions_registry import unregister_position
        unregister_position(symbol='EUR_USD')
    except Exception:
        pass
    tid = engine.place_trade('EUR_USD', 'BUY')
    assert tid is not None

    found_conf = False
    with open(tmpfile) as f:
        for line in f:
            ev = json.loads(line)
            if ev.get('event_type') == 'TRADE_CONFIDENCE_DECOMPOSITION':
                found_conf = True
                details = ev.get('details', {})
                conf = details.get('confidence_decomposition', {})
                assert 'technical_score' in conf
                assert 'ml_confidence' in conf
                assert 'hive_confidence' in conf
                assert 'approval_score' in conf
                assert 'dyn_leverage' in conf
                break
    assert found_conf


# Entry: Run all tests if executed as main


def test_pre_trade_confidence_decomposition_on_gate_reject(tmp_path):
    tmpfile = tmp_path / 'test_pre_gate_narration_conf.jsonl'
    os.environ['NARRATION_FILE_OVERRIDE'] = str(tmpfile)
    os.environ['RICK_AGGRESSIVE_PLAN'] = '0'
    engine = OandaTradingEngine(environment='practice')
    engine.min_notional_usd = 999999999  # force charter violation
    engine.oanda = FakeOanda()
    # Monkeypatch the guardian gate to explicitly reject the trade, ensuring GATE_REJECTION is logged with decomposition
    try:
        from types import SimpleNamespace
        # Create a fake gate result-like object for pre_trade_gate
        fake_gate_result = SimpleNamespace(allowed=False, reason='test_block', action='AUTO_CANCEL')
        engine.gate.pre_trade_gate = lambda new_order, current_positions, pending_orders, total_margin_used: fake_gate_result
    except Exception:
        pass
    tid = engine.place_trade('EUR_USD', 'BUY')
    assert tid is None
    found_pre = False
    with open(tmpfile) as f:
        for line in f:
            ev = json.loads(line)
            if ev.get('event_type') == 'PRE_TRADE_CONFIDENCE_DECOMPOSITION':
                found_pre = True
                break
    assert found_pre
    # Also verify GATE_REJECTION includes the confidence_decomposition dict with core keys
    found_gate_rejection = False
    with open(tmpfile) as f:
        for line in f:
            ev = json.loads(line)
            if ev.get('event_type') == 'GATE_REJECTION':
                details = ev.get('details', {})
                conf = details.get('confidence_decomposition')
                if conf is not None and isinstance(conf, dict) and 'technical_score' in conf:
                    found_gate_rejection = True
                    break
    assert found_gate_rejection, 'No GATE_REJECTION with populated confidence_decomposition found'


def test_charter_violation_contains_decomposition(tmp_path):
    tmpfile = tmp_path / 'test_charter_narration_conf.jsonl'
    os.environ['NARRATION_FILE_OVERRIDE'] = str(tmpfile)
    engine = OandaTradingEngine(environment='practice')
    engine.min_notional_usd = 1_000_000_000  # extremely high to force CHARTER violation
    engine.oanda = FakeOanda()
    # Force small position size to ensure notional < min_notional_usd: patch calculate_position_size to always return 1
    engine.calculate_position_size = lambda symbol, price: 1
    tid = engine.place_trade('EUR_USD', 'BUY')
    assert tid is None
    found_charter = False
    with open(tmpfile) as f:
        for line in f:
            ev = json.loads(line)
            if ev.get('event_type') == 'CHARTER_VIOLATION':
                details = ev.get('details', {})
                conf = details.get('confidence_decomposition')
                if conf is not None and isinstance(conf, dict) and 'technical_score' in conf:
                    found_charter = True
                    break
    assert found_charter, 'No CHARTER_VIOLATION with populated confidence_decomposition found'


if __name__ == '__main__':
    tmp = Path('/tmp')
    test_trade_confidence_decomposition(tmp)
    test_pre_trade_confidence_decomposition_on_gate_reject(tmp)
    test_charter_violation_contains_decomposition(tmp)

