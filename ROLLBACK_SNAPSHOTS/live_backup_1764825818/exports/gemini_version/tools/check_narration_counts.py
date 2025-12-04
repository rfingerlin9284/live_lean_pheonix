#!/usr/bin/env python3
"""
Count recent narration events and print counts for key event types.
"""
import json
from pathlib import Path

N = 1000
NARRATION_FILE = Path('narration.jsonl')

counts = {
    'TRADE_SIGNAL': 0,
    'OCO_PLACED': 0,
    'ORDER_FILLED': 0,
    'CHARTER_VIOLATION': 0,
    'ORDER_REJECTED_MIN_NOTIONAL': 0,
    'GATE_REJECTION': 0,
    'PROFILE_STATUS': 0
}

if not NARRATION_FILE.exists():
    print('No narration file found:', NARRATION_FILE)
    raise SystemExit(1)

with open(NARRATION_FILE, 'r') as f:
    lines = f.readlines()[-N:]

for line in lines:
    try:
        ev = json.loads(line)
        et = ev.get('event_type')
        if et in counts:
            counts[et] += 1
    except json.JSONDecodeError:
        continue

print('Recent event counts (last', N, 'events):')
for k, v in counts.items():
    print(f'{k}: {v}')

# Show a small sample of last OCO_PLACED events
sample_ocos = [json.loads(l) for l in lines if 'OCO_PLACED' in l][-5:]
if sample_ocos:
    print('\nLast OCO_PLACED examples:')
    for o in sample_ocos:
        print(o)
