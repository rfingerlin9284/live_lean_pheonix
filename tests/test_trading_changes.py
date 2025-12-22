import asyncio
import time

import pytest

from oanda.oanda_trading_engine import OandaTradingEngine
import brokers.oanda_connector as oc


def make_engine(tmp_env=None):
    eng = OandaTradingEngine(environment='practice')
    # ensure toggles loaded
    eng.toggles = eng._load_toggles()
    return eng


@pytest.mark.asyncio
async def test_no_tp_and_initial_sl_5(monkeypatch):
    eng = make_engine()
    # fake price snapshot
    monkeypatch.setattr(eng.oanda, 'get_live_prices', lambda syms: { 'EUR_USD': {'bid': 1.1700, 'ask': 1.1702} })

    captured = {}

    def fake_place_oco(symbol, entry, sl, tp, units, ttl_hours=24.0, order_type='LIMIT'):
        captured['symbol'] = symbol
        captured['entry'] = entry
        captured['sl'] = sl
        captured['tp'] = tp
        captured['units'] = units
        return {'success': True, 'order_id': 'X'}

    monkeypatch.setattr(eng.oanda, 'place_oco_order', fake_place_oco)

    # Ensure no_take_profit is enabled
    eng.toggles['no_take_profit'] = True

    await eng._open_trade('EUR_USD', 'BUY', 0.8)

    assert captured['symbol'] == 'EUR_USD'
    # initial SL should be 5 pips below for BUY -> entry - 5*pip
    pip = 0.0001
    expected_sl = captured['entry'] - (5 * pip)
    assert round(captured['sl'], 6) == round(expected_sl, 6)
    assert captured['tp'] is None


@pytest.mark.asyncio
async def test_diversity_blocks(monkeypatch):
    eng = make_engine()
    # pretend there's already a EUR pair open
    eng.active_positions = {'1': {'instrument': 'EUR_USD'}}

    monkeypatch.setattr(eng.oanda, 'get_live_prices', lambda syms: { 'EUR_USD': {'bid': 1.17, 'ask': 1.1702}, 'GBP_USD': {'bid': 1.34, 'ask': 1.3402} })

    called = {'placed': False}

    def fake_place_oco(symbol, entry, sl, tp, units, ttl_hours=24.0, order_type='LIMIT'):
        called['placed'] = True
        return {'success': True}

    monkeypatch.setattr(eng.oanda, 'place_oco_order', fake_place_oco)

    # Attempt to open another EUR region trade (EUR pair) -> should be blocked
    await eng._open_trade('EUR_USD', 'BUY', 0.8)
    assert called['placed'] is False

    # Opening a different region (AUD) should attempt placement
    monkeypatch.setattr(eng.oanda, 'get_live_prices', lambda syms: { 'AUD_USD': {'bid': 0.6600, 'ask': 0.6602} })
    await eng._open_trade('AUD_USD', 'BUY', 0.8)
    assert called['placed'] is True


@pytest.mark.asyncio
async def test_closein_and_zombie(monkeypatch):
    eng = make_engine()

    # fake trade with profit >= 2*initial_stop_pips (2*5 = 10 pips)
    trade = {'id': 'T1', 'instrument': 'EUR_USD', 'price': 1.1700, 'currentUnits': 1000, 'stopLossOrder': {'price': 1.1695}}

    # fake prices to give profit 12 pips
    monkeypatch.setattr(eng.oanda, 'get_live_prices', lambda syms: { 'EUR_USD': {'bid': 1.1712, 'ask': 1.1713} })

    set_calls = []

    def fake_set_trade_stop(trade_id, price):
        set_calls.append((trade_id, price))
        return {'success': True}

    monkeypatch.setattr(eng.oanda, 'set_trade_stop', fake_set_trade_stop)

    # ensure close_in enabled
    eng.toggles['close_in_settings'] = eng.toggles.get('close_in_settings', {})
    eng.toggles['close_in_settings']['enabled'] = True
    eng.initial_stop_pips = 5

    # call manage - should trigger a step tighten
    await eng._manage_trade(trade)
    assert len(set_calls) >= 1

    # Now test zombie kill: create a trade that's in loss and older than threshold
    trade2 = {'id': 'T2', 'instrument': 'EUR_USD', 'price': 1.1700, 'currentUnits': 1000, 'stopLossOrder': {'price': 1.1701}}
    monkeypatch.setattr(eng.oanda, 'get_live_prices', lambda syms: { 'EUR_USD': {'bid': 1.1690, 'ask': 1.1691} })

    killed = []

    def fake_close_trade(trade_id, units=None):
        killed.append(trade_id)
        return {'success': True}

    monkeypatch.setattr(eng.oanda, 'close_trade', fake_close_trade)

    eng.toggles['zombie_kill_enabled'] = True
    eng.toggles['zombie_min_age_minutes'] = 0.1  # 6 seconds for test
    eng.toggles['zombie_threshold_pips'] = 1

    # set first seen time far enough in the past
    eng._trade_first_seen['T2'] = time.time() - (10 * 60)

    await eng._manage_trade(trade2)
    assert 'T2' in killed
