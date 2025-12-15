#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# FINAL LOCKDOWN: Protect your profitable setup permanently (code files only)
# PIN: 841921
#
# Notes:
# - Uses chmod 444 to make files read-only.
# - Does NOT touch tokens/.env so credentials can still rotate safely.
# - Idempotent: safe to run multiple times.
# =============================================================================

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

say() { printf '%s\n' "$*"; }

lock_file() {
  local f="$1"
  if [[ -f "$f" ]]; then
    chmod 444 "$f"
    say "locked: $f"
  else
    say "skip (missing): $f"
  fi
}

maybe_lock_matching() {
  # Lock any files matching a glob, but don't fail if glob doesn't match.
  local pattern="$1"
  shopt -s nullglob
  local matches=( $pattern )
  shopt -u nullglob
  if (( ${#matches[@]} )); then
    local f
    for f in "${matches[@]}"; do
      lock_file "$f"
    done
  else
    say "skip (no match): $pattern"
  fi
}

say "=================================================="
say "FINAL LOCKDOWN (PIN: 841921)"
say "Repo: $repo_root"
say "=================================================="

# Canonical engine (real entrypoint)
lock_file "oanda/oanda_trading_engine.py"

# Backwards-compatible wrapper (optional but helps prevent accidental drift)
lock_file "oanda_trading_engine.py"

# Profitable brain
lock_file "core/momentum_signals.py"

# Connector(s)
lock_file "brokers/oanda_connector.py"
lock_file "brokers/oanda_connector_enhanced.py"
lock_file "brokers/oanda_connector_proto.py"

# Charter/gates (names can vary over time)
maybe_lock_matching "**/*charter*.py"
maybe_lock_matching "**/*gate*.py"

say ""
say "=================================================="
say "LOCKDOWN COMPLETE (code files set to read-only)"
say "=================================================="
