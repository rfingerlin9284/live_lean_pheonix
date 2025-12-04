#!/usr/bin/env python3
"""
Helper to load and validate the trading sectors YAML configuration.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

logger = logging.getLogger('sector_loader')

def _load_yaml(path: Path) -> Dict:
    try:
        import yaml
    except Exception:
        # If PyYAML is not available, return an empty dict and allow callers to proceed with defaults
        logger.warning('PyYAML is not installed; sector configuration cannot be loaded. Using defaults.')
        return {}
    with path.open('r') as f:
        data = yaml.safe_load(f)
    return data or {}


def load_sectors(config_path: str = 'config/trading_sectors.yaml') -> Dict:
    path = Path(config_path)
    # Default sectors to ensure safe failures when the YAML is missing or invalid
    defaults = {
        'oanda': {'enabled': True, 'mode': 'practice', 'profile': {'MIN_EXPECTED_PNL_USD': 35.0, 'MIN_NOTIONAL_USD': 10000, 'MAX_MARGIN_UTILIZATION_PCT': 0.2}},
        'coinbase': {'enabled': True, 'mode': 'canary', 'profile': {'MIN_EXPECTED_PNL_USD': 35.0, 'MIN_NOTIONAL_USD': 10000, 'MAX_MARGIN_UTILIZATION_PCT': 0.25}},
        'ibkr': {'enabled': True, 'mode': 'paper', 'profile': {'MIN_EXPECTED_PNL_USD': 35.0, 'MIN_NOTIONAL_USD': 10000, 'MAX_MARGIN_UTILIZATION_PCT': 0.15}}
    }
    if not path.exists():
        logger.warning('Sector configuration not found at %s. Using defaults.', config_path)
        return defaults
    data = _load_yaml(path)
    if not data:
        # If YAML loading failed, return the defaults
        return defaults
    # Validate presence of supported sectors
    allowed = {'oanda', 'coinbase', 'ibkr'}
    found = set(data.keys())
    invalid = found - allowed
    if invalid:
        logger.warning('Unexpected sector keys: %s', ', '.join(sorted(invalid)))
    # Apply defaults and validate types
    for k in allowed:
        if k not in data:
            data[k] = {'enabled': False, 'mode': 'disabled', 'profile': {}}
        else:
            data[k].setdefault('enabled', False)
            data[k].setdefault('mode', 'disabled')
            data[k].setdefault('profile', {})
    return data


if __name__ == '__main__':
    import json
    print(json.dumps(load_sectors(), indent=2))
