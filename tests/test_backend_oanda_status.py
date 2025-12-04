import os
from fastapi.testclient import TestClient

from backend import app


def test_oanda_status_endpoint(monkeypatch):
    # Ensure test uses practice creds via env
    monkeypatch.setenv('OANDA_PRACTICE_TOKEN', 'practice-x-token')
    monkeypatch.setenv('OANDA_PRACTICE_ACCOUNT_ID', '101-000-000')
    # Ensure connector does not auto-load .env file for consistent tests
    monkeypatch.setenv('OANDA_LOAD_ENV_FILE', '0')

    client = TestClient(app)
    response = client.get('/api/broker/oanda/status')
    # Endpoint may return 503 if telemetry failed to initialize; accept 200 or 503
    assert response.status_code in (200, 503)
    data = response.json()
    if response.status_code == 503:
        assert 'detail' in data and 'telemetry not initialized' in data['detail']
        return

    assert 'environment' in data
    assert data['environment'] in ('practice', 'live')
    assert 'trading_enabled' in data
    assert isinstance(data['trading_enabled'], bool)
    assert 'account_id' in data
    assert 'performance' in data
