#!/usr/bin/env python3
"""
Interactive Configuration Manager for RICK Phoenix V2.
Allows non-coders to adjust system settings safely.
"""

import os
import re
import sys
from datetime import datetime

CHARTER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PhoenixV2/config/charter.py")
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs", "settings_history.log")

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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_change(setting, old_val, new_val):
    """Records the change to a persistent log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] UPDATE: {setting} changed from [{old_val}] to [{new_val}]\n"
    
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a") as f:
            f.write(log_entry)
        return True
    except Exception as e:
        print(f"⚠️  Log Error: {e}")
        return False

def read_charter():
    if not os.path.exists(CHARTER_PATH):
        print(f"Error: Could not find {CHARTER_PATH}")
        sys.exit(1)
    with open(CHARTER_PATH, 'r') as f:
        return f.read()

def update_charter(content, setting, new_value, comment=""):
    # Regex to find the setting assignment
    # Looks for: SETTING_NAME = value # comment
    pattern = fr"({setting}\s*=\s*)([^#\n]+)(.*)"
    
    match = re.search(pattern, content)
    if match:
        # Construct new line: SETTING = new_value # comment
        current_comment = match.group(3)
        if comment:
            new_line = f"{match.group(1)}{new_value} # {comment}"
        else:
            # Keep existing comment if no new one provided, or add one if missing
            new_line = f"{match.group(1)}{new_value}{current_comment}"
        
        new_content = content.replace(match.group(0), new_line)
        
        with open(CHARTER_PATH, 'w') as f:
            f.write(new_content)
        return True
    return False

def get_current_value(content, setting):
    pattern = fr"{setting}\s*=\s*([^#\n]+)"
    match = re.search(pattern, content)
    if match:
        return match.group(1).strip()
    return "Unknown"

def main():
    while True:
        clear_screen()
        content = read_charter()
        
        max_pos = get_current_value(content, "MAX_CONCURRENT_POSITIONS")
        wolf_conf = get_current_value(content, "WOLF_MIN_CONFIDENCE") # Note: This might be inside a getenv
        wolf_sharpe = get_current_value(content, "WOLF_MIN_TOP_SHARPE")
        
        # Handle the getenv case for WOLF_MIN_CONFIDENCE if strictly parsed
        # The file has: WOLF_MIN_CONFIDENCE = float(os.getenv('WOLF_MIN_CONFIDENCE', '0.60'))
        # We want to extract the default value '0.60'
        wolf_conf_match = re.search(r"WOLF_MIN_CONFIDENCE.*'([\d\.]+)'\)\)", content)
        if wolf_conf_match:
            wolf_conf = wolf_conf_match.group(1)

        print(f"{Colors.HEADER}{Colors.BOLD}" + "="*60 + f"{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}🎛️  RICK PHOENIX V2 - SETTINGS CONTROL PANEL{Colors.ENDC}")
        print(f"{Colors.BLUE}   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}" + "="*60 + f"{Colors.ENDC}")
        print("")
        print(f"{Colors.CYAN}   1. Max Concurrent Positions{Colors.ENDC}")
        print(f"      Current Value: {Colors.GREEN}{Colors.BOLD}{max_pos}{Colors.ENDC}")
        print("")
        print(f"{Colors.CYAN}   2. WolfPack Confidence Threshold{Colors.ENDC}")
        print(f"      Current Value: {Colors.GREEN}{Colors.BOLD}{wolf_conf}{Colors.ENDC}")
        print("")
        print(f"{Colors.CYAN}   3. WolfPack Min Sharpe Ratio{Colors.ENDC}")
        print(f"      Current Value: {Colors.GREEN}{Colors.BOLD}{wolf_sharpe}{Colors.ENDC}")
        print("")
        print(f"{Colors.HEADER}" + "-"*60 + f"{Colors.ENDC}")
        print(f"{Colors.WARNING}   4. Exit Control Panel{Colors.ENDC}")
        print(f"{Colors.HEADER}" + "="*60 + f"{Colors.ENDC}")
        
        choice = input(f"\n{Colors.BOLD}Select an option (1-4): {Colors.ENDC}")
        
        if choice == '1':
            new_val = input(f"\n{Colors.CYAN}Enter new Max Positions (e.g., 6, 12): {Colors.ENDC}")
            if new_val.isdigit():
                if update_charter(content, "MAX_CONCURRENT_POSITIONS", new_val, "User Adjusted via Menu"):
                    log_change("MAX_CONCURRENT_POSITIONS", max_pos, new_val)
                    print(f"\n{Colors.GREEN}✅ Updated & Logged successfully!{Colors.ENDC}")
                else:
                    print(f"\n{Colors.FAIL}❌ Failed to update.{Colors.ENDC}")
            else:
                print(f"\n{Colors.FAIL}❌ Invalid input. Must be a number.{Colors.ENDC}")
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

        elif choice == '2':
            new_val = input(f"\n{Colors.CYAN}Enter new Confidence (0.0 to 1.0, e.g., 0.60): {Colors.ENDC}")
            try:
                val = float(new_val)
                if 0 <= val <= 1.0:
                    # Special handling for the getenv line
                    # We replace the default value inside the getenv call
                    old_line_pattern = r"(WOLF_MIN_CONFIDENCE.*os\.getenv.*, ')([\d\.]+)('\)\))"
                    if re.search(old_line_pattern, content):
                        new_content = re.sub(old_line_pattern, f"\\g<1>{new_val}\\g<3>", content)
                        with open(CHARTER_PATH, 'w') as f:
                            f.write(new_content)
                        log_change("WOLF_MIN_CONFIDENCE", wolf_conf, new_val)
                        print(f"\n{Colors.GREEN}✅ Updated & Logged successfully!{Colors.ENDC}")
                    else:
                        print(f"\n{Colors.FAIL}❌ Could not find the configuration line pattern.{Colors.ENDC}")
                else:
                    print(f"\n{Colors.FAIL}❌ Value must be between 0.0 and 1.0{Colors.ENDC}")
            except ValueError:
                print(f"\n{Colors.FAIL}❌ Invalid number.{Colors.ENDC}")
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

        elif choice == '3':
            new_val = input(f"\n{Colors.CYAN}Enter new Min Sharpe Ratio (e.g., 0.5, 1.0): {Colors.ENDC}")
            try:
                float(new_val)
                if update_charter(content, "WOLF_MIN_TOP_SHARPE", new_val, "User Adjusted via Menu"):
                    log_change("WOLF_MIN_TOP_SHARPE", wolf_sharpe, new_val)
                    print(f"\n{Colors.GREEN}✅ Updated & Logged successfully!{Colors.ENDC}")
                else:
                    print(f"\n{Colors.FAIL}❌ Failed to update.{Colors.ENDC}")
            except ValueError:
                print(f"\n{Colors.FAIL}❌ Invalid number.{Colors.ENDC}")
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

        elif choice == '4':
            print(f"\n{Colors.WARNING}Exiting...{Colors.ENDC}")
            break

if __name__ == "__main__":
    main()
