#!/usr/bin/env bash
set -euo pipefail

# RICK_PHOENIX - LOCKDOWN
# Purpose: protect the profitable practice setup from accidental edits.
# NOTE: this is a filesystem-permission lock. It does not replace git hygiene.

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

echo "[lockdown] repo: $repo_root"

echo "[lockdown] locking critical code (444)"
chmod 444 \
  oanda/oanda_trading_engine.py \
  brokers/oanda_connector.py \
  core/momentum_signals.py \
  oanda_trading_engine.py

echo "[lockdown] locking secrets (600)"
# Keep secrets writable by owner only (so you can rotate tokens without chmod games).
chmod 600 \
  .env \
  token_practice.txt \
  token_paper.txt

echo "[lockdown] verifying permissions"
stat -c '%a %n' \
  oanda/oanda_trading_engine.py \
  brokers/oanda_connector.py \
  core/momentum_signals.py \
  oanda_trading_engine.py \
  .env \
  token_practice.txt \
  token_paper.txt

echo "[lockdown] done"
