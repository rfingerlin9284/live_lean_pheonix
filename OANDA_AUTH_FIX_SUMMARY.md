# OANDA API Authorization Errors - FIXED

## Problem Summary
The OANDA trading engine was experiencing 401 Unauthorized errors and invalid account ID errors when attempting to connect to the OANDA API.

### Root Causes Identified

1. **Multiple Stale Processes Running**
   - 6 instances of `oanda_trading_engine.py` were running with outdated authentication tokens
   - These processes had token: `bb3a14e64e0f01b3692a73130582e806-e1bd16353bdabf818dc7bd02695fa049`
   - Current valid token in `.env`: `7e4cf137dcaa0d014d98b3e9ffc1b1bf-f89d6c0d110db57fc2f002792a352696`

2. **Token Mismatch**
   - Running processes were using an expired/invalid token from a previous session
   - API requests were being rejected with 401 Unauthorized

## Solution Applied

### 1. Stop All Running Processes
Created and executed `stop_all_oanda.sh` to cleanly terminate all stale instances:
```bash
./stop_all_oanda.sh
```
Result: ✅ All 6 processes successfully stopped

### 2. Verified Credentials
Confirmed current credentials in `.env` are valid:
- Account ID: `101-001-31210531-002`
- Token: Valid and authenticated successfully
- Base URL: `https://api-fxpractice.oanda.com/v3`
- Test connection: ✅ SUCCESS
- Account Balance: $9,988.93

### 3. Created Clean Startup Script
Created `start_oanda_practice.sh` for reliable startup:
```bash
#!/usr/bin/env bash
cd /home/ing/RICK/RICK_PHOENIX
export RICK_ENV=practice
exec python3 oanda/oanda_trading_engine.py
```

### 4. Verified Fix
Tested startup with new credentials:
- ✅ No 401 Unauthorized errors
- ✅ Correct environment (practice)
- ✅ API connection successful
- ✅ Account data retrieved

## How to Use

### Start OANDA Trading Engine (Practice Mode)
```bash
cd /home/ing/RICK/RICK_PHOENIX
./start_oanda_practice.sh
```

### Stop All OANDA Engines
```bash
cd /home/ing/RICK/RICK_PHOENIX
./stop_all_oanda.sh
```

### Manual Start (Alternative)
```bash
cd /home/ing/RICK/RICK_PHOENIX
export RICK_ENV=practice
python3 oanda/oanda_trading_engine.py
```

## Environment Variables Required
Ensure these are set in `.env`:
- `OANDA_PRACTICE_ACCOUNT_ID=101-001-31210531-002`
- `OANDA_PRACTICE_TOKEN=<your-valid-token>`
- `OANDA_PRACTICE_BASE_URL=https://api-fxpractice.oanda.com/v3`

## Prevention Tips

1. **Always stop old processes before starting new ones**
   ```bash
   ./stop_all_oanda.sh && ./start_oanda_practice.sh
   ```

2. **Check for running processes**
   ```bash
   ps aux | grep oanda_trading_engine
   ```

3. **Verify credentials are current**
   ```bash
   python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OANDA_PRACTICE_TOKEN')[:20])"
   ```

4. **Monitor for authentication errors in logs**
   - 401 errors indicate invalid/expired token
   - 400 errors with "Invalid accountID" indicate environment mismatch

## Status
✅ **RESOLVED** - All OANDA API authentication errors fixed. System ready for practice trading.

Date: 2025-12-04
Fixed by: Copilot CLI
