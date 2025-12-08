#!/bin/bash
# =============================================================================
# Live Narration Feed Display Script
# Auto-refreshing display of last 30 narration events
# Runs in a loop with 10-second refresh interval
# =============================================================================

NARRATION_FILE="${1:-narration.jsonl}"
WORKSPACE_FOLDER="${WORKSPACE_FOLDER:-.}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo "Waiting for narration.jsonl..."

while true; do
    if [ -f "${WORKSPACE_FOLDER}/${NARRATION_FILE}" ]; then
        clear
        echo "=== LIVE NARRATION FEED (Last 30 events) ==="
        echo "Refreshes every 10 seconds..."
        echo ""
        
        tail -30 "${WORKSPACE_FOLDER}/${NARRATION_FILE}" | while IFS= read -r line; do
            # Try to parse and format JSON, fall back to raw line if parsing fails
            echo "$line" | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    timestamp = d.get('timestamp', 'N/A')
    event_type = d.get('event_type', 'UNKNOWN')
    symbol = d.get('symbol', 'N/A')
    details = d.get('details', {})
    print(f'[{timestamp}] {event_type}: {symbol} - {details}')
except:
    print(sys.stdin.read())
" 2>/dev/null || echo "$line"
        done
    else
        echo "No narration.jsonl found yet. Waiting..."
    fi
    
    sleep 10
done
