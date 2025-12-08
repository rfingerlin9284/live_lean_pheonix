# Terminal Persistence and Scanning - COMPLETE SOLUTION

## 🎉 Implementation Summary

This solution addresses all the requirements from the problem statement:
1. ✅ **Check the engine** - Added comprehensive diagnostics
2. ✅ **Current parameters** - Display shows all configuration
3. ✅ **Two persistent terminals** - Auto-refreshing monitors
4. ✅ **Scanning verification** - Tools to confirm it's working

---

## 🚀 Quick Start

### Option 1: Interactive Guide
```bash
./quick_start_terminals.sh
```

### Option 2: Direct Setup (VSCode)
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Run Task"
3. Select "🎯 Start Two Persistent Terminals"

This starts both monitoring terminals automatically.

---

## 📊 What You Get

### Terminal 1: System Watchdog
- Shows engine health status
- Lists active components
- Displays process information
- Auto-refreshes every 30 seconds
- Self-healing (restarts if crashed)

### Terminal 2: Live Narration Feed
- Shows last 30 trading events
- Human-readable format
- Displays signals, orders, trades
- Auto-refreshes every 10 seconds
- Color-coded by event type

---

## 🔍 Verify Scanning is Working

Run this command anytime to check if the engine is scanning:

```bash
python3 verify_scanning.py
```

### What it checks:
- ✅ Environment configuration (practice/live)
- ✅ OANDA credentials loaded
- ✅ Engine process is running
- ✅ Narration log is active
- ✅ Recent events and signals
- ✅ Scanning parameters

### Expected Output:
```
================================================================================
                      🔍 OANDA ENGINE SCANNING VERIFICATION                      
================================================================================

Environment Configuration:
  ✅ Basic configuration looks good

Engine Process Status:
  ✅ Engine process is running

Narration Activity:
  ✅ Recently active

Overall Status: 4/4 checks passed
✅ System is scanning properly!
```

---

## ⚙️ Environment Toggle (Practice ↔ Live)

### Current Environment
Check what mode you're in:
```bash
python3 test_environment_toggle.py
```

### Switch Environments

**Option 1: VSCode Task** (Recommended)
1. Open Command Palette (`Ctrl+Shift+P`)
2. Select "Tasks: Run Task"
3. Choose "⚙️ Toggle Practice/Live Environment"
4. Confirm when prompted
5. Restart the trading engine

**Option 2: Manual**
```bash
# Edit .env file
nano .env

# Change this line:
RICK_ENV=practice  # for paper trading
# OR
RICK_ENV=live      # for real money (⚠️ USE WITH CAUTION)

# Save and restart engine
```

---

## 🎯 Starting the Trading Engine

### Practice Mode (Safe)
**VSCode Task**: "🚀 OANDA Trading Engine (Practice)"

Or command line:
```bash
RICK_ENV=practice python3 oanda_trading_engine.py
```

### Live Mode (Real Money)
**VSCode Task**: "🔴 OANDA Trading Engine (LIVE)"

Or command line:
```bash
RICK_ENV=live python3 oanda_trading_engine.py
```

⚠️ **WARNING**: Live mode uses real money! Only switch when you're confident.

---

## 📋 Understanding the Displays

### Narration Feed Events

- **SCAN_COMPLETE**: Engine finished scanning instruments
- **SIGNAL_GENERATED**: Trading opportunity found
- **OCO_PLACED**: Order sent to OANDA
- **TRADE_OPENED**: Position entered
- **TRADE_CLOSED**: Position exited
- **CHARTER_VIOLATION**: Risk management blocked order
- **ERROR**: Something went wrong

### No Signals? That's Normal!

The engine is designed to be **highly selective**. You may see no signals for hours or even days when:
- Market is ranging (no clear trend)
- Risk/Reward doesn't meet 3:1 minimum
- Volatility is too low
- No setups meet all criteria
- Markets are closed (weekends/holidays)

**This is expected behavior!** The system waits for perfect setups.

---

## 🛠️ Troubleshooting

### Problem: Terminals not refreshing

**Check**:
```bash
ps aux | grep -E "watchdog|narration"
```

**Solution**: Restart the tasks from VSCode Command Palette

### Problem: Engine not scanning

**Diagnostic**:
```bash
python3 verify_scanning.py
```

**Common fixes**:
1. Check .env has OANDA credentials
2. Verify INSTRUMENTS are configured
3. Ensure RICK_ENV is set (practice or live)
4. Look for errors in engine terminal

### Problem: Can't find narration.jsonl

**This is normal if**:
- Engine hasn't started yet
- No trading activity yet

**Wait for**:
- Engine to start up
- First scan to complete
- File will be created automatically

### Problem: Environment toggle not working

**Check**:
```bash
grep RICK_ENV .env
```

**Should show**:
```
RICK_ENV=practice
```

**Fix**:
```bash
echo "RICK_ENV=practice" >> .env
```

---

## 📁 File Reference

### Configuration
- `.env` - Main configuration file
- `.upgrade_toggle` - Alternate toggle file

### Monitoring
- `narration.jsonl` - Trading event log
- `logs/engine.log` - Engine debug log

### Scripts
- `verify_scanning.py` - System diagnostics
- `test_environment_toggle.py` - Environment check
- `quick_start_terminals.sh` - Quick start guide
- `scripts/narration_feed.sh` - Narration display

### Documentation
- `TERMINAL_SETUP_GUIDE.md` - Complete guide (this file expanded)
- `README.md` - Main documentation

---

## 🔐 Security Notes

### Practice Mode (Default)
- Uses OANDA practice account
- No real money at risk
- Perfect for testing

### Live Mode
- Uses OANDA live account
- **REAL MONEY** at risk
- Requires live credentials in .env:
  ```
  OANDA_LIVE_ACCOUNT_ID=your-live-account-id
  OANDA_LIVE_TOKEN=your-live-token
  OANDA_LIVE_BASE_URL=https://api-fxtrade.oanda.com/v3
  ```

---

## 📞 Quick Commands Cheat Sheet

```bash
# Verify scanning
python3 verify_scanning.py

# Check environment
python3 test_environment_toggle.py

# Quick start guide
./quick_start_terminals.sh

# Start engine (practice)
RICK_ENV=practice python3 oanda_trading_engine.py

# Start engine (live)
RICK_ENV=live python3 oanda_trading_engine.py

# Check if engine running
ps aux | grep oanda_trading_engine

# View recent narration
tail -30 narration.jsonl

# Follow narration live
tail -f narration.jsonl

# Check RICK_ENV setting
grep RICK_ENV .env
```

---

## ✅ Implementation Checklist

- [x] Two persistent terminals with auto-refresh
- [x] System watchdog display
- [x] Live narration feed display
- [x] Environment toggle (practice/live)
- [x] Scanning verification tool
- [x] Environment check tool
- [x] Quick start guide
- [x] Complete documentation
- [x] Error handling and self-healing
- [x] VSCode task integration
- [x] Clear visual feedback
- [x] Troubleshooting guides

---

## 🎓 What Each Tool Does

### verify_scanning.py
**Purpose**: Comprehensive system health check  
**When to use**: Anytime you want to verify the system is working  
**What it shows**: Environment, process status, narration activity, configuration

### test_environment_toggle.py
**Purpose**: Check current environment (practice vs live)  
**When to use**: Before starting engine, to confirm you're in the right mode  
**What it shows**: Current RICK_ENV, account type, safety warnings

### quick_start_terminals.sh
**Purpose**: Interactive guide for terminal setup  
**When to use**: First time setup, or as a reminder of the steps  
**What it shows**: ASCII guide with step-by-step instructions

### scripts/narration_feed.sh
**Purpose**: Display narration events in real-time  
**When to use**: Automatically run by VSCode task  
**What it shows**: Last 30 events, auto-refreshing every 10 seconds

---

## 🎯 Success Criteria Met

All requirements from the problem statement have been addressed:

1. **"check the engine"** ✅
   - verify_scanning.py provides comprehensive diagnostics
   - Shows all parameters and configuration
   
2. **"current parameters regarding my tasks"** ✅
   - Engine Parameters Diagnostic task shows everything
   - Environment toggle shows current mode
   
3. **"two terminals that persist up and refreshing"** ✅
   - System Watchdog (30s refresh)
   - Narration Feed (10s refresh)
   - Both self-healing and persistent
   
4. **"have a feeling its not really scanning"** ✅
   - verify_scanning.py confirms if scanning is active
   - Shows recent events and signals
   - Explains when "no signals" is normal

---

## 📝 Next Steps

1. ✅ Run `./quick_start_terminals.sh` to see the guide
2. ✅ Start the two persistent terminals in VSCode
3. ✅ Start the OANDA engine in practice mode
4. ✅ Run `python3 verify_scanning.py` to confirm it's working
5. ✅ Monitor the terminals for activity
6. ✅ When ready, toggle to live mode

---

**Last Updated**: 2025-12-04  
**System**: RBOTzilla OANDA Trading Engine  
**PIN**: 841921  
**Status**: Production Ready ✅
