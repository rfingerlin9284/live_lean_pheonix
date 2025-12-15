#!/usr/bin/env bash
set -euo pipefail

# RICK_PHOENIX - UNLOCKDOWN
# Purpose: temporarily restore write permissions so you can maintain/patch code.

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

echo "[unlockdown] repo: $repo_root"

echo "[unlockdown] restoring code to owner-writable (644)"
chmod 644 \
  oanda/oanda_trading_engine.py \
  brokers/oanda_connector.py \
  core/momentum_signals.py \
  oanda_trading_engine.py

echo "[unlockdown] leaving secrets at 600 (owner-only)"
chmod 600 \
  .env \
  token_practice.txt \
  token_paper.txt

echo "[unlockdown] verifying permissions"
stat -c '%a %n' \
  oanda/oanda_trading_engine.py \
  brokers/oanda_connector.py \
  core/momentum_signals.py \
  oanda_trading_engine.py \
  .env \
  token_practice.txt \
  token_paper.txt

echo "[unlockdown] done"
