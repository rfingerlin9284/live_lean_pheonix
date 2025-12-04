#!/usr/bin/env bash
set -euo pipefail

# Script to write a canonical environment template to `.env.oanda_only` and `.env` (with backup + lock)
# Usage: ./scripts/write_env_file.sh [target_oanda_file] [target_env_file]

DRY_RUN=false
NO_LOCK=false
TARGET_OANDA=.env.oanda_only
TARGET_ENV=.env

# very simple cli: accept --dry-run and positional targets
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [TARGET_OANDA] [TARGET_ENV] [--dry-run] [--no-lock]"
      exit 0
      ;;
    --no-lock)
      NO_LOCK=true
      shift
      ;;
    *)
      if [[ "${TARGET_OANDA}" == ".env.oanda_only" && "${TARGET_ENV}" == ".env" ]]; then
        TARGET_OANDA="$1"
      elif [[ "${TARGET_ENV}" == ".env" ]]; then
        TARGET_ENV="$1"
      fi
      shift
      ;;
  esac
done

BACKUP_OANDA=${TARGET_OANDA}.bak.$(date -u +%Y%m%dT%H%M%SZ)
BACKUP_ENV=${TARGET_ENV}.bak.$(date -u +%Y%m%dT%H%M%SZ)
BACKUP_OANDA=${TARGET_OANDA}.bak.$(date -u +%Y%m%dT%H%M%SZ)
BACKUP_ENV=${TARGET_ENV}.bak.$(date -u +%Y%m%dT%H%M%SZ)

echo "Backing up existing ${TARGET_OANDA} -> ${BACKUP_OANDA} (if exists)"
if [ -f "${TARGET_OANDA}" ]; then
  if [ "$DRY_RUN" = false ]; then
    cp -p "${TARGET_OANDA}" "${BACKUP_OANDA}"
  else
    echo "DRY RUN: would copy ${TARGET_OANDA} to ${BACKUP_OANDA}"
  fi
fi
echo "Backing up existing ${TARGET_ENV} -> ${BACKUP_ENV} (if exists)"
if [ -f "${TARGET_ENV}" ]; then
  if [ "$DRY_RUN" = false ]; then
    cp -p "${TARGET_ENV}" "${BACKUP_ENV}"
  else
    echo "DRY RUN: would copy ${TARGET_ENV} to ${BACKUP_ENV}"
  fi
fi

echo "Writing new environment file to ${TARGET_OANDA} and ${TARGET_ENV}..."
if [ "$DRY_RUN" = true ]; then
  echo "DRY RUN: would write template to ${TARGET_OANDA} and ${TARGET_ENV}."
  echo "--- ${TARGET_OANDA} preview ---"
  cat <<'ENV_PAYLOAD'
# RBOTzilla UNI Environment Template
# This file contains demonstration values; replace with your own API tokens/IDs.

RICK_PIN=841921

# OANDA Practice Account (placeholder values — DO NOT COMMIT REAL TOKENS)
OANDA_PRACTICE_ACCOUNT_ID=your-practice-account-id
OANDA_PRACTICE_TOKEN=your-practice-token
OANDA_PRACTICE_BASE_URL=https://api-fxpractice.oanda.com/v3

# Coinbase Sandbox (placeholder values)
COINBASE_SANDBOX_API_KEY=your-coinbase-api-key
COINBASE_SANDBOX_API_SECRET=your-coinbase-api-secret
COINBASE_SANDBOX_PASSPHRASE=your-coinbase-passphrase
COINBASE_SANDBOX_BASE_URL=https://public-sandbox.exchange.coinbase.com

# Default environment settings
MICRO_TRADING_MODE=true
DEFAULT_CAPITAL_USD=2000
TRADING_ENVIRONMENT=sandbox

# Alerting placeholders (replace with real tokens as needed)
TELEGRAM_BOT_TOKEN=your_telegram_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

ENV_PAYLOAD
  echo "--- end preview ---"
else
cat > "${TARGET_OANDA}" <<'ENV_PAYLOAD'
# RBOTzilla UNI Environment Template
# This file contains demonstration values; replace with your own API tokens/IDs.

RICK_PIN=841921

# OANDA Practice Account (placeholder values — DO NOT COMMIT REAL TOKENS)
OANDA_PRACTICE_ACCOUNT_ID=your-practice-account-id
OANDA_PRACTICE_TOKEN=your-practice-token
OANDA_PRACTICE_BASE_URL=https://api-fxpractice.oanda.com/v3

# Coinbase Sandbox (placeholder values)
COINBASE_SANDBOX_API_KEY=your-coinbase-api-key
COINBASE_SANDBOX_API_SECRET=your-coinbase-api-secret
COINBASE_SANDBOX_PASSPHRASE=your-coinbase-passphrase
COINBASE_SANDBOX_BASE_URL=https://public-sandbox.exchange.coinbase.com

# Default environment settings
MICRO_TRADING_MODE=true
DEFAULT_CAPITAL_USD=2000
TRADING_ENVIRONMENT=sandbox

# Alerting placeholders (replace with real tokens as needed)
TELEGRAM_BOT_TOKEN=your_telegram_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

ENV_PAYLOAD
fi

if [ "$DRY_RUN" = true ]; then
  echo "--- ${TARGET_ENV} preview ---"
cat <<'ENV_PAYLOAD_COPY'
RICK_PIN=841921
OANDA_PRACTICE_ACCOUNT_ID=your-practice-account-id
OANDA_PRACTICE_TOKEN=your-practice-token
OANDA_PRACTICE_BASE_URL=https://api-fxpractice.oanda.com/v3
ENV_PAYLOAD_COPY
  echo "--- end preview ---"
else
  # Copy core required values into root .env for convenience
cat > "${TARGET_ENV}" <<'ENV_PAYLOAD_COPY'
RICK_PIN=841921
OANDA_PRACTICE_ACCOUNT_ID=your-practice-account-id
OANDA_PRACTICE_TOKEN=your-practice-token
OANDA_PRACTICE_BASE_URL=https://api-fxpractice.oanda.com/v3
ENV_PAYLOAD_COPY
fi

echo "Env files written. Applying safe file permissions..."
# Respect either explicit flag or SIMPLIFY_MODE env variable
if [ "$DRY_RUN" = false ] && [ "$NO_LOCK" = false ] && [ "${SIMPLIFY_MODE:-0}" != '1' ]; then
  chmod 600 "${TARGET_OANDA}" || true
  chmod 600 "${TARGET_ENV}" || true
else
  echo "Skipping permission hardening (NO_LOCK=$NO_LOCK SIMPLIFY_MODE=${SIMPLIFY_MODE:-0})"
fi

echo "Running ops/lock_secrets.sh to enforce perms and safety"
if [ "$DRY_RUN" = false ] && [ "$NO_LOCK" = false ] && [ "${SIMPLIFY_MODE:-0}" != '1' ] && [ -f ops/lock_secrets.sh ]; then
  bash ops/lock_secrets.sh "${TARGET_OANDA}" || true
  bash ops/lock_secrets.sh "${TARGET_ENV}" || true
else
  echo "Skipping ops/lock_secrets.sh (NO_LOCK=$NO_LOCK SIMPLIFY_MODE=${SIMPLIFY_MODE:-0})"
fi

if [ "$DRY_RUN" = true ]; then
  echo "DRY RUN complete — no files were changed."
else
  echo "Done. ${TARGET_OANDA} and ${TARGET_ENV} updated and locked."
fi
