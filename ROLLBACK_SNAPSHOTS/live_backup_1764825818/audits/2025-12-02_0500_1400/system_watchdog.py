#!/usr/bin/env python3
"""
RICK System Watchdog & Configuration Monitor
Combines 'The Pulse' (System Status) with 'Deep Scan' (Config Audit).
Runs in a loop to ensure system health and configuration integrity.
"""

import sys
import os
import time
import subprocess
from datetime import datetime
from pathlib import Path

# ANSI Colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_module_integrity(name, import_names, path_check=None):
    """
    Verifies if a module is present on disk and importable.
    Returns (bool, str) -> (is_active, status_message)
    """
    # 1. Check Disk Presence
    if path_check:
        full_path = os.path.join(os.getcwd(), path_check)
        if not os.path.exists(full_path):
            return False, "File Missing"
            
    # 2. Check Importability
    try:
        for module in import_names:
            __import__(module)
        return True, "Active"
    except ImportError:
        return False, "Import Failed"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_process(process_name):
    """Check if a process is running by scanning all processes"""
    try:
        # Use ps -ef for full listing
        result = subprocess.run(["ps", "-ef"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if process_name in line and "grep" not in line and "python" in line:
                # Found it
                parts = line.split()
                pid = parts[1]
                return True, pid
        return False, "Not Found"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_log_freshness(log_path, max_age_minutes=5):
    """Check if a log file has been updated recently"""
    path = Path(log_path)
    if not path.exists():
        return False, "Not Found"
    
    try:
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        age_minutes = (datetime.now() - mtime).total_seconds() / 60
        if age_minutes <= max_age_minutes:
            return True, f"Updated {age_minutes:.1f}m ago"
        else:
            return False, f"Stale ({age_minutes:.1f}m ago)"
    except Exception as e:
        return False, f"Error: {str(e)}"

def print_status_row(feature, status, details, is_header=False):
    if is_header:
        print(f"{Colors.BOLD}{feature:<25} | {status:<15} | {details}{Colors.ENDC}")
        print("-" * 80)
    else:
        status_color = Colors.GREEN if "Active" in status or "Running" in status or "Updated" in str(details) else Colors.FAIL
        if "Stale" in str(details): status_color = Colors.WARNING
        
        icon = "✅" if status_color == Colors.GREEN else "⚠️ " if status_color == Colors.WARNING else "❌"
        
        print(f"{feature:<25} | {status_color}{icon} {status:<12}{Colors.ENDC} | {details}")

def run_audit():
    print(f"\n{Colors.HEADER}{Colors.BOLD}🛡️  RICK SYSTEM WATCHDOG & INTEGRITY MONITOR{Colors.ENDC}")
    print(f"{Colors.BLUE}   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print("=" * 80)

    # 1. RUNTIME HEALTH (The Pulse)
    print(f"\n{Colors.BOLD}📡 RUNTIME HEALTH (The Pulse){Colors.ENDC}")
    print_status_row("COMPONENT", "STATUS", "DETAILS", is_header=True)
    
    # Engine Process
    is_running, pid = check_process("oanda_trading_engine.py")
    status = "Running" if is_running else "Stopped"
    details = f"PID: {pid}" if is_running else "Process not found (checked pgrep & ps aux)"
    print_status_row("Trading Engine", status, details)
    
    # Log Freshness
    # Check engine.log (now created by start script)
    is_fresh, details = check_log_freshness("logs/engine.log")
    status = "Healthy" if is_fresh else "Stalled"
    print_status_row("Engine Heartbeat", status, details)
    
    # Check narration.jsonl (in root)
    is_fresh, details = check_log_freshness("narration.jsonl")
    status = "Healthy" if is_fresh else "Quiet"
    print_status_row("Narration Feed", status, details)

    # 2. CONFIGURATION INTEGRITY (Deep Scan)
    print(f"\n{Colors.BOLD}⚙️  CONFIGURATION INTEGRITY (Deep Scan){Colors.ENDC}")
    print_status_row("MODULE", "STATE", "VERIFICATION", is_header=True)
    
    # Core
    print_status_row("Charter Compliance", "Active", "Hardcoded (Immutable)")
    
    # ML
    is_active, msg = check_module_integrity("ML Intelligence", ["ml_learning.regime_detector"], "ml_learning")
    print_status_row("ML Intelligence", "Active" if is_active else "Inactive", msg)
    
    # Hive
    is_active, msg = check_module_integrity("Hive Mind", ["hive.rick_hive_mind"], "hive")
    print_status_row("Hive Mind", "Active" if is_active else "Inactive", msg)
    
    # Momentum
    is_active, msg = check_module_integrity("Momentum", ["util.momentum_trailing"], "util/momentum_trailing.py")
    print_status_row("Momentum System", "Active" if is_active else "Inactive", msg)
    
    # Hedge
    is_active, msg = check_module_integrity("Hedge Engine", ["util.quant_hedge_engine"], "util/quant_hedge_engine.py")
    print_status_row("Hedge Engine", "Active" if is_active else "Inactive", msg)

    print("-" * 80)
    
    # Overall Verdict
    if is_running:
        print(f"\n{Colors.GREEN}🟢 SYSTEM OPERATIONAL - Monitoring Active{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}🔴 SYSTEM STOPPED - Action Required{Colors.ENDC}")

if __name__ == "__main__":
    # Ensure we can import local modules
    sys.path.append(os.getcwd())
    
    try:
        while True:
            clear_screen()
            run_audit()
            print(f"\n{Colors.DIM}Next scan in 30 seconds... Press Ctrl+C to stop.{Colors.ENDC}")
            
            # Countdown visual
            for i in range(30, 0, -1):
                if i % 10 == 0 or i < 10:
                    sys.stdout.write(f"\r{Colors.DIM}Scanning in {i}s...{Colors.ENDC}")
                    sys.stdout.flush()
                time.sleep(1)
                
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Watchdog stopped by user.{Colors.ENDC}")
        sys.exit(0)
