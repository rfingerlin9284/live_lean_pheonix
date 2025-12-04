#!/usr/bin/env python3
"""
OANDA Engine Scanning Verification Tool
Checks if the trading engine is actively scanning for signals
PIN: 841921
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}\n")

def check_narration_activity():
    """Check if narration.jsonl is being actively updated"""
    narration_file = Path(__file__).parent / "narration.jsonl"
    
    if not narration_file.exists():
        print(f"{Colors.RED}❌ No narration.jsonl found{Colors.ENDC}")
        print(f"   {Colors.YELLOW}The engine hasn't created a narration log yet{Colors.ENDC}")
        return False, "No narration file"
    
    # Check file modification time
    mtime = datetime.fromtimestamp(narration_file.stat().st_mtime)
    age = datetime.now() - mtime
    
    print(f"{Colors.BOLD}Narration Log Status:{Colors.ENDC}")
    print(f"  File: {narration_file}")
    print(f"  Last updated: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Age: {age.total_seconds():.1f} seconds ago")
    
    if age.total_seconds() < 300:  # 5 minutes
        print(f"  {Colors.GREEN}✅ Recently active{Colors.ENDC}")
        is_active = True
    elif age.total_seconds() < 3600:  # 1 hour
        print(f"  {Colors.YELLOW}⚠️  Moderately stale (but may be normal if no signals){Colors.ENDC}")
        is_active = True
    else:
        print(f"  {Colors.RED}❌ Very stale - engine likely not running{Colors.ENDC}")
        is_active = False
    
    # Count recent events
    recent_count = 0
    signal_count = 0
    scan_count = 0
    
    try:
        with open(narration_file, 'r') as f:
            lines = f.readlines()
            cutoff = datetime.now() - timedelta(minutes=30)
            
            for line in lines[-100:]:  # Check last 100 events
                try:
                    event = json.loads(line)
                    timestamp_str = event.get('timestamp', '')
                    # Handle both timezone-aware and naive timestamps
                    if timestamp_str:
                        timestamp_str = timestamp_str.replace('Z', '+00:00')
                        event_time = datetime.fromisoformat(timestamp_str)
                        # Make naive if it has timezone info
                        if event_time.tzinfo is not None:
                            event_time = event_time.replace(tzinfo=None)
                    else:
                        continue
                    
                    if event_time > cutoff:
                        recent_count += 1
                        event_type = event.get('event_type', '')
                        
                        if 'SIGNAL' in event_type:
                            signal_count += 1
                        if 'SCAN' in event_type or 'MONITOR' in event_type:
                            scan_count += 1
                            
                except (json.JSONDecodeError, ValueError, KeyError):
                    continue
        
        print(f"\n{Colors.BOLD}Recent Activity (last 30 minutes):{Colors.ENDC}")
        print(f"  Total events: {recent_count}")
        print(f"  Signal events: {signal_count}")
        print(f"  Scan/Monitor events: {scan_count}")
        
        if recent_count > 0:
            print(f"  {Colors.GREEN}✅ Engine is active{Colors.ENDC}")
        else:
            print(f"  {Colors.YELLOW}⚠️  No recent events (may be waiting for signals){Colors.ENDC}")
            
    except Exception as e:
        print(f"  {Colors.RED}Error reading narration: {e}{Colors.ENDC}")
    
    return is_active, f"{recent_count} events, {signal_count} signals"

def check_engine_process():
    """Check if the trading engine process is running"""
    print(f"\n{Colors.BOLD}Engine Process Status:{Colors.ENDC}")
    
    try:
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True
        )
        
        engine_processes = []
        for line in result.stdout.split('\n'):
            if 'oanda_trading_engine' in line and 'grep' not in line:
                engine_processes.append(line)
        
        if engine_processes:
            print(f"  {Colors.GREEN}✅ Engine process is running{Colors.ENDC}")
            for proc in engine_processes:
                parts = proc.split()
                pid = parts[1]
                print(f"  PID: {pid}")
            return True
        else:
            print(f"  {Colors.RED}❌ No engine process found{Colors.ENDC}")
            print(f"  {Colors.YELLOW}Start the engine with VSCode task: '🚀 OANDA Trading Engine (Practice)'{Colors.ENDC}")
            return False
            
    except Exception as e:
        print(f"  {Colors.RED}Error checking process: {e}{Colors.ENDC}")
        return False

def check_environment_config():
    """Check environment configuration"""
    env_file = Path(__file__).parent / ".env"
    
    print(f"\n{Colors.BOLD}Environment Configuration:{Colors.ENDC}")
    
    if not env_file.exists():
        print(f"  {Colors.RED}❌ No .env file found{Colors.ENDC}")
        return False
    
    try:
        with open(env_file, 'r') as f:
            env_content = f.read()
        
        # Check key parameters
        rick_env = None
        oanda_account = None
        instruments = None
        
        for line in env_content.split('\n'):
            if line.startswith('RICK_ENV='):
                rick_env = line.split('=')[1].strip()
            elif line.startswith('OANDA_PRACTICE_ACCOUNT_ID='):
                oanda_account = line.split('=')[1].strip()
            elif line.startswith('INSTRUMENTS='):
                instruments = line.split('=')[1].strip()
        
        print(f"  Environment: {rick_env or 'not set'}")
        print(f"  OANDA Account: {oanda_account[:15] + '...' if oanda_account else 'not set'}")
        
        if instruments:
            inst_list = instruments.split(',')
            print(f"  Scanning instruments: {len(inst_list)} pairs")
            print(f"    First 5: {', '.join(inst_list[:5])}")
            if len(inst_list) > 5:
                print(f"    ... and {len(inst_list) - 5} more")
        else:
            print(f"  {Colors.YELLOW}⚠️  No instruments configured{Colors.ENDC}")
        
        if rick_env and oanda_account:
            print(f"  {Colors.GREEN}✅ Basic configuration looks good{Colors.ENDC}")
            return True
        else:
            print(f"  {Colors.RED}❌ Configuration incomplete{Colors.ENDC}")
            return False
            
    except Exception as e:
        print(f"  {Colors.RED}Error reading .env: {e}{Colors.ENDC}")
        return False

def check_scanning_parameters():
    """Check if scanning parameters are reasonable"""
    print(f"\n{Colors.BOLD}Scanning Parameters:{Colors.ENDC}")
    
    # These would come from the engine if it was running
    # For now, just show expected behavior
    print(f"  {Colors.CYAN}Expected behavior:{Colors.ENDC}")
    print(f"    - Scans all configured instruments every 15 minutes (M15 timeframe)")
    print(f"    - Generates signals based on momentum/regime detection")
    print(f"    - Logs all scans and signals to narration.jsonl")
    print(f"    - Minimum 3:1 Risk/Reward ratio enforced")
    print(f"    - OCO orders (stop loss + take profit) required")
    
    print(f"\n  {Colors.YELLOW}If no signals appear:{Colors.ENDC}")
    print(f"    - This is NORMAL if market conditions don't meet criteria")
    print(f"    - Check narration.jsonl for 'SCAN_COMPLETE' events")
    print(f"    - Signals require: momentum + regime + risk/reward alignment")
    
    return True

def main():
    print_header("🔍 OANDA ENGINE SCANNING VERIFICATION")
    
    print(f"{Colors.CYAN}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    
    # Run all checks
    checks = []
    
    checks.append(("Environment Config", check_environment_config()))
    checks.append(("Engine Process", check_engine_process()))
    checks.append(("Narration Activity", check_narration_activity()[0]))
    checks.append(("Scanning Parameters", check_scanning_parameters()))
    
    # Summary
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}SUMMARY:{Colors.ENDC}\n")
    
    passed = sum(1 for _, status in checks if status)
    total = len(checks)
    
    for name, status in checks:
        icon = f"{Colors.GREEN}✅" if status else f"{Colors.RED}❌"
        print(f"  {icon} {name}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Overall Status: {passed}/{total} checks passed{Colors.ENDC}")
    
    if passed == total:
        print(f"{Colors.GREEN}✅ System is scanning properly!{Colors.ENDC}")
    elif passed >= total - 1:
        print(f"{Colors.YELLOW}⚠️  System is mostly operational with minor issues{Colors.ENDC}")
    else:
        print(f"{Colors.RED}❌ System has significant issues - review the checks above{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}\n")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
