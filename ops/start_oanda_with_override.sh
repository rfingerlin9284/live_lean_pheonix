#!/usr/bin/env bash
set -euo pipefail

# Start OANDA practice engine with a secure temporary override token.
# Usage: UNLOCK_SECRET=secret ./ops/start_oanda_with_override.sh [ttl_seconds] [--dry-run]

TTL=${1:-600}
DRY_RUN=false
if [ "${2:-}" == "--dry-run" ]; then
  DRY_RUN=true
fi

if [ -z "${UNLOCK_SECRET:-}" ]; then
  echo "ERROR: UNLOCK_SECRET is not set. Please set it before running this script." >&2
  exit 1
fi

echo "Generating temporary override token (TTL=${TTL}s)..."
# We capture the relevant lines from create_unlocked_token.sh (lines 2-4 in its output)
ENV_ASSIGN=$(bash ./ops/create_unlocked_token.sh "$TTL" | grep -E '^PROTOCOL_UNCHAINED|^PROTOCOL_UNCHAINED_TS|^PROTOCOL_UNCHAINED_TOKEN' | sed 's/^/export /' | tr '\n' ';')

echo "Token generated. The following environment variables will be set:" 
echo "$ENV_ASSIGN"

if [ "$DRY_RUN" = true ]; then
  echo "DRY RUN: not actually starting engine. To start, re-run without --dry-run." 
  echo "Next step would be to set ALLOW/CONFIRM and start the engine in practice mode."
  exit 0
fi

# Evaluate environment assignments
eval "$ENV_ASSIGN"

# Ensure we EXPORT the token variables so child processes see them
eval "export $ENV_ASSIGN"

# Load environment variables from .env.oanda_only or .env (if present) so engine has credentials
if [ -f .env.oanda_only ]; then
  set -o allexport
  source .env.oanda_only
  set +o allexport
elif [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi

# Intent gating
export ALLOW_PRACTICE_ORDERS=1
export CONFIRM_PRACTICE_ORDER=1
export OANDA_LOAD_ENV_FILE=1
export OANDA_FORCE_ENV=practice
export RICK_ENV=practice

echo "Starting OANDA engine in practice mode with override token..."
# Use the start_with_integrity.sh wrapper (it sets PYTHONPATH, integrity checks, and .env behavior)
bash ./start_with_integrity.sh
