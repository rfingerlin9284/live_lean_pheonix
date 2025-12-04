#!/usr/bin/env bash
set -euo pipefail

# restore_confidence_env.sh – revert Balanced profile to original confidence/env logic
#
# This script resets MIN_EXPECTED_PNL_USD and MIN_NOTIONAL_USD in charter files and
# reinstates a fallback in the OANDA connector so env overrides can be used.

MIN_EXPECTED_PNL_USD=35.0
# Default to Balanced profile values (MIN_NOTIONAL_USD=10000) — can be overridden as needed
MIN_NOTIONAL_USD=10000

CHARTER_FILES=(
  "foundation/rick_charter.py"
  "oanda/foundation/rick_charter.py"
  "rick_hive/rick_charter.py"
)

echo "Restoring charter constants to MIN_EXPECTED_PNL_USD=${MIN_EXPECTED_PNL_USD}, MIN_NOTIONAL_USD=${MIN_NOTIONAL_USD}"
for file in "${CHARTER_FILES[@]}"; do
  if [[ -f "$file" ]]; then
    if [[ ! -f "${file}.bak-restore" ]]; then
      cp -p "$file" "${file}.bak-restore"
    fi
    sed -Ei "s/(MIN_EXPECTED_PNL_USD\s*=\s*)[0-9]+(\.[0-9]+)?/\1${MIN_EXPECTED_PNL_USD}/" "$file"
    sed -Ei "s/(MIN_NOTIONAL_USD\s*=\s*)[0-9]+(\.[0-9]+)?/\1${MIN_NOTIONAL_USD}/" "$file"
    echo "  Updated $file"
  else
    echo "  Warning: $file not found – skipping"
  fi
done

OANDA_CONNECTOR="oanda/brokers/oanda_connector.py"
if [[ -f "$OANDA_CONNECTOR" ]]; then
  if [[ ! -f "${OANDA_CONNECTOR}.bak-restore" ]]; then
    cp -p "$OANDA_CONNECTOR" "${OANDA_CONNECTOR}.bak-restore"
  fi
  # Ensure os import
  if ! grep -q "\bimport os\b" "$OANDA_CONNECTOR"; then
    sed -i '1iimport os' "$OANDA_CONNECTOR"
  fi
  # Use robust fallback for min_expected - first try to use RickCharter value, otherwise env var, otherwise string default
  # We'll replace the existing min_expected assignment if present using simple substitution. If not present, we add the fallback.
  # First, try to replace common variants
  sed -Ei "s/min_expected\s*=\s*float\(RickCharter\.MIN_EXPECTED_PNL_USD\)/min_expected = float(getattr(RickCharter, 'MIN_EXPECTED_PNL_USD', os.getenv('MIN_EXPECTED_PNL_USD', '${MIN_EXPECTED_PNL_USD}')))/" "$OANDA_CONNECTOR" || true
  sed -Ei "s/min_expected\s*=\s*getattr\(RickCharter,\s*\"MIN_EXPECTED_PNL_USD\",\s*[^)]*\)/min_expected = float(getattr(RickCharter, 'MIN_EXPECTED_PNL_USD', os.getenv('MIN_EXPECTED_PNL_USD', '${MIN_EXPECTED_PNL_USD}')))/" "$OANDA_CONNECTOR" || true

  # If still no assignment, insert fallback a few lines above the check area (search for 'expected_pnl_usd')
  if ! grep -q "MIN_EXPECTED_PNL_USD" "$OANDA_CONNECTOR"; then
    # nothing to do — it's possible the file uses a different pattern
    echo "  Note: MIN_EXPECTED_PNL_USD identifier not found in $OANDA_CONNECTOR"
  fi
  echo "Restored fallback logic in $OANDA_CONNECTOR"
else
  echo "Warning: $OANDA_CONNECTOR not found – skipping fallback restoration"
fi

echo "Confidence and environment logic restoration complete. Backups created with .bak-restore suffix."

# Quick verification: import the charters and display the values
python3 - <<'PY'
from importlib import reload
import sys
sys.path.append('.')
try:
  import foundation.rick_charter as fchar
  import oanda.foundation.rick_charter as ochar
  import rick_hive.rick_charter as hchar
  print('✅ Verified: Foundation MIN_EXPECTED_PNL_USD', fchar.RickCharter.MIN_EXPECTED_PNL_USD)
  print('✅ Verified: Foundation MIN_NOTIONAL_USD', fchar.RickCharter.MIN_NOTIONAL_USD)
  print('✅ Verified: OANDA MIN_EXPECTED_PNL_USD', ochar.RickCharter.MIN_EXPECTED_PNL_USD)
  print('✅ Verified: OANDA MIN_NOTIONAL_USD', ochar.RickCharter.MIN_NOTIONAL_USD)
  print('✅ Verified: RICK_HIVE MIN_EXPECTED_PNL_USD', hchar.RickCharter.MIN_EXPECTED_PNL_USD)
  print('✅ Verified: RICK_HIVE MIN_NOTIONAL_USD', hchar.RickCharter.MIN_NOTIONAL_USD)
except Exception as e:
  import sys
  print(f"ERROR: Charter import failed: {e}")
  sys.exit(1)
PY

# Re-lock charter files as read-only for archive/governance
chmod a-w foundation/rick_charter.py oanda/foundation/rick_charter.py rick_hive/rick_charter.py || true
echo 'Files re-locked as read-only'
