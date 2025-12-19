#!/bin/bash
# Single Instance Guard - Prevents duplicate trading engine instances
# Uses flock for atomic locking

LOCK_FILE="/tmp/oanda_trading_engine.lock"
LOCK_FD=200

# Function to acquire lock
acquire_lock() {
    eval "exec $LOCK_FD>$LOCK_FILE"
    
    # Try to acquire exclusive lock (non-blocking)
    flock -n $LOCK_FD
    
    if [ $? -ne 0 ]; then
        echo "❌ ALREADY RUNNING — Another instance of the trading engine is active"
        echo "   Lock file: $LOCK_FILE"
        echo "   EXITING to prevent duplicate engines"
        exit 1
    fi
    
    echo "✅ LOCK ACQUIRED — Trading engine starting"
    echo "   Lock file: $LOCK_FILE"
    
    # Write PID to lock file for debugging
    echo $$ > $LOCK_FILE
}

# Function to release lock on exit
release_lock() {
    flock -u $LOCK_FD
    echo "🔓 LOCK RELEASED — Trading engine stopped"
}

# Trap exit signals to clean up lock
trap release_lock EXIT INT TERM

# Acquire lock before continuing
acquire_lock

# If we get here, lock is acquired - continue with the actual command
exec "$@"
