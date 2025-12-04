#!/usr/bin/env bash
# Validate exported files, run simple checks and create a snapshot JSON file
set -euo pipefail

OUTDIR=${1:-.}
cd "$OUTDIR"

SNAPSHOT_FILE="snapshot_status.json"

python3 - <<PY > "$SNAPSHOT_FILE"
import json, os, subprocess, sys, time

snapshot = {
    'generated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    'files_present': [],
    'python_version': sys.version.split('\n')[0],
    'tests': None,
    'errors': [],
}

# Check for key files
key_files = [
    'oanda/oanda_trading_engine.py',
    'oanda/foundation/rick_charter.py',
    'oanda/brokers/oanda_connector.py',
    'rick_institutional_full.py',
    'rick_hive/guardian_gates.py',
    'util/narration_logger.py',
]

for f in key_files:
    snapshot['files_present'].append({f: os.path.exists(f)})

# Run simple tests if pytest available
try:
    import pytest
    # Run tests and capture result
    try:
        import subprocess
        result = subprocess.run(['pytest','-q','tests/test_charter_gates.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120)
        snapshot['tests'] = {'returncode': result.returncode, 'output': result.stdout.splitlines()[-10:]}
    except Exception as e:
        snapshot['errors'].append('pytest run error: ' + str(e))
except Exception:
    snapshot['errors'].append('pytest not installed - skip tests')

# Execute the narration check helper if present
if os.path.exists('tools/check_narration_counts.py'):
    try:
        out = subprocess.run(['python3','tools/check_narration_counts.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=30)
        snapshot['narration_summary'] = out.stdout.splitlines()
    except Exception as e:
        snapshot['errors'].append('check_narration_counts failed: ' + str(e))

# Privately inspect env or config settings
env_example_present = os.path.exists('.env.example')
snapshot['env_example_present'] = env_example_present

# Compose final snapshot
print(json.dumps(snapshot, indent=2))
PY

# Print the created snapshot
cat "$SNAPSHOT_FILE"

exit 0
