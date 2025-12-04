#!/usr/bin/env bash
# Export minimal consolidated source to a destination folder suitable for upload to Gemini
# Usage:
#   ./tools/export_for_gemini.sh /mnt/c/Users/<user>/Downloads
#   ./tools/export_for_gemini.sh  (defaults to ./export_gemini_minimal)

set -euo pipefail

DEST=${1:-"${PWD}/export_gemini_minimal"}

# If on WSL and C drive present, choose Windows downloads automatically
if [ -d "/mnt/c/Users" ] && [ -z "${1:-}" ]; then
  WIN_USER=$(ls /mnt/c/Users | head -n 1)
  if [ -n "$WIN_USER" ]; then
    DEST="/mnt/c/Users/$WIN_USER/Downloads/RICK_GEMINI_EXPORT"
  fi
fi

echo "Export destination: $DEST"
rm -rf "$DEST"
mkdir -p "$DEST"

# Files & folders to export (curated, minimal set) - relative to repo root
FILES=(
  "oanda/oanda_trading_engine.py"
  "oanda/foundation/rick_charter.py"
  "brokers/oanda_connector.py"
  "foundation/rick_charter.py"
  "rick_institutional_full.py"
  "rick_hive/guardian_gates.py"
  "util/narration_logger.py"
  "util/rick_narrator.py"
  "util/position_police.py"
  "pretty_print_narration.py"
  "bridges/oanda_live_bridge.py"
  "bridges/oanda_charter_bridge.py"
  "brokers/coinbase_advanced_connector.py"
  "oanda/brokers/oanda_connector.py"
  "start_with_integrity.sh"
  "start_tmux_dashboard.sh"
  "auto_diagnostic_monitor.py"
  "active_trade_monitor.py"
  "system_watchdog.py"
  "config/gates.yaml"
  "config/aggressive_machine_config.py"
  "tools/check_narration_counts.py"
  "tools/export_for_gemini.sh"
  ".vscode/tasks.json"
  ".vscode/cheatsheet.md"
  "tests/test_charter_gates.py"
)

# Create dirs and copy files
for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then
    target_dir="$DEST/$(dirname "$f")"
    mkdir -p "$target_dir"
    cp "$f" "$target_dir/"
    echo "Copied $f -> $target_dir/"
  else
    echo "Warning: $f not found, skipping"
  fi
done

# Create manifest and README
MANIFEST="$DEST/manifest.txt"
README="$DEST/README_GEMINI_EXPORT.md"

echo "Creating manifest: $MANIFEST"
for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then
    echo "$f" >> "$MANIFEST"
  fi
done

# Include generated manifest files themselves for completeness
echo "manifest.txt" >> "$MANIFEST"
echo "manifest.json" >> "$MANIFEST"

echo "Creating README: $README"
cat > "$README" <<'EOF'
# RICK Gemini Consolidated Export

This folder is a minimal consolidated export for upload to the Gemini 3 Studio App Builder.
It contains the essential code to get an OANDA-connected autonomous agent running with the core
Rick Charter rules, logging, and the Hive/guardian gates. The goal of the minimal export is to
allow you to quickly load and run the key features in an app builder or remote environment.

Files included (manifest.txt lists them all):

- OANDA trading engine: `oanda/oanda_trading_engine.py`
- OANDA Charter: `oanda/foundation/rick_charter.py`
- Global Charter: `foundation/rick_charter.py`
- OANDA connector: `oanda/brokers/oanda_connector.py`
- Rick institutional agent: `rick_institutional_full.py`
- Guardian gates: `rick_hive/guardian_gates.py`
- Narration logger: `util/narration_logger.py`
- Narrator (CLI/LLM helper): `util/rick_narrator.py`
- Position police (min-notional enforcement): `util/position_police.py`
- Pretty print narration: `pretty_print_narration.py`
- Bridges (OANDA & Coinbase): `bridges/*`
- Coinbase connector: `brokers/coinbase_advanced_connector.py`
- Monitoring & management scripts: `start_with_integrity.sh`, `start_tmux_dashboard.sh`, `system_watchdog.py`, `auto_diagnostic_monitor.py`
- Config files: `config/gates.yaml`, `config/aggressive_machine_config.py`
- Tests: `tests/test_charter_gates.py`
- Utility tasks and cheatsheet: `.vscode/tasks.json`, `.vscode/cheatsheet.md`

## Expected Performance (Conservative)
- The OANDA engine should operate in practice mode with full gating applied.
- It will process M15 candle signals and place OCO orders according to the Charter.
- Expected notional sizing will follow MIN_NOTIONAL_USD (10k in balanced profile).
- Expect safe operation in practice; production/live modes require valid API keys and a carefully controlled environment.

## Headless & Platform Independence
- The system is built to run headless by default — the critical entry script is `start_with_integrity.sh`.
- Monitor logs via `narration.jsonl` and `pretty_print_narration.py` piped to tail.
- Platform independence: OANDA-specific code is in the `oanda/` directory; the global charter and guardian logic are platform-agnostic.

## Rick Hive Agent (Connector & Pipeline)
- The institutional agent (`rick_institutional_full.py`) coordinates gates and positions.
- The bridge connectors act as the pipeline between the agent and each broker.
- To connect a new broker (e.g., IBKR): implement a `brokers/ibkr_connector.py` with the same API signatures as `oanda_connector.py` and add a `bridges/ibkr_bridge.py` to build orders from hive signals.

## Remaining work (High-level)
1. Complete Coinbase & IBKR connectors parity with OANDA (slightly different order fields and pip calculations).
2. Unit tests for all gateways and live system integration tests for each broker.
3. Dashboard: add the web UI integration (Streamlit/Next) that consumes narration.jsonl and allows manual control (already present in the streamlit readme; needs complete wiring for live toggles).
4. Harden the autopilot watchdogs & alerts: integrate with the narrator to send alerts when the UI is down; e.g., via email or Slack integration.
5. Add CI & testing automation to validate API changes for each broker.
6. Complete scripts for production deploy (systemd/service) and containerization (Dockerfile), with secrets management for API keys.

## How to Upload
- Use the `manifest.txt` and the files in this directory. Gemini does not accept zip files; upload the listed files individually or via their file-browse UI.
- Alternatively, copy this directory to `%USERPROFILE%\Downloads\RICK_GEMINI_EXPORT` on Windows prior to uploading.

## Building out other platforms (step-by-step)
- For Coinbase: replicate `oanda/brokers/oanda_connector.py` logic but use Coinbase API endpoints and adjust notional calculation using quote currency conversion.
- For IBKR: implment `brokers/ibkr_connector.py` using IBKR API, mapping OCO semantics to IBKR order types.
- Implement a statistical adapter for each platform to compute `units` per their instrument definitions.

## Headless Mode
- If the dashboard fails, use `start_with_integrity.sh` or `system_watchdog.py` to re-launch OANDA engine in 'practice' and continue operations Headless.
- Ensure `start_with_integrity.sh` is configured to launch processes as background jobs and to restart on failure.

EOF

# Add README to the manifest (for upload trackers)
echo "README_GEMINI_EXPORT.md" >> "$MANIFEST"

# Create a JSON-LD for the manifest for visibility as well
# Build a basic manifest.json without jq (portable)
python3 - <<PY > "$DEST/manifest.json"
import json
import os
manifest = []
with open("$MANIFEST") as f:
  for line in f:
    ln = line.strip()
    if ln:
      manifest.append(ln)
json.dump({"generated_at": __import__('datetime').datetime.utcnow().isoformat()+"Z","manifest": manifest},
      open("$DEST/manifest.json","w"), indent=2)
PY

# Done

echo "Export completed: $DEST"

echo "Please copy or upload these files to Gemini Studio as needed."

# Verify manifest and exported files are consistent
echo "\nVerifying manifest vs exported files..."
TMP_MANIFEST="$(mktemp)"
TMP_ACTUAL="$(mktemp)"
cat "$MANIFEST" | sed 's|\r||g' | sort > "$TMP_MANIFEST"
cd "$DEST"
find . -type f | sed 's|^./||' | sort > "$TMP_ACTUAL"
echo "Files in manifest (count): $(wc -l < $TMP_MANIFEST)"
echo "Files actually exported (count): $(wc -l < $TMP_ACTUAL)"
echo "\nFiles in manifest but not exported (if any):"
comm -23 "$TMP_MANIFEST" "$TMP_ACTUAL" || true
echo "\nFiles exported but not in manifest (if any):"
comm -13 "$TMP_MANIFEST" "$TMP_ACTUAL" || true
rm -f "$TMP_MANIFEST" "$TMP_ACTUAL"

exit 0
