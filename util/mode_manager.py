"""Simple mode manager stub used during tests.
Implements a minimal mode switching and info retrieval API to satisfy tests and scripts.
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional

_CURRENT_MODE = 'OFF'
_MODE_HISTORY: List[Dict[str, Any]] = []


def get_mode_info() -> Dict[str, Any]:
    return {
        'mode': _CURRENT_MODE,
        'api': True if _CURRENT_MODE == 'LIVE' else False,
        'description': 'Mode manager stub for tests'
    }


def switch_mode(mode: str, pin: Optional[int] = None, brokers: Optional[List[str]] = None) -> Dict[str, Any]:
    global _CURRENT_MODE
    _CURRENT_MODE = mode
    entry = {'mode': mode, 'pin': pin, 'brokers': brokers}
    _MODE_HISTORY.append(entry)
    return {'ok': True, 'mode': mode}


def get_connector_environment(connector: str) -> str:
    """Return connector environment string.

    Connectors in this repo generally expect a string like 'live' or 'practice'.
    This stub keeps tests/scripts happy without relying on external state.
    """
    return 'live' if _CURRENT_MODE == 'LIVE' else 'practice'


def read_upgrade_toggle() -> bool:
    return False
