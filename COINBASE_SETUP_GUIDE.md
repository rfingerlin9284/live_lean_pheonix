# Coinbase Trading System - Setup Guide

## 🎯 Coinbase Foundation Complete

This guide covers the Coinbase Advanced Trade integration for the RICK trading system.

### Quick Start

1. **Open VSCode Command Palette**: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. **Run Task**: Type "Run Task" and press Enter
3. **Select**: "💰 Coinbase Trading Engine (Safe Mode)"

---

## 🚀 Starting the Coinbase Engine

### Safe Mode (Recommended Start)
**Task**: `💰 Coinbase Trading Engine (Safe Mode)`

- Starts in practice/sandbox mode
- Validates configuration before any trades
- Logs all activity to narration.jsonl

### Live Mode (Real Money)
**Task**: `🔴 Coinbase Trading Engine (LIVE)`

⚠️ **WARNING**: Connects to real Coinbase account with real money!

### Steps to Start:
1. Open Command Palette (`Ctrl+Shift+P`)
2. Select "Tasks: Run Task"
3. Choose the appropriate engine task (Safe Mode or LIVE)
4. The engine will run in its own dedicated terminal panel

---

## ⚙️ Environment Configuration

### Required Environment Variables

```bash
# Coinbase Advanced Trade API
COINBASE_LIVE_API_KEY=your-api-key-here
COINBASE_LIVE_API_SECRET=your-private-key-here
COINBASE_LIVE_BASE_URL=https://api.coinbase.com

# Crypto instruments to trade
COINBASE_INSTRUMENTS=BTC-USD,ETH-USD,SOL-USD,AVAX-USD,MATIC-USD
```

### Environment Toggle (Practice ↔ Live)

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

## 🔍 Verify Coinbase System

**Task**: `🔍 Verify Coinbase System`

**What it shows**:
- Current environment (practice/live)
- Coinbase API configuration
- Crypto instruments configured
- Process status
- Recent narration activity

**To run**:
```bash
python3 verify_coinbase.py
```

Or use the VSCode task: `🔍 Verify Coinbase System`

### What to expect:
- ✅ All checks should pass for proper operation
- If narration.jsonl shows no recent events, this is NORMAL if:
  - Market conditions don't meet signal criteria
  - No suitable entry points exist
  - The engine is waiting for the right setup (crypto is selective)

### System is working if you see:
1. Engine process is running (check with `ps aux | grep coinbase`)
2. narration.jsonl file exists and is being updated
3. Periodic scan events in narration
4. No errors in the engine terminal

---

## 📋 Understanding Coinbase Specifics

### Crypto vs Forex Differences:

**Market Hours**:
- Crypto: 24/7 operation (no session breaks)
- Forex: 5 days/week with session gaps

**Charter Parameters** (adjusted for crypto):
- Minimum Notional: $3,000 (vs $15,000 forex)
- Minimum Expected PnL: $150 (vs higher for forex)
- Maximum Hold Time: 4 hours (vs 6 hours)
- Risk/Reward Ratio: 3:1 (same as forex)

**Trading Features**:
- Spot trading (BTC-USD, ETH-USD, etc.)
- Perpetual futures (funding rate aware)
- Higher frequency cycles (3-5 min)
- WebSocket streaming for real-time prices
- REST API for order execution

### Why You Might See No Signals:

This is **NORMAL** and **expected** when:
- Crypto volatility is too high (risk management blocks)
- Funding rates are unfavorable (for perps)
- No clear momentum in any pair
- Risk/Reward ratio doesn't meet 3:1 minimum
- No instruments meet all entry criteria

The engine is designed to be **highly selective** - it will pass on many setups to find the perfect one.

---

## 🛠️ Troubleshooting

### Problem: Engine not starting

**Solution**:
1. Check Coinbase API credentials in .env
2. Verify COINBASE_LIVE_API_KEY is set
3. Verify COINBASE_LIVE_API_SECRET is set (multi-line private key)
4. Check COINBASE_INSTRUMENTS are configured
5. Look for errors in the engine terminal

### Problem: No trades happening

**Not a Problem!** The system is selective. Check:
1. narration.jsonl shows periodic scans
2. Engine terminal shows no errors
3. Crypto markets are open (24/7 but can be quiet)
4. Run `python3 verify_coinbase.py` for diagnostics

### Problem: API authentication errors

**Solution**:
1. Verify API key format: `organizations/.../apiKeys/...`
2. Check private key has proper BEGIN/END markers
3. Ensure no extra quotes or whitespace
4. Test with Coinbase API playground first

---

## 📁 File Locations

- **Configuration**: `.env` (root directory)
- **Narration Log**: `narration.jsonl` (root directory)
- **Tasks Config**: `.vscode/tasks.json`
- **Trading Engine**: `coinbase_safe_mode_engine.py`
- **Connector**: `brokers/coinbase_advanced_connector.py`
- **Verification**: `verify_coinbase.py`

---

## 🔐 Environment Variables Reference

### Required for Safe Mode:
```bash
RICK_ENV=practice
COINBASE_LIVE_API_KEY=your-api-key
COINBASE_LIVE_API_SECRET=-----BEGIN EC PRIVATE KEY-----
...
-----END EC PRIVATE KEY-----
COINBASE_LIVE_BASE_URL=https://api.coinbase.com
```

### Crypto Configuration:
```bash
COINBASE_INSTRUMENTS=BTC-USD,ETH-USD,ADA-USD,XRP-USD,DOT-USD,LINK-USD,LTC-USD,BCH-USD,XLM-USD,EOS-USD,TRX-USD,VET-USD,ALGO-USD,ATOM-USD,AVAX-USD,MATIC-USD,SOL-USD,UNI-USD
```

---

## 💡 Tips

1. **Start with Safe Mode** to verify everything works
2. **Monitor narration feed** for signals and activity
3. **Use smaller position sizes** initially (crypto is volatile)
4. **Understand funding rates** if trading perpetuals
5. **Only switch to Live** when you're confident the system works

---

## ⚡ Quick Commands

```bash
# Start engine (safe mode)
RICK_ENV=practice python3 coinbase_safe_mode_engine.py

# Start engine (live) - CAREFUL!
RICK_ENV=live python3 coinbase_safe_mode_engine.py

# Verify system
python3 verify_coinbase.py

# Check engine status
ps aux | grep coinbase

# View recent narration
tail -30 narration.jsonl

# Monitor narration live
tail -f narration.jsonl
```

---

## 📊 Monitoring Integration

The Coinbase engine integrates with the same monitoring system as OANDA:

**Terminal 1: System Watchdog**
- Shows Coinbase engine health
- Displays component status
- Auto-refreshes every 30s

**Terminal 2: Live Narration Feed**
- Shows crypto trading events
- Displays signals and orders
- Auto-refreshes every 10s

Use VSCode task: "🎯 Start Two Persistent Terminals"

---

## 🔄 Integration with OANDA

Both engines can run simultaneously:

1. **OANDA**: Forex trading (EUR/USD, GBP/USD, etc.)
2. **Coinbase**: Crypto trading (BTC-USD, ETH-USD, etc.)

Each engine:
- Uses the same RICK_ENV setting
- Logs to the same narration.jsonl
- Follows the same charter rules
- Can be monitored in the same terminals

---

## 📞 Support

If Coinbase engine isn't working:

1. Run `python3 verify_coinbase.py` and review all checks
2. Check .env has all required Coinbase credentials
3. Verify API key format is correct
4. Look for errors in the engine terminal output
5. Check narration.jsonl for error events

---

**Last Updated**: 2025-12-04  
**System**: RBOTzilla Coinbase Trading Engine  
**PIN**: 841921  
**API**: Coinbase Advanced Trade
