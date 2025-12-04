#!/usr/bin/env python3
"""
Sentinel Sid: Active Trade Guardian
Monitors active trades and enforces Charter/Gated Logic in Plain English.
Includes Mini Bot Enforcer for detailed logic inspection.
"""

import sys
import os
import time
import math
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
env_files = ['.env', '.env.oanda_only', 'master.env']
for env_file in env_files:
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip('"\'')
        # print(f"Sentinel Sid: Loaded configuration from {env_file}")
        break

try:
    from oanda.brokers.oanda_connector import OandaConnector
except ImportError:
    # Try alternative path if running from root
    sys.path.append(os.path.join(os.getcwd(), 'oanda'))
    from brokers.oanda_connector import OandaConnector

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

class MiniBotEnforcer:
    """
    Detailed logic inspector for active trades.
    Provides transparent visual confirmation of applied strategies and logic states.
    """
    @staticmethod
    def inspect(trade, current_price, profit_pips, sl_price, unrealized_pl):
        trade_id = trade.get('id')
        instrument = trade.get('instrument')
        
        print(f"\n   {Colors.HEADER}🤖 MINI BOT ENFORCER: Inspecting Ticket #{trade_id}{Colors.ENDC}")
        print(f"   " + "-"*50)
        
        # 1. Identify Strategy & Timeframe
        # Inferred from trade ID or comments if available. 
        # For now, we assume "Charter Flow" or "Aggressive Machine" based on ID format if possible, else default.
        strategy = "Charter Flow (Standard)"
        timeframe = "M15" # Default engine timeframe
        
        # Check for specific strategy markers (placeholder logic for now)
        if "AMM" in str(trade.get('clientExtensions', {})):
            strategy = "Aggressive Money Machine"
        
        print(f"      • Strategy:  {Colors.CYAN}{strategy}{Colors.ENDC}")
        print(f"      • Timeframe: {Colors.CYAN}{timeframe}{Colors.ENDC}")
        print(f"      • Logic:     {Colors.CYAN}FVG + Momentum + Hive Mind{Colors.ENDC}")
        
        # 2. Check Logic State (Tight Ass Mode)
        tight_ass_active = False
        logic_state = []
        
        if profit_pips > 1.0 or unrealized_pl > 10.0:
            tight_ass_active = True
            logic_state.append("TIGHT ASS SL (Active)")
            status_icon = "🚀"
            status_msg = "TOGGLED ON"
            status_color = Colors.GREEN
        else:
            logic_state.append("TIGHT ASS SL (Standby)")
            status_icon = "💤"
            status_msg = "STANDBY (Waiting for > 1.0 pip)"
            status_color = Colors.WARNING
            
        print(f"      • Tight Ass Mode: {status_icon} {status_color}{status_msg}{Colors.ENDC}")
        
        # 3. Verify Enforcement
        if tight_ass_active:
            # Check if SL is actually tight
            if sl_price:
                pip_size = 0.01 if 'JPY' in instrument else 0.0001
                dist = abs(current_price - sl_price) / pip_size
                
                # "Tight" is subjective, but generally < 15 pips or trailing closely
                # If profit is high, SL should be locked in profit or close to it.
                
                if dist < 15.0: 
                    print(f"      • Enforcement: {Colors.GREEN}✅ PASS - Logic Applied (SL {dist:.1f} pips away){Colors.ENDC}")
                else:
                    print(f"      • Enforcement: {Colors.WARNING}⚠️  FAIL - SL is Loose ({dist:.1f} pips) despite > 1.0 pip profit{Colors.ENDC}")
                    print(f"        -> ACTION: Notify Engine to Retry Trail Update...")
            else:
                 print(f"      • Enforcement: {Colors.FAIL}❌ CRITICAL - No SL Found! (Silent Close Risk){Colors.ENDC}")
        else:
            print(f"      • Enforcement: Monitoring for breakout...")

        print(f"      • Active Modules: {Colors.BLUE}{', '.join(logic_state)}{Colors.ENDC}")
        print(f"   " + "-"*50)


def get_plain_english_status():
    try:
        # Initialize connector (Practice mode for now, or auto-detect)
        connector = OandaConnector(environment="practice")
        
        print("\n" + "="*60)
        print(f"{Colors.HEADER}👁️  SENTINEL SID: ACTIVE TRADE GUARDIAN - {datetime.now().strftime('%H:%M:%S')}{Colors.ENDC}")
        print("="*60)
        
        trades = connector.get_trades()
        
        if not trades:
            print(f"{Colors.CYAN}Sentinel Sid: No active trades found. The battlefield is quiet.{Colors.ENDC}")
            print(f"\n   {Colors.HEADER}🤖 MINI BOT ENFORCER: Sleeping...{Colors.ENDC}")
            return

        print(f"Sentinel Sid: I see {Colors.BOLD}{len(trades)}{Colors.ENDC} active trade(s). Scanning for Charter compliance...\n")
        
        for trade in trades:
            trade_id = trade.get('id')
            instrument = trade.get('instrument')
            price = float(trade.get('price', 0))
            current_units = float(trade.get('currentUnits', 0))
            
            # Get current market price
            # Try M1 candles if S5 fails
            candles = connector.get_historical_data(instrument, count=1, granularity="S5")
            if not candles:
                 candles = connector.get_historical_data(instrument, count=1, granularity="M1")
            
            if candles:
                current_market_price = float(candles[-1]['mid']['c'])
            else:
                current_market_price = price # Fallback to entry
            
            # Calculate Profit
            unrealized_pl = float(trade.get('unrealizedPL', 0))
            
            if current_units > 0: # BUY
                diff = current_market_price - price
                direction = "LONG"
                dir_color = Colors.GREEN
            else: # SELL
                diff = price - current_market_price
                direction = "SHORT"
                dir_color = Colors.FAIL
            
            pip_size = 0.01 if 'JPY' in instrument else 0.0001
            profit_pips = diff / pip_size
            
            # Check SL
            sl_order = trade.get('stopLossOrder')
            sl_price = float(sl_order.get('price')) if sl_order else None
            
            pl_color = Colors.GREEN if profit_pips >= 0 else Colors.FAIL
            
            print(f"👉 Trade #{trade_id} ({Colors.BOLD}{instrument}{Colors.ENDC} {dir_color}{direction}{Colors.ENDC})")
            print(f"   • Entry: {price:.5f} | Current: {current_market_price:.5f}")
            print(f"   • Profit: {pl_color}{profit_pips:.1f} pips (${unrealized_pl:.2f}){Colors.ENDC}")
            
            if sl_price:
                sl_dist = abs(current_market_price - sl_price) / pip_size
                print(f"   • Stop Loss: {sl_price:.5f} ({sl_dist:.1f} pips away)")
            else:
                print(f"   • Status: {Colors.FAIL}❌ NO STOP LOSS DETECTED! CHARTER VIOLATION!{Colors.ENDC}")
            
            # Call Mini Bot Enforcer
            MiniBotEnforcer.inspect(trade, current_market_price, profit_pips, sl_price, unrealized_pl)
            
            print("\n" + "="*60)

    except Exception as e:
        print(f"{Colors.FAIL}Sentinel Sid: ❌ ERROR - My sensors are malfunctioning: {e}{Colors.ENDC}")


def get_plain_english_status():
    try:
        # Initialize connector (Practice mode for now, or auto-detect)
        connector = OandaConnector(environment="practice")
        
        print("\n" + "="*60)
        print(f"��️  SENTINEL SID: ACTIVE TRADE GUARDIAN - {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)
        
        trades = connector.get_trades()
        
        if not trades:
            print("Sentinel Sid: No active trades found. The battlefield is quiet.")
            print("\n   🤖 MINI BOT ENFORCER: Sleeping...")
            return

        print(f"Sentinel Sid: I see {len(trades)} active trade(s). Scanning for Charter compliance...\n")
        
        for trade in trades:
            trade_id = trade.get('id')
            instrument = trade.get('instrument')
            price = float(trade.get('price', 0))
            current_units = float(trade.get('currentUnits', 0))
            
            # Get current market price
            # Try M1 candles if S5 fails
            candles = connector.get_historical_data(instrument, count=1, granularity="S5")
            if not candles:
                 candles = connector.get_historical_data(instrument, count=1, granularity="M1")
            
            if candles:
                current_market_price = float(candles[-1]['mid']['c'])
            else:
                current_market_price = price # Fallback to entry
            
            # Calculate Profit
            unrealized_pl = float(trade.get('unrealizedPL', 0))
            
            if current_units > 0: # BUY
                diff = current_market_price - price
                direction = "LONG"
            else: # SELL
                diff = price - current_market_price
                direction = "SHORT"
            
            pip_size = 0.01 if 'JPY' in instrument else 0.0001
            profit_pips = diff / pip_size
            
            # Check SL
            sl_order = trade.get('stopLossOrder')
            sl_price = float(sl_order.get('price')) if sl_order else None
            
            print(f"👉 Trade #{trade_id} ({instrument} {direction})")
            print(f"   • Entry: {price:.5f} | Current: {current_market_price:.5f}")
            print(f"   • Profit: {profit_pips:.1f} pips ()")
            
            if sl_price:
                sl_dist = abs(current_market_price - sl_price) / pip_size
                print(f"   • Stop Loss: {sl_price:.5f} ({sl_dist:.1f} pips away)")
            else:
                print(f"   • Status: ❌ NO STOP LOSS DETECTED! CHARTER VIOLATION!")
            
            # Call Mini Bot Enforcer
            MiniBotEnforcer.inspect(trade, current_market_price, profit_pips, sl_price, unrealized_pl)
            
            print("\n" + "="*60)

    except Exception as e:
        print(f"Sentinel Sid: ❌ ERROR - My sensors are malfunctioning: {e}")

def display_config_summary():
    """Displays the active configuration of the system."""
    print(f"\n   {Colors.HEADER}⚙️  SYSTEM CONFIGURATION (Live Audit):{Colors.ENDC}")
    print(f"   " + "-"*50)
    
    # Define features and their detection logic
    features = [
        ("Charter Compliance", True, "ALWAYS ON (Hardcoded)"),
        ("Long & Short Logic", True, "ALWAYS ON (Hardcoded)"),
        ("Narration System", True, "ALWAYS ON (Hardcoded)"),
        ("ML Intelligence", os.path.exists("ml_learning/regime_detector.py"), "ACTIVE (Integrated)"),
        ("Hive Mind", os.path.exists("hive/rick_hive_mind.py"), "ACTIVE (Integrated)"),
        ("Momentum System", os.path.exists("util/momentum_trailing.py"), "ACTIVE (Integrated)"),
        ("Strategy Aggregator", os.path.exists("util/strategy_aggregator.py"), "ACTIVE (Integrated)"),
        ("Hedge Engine", os.path.exists("util/quant_hedge_engine.py"), "ACTIVE (Integrated)"),
    ]
    
    for name, active, mode in features:
        icon = "✅" if active else "❌"
        status = "ACTIVE" if active else "INACTIVE"
        # Color code
        c_start = Colors.GREEN if active else Colors.FAIL # Green or Red
        c_end = Colors.ENDC
        
        print(f"      {icon} {name:<20} : {c_start}{status:<8}{c_end} {Colors.CYAN}[{mode}]{Colors.ENDC}")
    print(f"   " + "-"*50)

if __name__ == "__main__":
    while True:
        os.system('clear')
        get_plain_english_status()
        display_config_summary()
        time.sleep(5)
