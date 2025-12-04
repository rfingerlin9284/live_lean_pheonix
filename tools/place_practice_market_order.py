#!/usr/bin/env python3
"""
Safely place a practice market order using the OandaConnector.

This script enforces explicit opt-in flags and will refuse to place orders
unless the following conditions are met:

- OANDA environment is 'practice' (or OANDA_FORCE_ENV=practice)
- ALLOW_PRACTICE_ORDERS env var is set to '1' (or true/yes)
- --confirm flag is present on the command line

This tool is provided as an explicit, gated way to exercise the practice API.
It will not bypass the AgentCharter, min notional, or other security checks
already implemented by the `OandaConnector`.
"""
from __future__ import annotations

import argparse
import os
import logging
from typing import Optional
try:
    from foundation.agent_charter import AgentCharter
except Exception:
    try:
        from agent_charter import AgentCharter
    except Exception:
        # Best-effort fallback; practice gating will use env flags only
        AgentCharter = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("place_practice_market_order")

try:
    from oanda.brokers.oanda_connector import OandaConnector
except Exception:
    raise


def main() -> int:
    parser = argparse.ArgumentParser(description="Place a practice market order on OANDA (safely gated)")
    parser.add_argument("instrument", help="Trading pair, e.g., EUR_USD or EUR_USD")
    parser.add_argument("units", type=int, help="Units to trade (positive = buy, negative = sell)")
    parser.add_argument("--confirm", action="store_true", help="Confirm that you want to place the practice market order")
    parser.add_argument("--stop-loss", dest="stop_loss", type=float, required=True, help="Stop loss price (e.g., 1.0750)")
    parser.add_argument("--take-profit", dest="take_profit", type=float, required=True, help="Take profit price (e.g., 1.0950)")
    parser.add_argument("--env", choices=["practice", "live"], default=None, help="Force environment mode")
    parser.add_argument("--pin", dest="pin", type=int, default=None, help="Optional PIN for practice approval (required if AgentCharter requires pin)")
    args = parser.parse_args()

    # Safety checks
    if args.env and args.env != "practice":
        logger.error("This script only allows practice trading. If you intended to use live environment, use the backend or UI with AgentCharter approvals.")
        return 2

    # Enforce ALLOW_PRACTICE_ORDERS env gating
    allow = os.getenv("ALLOW_PRACTICE_ORDERS", "0").lower() in ("1", "true", "yes")
    if not allow:
        logger.error("Practice orders are disabled. Set ALLOW_PRACTICE_ORDERS=1 to enable practice order placement.")
        return 3

    if not args.confirm:
        logger.error("Order not confirmed. Rerun with --confirm to place the practice market order.")
        return 4

    # Enforce practice environment
    connector_env = (args.env or os.getenv("OANDA_FORCE_ENV") or os.getenv("OANDA_PRACTICE_ENV"))
    if connector_env and connector_env != "practice":
        logger.error("OANDA is not configured to use practice environment. Set OANDA_FORCE_ENV=practice to override.")
        return 5

    # Enforce AgentCharter gating (if available)
    try:
        if AgentCharter:
            allowed = AgentCharter.practice_allowed(pin=args.pin)
            if not allowed:
                logger.error("Practice placement blocked by AgentCharter practice gating. ")
                logger.error("Ensure ALLOW_PRACTICE_ORDERS=1, CONFIRM_PRACTICE_ORDER=1, and correct PRACTICE_PIN is set (or pass --pin).")
                return 8
    except Exception as e:
        logger.warning(f"AgentCharter check failed or not available: {e}")

    # Create connector
    connector = OandaConnector(pin=None, environment="practice")
    if not connector.trading_enabled:
        logger.error("Connector reports trading_enabled=False. Check OANDA_PRACTICE_TOKEN and OANDA_PRACTICE_ACCOUNT_ID in environment (or set OANDA_LOAD_ENV_FILE=1).")
        return 6

    # Validate stop loss and take profit
    if args.stop_loss is None or args.take_profit is None:
        logger.error("stop_loss and take_profit are required to place an OCO order in this tool.")
        return 7

    # Place market-style OCO order via connector (order_type=MARKET will place a market entry with OCO)
    logger.info("Placing practice market OCO order: %s %s units (practice)", args.instrument, args.units)
    result = connector.place_oco_order(
        instrument=args.instrument,
        entry_price=0.0,  # Not needed for market order; connector will still interpret correctly
        stop_loss=args.stop_loss,
        take_profit=args.take_profit,
        units=args.units,
        ttl_hours=24.0,
        order_type="MARKET"
    )

    if result.get("success"):
        logger.info("Practice order placed successfully (practice): %s", result)
        return 0
    else:
        logger.error("Practice order failed: %s", result)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
