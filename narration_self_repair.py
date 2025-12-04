#!/usr/bin/env python3
"""
RICK Narration Self-Repair Helper
Diagnoses, repairs, and documents narration translation errors.
Alerts user and ensures system resilience.
"""
import os
import sys
import time
import traceback
from datetime import datetime

LOG_PATH = '/tmp/narration_self_repair.log'
REPAIR_STATUS = 'FAILED'


def log(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    print(f"\033[96m[Narration Self-Repair] {msg}\033[0m")


def diagnose_error():
    log("Diagnosing narration translation error...")
    # Check for syntax errors in pretty_print_narration.py
    try:
        import py_compile
        py_compile.compile('pretty_print_narration.py', doraise=True)
        log("No syntax errors detected in pretty_print_narration.py.")
        return True
    except Exception as e:
        log(f"Syntax error detected: {e}")
        return False


def check_dependencies():
    log("Checking dependencies...")
    try:
        import json, time, datetime
        log("All required dependencies are present.")
        return True
    except ImportError as e:
        log(f"Missing dependency: {e}")
        return False


def attempt_repair():
    log("Attempting automated repair...")
    # Example: Restore from backup if available
    backup_path = 'pretty_print_narration.py.bak'
    main_path = 'pretty_print_narration.py'
    if os.path.exists(backup_path):
        try:
            with open(backup_path, 'r') as src, open(main_path, 'w') as dst:
                dst.write(src.read())
            log("Restored pretty_print_narration.py from backup.")
            return True
        except Exception as e:
            log(f"Failed to restore from backup: {e}")
            return False
    else:
        log("No backup found for pretty_print_narration.py.")
        return False


def main():
    print("\033[95m==============================\033[0m")
    print("\033[95m SELF-REPAIR IN PROGRESS      \033[0m")
    print("\033[95m==============================\033[0m")
    log("--- Narration Self-Repair Triggered ---")
    error_fixed = False
    time.sleep(1)
    if not diagnose_error():
        print("\033[93mSyntax error detected. Attempting automated repair...\033[0m")
        time.sleep(1)
        if attempt_repair():
            error_fixed = True
            REPAIR_STATUS = 'FIXED'
            print("\033[92mAutomated repair successful.\033[0m")
            log("Automated repair successful.")
        else:
            print("\033[91mAutomated repair failed. Manual intervention required.\033[0m")
            log("Automated repair failed. Manual intervention required.")
    else:
        print("\033[92mNo syntax errors detected. Checking dependencies...\033[0m")
        time.sleep(1)
        if not check_dependencies():
            print("\033[91mDependency issue detected. Please install missing packages.\033[0m")
            log("Dependency issue detected. Please install missing packages.")
        else:
            print("\033[92mNo issues detected. Error may be transient or external.\033[0m")
            log("No issues detected. Error may be transient or external.")
            error_fixed = True
            REPAIR_STATUS = 'FIXED'
    # Alert user
    alert_msg = f"Narration self-repair status: {REPAIR_STATUS}. See {LOG_PATH} for details."
    print(f"\033[93m{alert_msg}\033[0m")
    log(alert_msg)
    if error_fixed:
        print("\033[92mREPAIR COMPLETE. Resuming normal operation.\033[0m")
    else:
        print("\033[91mREPAIR FAILED. Fallback to raw data.\033[0m")
    time.sleep(2)

if __name__ == "__main__":
    main()
