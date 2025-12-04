import os
import pytest

from oanda.brokers.oanda_connector import OandaConnector


def test_get_historical_data_success(monkeypatch):
    # Prepare a fake candles response
    fake_candles = [{
        'time': '2025-12-03T00:00:00Z',
        'volume': 100,
        'mid': {'o': '1.1000', 'h': '1.1010', 'l': '1.0990', 'c': '1.1005'}
    }]

    def fake_make_request(self, method, endpoint, data=None, params=None):
        return {'success': True, 'data': {'candles': fake_candles}}

    monkeypatch.setattr(OandaConnector, '_make_request', fake_make_request)

    c = OandaConnector(pin=841921, environment='practice')
    candles = c.get_historical_data('EUR_USD', count=1, granularity='M15')
    assert isinstance(candles, list)
    assert len(candles) == 1
    assert candles[0]['mid']['c'] == '1.1005'


def test_get_historical_data_failure(monkeypatch):
    def fake_make_request(self, method, endpoint, data=None, params=None):
        return {'success': False, 'error': 'some error'}

    monkeypatch.setattr(OandaConnector, '_make_request', fake_make_request)
    c = OandaConnector(pin=841921, environment='practice')
    candles = c.get_historical_data('EUR_USD', count=1, granularity='M15')
    assert isinstance(candles, list)
    assert candles == []


def test_headers_auth_present(monkeypatch, tmp_path):
    # Ensure a token is present and that the header is set
    monkeypatch.setenv('OANDA_PRACTICE_TOKEN', 'my_test_token')
    c = OandaConnector(pin=841921, environment='practice')
    assert 'Authorization' in c.headers
    assert c.headers['Authorization'] == 'Bearer my_test_token'
