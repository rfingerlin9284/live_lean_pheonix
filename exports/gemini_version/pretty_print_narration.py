#!/usr/bin/env python3
"""
The Voice: RICK's Inner Monologue
Translates raw JSON logs into Plain English narration.
Clean, color-coded, human-readable output with alternating backgrounds.
"""
import sys
import json
import time
from datetime import datetime

class Colors:
    # Bright colors for readability
    HEADER = '\033[95m'      # Magenta
    BLUE = '\033[94m'        # Blue
    CYAN = '\033[96m'        # Cyan
    GREEN = '\033[92m'       # Green (success/profit)
    YELLOW = '\033[93m'      # Yellow (warning)
    RED = '\033[91m'         # Red (error/loss)
    WHITE = '\033[97m'       # White
    GRAY = '\033[90m'        # Gray (timestamps)
    
    # Text styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    # Background colors for alternating rows
    BG_DARK = '\033[48;5;236m'    # Dark gray background
    BG_LIGHT = '\033[48;5;238m'   # Slightly lighter gray
    BG_GREEN = '\033[48;5;22m'    # Dark green for wins
    BG_RED = '\033[48;5;52m'      # Dark red for losses
    BG_BLUE = '\033[48;5;17m'     # Dark blue for signals
    BG_YELLOW = '\033[48;5;58m'   # Dark yellow for warnings

# Global counter for alternating colors
message_count = 0

def format_timestamp(ts_str):
    try:
        dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        return dt.strftime('%H:%M:%S')
    except:
        return ts_str[:8] if ts_str else "??:??:??"

def format_money(amount):
    """Format money with color (green for profit, red for loss)"""
    try:
        val = float(amount)
        if val > 0:
            return f"{Colors.GREEN}{Colors.BOLD}+${val:,.2f}{Colors.RESET}"
        elif val < 0:
            return f"{Colors.RED}{Colors.BOLD}-${abs(val):,.2f}{Colors.RESET}"
        else:
            return f"${val:,.2f}"
    except:
        return str(amount)

def format_pips(pips):
    """Format pips with color"""
    try:
        val = float(pips)
        if val > 0:
            return f"{Colors.GREEN}+{val:.1f} pips{Colors.RESET}"
        elif val < 0:
            return f"{Colors.RED}{val:.1f} pips{Colors.RESET}"
        else:
            return f"{val:.1f} pips"
    except:
        return str(pips)

def format_percent(pct):
    """Format percentage"""
    try:
        val = float(pct) * 100 if float(pct) <= 1 else float(pct)
        return f"{val:.0f}%"
    except:
        return str(pct)

def parse_market_insights(msg):
    """Parse the market insights message into readable lines"""
    if not msg:
        return []
    
    # Split by comma and clean up each pair
    parts = msg.split(',')
    results = []
    for part in parts:
        part = part.strip()
        if ':' in part:
            pair_info = part.split(':')
            if len(pair_info) >= 2:
                pair = pair_info[0].strip()
                status = ':'.join(pair_info[1:]).strip()
                # Color code based on status
                if 'BULLISH' in status.upper():
                    color = Colors.GREEN
                elif 'BEARISH' in status.upper():
                    color = Colors.RED
                else:
                    color = Colors.YELLOW
                results.append(f"  {Colors.CYAN}{pair:<10}{Colors.RESET} {color}{status}{Colors.RESET}")
    return results

def translate_to_plain_english(event_type, details, symbol):
    """
    Converts technical event data into human-readable sentences.
    Returns (icon, bg_color, text_color, narrative, extra_lines)
    extra_lines is a list of additional lines to print
    """
    d = details
    extra_lines = []
    
    # ══════════════════════════════════════════════════════════════════
    # STARTUP & SYSTEM EVENTS
    # ══════════════════════════════════════════════════════════════════
    if event_type == "ENGINE_START":
        env = d.get('environment', 'unknown').upper()
        bg = Colors.BG_BLUE if env == "PRACTICE" else Colors.BG_RED
        return "🚀", bg, Colors.CYAN, f"Engine starting in {Colors.BOLD}{env}{Colors.RESET} mode", extra_lines
    
    if event_type == "HEARTBEAT":
        msg = d.get('message', 'Scanning markets...')
        positions = d.get('open_positions', 0)
        status = d.get('status', 'SCANNING')
        
        # Parse out the market insights
        msg_clean = msg.replace('Scanning...', '').strip()
        if msg_clean:
            extra_lines = parse_market_insights(msg_clean)
        
        return "💓", Colors.BG_DARK, Colors.GRAY, f"Status: {status} | {positions} open positions", extra_lines

    if event_type == "SYSTEM_HEALTH":
        status = d.get('status', 'unknown')
        bg = Colors.BG_GREEN if status == 'healthy' else Colors.BG_YELLOW
        return "🏥", bg, Colors.GREEN if status == 'healthy' else Colors.YELLOW, f"System health: {status.upper()}", extra_lines

    # ══════════════════════════════════════════════════════════════════
    # MARKET ANALYSIS & SIGNALS
    # ══════════════════════════════════════════════════════════════════
    if event_type == "TRADE_SIGNAL":
        direction = d.get('direction', '?')
        entry = d.get('entry', 0)
        sl = d.get('stop_loss', 0)
        tp = d.get('take_profit', 0)
        rr = d.get('rr_ratio', 0)
        notional = d.get('notional', 0)
        units = d.get('units', 0)
        
        dir_color = Colors.GREEN if direction == "BUY" else Colors.RED
        extra_lines = [
            f"  ├─ Entry Price:  {Colors.WHITE}{entry:.5f}{Colors.RESET}",
            f"  ├─ Stop Loss:    {Colors.RED}{sl:.5f}{Colors.RESET}",
            f"  ├─ Take Profit:  {Colors.GREEN}{tp:.5f}{Colors.RESET}",
            f"  ├─ Risk:Reward:  {Colors.YELLOW}{rr:.1f}:1{Colors.RESET}",
            f"  ├─ Units:        {Colors.WHITE}{abs(units):,}{Colors.RESET}",
            f"  └─ Notional:     {Colors.CYAN}${notional:,.0f}{Colors.RESET}",
        ]
        return "📊", Colors.BG_BLUE, Colors.BLUE, f"SIGNAL: {dir_color}{Colors.BOLD}{direction}{Colors.RESET} {Colors.CYAN}{Colors.BOLD}{symbol}{Colors.RESET}", extra_lines

    if event_type == "HIVE_ANALYSIS":
        consensus = d.get('consensus', '?')
        confidence = d.get('confidence', 0)
        profit_atr = d.get('profit_atr', 0)
        order_id = d.get('order_id', '?')
        conf_pct = format_percent(confidence)
        extra_lines = [
            f"  ├─ Consensus:   {Colors.HEADER}{consensus}{Colors.RESET}",
            f"  ├─ Confidence:  {Colors.YELLOW}{conf_pct}{Colors.RESET}",
            f"  └─ Profit ATR:  {Colors.GREEN}{profit_atr:.2f}x{Colors.RESET}",
        ]
        return "🐝", Colors.BG_DARK, Colors.HEADER, f"HIVE MIND ANALYSIS for {symbol}", extra_lines

    if event_type == "MOMENTUM_DETECTED":
        strength = d.get('momentum_strength', 0)
        profit_atr = d.get('profit_atr', 0)
        order_id = d.get('order_id', '?')
        extra_lines = [
            f"  ├─ Strength:   {Colors.GREEN}{strength:.1f}x{Colors.RESET}",
            f"  └─ Profit ATR: {Colors.GREEN}{profit_atr:.2f}x{Colors.RESET}",
        ]
        return "🔥", Colors.BG_GREEN, Colors.GREEN, f"MOMENTUM DETECTED on {symbol}!", extra_lines

    if event_type == "ML_SIGNAL_APPROVED":
        strength = format_percent(d.get('strength', 0))
        regime = d.get('regime', 'unknown')
        return "🤖", Colors.BG_GREEN, Colors.GREEN, f"AI APPROVED | Market: {regime} | Confidence: {strength}", extra_lines

    if event_type == "ML_SIGNAL_REJECTED":
        reason = d.get('reason', 'unknown')
        return "🤖", Colors.BG_YELLOW, Colors.YELLOW, f"AI REJECTED | Reason: {reason}", extra_lines

    # ══════════════════════════════════════════════════════════════════
    # TRADE EXECUTION
    # ══════════════════════════════════════════════════════════════════
    if event_type == "TRADE_OPENED":
        direction = d.get('direction', '?')
        entry = d.get('entry_price', 0)
        sl = d.get('stop_loss', 0)
        tp = d.get('take_profit', 0)
        size = d.get('size', 0)
        notional = d.get('notional', 0)
        rr = d.get('rr_ratio', 0)
        order_id = d.get('order_id', '?')
        trade_id = d.get('trade_id', '?')
        
        dir_color = Colors.GREEN if direction == "BUY" else Colors.RED
        extra_lines = [
            f"  ├─ Ticket:      {Colors.WHITE}#{order_id}{Colors.RESET}",
            f"  ├─ Entry:       {Colors.WHITE}{entry:.5f}{Colors.RESET}",
            f"  ├─ Stop Loss:   {Colors.RED}{sl:.5f}{Colors.RESET}",
            f"  ├─ Take Profit: {Colors.GREEN}{tp:.5f}{Colors.RESET}",
            f"  ├─ Units:       {Colors.WHITE}{size:,}{Colors.RESET}",
            f"  ├─ Notional:    {Colors.CYAN}${notional:,.0f}{Colors.RESET}",
            f"  └─ R:R Ratio:   {Colors.YELLOW}{rr:.1f}:1{Colors.RESET}",
        ]
        return "✅", Colors.BG_GREEN, Colors.GREEN, f"TRADE OPENED: {dir_color}{Colors.BOLD}{direction}{Colors.RESET} {Colors.CYAN}{Colors.BOLD}{symbol}{Colors.RESET}", extra_lines

    if event_type == "TRADE_CLOSED" or event_type == "TRADE_CLOSED_DETECTED":
        pnl = d.get('pnl', d.get('realized_pl', 0))
        outcome = d.get('outcome', 'unknown')
        order_id = d.get('order_id', '?')
        trade_id = d.get('trade_id', '?')
        age = d.get('age_seconds', 0)
        
        is_win = outcome == 'win' or (isinstance(pnl, (int, float)) and pnl > 0)
        bg = Colors.BG_GREEN if is_win else Colors.BG_RED
        color = Colors.GREEN if is_win else Colors.RED
        result_text = "WINNER!" if is_win else "LOSS"
        
        extra_lines = [
            f"  ├─ Ticket:   {Colors.WHITE}#{order_id}{Colors.RESET}",
            f"  ├─ P&L:      {format_money(pnl)}",
            f"  └─ Result:   {color}{Colors.BOLD}{result_text}{Colors.RESET}",
        ]
        return "💰" if is_win else "📉", bg, color, f"TRADE CLOSED: {symbol}", extra_lines

    if event_type == "ORDER_FAILED":
        error = d.get('error', 'unknown')
        direction = d.get('direction', '?')
        extra_lines = [
            f"  └─ Error: {Colors.RED}{error}{Colors.RESET}",
        ]
        return "❌", Colors.BG_RED, Colors.RED, f"ORDER FAILED: {symbol} {direction}", extra_lines

    # ══════════════════════════════════════════════════════════════════
    # TRAILING STOP & RISK MANAGEMENT
    # ══════════════════════════════════════════════════════════════════
    if event_type == "TP_CANCEL_ATTEMPT":
        trigger = d.get('trigger_source', [])
        profit_atr = d.get('profit_atr', 0)
        order_id = d.get('order_id', '?')
        cancel_resp = d.get('cancel_response', None)
        trigger_str = ' + '.join(trigger) if trigger else 'Auto'
        extra_lines = [
            f"  ├─ Trigger:    {Colors.YELLOW}{trigger_str}{Colors.RESET}",
            f"  ├─ Profit ATR: {Colors.GREEN}{profit_atr:.2f}x{Colors.RESET}",
            f"  └─ Order:      #{order_id}",
        ]
        return "🎯", Colors.BG_YELLOW, Colors.YELLOW, f"CONVERTING TO TRAILING SL: {symbol}", extra_lines

    if event_type == "TRAILING_SL_SET" or event_type == "TRAILING_SL_SET_CONFIRMED":
        price = d.get('new_sl_price', d.get('sl_price', '?'))
        pips_behind = d.get('pips_behind_price', '?')
        trade_id = d.get('trade_id', '?')
        extra_lines = [
            f"  ├─ New SL:      {Colors.GREEN}{price}{Colors.RESET}",
            f"  └─ Pips Behind: {Colors.CYAN}{pips_behind}{Colors.RESET}",
        ]
        return "🛡️", Colors.BG_GREEN, Colors.GREEN, f"TRAILING SL ACTIVE: {symbol}", extra_lines

    if event_type == "TRAILING_SL_SET_FAILED":
        reason = d.get('reason', d.get('error', 'unknown'))
        return "⚠️", Colors.BG_RED, Colors.RED, f"TRAILING SL FAILED: {reason}", extra_lines

    if event_type == "TIGHT_ASS_MODE":
        profit_pips = d.get('profit_pips', 0)
        return "🔒", Colors.BG_GREEN, Colors.GREEN, f"TIGHT ASS MODE: Locking in {format_pips(profit_pips)} profit", extra_lines

    # ══════════════════════════════════════════════════════════════════
    # CHARTER & GATE ENFORCEMENT
    # ══════════════════════════════════════════════════════════════════
    if event_type == "CHARTER_VIOLATION":
        violation = d.get('violation', 'unknown')
        action = d.get('action', '')
        notional = d.get('notional_usd', 0)
        min_req = d.get('min_required_usd', 0)
        extra_lines = [
            f"  ├─ Violation: {Colors.RED}{violation}{Colors.RESET}",
        ]
        if notional:
            extra_lines.append(f"  ├─ Notional:  ${notional:,.0f}")
        if min_req:
            extra_lines.append(f"  ├─ Required:  ${min_req:,.0f}")
        if action:
            extra_lines.append(f"  └─ Action:    {action}")
        return "🚫", Colors.BG_RED, Colors.RED, f"CHARTER VIOLATION: {symbol}", extra_lines

    if event_type == "GATE_REJECTION":
        reason = d.get('reason', 'unknown')
        action = d.get('action', '')
        margin = d.get('margin_used', 0)
        extra_lines = [
            f"  ├─ Reason: {Colors.YELLOW}{reason}{Colors.RESET}",
        ]
        if margin:
            extra_lines.append(f"  └─ Margin: ${margin:,.2f}")
        return "🚧", Colors.BG_YELLOW, Colors.YELLOW, f"GUARDIAN GATE BLOCKED: {symbol}", extra_lines

    if event_type == "PRICE_ERROR":
        error = d.get('error', 'No price data')
        return "📡", Colors.BG_YELLOW, Colors.YELLOW, f"PRICE FEED ISSUE: {symbol} - {error}", extra_lines

    # ══════════════════════════════════════════════════════════════════
    # BROKER & REGISTRY
    # ══════════════════════════════════════════════════════════════════
    if event_type == "BROKER_MAPPING":
        order_id = d.get('order_id', '?')
        trade_id = d.get('trade_id', '?')
        units = d.get('units', 0)
        entry = d.get('entry_price', 0)
        extra_lines = [
            f"  ├─ Ticket:   #{order_id}",
            f"  ├─ Internal: {trade_id}",
            f"  ├─ Units:    {units:,}",
            f"  └─ Entry:    {entry:.5f}",
        ]
        return "🔗", Colors.BG_DARK, Colors.GRAY, f"BROKER MAPPING: {symbol}", extra_lines

    if event_type == "BROKER_REGISTRY_ERROR":
        error = d.get('error', 'unknown')
        return "⚠️", Colors.BG_YELLOW, Colors.YELLOW, f"Registry issue: {error}", extra_lines

    # ══════════════════════════════════════════════════════════════════
    # HEDGE ENGINE
    # ══════════════════════════════════════════════════════════════════
    if event_type == "HEDGE_OPENED":
        hedge_symbol = d.get('hedge_symbol', '?')
        correlation = d.get('correlation', 0)
        return "🛡️", Colors.BG_BLUE, Colors.CYAN, f"Hedge opened: {hedge_symbol} (correlation: {correlation:.2f})", extra_lines

    if event_type == "HEDGE_SKIPPED":
        reason = d.get('reason', 'not needed')
        return "↔️", Colors.BG_DARK, Colors.GRAY, f"Hedge skipped: {reason}", extra_lines

    # ══════════════════════════════════════════════════════════════════
    # FALLBACK - GENERIC FORMATTING (SHOW ALL DATA)
    # ══════════════════════════════════════════════════════════════════
    for k, v in d.items():
        if k not in ['timestamp', 'event_type', 'symbol', 'venue']:
            # Format values nicely
            if isinstance(v, float):
                if 'price' in k.lower() or 'entry' in k.lower() or 'sl' in k.lower() or 'tp' in k.lower():
                    extra_lines.append(f"  ├─ {k}: {v:.5f}")
                elif 'pnl' in k.lower() or 'notional' in k.lower():
                    extra_lines.append(f"  ├─ {k}: ${v:,.2f}")
                else:
                    extra_lines.append(f"  ├─ {k}: {v:.2f}")
            elif isinstance(v, (list, dict)):
                extra_lines.append(f"  ├─ {k}: {json.dumps(v)}")
            else:
                extra_lines.append(f"  ├─ {k}: {v}")
    
    # Fix the last item to use └─
    if extra_lines:
        extra_lines[-1] = extra_lines[-1].replace('├─', '└─')
    
    return "📋", Colors.BG_DARK, Colors.WHITE, f"{event_type}: {symbol}", extra_lines

def process_line(line):
    global message_count
    try:
        data = json.loads(line)
        timestamp = format_timestamp(data.get('timestamp', ''))
        event_type = data.get('event_type', 'UNKNOWN')
        symbol = data.get('symbol', '')
        details = data.get('details', {})
        
        # Get human-readable translation
        icon, bg_color, text_color, narrative, extra_lines = translate_to_plain_english(event_type, details, symbol)
        
        # Alternate row colors for visibility
        message_count += 1
        row_bg = Colors.BG_DARK if message_count % 2 == 0 else Colors.BG_LIGHT
        
        # Use special backgrounds for important events
        if bg_color in [Colors.BG_GREEN, Colors.BG_RED, Colors.BG_BLUE, Colors.BG_YELLOW]:
            row_bg = bg_color
        
        # Print separator line for major events
        if event_type in ["TRADE_OPENED", "TRADE_CLOSED", "TRADE_CLOSED_DETECTED", "TRADE_SIGNAL", "CHARTER_VIOLATION", "ENGINE_START"]:
            print(f"{Colors.DIM}{'─' * 70}{Colors.RESET}")
        
        # Print main line with background
        print(f"{row_bg} {Colors.GRAY}{timestamp}{Colors.RESET}{row_bg} {icon}  {text_color}{narrative}{Colors.RESET} ")
        
        # Print extra detail lines
        for line in extra_lines:
            print(f"         {line}")
        
        # Print closing separator for major events
        if event_type in ["TRADE_OPENED", "TRADE_CLOSED", "TRADE_CLOSED_DETECTED"]:
            print(f"{Colors.DIM}{'─' * 70}{Colors.RESET}")
        
    except json.JSONDecodeError:
        pass
    except Exception as e:
        # Show errors for debugging
        # print(f"{Colors.RED}Parse error: {e}{Colors.RESET}")
        pass

def main():
    print(f"\n{Colors.BOLD}{'═' * 70}{Colors.RESET}")
    print(f"{Colors.HEADER}{Colors.BOLD}  🗣️  THE VOICE: RICK'S INNER MONOLOGUE{Colors.RESET}")
    print(f"{Colors.GRAY}  Plain English • Color Coded • Full Details{Colors.RESET}")
    print(f"{Colors.BOLD}{'═' * 70}{Colors.RESET}\n")
    print(f"{Colors.DIM}  Legend:{Colors.RESET}")
    print(f"{Colors.DIM}  🚀 Start   💓 Heartbeat   📊 Signal   ✅ Opened   💰 Win   📉 Loss{Colors.RESET}")
    print(f"{Colors.DIM}  🐝 Hive    🔥 Momentum    🛡️ Trailing  🚫 Blocked  🔗 Mapping{Colors.RESET}")
    print(f"{Colors.BOLD}{'─' * 70}{Colors.RESET}\n")
    
    try:
        for line in sys.stdin:
            process_line(line)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Voice signing off...{Colors.RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
