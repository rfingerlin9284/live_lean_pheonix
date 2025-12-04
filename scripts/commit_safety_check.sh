#!/usr/bin/env bash
set -euo pipefail

# Check the repository for obvious secrets using the helpers
python3 scripts/find_secrets.py | tee /tmp/find_secrets_output.txt
if grep -q "potential secret matches found" /tmp/find_secrets_output.txt 2>/dev/null; then
  echo "Potential secrets found - please review the output above, sanitize and re-run the check. Aborting commit/safety check."
  exit 1
fi
echo "No obvious secrets found."
