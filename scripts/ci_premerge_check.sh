#!/usr/bin/env bash
set -euo pipefail

echo "Running CI pre-merge checks: secrets + no 100.0 fallback + tune dry-run"

# Please read: This CI script is intended to run WITHOUT scanning local .env file for secrets
# because the test environment uses `.env` to provide credentials. We'll temporarily move
# any `.env` file outside the repository directory while running the secret scanner.
export OANDA_LOAD_ENV_FILE=1

TMP_ENV_MOVED=false
if [[ -f ".env" ]]; then
    mv .env /tmp/.env.ci_temp
    TMP_ENV_MOVED=true
fi

python3 scripts/find_secrets.py --strict | tee /tmp/find_secrets_output.txt
if grep -q "High confidence secrets found" /tmp/find_secrets_output.txt 2>/dev/null; then
    echo "High confidence secrets found; aborting CI check"
    # restore the env file if it was moved
    if [[ "$TMP_ENV_MOVED" == true ]]; then
        mv /tmp/.env.ci_temp .env || true
    fi
    exit 1
fi

# Restore the .env file now that the scanner has run (it was moved out of the repo for safety)
if [[ "$TMP_ENV_MOVED" == true ]]; then
    mv /tmp/.env.ci_temp .env || true
fi

echo "No apparent secrets found (excluding local .env). Next: assert charters have MIN_EXPECTED_PNL_USD=35 and no 100.0 fallback in runtime code."
python3 - <<'PY'
import importlib.util
spec = importlib.util.spec_from_file_location('t', 'tests/test_no_100pnl_fallback.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.test_foundation_min_expected_pnl()
mod.test_oanda_min_expected_pnl()
mod.test_rick_hive_min_expected_pnl()
mod.test_no_100_fallback_in_code()
print('Charter checks passed')
PY

echo "Running tuning script dry-run..."
python3 scripts/tune_oanda_confidence_profile.py --dry-run

echo "CI pre-merge checks passed"
