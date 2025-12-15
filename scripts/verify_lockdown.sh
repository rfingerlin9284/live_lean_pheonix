#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# Verify that protected files are read-only (444/0444), without failing if a file is missing.
files=(
  "oanda/oanda_trading_engine.py"
  "oanda_trading_engine.py"
  "core/momentum_signals.py"
  "brokers/oanda_connector.py"
  "brokers/oanda_connector_enhanced.py"
  "brokers/oanda_connector_proto.py"
)

shopt -s globstar nullglob
for f in **/*charter*.py **/*gate*.py; do
  files+=("$f")
done
shopt -u globstar nullglob

ok=1
for f in "${files[@]}"; do
  if [[ -f "$f" ]]; then
    mode="$(stat -c "%a" "$f")"
    if [[ "$mode" != "444" ]]; then
      printf 'NOT LOCKED: %s mode=%s\n' "$f" "$mode"
      ok=0
    else
      printf 'LOCKED:     %s mode=%s\n' "$f" "$mode"
    fi
  else
    printf 'MISSING:    %s\n' "$f"
  fi
done

if [[ "$ok" -ne 1 ]]; then
  echo ""
  echo "Some files are not locked. Run: scripts/final_lockdown.sh"
  exit 2
fi
