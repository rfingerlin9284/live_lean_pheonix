#!/usr/bin/env python3
"""
Basic test for util/map_oanda_to_amm.py
"""
import json
import sys
import os
from pathlib import Path
# Ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.map_oanda_to_amm import load_events


def test_explicit_mapping(tmp_path: Path):
    narration_file = tmp_path / 'narration.jsonl'
    event = {
        'timestamp': '2025-01-01T00:00:00+00:00',
        'event_type': 'BROKER_MAPPING',
        'symbol': 'EUR_USD',
        'venue': 'oanda',
        'details': {
            'order_id': 'TEST_ORD_999',
            'trade_id': 'TEST_TRADE_999',
        },
    }
    narration_file.write_text(json.dumps(event) + '\n')

    oanda_orders, amm_trades, mappings = load_events(str(narration_file))
    explicit = {m['order_id']: m['trade_id'] for m in mappings if m.get('order_id')}
    assert explicit.get('TEST_ORD_999') == 'TEST_TRADE_999'

