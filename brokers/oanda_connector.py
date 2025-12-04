#!/usr/bin/env python3
"""
Wrapper for the canonical OANDA connector.

This module preserves backward compatibility for historic imports that reference
the top-level `brokers` package while delegating implementation to the new
`oanda.brokers.oanda_connector` module.

The original file contained a full implementation; to avoid duplication and
DRY violations we now import and re-export names from the canonical
implementation.
"""

from importlib import import_module
import logging

logger = logging.getLogger(__name__)

try:
    _module = import_module('oanda.brokers.oanda_connector')
    
    # Re-export the public API surface
    OandaConnector = getattr(_module, 'OandaConnector', None)
    get_oanda_connector = getattr(_module, 'get_oanda_connector', None)
    place_oanda_oco = getattr(_module, 'place_oanda_oco', None)
    __all__ = ['OandaConnector', 'get_oanda_connector', 'place_oanda_oco']
    
except Exception as e:
    logger.error(f'Failed to import canonical oanda connector: {e}')
    __all__ = []
    raise ImportError('Unable to import canonical oanda connector module') from e
