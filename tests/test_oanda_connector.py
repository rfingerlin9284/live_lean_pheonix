import pytest
from oanda.brokers.oanda_connector import OandaConnector
from unittest.mock import patch

def test_confidence_score_basic():
    connector = OandaConnector(pin=841921, environment="practice")
    # Use typical FX values
    with patch.object(connector, '_get_spread', return_value=0.0005):
        result = connector._compute_confidence_score(
            instrument="EUR_USD",
            entry_price=1.1000,
            stop_loss=1.0950,
            take_profit=1.1150,
            units=10000
        )
    assert isinstance(result, dict)
    assert 0.0 <= result['score'] <= 1.0
    assert result['rr_ratio'] > 0
    assert result['expected_pnl'] > 0
    assert result['notional'] > 0
    assert 'spread' in result
    assert 'recent_win_rate' in result
    assert 'model_signal' in result
    # Check normalized fields
    assert 0.0 <= result['rr_ratio_norm'] <= 1.0
    assert 0.0 <= result['expected_pnl_norm'] <= 1.0
    assert 0.0 <= result['notional_norm'] <= 1.0
    assert 0.0 <= result['spread_norm'] <= 1.0

def test_confidence_score_zero_units():
    connector = OandaConnector(pin=841921, environment="practice")
    with patch.object(connector, '_get_spread', return_value=0.0005):
        result = connector._compute_confidence_score(
            instrument="EUR_USD",
            entry_price=1.1000,
            stop_loss=1.0950,
            take_profit=1.1150,
            units=0
        )
    assert result['expected_pnl'] == 0
    assert result['notional'] == 0
    assert 0.0 <= result['score'] <= 1.0
