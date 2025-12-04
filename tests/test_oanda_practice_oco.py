import os
import json
from fastapi.testclient import TestClient

from backend import app

def test_place_practice_oco(monkeypatch):
    # Monkeypatch environment to allow practice orders
    monkeypatch.setenv('OANDA_FORCE_ENV', 'practice')
    monkeypatch.setenv('ALLOW_PRACTICE_ORDERS', '1')
    monkeypatch.setenv('CONFIRM_PRACTICE_ORDER', '1')
    monkeypatch.setenv('PRACTICE_PIN', '841921')
    monkeypatch.setenv('OANDA_PRACTICE_TOKEN', 'practice-token')
    monkeypatch.setenv('OANDA_PRACTICE_ACCOUNT_ID', '101-000-000')
    monkeypatch.setenv('OANDA_LOAD_ENV_FILE', '0')

    # Monkeypatch the connector's place_oco_order to avoid real API calls
    from oanda.brokers.oanda_connector import OandaConnector
    def fake_place_oco(self, instrument, entry_price, stop_loss, take_profit, units, ttl_hours=24.0, order_type='LIMIT'):
        return {
            'success': True,
            'order_id': 'phony-123',
            'instrument': instrument,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'units': units
        }
    monkeypatch.setattr(OandaConnector, 'place_oco_order', fake_place_oco)

    client = TestClient(app)
    payload = {
        'instrument': 'EUR_USD',
        'entry_price': 1.08,
        'stop_loss': 1.075,
        'take_profit': 1.095,
        'units': 100,
        'confirm': True
        , 'pin': 841921
    }

    response = client.post('/api/broker/oanda/place_practice_oco', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get('success') is True
    assert data.get('order_id') == 'phony-123'
