#!/usr/bin/env python3
"""
RICK System Status Checker - Human-Readable Visual Display
PIN: 841921
Shows at a glance if trading bot is running and managing positions
"""

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

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

def print_header():
    print("\n" + "="*80)
    print(f"{Colors.HEADER}{Colors.BOLD}🤖 RICK TRADING SYSTEM - STATUS CHECK{Colors.ENDC}")
    print(f"{Colors.BLUE}   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print("="*80 + "\n")

def check_engine_running():
    """Check if oanda_trading_engine.py is running"""
    result = subprocess.run(
        ["pgrep", "-af", "oanda_trading_engine.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        pid = result.stdout.split()[0] if result.stdout else "Unknown"
        print(f"{Colors.GREEN}✅ ENGINE STATUS: RUNNING{Colors.ENDC}")
        print(f"   Process ID: {Colors.BOLD}{pid}{Colors.ENDC}")
        print(f"   Command: {Colors.CYAN}oanda_trading_engine.py{Colors.ENDC}")
        return True
    else:
        print(f"{Colors.FAIL}❌ ENGINE STATUS: STOPPED{Colors.ENDC}")
        print(f"   The trading bot is NOT running")
        print(f"   To start: {Colors.YELLOW}./start_with_integrity.sh{Colors.ENDC}")
        return False

def check_active_positions():
    """Check for active positions via OANDA API"""
    try:
        # Load environment variables
        env_file = Path(".env.oanda_only")
        if not env_file.exists():
            print(f"\n{YELLOW}⚠️  POSITIONS: Cannot check (no credentials){RESET}")
            return
        
        # Try to check via Python
        result = subprocess.run([
            "python3", "-c",
            """
import os, requests, json
from pathlib import Path

# Load env
env_file = Path('.env.oanda_only')
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            os.environ[key.strip()] = value.strip()

account_id = os.environ.get('OANDA_PRACTICE_ACCOUNT_ID', '')
token = os.environ.get('OANDA_PRACTICE_TOKEN', '')

if not account_id or not token:
    print('NO_CREDS')
    exit()

try:
    api = 'https://api-fxpractice.oanda.com'
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(f'{api}/v3/accounts/{account_id}/openPositions', headers=headers, timeout=10)
    
    if r.status_code == 200:
        positions = r.json().get('positions', [])
        print(f'POSITIONS:{len(positions)}')
        for p in positions:
            instrument = p.get('instrument', '?')
            units = p.get('long', {}).get('units', '0')
            if units == '0':
                units = p.get('short', {}).get('units', '0')
            unrealized_pl = p.get('unrealizedPL', '0')
            print(f'{instrument}|{units}|{unrealized_pl}')
    else:
        print(f'API_ERROR:{r.status_code}')
except Exception as e:
    print(f'ERROR:{str(e)}')
"""
        ], capture_output=True, text=True, timeout=15)
        
        output = result.stdout.strip()
        
        if 'NO_CREDS' in output:
            print(f"\n{Colors.WARNING}⚠️  POSITIONS: Cannot check (credentials not loaded){Colors.ENDC}")
        elif 'ERROR:' in output or 'API_ERROR:' in output:
            error_msg = output.split(':', 1)[1] if ':' in output else output
            print(f"\n{Colors.WARNING}⚠️  POSITIONS: API Error - {error_msg}{Colors.ENDC}")
        elif 'POSITIONS:' in output:
            lines = output.split('\n')
            pos_count = lines[0].split(':')[1]
            
            if pos_count == '0':
                print(f"\n{Colors.CYAN}📊 POSITIONS: 0 (No active trades){Colors.ENDC}")
                print(f"   System is running but no positions open")
            else:
                print(f"\n{Colors.GREEN}📊 POSITIONS: {pos_count} Active Trade(s){Colors.ENDC}")
                for line in lines[1:]:
                    if '|' in line:
                        parts = line.split('|')
                        if len(parts) == 3:
                            instrument, units, pnl = parts
                            pnl_float = float(pnl)
                            pnl_color = Colors.GREEN if pnl_float >= 0 else Colors.FAIL
                            
                            # Format P&L: ($123.45) for negative, +$123.45 for positive
                            if pnl_float < 0:
                                pnl_display = f"(${abs(pnl_float):.2f})"
                            else:
                                pnl_display = f"+${pnl_float:.2f}"
                            
                            # Format units: (32,900) for negative (short), 32,900 for positive (long)
                            units_float = float(units)
                            if units_float < 0:
                                units_display = f"({abs(units_float):,.0f})"
                            else:
                                units_display = f"{units_float:,.0f}"
                            
                            print(f"   • {Colors.BOLD}{instrument}{Colors.ENDC}: {units_display} units | P&L: {pnl_color}{pnl_display}{Colors.ENDC}")
        else:
            print(f"\n{Colors.WARNING}⚠️  POSITIONS: Unknown status{Colors.ENDC}")
            
    except subprocess.TimeoutExpired:
        print(f"\n{Colors.WARNING}⚠️  POSITIONS: Timeout checking OANDA API{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.WARNING}⚠️  POSITIONS: Error - {str(e)}{Colors.ENDC}")

def check_logs_active():
    """Check if narration logging is happening"""
    narration_log = Path("logs/narration.jsonl")
    engine_log = Path("logs/engine.log")
    
    print(f"\n{Colors.HEADER}📝 LOGGING STATUS:{Colors.ENDC}")
    
    if narration_log.exists():
        size = narration_log.stat().st_size
        mtime = datetime.fromtimestamp(narration_log.stat().st_mtime)
        age_minutes = (datetime.now() - mtime).total_seconds() / 60
        
        if age_minutes < 5:
            print(f"   {Colors.GREEN}✅ Narration Log: Active (updated {age_minutes:.0f}m ago){Colors.ENDC}")
        elif size > 0:
            print(f"   {Colors.WARNING}⚠️  Narration Log: Stale (last update {age_minutes:.0f}m ago){Colors.ENDC}")
        else:
            print(f"   {Colors.WARNING}⚠️  Narration Log: Empty{Colors.ENDC}")
    else:
        print(f"   {Colors.FAIL}❌ Narration Log: Not found{Colors.ENDC}")
    
    if engine_log.exists():
        size = engine_log.stat().st_size
        mtime = datetime.fromtimestamp(engine_log.stat().st_mtime)
        age_minutes = (datetime.now() - mtime).total_seconds() / 60
        
        if age_minutes < 5:
            print(f"   {Colors.GREEN}✅ Engine Log: Active (updated {age_minutes:.0f}m ago){Colors.ENDC}")
        elif size > 0:
            print(f"   {Colors.WARNING}⚠️  Engine Log: Stale (last update {age_minutes:.0f}m ago){Colors.ENDC}")
        else:
            print(f"   {Colors.WARNING}⚠️  Engine Log: Empty{Colors.ENDC}")
    else:
        print(f"   {Colors.FAIL}❌ Engine Log: Not found{Colors.ENDC}")

def check_safety_systems():
    """Check if safety systems are present"""
    print(f"\n{Colors.HEADER}🛡️  SAFETY SYSTEMS:{Colors.ENDC}")
    
    systems = [
        ("Position Police", "oanda_trading_engine.py", "_rbz_force_min_notional_position_police"),
        ("Runtime Guard", "runtime_guard/sitecustomize.py", "POSITION_POLICE_STUB_INJECTED"),
        ("Integrity Check", "check_integrity.py", "Charter constants verified"),
        ("3h Monitor", "monitor_3h_checkpoint.py", "CHECKPOINT_3H_ALERT"),
    ]
    
    for name, filepath, marker in systems:
        file_path = Path(filepath)
        if file_path.exists():
            if marker in file_path.read_text():
                print(f"   {Colors.GREEN}✅ {name}: Present{Colors.ENDC}")
            else:
                print(f"   {Colors.WARNING}⚠️  {name}: File exists but marker not found{Colors.ENDC}")
        else:
            print(f"   {Colors.FAIL}❌ {name}: File not found{Colors.ENDC}")

def print_quick_actions():
    """Show quick action commands"""
    print(f"\n{Colors.HEADER}🔧 QUICK ACTIONS:{Colors.ENDC}")
    print(f"\n   {Colors.BLUE}Start Engine:{Colors.ENDC}")
    print(f"   ./start_with_integrity.sh")
    print(f"\n   {Colors.BLUE}Stop Engine:{Colors.ENDC}")
    print(f"   pkill -f oanda_trading_engine.py")
    print(f"\n   {Colors.BLUE}Watch Live Activity:{Colors.ENDC}")
    print(f"   tail -f logs/narration.jsonl")
    print(f"\n   {Colors.BLUE}Check Positions (OANDA):{Colors.ENDC}")
    print(f"   python3 check_system_status.py --positions")
    print(f"\n   {Colors.BLUE}Full Status:{Colors.ENDC}")
    print(f"   python3 check_system_status.py")
    print()

def main():
    print_header()
    
    # Check if we're just checking positions
    if '--positions' in sys.argv:
        check_active_positions()
        return
    
    # Full status check
    engine_running = check_engine_running()
    check_active_positions()
    check_logs_active()
    check_safety_systems()
    
    # Overall verdict
    print("\n" + "="*80)
    if engine_running:
        print(f"{Colors.BOLD}{Colors.GREEN}🟢 OVERALL STATUS: SYSTEM IS RUNNING{Colors.ENDC}")
        print(f"   The trading bot is active and managing positions")
    else:
        print(f"{Colors.BOLD}{Colors.FAIL}🔴 OVERALL STATUS: SYSTEM IS STOPPED{Colors.ENDC}")
        print(f"   The trading bot is NOT running - no trades being executed")
    print("="*80)
    
    print_quick_actions()

if __name__ == "__main__":
    main()
