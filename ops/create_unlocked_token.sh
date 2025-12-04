#!/usr/bin/env bash
set -euo pipefail

# Create a time-limited HMAC token for PROTOCOL_UNCHAINED override
# Usage: UNLOCK_SECRET=your_secret ./ops/create_unlocked_token.sh [ttl_seconds]

TTL=${1:-600}
SECRET=${UNLOCK_SECRET:-}
if [ -z "$SECRET" ]; then
  echo "UNLOCK_SECRET not set. Please set UNLOCK_SECRET environment variable to generate token." >&2
  exit 1
fi

TS=$(date -u +%s)
# Compute HMAC-SHA256 token
TOKEN=$(printf "%s" "$TS" | openssl dgst -sha256 -hmac "$SECRET" -hex | sed 's/^.* //')

echo
echo "Generated token (valid for $TTL seconds):"
echo "PROTOCOL_UNCHAINED=1"
echo "PROTOCOL_UNCHAINED_TS=$TS"
echo "PROTOCOL_UNCHAINED_TOKEN=$TOKEN"
echo
echo "Usage (example):"
echo "  export PROTOCOL_UNCHAINED=1"
echo "  export PROTOCOL_UNCHAINED_TS=$TS"
echo "  export PROTOCOL_UNCHAINED_TOKEN=$TOKEN"
echo "  export ALLOW_PRACTICE_ORDERS=1"
echo "  export CONFIRM_PRACTICE_ORDER=1"
echo "  PYTHONPATH=$PWD .venv/bin/python oanda/oanda_trading_engine.py"
