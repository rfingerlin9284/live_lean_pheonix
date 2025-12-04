#!/usr/bin/env python3
"""
Test script for environment switching
Verifies that RICK_ENV can be toggled between practice and live
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from util.mode_manager import get_connector_environment, get_mode_info, _read_rick_env

def main():
    print("=" * 60)
    print("ENVIRONMENT TOGGLE TEST")
    print("=" * 60)
    
    # Read current environment
    current_env = _read_rick_env()
    print(f"\nCurrent RICK_ENV from .env: {current_env}")
    
    # Get mode info
    mode_info = get_mode_info()
    print(f"Mode info: {mode_info}")
    
    # Get connector environment
    connector_env = get_connector_environment("oanda")
    print(f"Connector environment for OANDA: {connector_env}")
    
    # Verify environment variable
    import os
    env_var = os.getenv('RICK_ENV', 'not set')
    print(f"RICK_ENV environment variable: {env_var}")
    
    print("\n" + "=" * 60)
    print("ENVIRONMENT CONFIGURATION:")
    print("=" * 60)
    
    if current_env == 'practice':
        print("✅ System is in PRACTICE mode (safe for testing)")
        print("   - Uses OANDA practice account")
        print("   - Paper trading only")
        print("   - No real money at risk")
    elif current_env == 'live':
        print("⚠️  System is in LIVE mode (REAL MONEY)")
        print("   - Uses OANDA live account")
        print("   - Real trades will be executed")
        print("   - USE WITH CAUTION")
    else:
        print(f"⚠️  Unknown environment: {current_env}")
        print("   - Defaulting to practice mode for safety")
    
    print("\n" + "=" * 60)
    print("To switch environments:")
    print("  1. Use VSCode task: '⚙️ Toggle Practice/Live Environment'")
    print("  2. Or manually edit .env file: RICK_ENV=practice or RICK_ENV=live")
    print("  3. Then restart the trading engine")
    print("=" * 60)

if __name__ == "__main__":
    main()
