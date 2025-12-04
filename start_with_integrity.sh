#!/bin/bash
set -e
# Use current directory (RICK_PHOENIX)
cd "$(dirname "$0")"

echo "=== RICK START WITH INTEGRITY (PIN 841921) ==="

# Kill any existing instances to prevent duplicates
pkill -f oanda_trading_engine.py || true

# Ensure PYTHONPATH prefers clean runtime guard before project root
export PYTHONPATH="runtime_guard:${PYTHONPATH:+$PYTHONPATH:}.:$(pwd)"

# Verify sitecustomize.py exists and is loadable
if python3 -c "import sitecustomize, sys; import os; p=getattr(sitecustomize,'__file__',''); print(p)" >/tmp/.sitecustomize_path 2>/dev/null; then
    SC_PATH=$(cat /tmp/.sitecustomize_path)
    if echo "$SC_PATH" | grep -q "/runtime_guard/sitecustomize.py"; then
        echo "✓ sitecustomize validated: $SC_PATH"
    else
        echo "⚠️  WARNING: sitecustomize loaded from unexpected location: $SC_PATH"
    fi
else
    echo "⚠️  sitecustomize load warning"
fi

# Run integrity check
if ! python3 check_integrity.py; then
    echo "❌ STARTUP BLOCKED: Integrity check failed"
    exit 1
fi

# Load environment
if [ -f .env ]; then
    set -o allexport
    source .env
    set +o allexport
fi

# Set safe defaults for environment flags
# Default to practice environment for OANDA unless explicitly overridden
export OANDA_FORCE_ENV=${OANDA_FORCE_ENV:-practice}
# Expose RICK_ENV derived from TRADING_ENVIRONMENT for single-engine selection
export RICK_ENV=${RICK_ENV:-${TRADING_ENVIRONMENT:-practice}}
# Allow connectors to auto-load .env if they want; Start script already sources .env, but set flag for scripts
export OANDA_LOAD_ENV_FILE=${OANDA_LOAD_ENV_FILE:-1}

# If we're in practice mode and credentials exist (and are not obviously placeholders),
# enable paper execution for convenience (user has signed consent). This will only set
# EXECUTION_ENABLED when a token & account id look valid.
if [ "${OANDA_FORCE_ENV}" = "practice" ]; then
    # Check token and account look valid (not 'xxx' or placeholders)
    if [ -n "${OANDA_PAPER:-}" ] && [ -n "${OANDA_PRACTICE_ACCOUNT_ID:-}" ]; then
        case "${OANDA_PAPER}" in
            *xxx*|*YOUR*|*your*|"your_practice_token_here")
                # Placeholder token - don't auto-enable
                ;;
            *)
                export EXECUTION_ENABLED=${EXECUTION_ENABLED:-1}
                echo "✓ OANDA practice credentials detected - enabling paper execution (EXECUTION_ENABLED=1)"
                ;;
        esac
    fi
fi

# Verify credentials
if [ -z "${OANDA_PAPER:-}" ] || [ -z "${OANDA_PRACTICE_ACCOUNT_ID:-}" ]; then
    echo "❌ STARTUP BLOCKED: Missing OANDA credentials"
    exit 2
fi

echo "✓ Integrity validated"
echo "✓ Credentials loaded"
# Check .env permissions and try to lock them if insecure (skip if SIMPLIFY_MODE active)
if [ "${SIMPLIFY_MODE:-0}" != '1' ]; then
    if [ -f ops/check_env_permissions.py ]; then
        python3 ops/check_env_permissions.py || true
        rc=$?
        if [ $rc -eq 2 ]; then
            echo "⚠️  .env permissions appear insecure. Attempting to lock via ops/lock_secrets.sh"
            if [ -f ops/lock_secrets.sh ]; then
                bash ops/lock_secrets.sh ./.env || true
                python3 ops/check_env_permissions.py || true
            fi
        fi
    fi
else
    echo "SIMPLIFY_MODE=1: skipping env permission checks and lock operations"
fi
echo "🚀 Starting engine with runtime guards..."

# Start engine with explicit PYTHONPATH
mkdir -p logs
exec env PYTHONPATH="$PYTHONPATH" python3 -u oanda/oanda_trading_engine.py 2>&1 | tee logs/engine.log
