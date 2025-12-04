import os
import io
import sys
import pytest

from util.position_police import _rbz_force_min_notional_position_police
from oanda.oanda_trading_engine import OandaTradingEngine


def capture_stdout(func, *args, **kwargs):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        func(*args, **kwargs)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def test_module_level_police_skips_without_creds(monkeypatch):
    # Ensure environment tokens are unset
    monkeypatch.delenv('OANDA_PRACTICE_ACCOUNT_ID', raising=False)
    monkeypatch.delenv('OANDA_PRACTICE_TOKEN', raising=False)
    out = capture_stdout(_rbz_force_min_notional_position_police)
    assert '[RBZ_POLICE] skipped' in out


def test_class_wrapper_no_exception_on_missing_creds(monkeypatch):
    # Instantiate engine in practice mode (safe), ensure no creds
    monkeypatch.delenv('OANDA_PRACTICE_ACCOUNT_ID', raising=False)
    monkeypatch.delenv('OANDA_PRACTICE_TOKEN', raising=False)
    eng = OandaTradingEngine(environment='practice')
    out = capture_stdout(eng._rbz_force_min_notional_position_police)
    assert 'skipped' in out or 'Position Police' in out
    # Should return True
    assert eng._rbz_force_min_notional_position_police() is True
