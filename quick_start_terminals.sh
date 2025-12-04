#!/bin/bash
# =============================================================================
# Quick Start Script - Two Persistent Terminals for OANDA Trading
# =============================================================================
# This script provides instructions for setting up the two persistent
# monitoring terminals in VSCode
#
# PIN: 841921
# =============================================================================

cat << 'EOF'
╔════════════════════════════════════════════════════════════════════════════╗
║                  OANDA TRADING SYSTEM - QUICK START                        ║
║                     Two Persistent Terminals Setup                         ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 GOAL: Get two auto-refreshing monitoring terminals running

📋 PREREQUISITES:
   ✓ VSCode installed
   ✓ This repository opened in VSCode
   ✓ OANDA credentials configured in .env file

🚀 QUICK START (3 STEPS):

   STEP 1: Open Command Palette
   ────────────────────────────────────────────────────────────
   • Press: Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (Mac)
   
   STEP 2: Run the Two-Terminal Task
   ────────────────────────────────────────────────────────────
   • Type: "Run Task"
   • Select: "🎯 Start Two Persistent Terminals"
   
   STEP 3: Start the Trading Engine
   ────────────────────────────────────────────────────────────
   • Open Command Palette again (Ctrl+Shift+P)
   • Type: "Run Task"
   • Select: "🚀 OANDA Trading Engine (Practice)"

✅ WHAT YOU SHOULD SEE:

   Terminal 1: System Watchdog
   ────────────────────────────────────────────────────────────
   • Shows system health status
   • Lists active components (ML, Hive Mind, etc.)
   • Displays engine process status
   • Auto-refreshes every 30 seconds
   
   Terminal 2: Live Narration Feed
   ────────────────────────────────────────────────────────────
   • Shows last 30 trading events
   • Displays signals, orders, trades
   • Human-readable format
   • Auto-refreshes every 10 seconds
   
   Terminal 3: Trading Engine
   ────────────────────────────────────────────────────────────
   • Shows engine startup and configuration
   • Logs scanning activity
   • Reports signals and order placement
   • Stays running until you stop it

🔍 VERIFY IT'S WORKING:

   Run this command to check system status:
   ────────────────────────────────────────────────────────────
   python3 verify_scanning.py

   Expected results:
   • ✅ Environment Config
   • ✅ Engine Process
   • ✅ Narration Activity
   • ✅ Scanning Parameters

⚙️  SWITCH TO LIVE MODE (CAREFUL!):

   1. Stop the trading engine (Ctrl+C in engine terminal)
   2. Open Command Palette (Ctrl+Shift+P)
   3. Run Task: "⚙️ Toggle Practice/Live Environment"
   4. Confirm the switch when prompted
   5. Restart the engine with "🔴 OANDA Trading Engine (LIVE)"

❓ TROUBLESHOOTING:

   Problem: Terminals not showing up
   Solution: Check .vscode/tasks.json exists and is valid JSON
   
   Problem: Engine not scanning
   Solution: Run "python3 verify_scanning.py" for diagnostics
   
   Problem: No signals appearing
   Solution: This is NORMAL! The system is very selective.
            Check narration.jsonl for periodic scan events.

📚 DOCUMENTATION:

   Complete guide: TERMINAL_SETUP_GUIDE.md
   Environment config: .env file
   Tasks configuration: .vscode/tasks.json

═══════════════════════════════════════════════════════════════════════════════

Ready to start? Follow the 3 steps above! 🚀

Press Enter to close...
EOF

read -r
