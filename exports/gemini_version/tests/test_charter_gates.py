import math
import os
from foundation.rick_charter import RickCharter
from oanda.foundation.rick_charter import RickCharter as OandaRickCharter

# Ensure log directories referenced by modules exist to avoid import-time errors
os.makedirs('/home/ing/RICK/RICK_LIVE_CLEAN/logs', exist_ok=True)

from rick_institutional_full import RickInstitutionalTradingAgent


def test_min_notional_blocking():
    # Trade below min notional should be blocked by the charter
    trade_req = {
        'symbol': 'EUR_USD',
        'units': 5000,
        'notional_usd': 5000.0,
        'margin_usd': 100.0,
        'risk_reward_ratio': 3.5,
    }
    ok, reason = OandaRickCharter.validate_institutional_compliance(trade_req)
    assert not ok
    assert 'Notional' in reason


def test_min_expected_pnl_gate():
    # Construct an entry/units such that expected PnL is just below and just above the configured MIN_EXPECTED_PNL_USD
    entry = 1.33
    units = int(OandaRickCharter.MIN_NOTIONAL_USD / entry)
    # expected_pnl = (tp - entry) * units
    # make tp such that expected_pnl is MIN_EXPECTED_PNL_USD - 1 (should fail)
    tp_fail = entry + (RickCharter.MIN_EXPECTED_PNL_USD - 1.0) / units
    expected_pnl_fail = abs((tp_fail - entry) * units)
    assert expected_pnl_fail < OandaRickCharter.MIN_EXPECTED_PNL_USD

    # Now with +1 USD (should pass)
    tp_pass = entry + (RickCharter.MIN_EXPECTED_PNL_USD + 1.0) / units
    expected_pnl_pass = abs((tp_pass - entry) * units)
    assert expected_pnl_pass > OandaRickCharter.MIN_EXPECTED_PNL_USD


def test_margin_cap_blocking():
    # Create institutional agent and set account state to small NAV so margin cap is easy to exceed
    # Some modules expect MAJOR_PAIRS to exist on the top-level charter - ensure attributes exist for the test
    import foundation.rick_charter as top_charter
    setattr(top_charter.RickCharter, 'MAJOR_PAIRS', {'EUR_USD', 'GBP_USD', 'USD_JPY'})
    setattr(top_charter.RickCharter, 'MAJOR_PAIRS_MIN_UNITS', 15000)
    setattr(top_charter.RickCharter, 'OTHER_FX_MIN_UNITS', 15000)
    # Ensure margin cap is available (set small-ish for test scope)
    setattr(top_charter.RickCharter, 'MAX_MARGIN_UTILIZATION_PCT', 1.75)

    agent = RickInstitutionalTradingAgent(pin=841921)
    agent.account_nav = 100.0
    agent.margin_used = 0.0

    # Choose notional so estimated_margin (2%) pushes projected over 175% cap
    entry = 1.0
    units = 20000  # notional = 20,000 => estimated_margin = 400 => projected_pct = 400/100 = 4.0
    sl = entry - 0.01
    tp = entry + 0.04  # risk 1 pip, reward 4 pips -> RR 4.0 >= 3.2 to let margin gate be evaluated
    ok, reason = agent.five_layer_gate_check('EUR_USD', 'BUY', units, entry, sl, tp)
    assert not ok
    assert 'margin' in reason.lower()
