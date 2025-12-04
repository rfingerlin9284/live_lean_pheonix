# OANDA Trading System - Terminal Setup Guide

## 🎯 Two Persistent Terminals Setup

This system provides two dedicated, auto-refreshing terminal panels for monitoring your OANDA trading engine.

### Quick Start

1. **Open VSCode Command Palette**: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. **Run Task**: Type "Run Task" and press Enter
3. **Select**: "🎯 Start Two Persistent Terminals"

This will automatically start both monitoring terminals in separate panels.

---

## 📊 Terminal 1: System Watchdog (Live Status)

**Task Name**: `📡 Persistent Monitor (System Watchdog)`

**What it does**:
- Shows real-time system health
- Monitors trading engine process
- Displays component status (ML, Hive Mind, etc.)
- Auto-refreshes every 30 seconds
- Self-healing: Automatically restarts if it crashes

**How to start manually**:
1. Open Command Palette (`Ctrl+Shift+P`)
2. Select "Tasks: Run Task"
3. Choose "📡 Persistent Monitor (System Watchdog)"

---

## 📈 Terminal 2: Live Narration Feed

**Task Name**: `📊 Live Narration Feed (Auto-refresh)`

**What it does**:
- Shows last 30 trading events from narration.jsonl
- Displays signals, orders, trades, and errors
- Auto-refreshes every 10 seconds
- Human-readable format with timestamps

**How to start manually**:
1. Open Command Palette (`Ctrl+Shift+P`)
2. Select "Tasks: Run Task"
3. Choose "📊 Live Narration Feed (Auto-refresh)"

---

## 🚀 Starting the Trading Engine

### Practice Mode (Safe Testing)
**Task**: `🚀 OANDA Trading Engine (Practice)`

Connects to OANDA practice account (paper trading).

### Live Mode (Real Money)
**Task**: `🔴 OANDA Trading Engine (LIVE)`

⚠️ **WARNING**: Connects to real OANDA account with real money!

### Steps to Start:
1. Open Command Palette (`Ctrl+Shift+P`)
2. Select "Tasks: Run Task"
3. Choose the appropriate engine task (Practice or LIVE)
4. The engine will run in its own dedicated terminal panel

---

## ⚙️ Environment Toggle (Practice ↔ Live)

**Task**: `⚙️ Toggle Practice/Live Environment`

**What it does**:
- Shows current environment (practice or live)
- Allows you to switch between modes
- Updates the .env file with new RICK_ENV setting
- Prompts for confirmation before switching

**Usage**:
1. Run the task from Command Palette
2. Review current environment
3. Confirm switch when prompted
4. **Important**: Restart the trading engine for changes to take effect

---

## 🔍 Verify Scanning is Working

**Task**: `🔍 Engine Parameters Diagnostic`

**What it shows**:
- Current environment (practice/live)
- OANDA account configuration
- Scanning instruments (currency pairs)
- Process status
- Toggle file status

**To run**:
```bash
python3 verify_scanning.py
```

Or use the VSCode task: `🔍 Engine Parameters Diagnostic`

### What to expect:
- ✅ All checks should pass for proper operation
- If narration.jsonl shows no recent events, this is NORMAL if:
  - Market conditions don't meet signal criteria
  - No suitable entry points exist
  - The engine is waiting for the right setup

### Scanning is working if you see:
1. Engine process is running (check with `ps aux | grep oanda_trading_engine`)
2. narration.jsonl file exists and is being updated
3. Periodic "SCAN_COMPLETE" or similar events in narration
4. No errors in the engine terminal

---

## 📋 Understanding the Narration Feed

### Event Types You'll See:

- **SCAN_COMPLETE**: Engine finished scanning all instruments
- **SIGNAL_GENERATED**: Trading opportunity identified
- **OCO_PLACED**: Order sent to OANDA with stop-loss and take-profit
- **TRADE_OPENED**: Position entered
- **TRADE_CLOSED**: Position exited
- **ERROR**: Something went wrong
- **CHARTER_VIOLATION**: Risk management blocked an order

### Why You Might See No Signals:

This is **NORMAL** and **expected** when:
- Market is ranging (no clear trend)
- Volatility is too low
- Risk/Reward ratio doesn't meet 3:1 minimum
- No instruments meet all entry criteria
- Market is closed (weekends, holidays)

The engine is designed to be **highly selective** - it will pass on hundreds of setups to find the perfect one.

---

## 🛠️ Troubleshooting

### Problem: Terminals not refreshing

**Solution**:
1. Check if tasks are set to `isBackground: true`
2. Verify the while loop is running: `ps aux | grep -E "watchdog|narration"`
3. Restart the tasks from Command Palette

### Problem: Engine not scanning

**Solution**:
1. Run `python3 verify_scanning.py` to diagnose
2. Check .env file has correct OANDA credentials
3. Verify INSTRUMENTS are configured in .env
4. Check narration.jsonl exists and is updating
5. Look for errors in the engine terminal

### Problem: No signals appearing

**Not a Problem!** The system is selective. Check:
1. narration.jsonl shows periodic scans (every 15 min typical)
2. Engine terminal shows no errors
3. Market is open (forex markets: Sunday 5pm - Friday 5pm EST)

### Problem: Can't switch to live mode

**Solution**:
1. Ensure you have live OANDA credentials in .env
2. Set `OANDA_LIVE_TOKEN` and `OANDA_LIVE_ACCOUNT_ID`
3. Run toggle task and confirm switch
4. **Stop and restart the engine** for changes to apply

---

## 📁 File Locations

- **Configuration**: `.env` (root directory)
- **Narration Log**: `narration.jsonl` (root directory)
- **Tasks Config**: `.vscode/tasks.json`
- **Trading Engine**: `oanda_trading_engine.py`
- **Watchdog**: `system_watchdog.py`
- **Verification**: `verify_scanning.py`

---

## 🔐 Environment Variables Reference

### Required for Practice Mode:
```bash
RICK_ENV=practice
OANDA_PRACTICE_ACCOUNT_ID=your-practice-account-id
OANDA_PRACTICE_TOKEN=your-practice-token
OANDA_PRACTICE_BASE_URL=https://api-fxpractice.oanda.com/v3
```

### Required for Live Mode:
```bash
RICK_ENV=live
OANDA_LIVE_ACCOUNT_ID=your-live-account-id
OANDA_LIVE_TOKEN=your-live-token
OANDA_LIVE_BASE_URL=https://api-fxtrade.oanda.com/v3
```

### Scanning Configuration:
```bash
INSTRUMENTS=EUR_USD,GBP_USD,USD_JPY,USD_CHF,AUD_USD,...
MICRO_TRADING_MODE=false
```

---

## 💡 Tips

1. **Keep both monitoring terminals open** for full visibility
2. **Don't restart terminals unnecessarily** - they auto-refresh
3. **Check narration feed regularly** for new signals
4. **Use Practice mode first** to verify everything works
5. **Only switch to Live** when you're confident the system works

---

## ⚡ Quick Commands

```bash
# Start engine (practice)
RICK_ENV=practice python3 oanda_trading_engine.py

# Start engine (live)
RICK_ENV=live python3 oanda_trading_engine.py

# Verify scanning
python3 verify_scanning.py

# Check engine status
ps aux | grep oanda_trading_engine

# View recent narration
tail -30 narration.jsonl

# Monitor narration live
tail -f narration.jsonl
```

---

## 📞 Support

If terminals aren't persisting or scanning isn't working:

1. Run `python3 verify_scanning.py` and review all checks
2. Check VSCode tasks are configured correctly in `.vscode/tasks.json`
3. Verify .env has all required credentials
4. Look for errors in the engine terminal output
5. Check narration.jsonl for error events

---

**Last Updated**: 2025-12-04  
**System**: RBOTzilla OANDA Trading Engine  
**PIN**: 841921
