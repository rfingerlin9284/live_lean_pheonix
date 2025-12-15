#!/usr/bin/env python3
"""
System Diagnostic Check
Verifies the current configuration against the 'Friday 5 PM' baseline.
"""
import os
import sys
import yaml
from dotenv import load_dotenv

# Load environment
load_dotenv()

def check_config():
    print("=== RICK PHOENIX SYSTEM DIAGNOSTIC ===")
    print(f"Time: {os.popen('date').read().strip()}")
    
    # 1. Check Strategy Toggles
    try:
        with open("config/strategy_toggles.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        print("\n[Strategy Configuration]")
        print(f"Active Profile: {config.get('active_profile')}")
        
        oanda_sessions = config.get('sessions', {}).get('oanda', {})
        print("\n[OANDA Sessions]")
        for session, details in oanda_sessions.items():
            status = "✅ ACTIVE" if details.get('active') else "❌ INACTIVE"
            strategies = details.get('strategies', [])
            print(f"  {session.ljust(10)}: {status} | Strategies: {strategies}")
            
    except Exception as e:
        print(f"❌ Error reading strategy_toggles.yaml: {e}")

    # 2. Check Environment Variables (Two-Step SL)
    print("\n[Environment / Two-Step SL]")
    sl_mode = os.getenv("TWO_STEP_SL_MODE", "OFF")
    step2_trigger = os.getenv("STEP2_TRIGGER_PIPS", "N/A")
    print(f"  TWO_STEP_SL_MODE: {sl_mode}")
    print(f"  STEP2_TRIGGER_PIPS: {step2_trigger}")

    # 3. Check Charter
    print("\n[Charter Status]")
    if os.path.exists("foundation/rick_charter.py"):
        print("  ✅ RickCharter: Present")
    else:
        print("  ❌ RickCharter: MISSING")
        
    if os.path.exists("foundation/agent_charter.py"):
        print("  ✅ AgentCharter: Present")
    else:
        print("  ❌ AgentCharter: MISSING")

    # 4. Check OANDA Connector
    print("\n[Components]")
    if os.path.exists("brokers/oanda_connector.py"):
        print("  ✅ OANDA Connector: Installed")
    else:
        print("  ❌ OANDA Connector: MISSING")

    print("\n=== DIAGNOSTIC COMPLETE ===")

if __name__ == "__main__":
    check_config()
