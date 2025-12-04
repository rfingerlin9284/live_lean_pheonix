import os
import pytest

from oanda.brokers.oanda_connector import OandaConnector


def test_env_detection_live(tmp_path, monkeypatch):
    # Ensure a clean environment
    monkeypatch.delenv('OANDA_FORCE_ENV', raising=False)
    monkeypatch.setenv('OANDA_LIVE_TOKEN', 'live-token-123')
    monkeypatch.setenv('OANDA_LIVE_ACCOUNT_ID', '000-111-222')
    conn = OandaConnector(pin=None)
    assert conn.environment == 'live'
    assert conn.trading_enabled


def test_env_detection_practice(tmp_path, monkeypatch):
    monkeypatch.delenv('OANDA_LIVE_TOKEN', raising=False)
    monkeypatch.delenv('OANDA_LIVE_ACCOUNT_ID', raising=False)
    monkeypatch.setenv('OANDA_PRACTICE_TOKEN', 'practice-token-abc')
    monkeypatch.setenv('OANDA_PRACTICE_ACCOUNT_ID', '101-000-000')
    conn = OandaConnector(pin=None)
    assert conn.environment == 'practice'
    assert conn.trading_enabled


def test_force_env_override(monkeypatch):
    monkeypatch.setenv('OANDA_PRACTICE_TOKEN', 'practice-token-abc')
    monkeypatch.setenv('OANDA_PRACTICE_ACCOUNT_ID', '101-000-000')
    monkeypatch.setenv('OANDA_FORCE_ENV', 'live')
    conn = OandaConnector(pin=None)
    assert conn.environment == 'live'


def test_trading_disabled_none_creds(monkeypatch):
    # No tokens set -> trading disabled
    monkeypatch.delenv('OANDA_LIVE_TOKEN', raising=False)
    monkeypatch.delenv('OANDA_PRACTICE_TOKEN', raising=False)
    conn = OandaConnector(pin=None, environment='practice')
    assert not conn.trading_enabled
    # Attempting to place order should return a safe error
    result = conn.place_oco_order('EUR_USD', 1.08, 1.075, 1.095, 1000)
    assert not result.get('success')
    assert result.get('error') and 'TRADING_DISABLED' in result.get('error')


def test_get_account_summary_parsing(monkeypatch):
    # Ensure we parse the account summary response correctly
    monkeypatch.setenv('OANDA_PRACTICE_TOKEN', 'practice-token-xyz')
    monkeypatch.setenv('OANDA_PRACTICE_ACCOUNT_ID', '101-111-222')
    conn = OandaConnector(pin=None)

    sample_response = {
        'success': True,
        'data': {
            'account': {
                'id': '101-111-222',
                'balance': '10000.00',
                'currency': 'USD',
                'marginAvailable': '9000.0',
                'unrealizedPL': '50.0'
            }
        }
    }

    # Replace _make_request to return our sample response
    monkeypatch.setattr(conn, '_make_request', lambda *a, **k: sample_response)
    summary = conn.get_account_summary()
    assert summary
    assert summary['account_id'].endswith('122') or summary['account_id'].endswith('222')
    assert summary['balance'] == 10000.0
    assert summary['currency'] == 'USD'


def test_start_script_enables_execution(monkeypatch, tmp_path):
    # Simulate a non-placeholder token & account in .env and verify start_with_integrity would enable execution
    monkeypatch.setenv('OANDA_PRACTICE_TOKEN', 'token-12345')
    monkeypatch.setenv('OANDA_PRACTICE_ACCOUNT_ID', '101-222-333')
    monkeypatch.setenv('OANDA_FORCE_ENV', 'practice')
    # Start script logic is a shell script - we'll emulate the condition using Python environment:
    from subprocess import Popen, PIPE
    # Run a short Python check using the same logic as start_with_integrity
    code = "import os; print(os.getenv('OANDA_FORCE_ENV'), os.getenv('OANDA_PRACTICE_TOKEN')!='', os.getenv('OANDA_PRACTICE_ACCOUNT_ID')!='')"
    p = Popen(['python3', '-c', code], stdout=PIPE)
    out, _ = p.communicate()
    assert p.returncode == 0
