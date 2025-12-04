#!/usr/bin/env python3
"""
Verify OANDA credentials and connectivity using read-only account summary endpoint.
This script is safe to run: it will NOT place orders or modify the account.

Usage:
    python3 tools/verify_oanda_live.py [--env live|practice]

It will read credentials from environment variables or repo .env as loaded by the connector.
"""
from __future__ import annotations

import argparse
import logging
import os

from oanda.brokers.oanda_connector import OandaConnector
try:
    from foundation.agent_charter import AgentCharter
except Exception:
    AgentCharter = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('verify_oanda_live')


def main():
    parser = argparse.ArgumentParser(description='Verify OANDA connection in read-only mode.')
    parser.add_argument('--env', choices=['live', 'practice'], help='Force environment for connector (overrides auto-detection)')
    parser.add_argument('--env-file', dest='env_file', help='Path to dotenv-style env file to load for this run (explicit opt-in)')
    args = parser.parse_args()

    env = args.env
    env_file = getattr(args, 'env_file', None)

    if env_file:
        try:
            if os.path.exists(env_file):
                logger.info(f"Loading environment values from {env_file}")
                with open(env_file, 'r') as f:
                    for line in f:
                        if '=' in line and not line.strip().startswith('#'):
                            key, val = line.strip().split('=', 1)
                            os.environ.setdefault(key, val.strip().strip('"\''))
                os.environ['OANDA_LOAD_ENV_FILE'] = '1'
            else:
                logger.warning(f"Env file {env_file} not found; skipping load")
        except Exception as e:
            logger.error(f"Failed to load env file {env_file}: {e}")

    try:
        connector = OandaConnector(pin=None, environment=env) if env else OandaConnector(pin=None)

        logger.info(f'Connector environment: {connector.environment}  trading_enabled={connector.trading_enabled}')

        summary = connector.get_account_summary()
        if not summary:
            # Improve messages for common HTTP errors
            logger.error('Failed to resolve account summary. Are credentials configured and valid?')
            # If an account_id exists, attempt a direct call to get diagnostic payload
            if connector.account_id:
                resp = connector._make_request('GET', f"/v3/accounts/{connector.account_id}/summary")
                if not resp.get('success'):
                    print('\nAPI response:')
                    print(resp.get('error'))
                    if isinstance(resp.get('error'), str) and 'accountID' in resp.get('error'):
                        print('\nIt looks like the account ID may be invalid or malformed. Please check OANDA_PRACTICE_ACCOUNT_ID in your .env')
            return 2

        # Mask account id for safety
        acct = summary.get('account_id')
        masked_acct = f"***{acct[-4:]}" if acct and len(acct) > 4 else acct
        balance = summary.get('balance')
        currency = summary.get('currency')

        print(f"OANDA {connector.environment.upper()} ACCOUNT SUMMARY")
        print(f"Account: {masked_acct}")
        print(f"Balance: {balance} {currency}")
        print(f"Unrealized PnL: {summary.get('unrealized_pl')}")
        print('\nVerification successful - no orders placed.\n')
        if not connector.trading_enabled:
            print('⚠️ NOTE: Connector reports trading_enabled=False. Orders will not be placed until credentials are valid.')
        if AgentCharter:
            print(AgentCharter.approval_tag())
        return 0

    except Exception as e:
        logger.exception('Error during verification: %s', e)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
