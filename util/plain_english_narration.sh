#!/usr/bin/env bash
set -euo pipefail

# Live plain-English narration viewer for RICK.
# Streams `narration.jsonl` in real time.
# Filters out GHOST trades by default (use --show-ghost to show them)
# No GUI required — runs inside your terminal / tmux.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT_DIR}" || exit 1

# Handle different possible locations for narration.jsonl (project root vs logs/)
NARR_FILE="${ROOT_DIR}/narration.jsonl"
if [[ ! -f "$NARR_FILE" ]]; then
  NARR_FILE="${ROOT_DIR}/logs/narration.jsonl"
fi
if [[ ! -f "$NARR_FILE" ]]; then
  echo "ERROR: narration.jsonl not found in ${ROOT_DIR} or ${ROOT_DIR}/logs" >&2
  exit 3
fi

HAS_JQ=true
if ! command -v jq >/dev/null 2>&1; then
  HAS_JQ=false
fi

echo "RICK LIVE NARRATION — PLAIN ENGLISH — REAL TIME"
echo "===================================================="
echo "Press Ctrl+C to close this window (does NOT stop trading)"
echo

# Accept optional flag to show ghost trades
ALLOW_GHOST=false
if [[ "${1:-}" == "--show-ghost" || "${1:-}" == "-g" ]]; then
  ALLOW_GHOST=true
  echo "NOTE: Showing GHOST trades in the stream"
fi

# Use tail -n0 -F so we only see new events and handle file rotation/recreate safely

if [[ "$HAS_JQ" == "true" ]]; then
  tail -n 0 -F "$NARR_FILE" 2>/dev/null |
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue

    if ! echo "$line" | jq -e . >/dev/null 2>&1; then
      echo "[INVALID JSON] $line"
      continue
    fi

    if [[ "$ALLOW_GHOST" == "false" ]] && echo "$line" | jq -r '.details.trade_id? // ""' | grep -q '^GHOST'; then
      continue
    fi

    out=$(echo "$line" | jq -r '
      . as $e |
      ($e.timestamp // "") + " | " + ($e.event_type // "UNKNOWN") + " | " + ($e.venue // "") + " | " + ($e.symbol // ($e.details.symbol // "")) + " | " +
      ( if $e.event_type == "TRADE_EXECUTED" then
          ("ID:" + ($e.details.trade_id // "") + " ") +
          ("SIDE:" + (($e.details.side // "") | ascii_upcase) + " ") +
          ("ENTRY:" + (( $e.details.entry // $e.details.entry_price // "") | tostring) + " ") +
          ("SL:" + (( $e.details.sl // $e.details.sl_price // "") | tostring) + " ") +
          ("TP:" + (( $e.details.tp // $e.details.tp_price // "") | tostring) + " ") +
          ("WOLF:" + ($e.details.wolf_pack // "")) +
          ("ORDER_ID:" + ($e.details.order_id // "") + " ")
        elif $e.event_type == "TRADE_OPENED" then
          ("OPEN ID:" + ($e.details.trade_id // ($e.details.order_id // "")) + " ") +
          ("ORDER_ID:" + ($e.details.order_id // "") + " ") +
          ("SIDE:" + (($e.details.side // "") | ascii_upcase) + " ") +
          ("UNITS:" + (( $e.details.units // $e.details.position_size // "") | tostring) + " ") +
          ("ENTRY:" + (( $e.details.entry_price // $e.details.entry // "") | tostring))
        elif $e.event_type == "MACHINE_HEARTBEAT" then
          ("ITER:" + (($e.details.iteration // 0)| tostring) + " ") +
          ("REGIME:" + ($e.details.regime // "") + " ") +
          ("OPEN:" + (($e.details.open_positions // 0) | tostring) + " ") +
          ("PNL:" + (($e.details.session_pnl // 0) | tostring) + " ") +
          ("TRADES:" + (($e.details.trades_today // 0) | tostring))
          elif $e.event_type == "BROKER_ORDER_CREATED" then
            ("BROKER_ORDER: " + ($e.details.broker // "") + " " + ("ORDER_ID:" + ($e.details.order_id // "") + " ") + ("INST:" + ($e.details.instrument // "") + " ") + ("UNITS:" + (($e.details.units // "") | tostring) + " ") + ("ENTRY:" + (($e.details.entry_price // "") | tostring) + " ") + ("ENV:" + ($e.details.environment // "")))
          elif $e.event_type == "BROKER_MAPPING" then
            ("MAPPING: ORDERID:" + ($e.details.order_id // "") + " -> TRADEID:" + ($e.details.trade_id // "") + " ")
        elif ($e.event_type == "AGGRESSIVE_LEVERAGE_APPLIED") then
          ("AGGRESSIVE LEV: " + ($e.details.leverage | tostring) + "x " + ($e.details.symbol // "") + " units:" + (($e.details.units // "") | tostring) + " " + (($e.details.explanation // "") | tostring))
        elif ($e.event_type == "AUTONOMOUS_STARTUP" or $e.event_type == "CANARY_INIT" or $e.event_type == "CANARY_SESSION_START") then
          ("DETAILS: " + ($e.details | tostring))
        elif ($e.event_type == "ENTRY_CANDIDATE") then
          ("CANDIDATE " + ($e.details.direction // "") + " conf=" + (($e.details.confidence // 0) | tostring) + " confl=" + (($e.details.confluence // 0) | tostring))
        elif ($e.event_type == "ENTRY_ACCEPTED") then
          ("ACCEPTED " + ($e.details.direction // "") + " bucket=" + ($e.details.bucket // "") + " conf=" + (($e.details.confidence // 0) | tostring) + " confl=" + (($e.details.confluence // 0) | tostring))
        elif ($e.event_type == "ENTRY_REJECTED") then
          ("REJECTED " + ($e.details.reason_code // "") + ": " + (($e.details.explanation // "") | tostring) + " (bucket=" + (($e.details.bucket // "") | tostring) + ")")
        elif ($e.event_type == "ENTRY_VOL_GATED") then
          ("REJECTED vol_gate: ADR " + (($e.details.adr_pips // "?") | tostring) + " > cap " + (($e.details.adr_cap_pips // "?") | tostring))
        else
          ($e.details | tostring)
        end)
    ')

    [[ -z "$out" ]] && echo "[PARSE EMPTY] $line" || echo "$out"
  done
else
  echo "NOTE: 'jq' not found — using Python fallback formatter" >&2
  export RBZ_ALLOW_GHOST="$ALLOW_GHOST"
  export RBZ_NARRATION_FILE="$NARR_FILE"
  tail -n 0 -F "$NARR_FILE" 2>/dev/null | python3 -u - <<'PY'
import json
import os
import sys

allow_ghost = os.environ.get('RBZ_ALLOW_GHOST', 'false').lower() in ('1', 'true', 'yes', 'on')

def _get(d, *keys, default=''):
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        ev = json.loads(line)
    except Exception:
        print(f"[INVALID JSON] {line}")
        continue

    details = ev.get('details') or {}
    trade_id = _get(details, 'trade_id', default='')
    if (not allow_ghost) and isinstance(trade_id, str) and trade_id.startswith('GHOST'):
        continue

    ts = ev.get('timestamp', '')
    et = ev.get('event_type', 'UNKNOWN')
    venue = ev.get('venue', '')
    sym = ev.get('symbol') or _get(details, 'symbol', default='')

    # Small, stable summary
    if et in ('TRADE_OPENED', 'TRADE_EXECUTED'):
        side = (details.get('side') or details.get('direction') or '').upper()
        entry = details.get('entry_price') or details.get('entry')
        units = details.get('units') or details.get('position_size')
        extra = f"ID:{trade_id} SIDE:{side} UNITS:{units} ENTRY:{entry}"
    elif et in ('BROKER_ORDER_CREATED', 'OCO_PLACED'):
        oid = details.get('order_id') or details.get('oanda_order')
        inst = details.get('instrument') or sym
        extra = f"ORDER_ID:{oid} INST:{inst}"
    elif et == 'BROKER_MAPPING':
        extra = f"ORDERID:{details.get('order_id')} -> TRADEID:{details.get('trade_id')}"
    else:
        # keep it short
        extra = str(details)
        if len(extra) > 240:
            extra = extra[:237] + '...'

    print(f"{ts} | {et} | {venue} | {sym} | {extra}")
PY
fi

