#!/usr/bin/env python3
"""
Lightweight Terminal Display for RICK Trading System (minimal subset)
This runtime-friendly variant provides the display functions used by engines
and avoids heavy terminal dependencies.
"""

import os


class Colors:
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class TerminalDisplay:
    def header(self, title: str, subtitle: str = None):
        print(f"\n{Colors.BRIGHT_MAGENTA}{Colors.BOLD}=== {title} ==={Colors.RESET}")
        if subtitle:
            print(f"{Colors.BRIGHT_BLUE}{subtitle}{Colors.RESET}\n")

    def section(self, title: str):
        print(f"\n{Colors.BRIGHT_CYAN}--- {title} ---{Colors.RESET}")

    def info(self, label: str, value: str = None, color = Colors.WHITE):
        """Display an informational line.

        Accepts either:
        - info(label, value, color) -> prints 'label: value' (preferred)
        - info(message) -> prints just the message when only a single string is provided
        """
        if value is None:
            # Single-argument call: print the message without a left label column
            print(f"  • {color}{label}{Colors.RESET}")
        else:
            print(f"  • {label:<20}: {color}{value}{Colors.RESET}")

    def success(self, message: str):
        print(f"{Colors.BRIGHT_GREEN}✅ {message}{Colors.RESET}")

    def error(self, message: str):
        print(f"{Colors.BRIGHT_RED}❌ {message}{Colors.RESET}")

    def warning(self, message: str):
        print(f"{Colors.BRIGHT_YELLOW}⚠️  {message}{Colors.RESET}")

    def trade_open(self, symbol: str, direction: str, price: float, details: str = ""):
        print(f"\n{Colors.BRIGHT_GREEN}💰 OPENED TRADE: {symbol} {direction} @ {price:.5f}{Colors.RESET}")
        print(f"   {Colors.BRIGHT_BLACK}Details: {details}{Colors.RESET}")

    def trade_win(self, symbol: str, pnl: float, details: str = ""):
        print(f"{Colors.BRIGHT_GREEN}🎉 WIN: {symbol} +${pnl:.2f}{Colors.RESET} ({details})")

    def trade_loss(self, symbol: str, pnl: float, details: str = ""):
        print(f"{Colors.BRIGHT_RED}📉 LOSS: {symbol} -${abs(pnl):.2f}{Colors.RESET} ({details})")

    def connection_status(self, broker: str, status: str):
        color = Colors.BRIGHT_GREEN if "READY" in status or "CONNECTED" in status else Colors.BRIGHT_RED
        print(f"  📡 {broker}: {color}{status}{Colors.RESET}")

    def market_data(self, symbol: str, bid: float, ask: float, spread: float):
        print(f"  📊 {symbol} | Bid: {bid:.5f} | Ask: {ask:.5f} | Spread: {spread:.1f}")

    def alert(self, message: str, level: str = "INFO"):
        color = Colors.BRIGHT_BLUE
        if level == "WARNING": color = Colors.BRIGHT_YELLOW
        if level == "ERROR": color = Colors.BRIGHT_RED
        if level == "SUCCESS": color = Colors.BRIGHT_GREEN
        print(f"{color}[{level}] {message}{Colors.RESET}")

    def rick_says(self, message: str):
        print(f"{Colors.BRIGHT_MAGENTA}🧠 RICK: {message}{Colors.RESET}")

    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def divider(self, char='─', length = 80):
        print(f"{Colors.BRIGHT_BLACK}{char * length}{Colors.RESET}")

    def stats_panel(self, stats: dict):
        print(f"\n{Colors.BRIGHT_CYAN}📊 SESSION STATS:{Colors.RESET}")
        for k, v in stats.items():
            print(f"   {k:<15}: {v}")
