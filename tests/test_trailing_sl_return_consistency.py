import types
import oanda.oanda_trading_engine as ote


def test_apply_adaptive_trailing_sl_returns_tuple(monkeypatch):
    # Instantiate engine in practice mode
    eng = ote.OandaTradingEngine(environment='practice')

    # Use a position with no change - should return (False, None)
    pos = {'stop_loss': 1.2, 'entry_price': 1.25, 'timestamp': None, 'rr_ratio': 3.2}
    ret = eng._apply_adaptive_trailing_sl(pos=pos, trade_id='test', order_id='ord', symbol='EUR_USD', current_price=1.25, estimated_atr_pips=0.5, pip_size=0.0001, profit_atr_multiple=0.1, direction='BUY')
    assert isinstance(ret, tuple) and len(ret) == 2
    assert ret == (False, None)

    # Monkeypatch the stop setter to force success path
    def fake_stop(self, trade_id, price, order_id=None, symbol=None, direction=None, trigger_source=None, retries=3, backoff=0.5):
        return True, {'success': True, 'set': price}, 1

    eng._set_trade_stop_with_retries = types.MethodType(fake_stop, eng)

    class FakeTrailing:
        def calculate_dynamic_trailing_distance(self, profit_atr_multiple, atr, momentum_active=True):
            return 0.001

    eng.trailing_system = FakeTrailing()

    ret2 = eng._apply_adaptive_trailing_sl(pos=pos, trade_id='test', order_id='ord', symbol='EUR_USD', current_price=1.26, estimated_atr_pips=12, pip_size=0.0001, profit_atr_multiple=2.0, direction='BUY')
    assert isinstance(ret2, tuple) and len(ret2) == 2
    assert ret2[0] is True and isinstance(ret2[1], dict)
