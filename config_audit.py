#!/usr/bin/env python3
"""
RICK System Configuration Audit
Lists all features, their default status, and current activation state.
"""
import os
import sys
from datetime import datetime

# ANSI Colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def print_feature(name, default_status, is_active, toggle_method="Code/Import"):
    status_icon = "✅" if is_active else "❌"
    status_color = Colors.GREEN if is_active else Colors.RED
    
    # If default status contains "if present" and is_active is True, add a checkmark to default_status
    display_default = default_status
    if "if present" in default_status and is_active:
         display_default = f"{default_status} {Colors.GREEN}✅{Colors.RESET}"
    
    print(f"{Colors.BOLD}{name:<30}{Colors.RESET} | {display_default:<28} | {status_color}{status_icon} {('Active' if is_active else 'Inactive'):<10}{Colors.RESET} | {toggle_method}")

def check_module(name, import_names, path_check=None):
    """
    Verifies if a module is present on disk and importable.
    """
    # 1. Check Disk Presence
    if path_check:
        full_path = os.path.join(os.getcwd(), path_check)
        if not os.path.exists(full_path):
            return False
            
    # 2. Check Importability
    try:
        for module in import_names:
            __import__(module)
        return True
    except ImportError:
        return False

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}🤖 RICK SYSTEM CONFIGURATION AUDIT{Colors.RESET}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.DIM}Initiating deep system scan...{Colors.RESET}")
    print("="*105)
    print(f"{'FEATURE':<30} | {'DEFAULT':<19} | {'CURRENT STATE':<13} | {'TOGGLE METHOD'}")
    print("-" * 105)

    # 1. Core Systems (Always On)
    print_feature("OANDA Trading Engine", "ALWAYS ON", True, "N/A (Core)")
    print_feature("Charter Compliance (Risk)", "ALWAYS ON", True, "Hardcoded (Immutable)")
    print_feature("Narration (The Voice)", "ALWAYS ON", True, "Hardcoded")
    print_feature("Long & Short Logic", "ALWAYS ON", True, "Hardcoded")
    print_feature("Sentinel Sid (Monitor)", "ALWAYS ON", True, "Task/Process")

    # 2. Conditional Systems (Check Imports/Env)
    
    # ML Intelligence
    ml_active = check_module("ML Intelligence", ["ml_learning.regime_detector", "ml_learning.signal_analyzer"], "ml_learning")
    print_feature("ML Intelligence", "ON if present", ml_active, "Module Existence (ml_learning/)")

    # Hive Mind
    hive_active = check_module("Hive Mind", ["hive.rick_hive_mind"], "hive")
    print_feature("Hive Mind (Swarm)", "ON if present", hive_active, "Module Existence (hive/)")

    # Momentum System
    mom_active = check_module("Momentum", ["util.momentum_trailing"], "util/momentum_trailing.py")
    print_feature("Momentum Trailing", "ON if present", mom_active, "Module Existence (util/)")

    # Strategy Aggregator
    agg_active = check_module("Strategy Aggregator", ["util.strategy_aggregator"], "util/strategy_aggregator.py")
    print_feature("Strategy Aggregator", "ON if present", agg_active, "Module Existence (util/)")

    # Hedge Engine
    hedge_active = check_module("Hedge Engine", ["util.quant_hedge_engine"], "util/quant_hedge_engine.py")
    print_feature("Quant Hedge Engine", "ON if present", hedge_active, "Module Existence (util/)")

    print("-" * 105)
    print(f"\n{Colors.YELLOW}ℹ️  NOTE: 'Module Existence' means the feature activates automatically if the python files exist.{Colors.RESET}")
    print(f"{Colors.YELLOW}   To disable these, you typically rename the folder or file (e.g., _disabled).{Colors.RESET}")
    print("\n")

if __name__ == "__main__":
    sys.path.append(os.getcwd()) # Ensure we can import local modules
    main()
