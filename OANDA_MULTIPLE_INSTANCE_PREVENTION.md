# OANDA Multiple Instance Prevention - IMPLEMENTED

## Problem
Previously, running `python3 oanda/oanda_trading_engine.py` multiple times would launch duplicate instances, leading to:
- Multiple engines competing for the same account
- Confusion about which process is active
- Stale processes with outdated credentials
- Resource waste

## Solution Implemented

### 1. Engine-Level Protection
Modified `oanda/oanda_trading_engine.py` to detect and prevent duplicate launches:

**Features:**
- Automatically detects existing running instances on startup
- Prompts user with 3 options:
  1. Stop existing instances and start fresh (recommended)
  2. Continue anyway (creates duplicate - not recommended)
  3. Cancel startup
- Clean shutdown of old instances before starting new one

**Code Location:** Lines 226-261 in `oanda/oanda_trading_engine.py`

### 2. Script-Level Protection  
Updated `start_oanda_practice.sh` to auto-stop existing instances:

**Features:**
- Checks for running engines before starting
- Automatically stops any found instances
- Shows clear status messages
- No user interaction required

## Usage

### Recommended: Use the Script (Auto-Stop)
```bash
./start_oanda_practice.sh
```
This will automatically stop any running instances and start fresh.

### Direct Python (Interactive)
```bash
export RICK_ENV=practice
python3 oanda/oanda_trading_engine.py
```
You'll be prompted if instances are running:
- Press `1` to stop them and start fresh
- Press `3` to cancel

### Manual Control
```bash
# Check for running instances
ps aux | grep oanda_trading_engine

# Stop all instances manually
./stop_all_oanda.sh

# Start fresh
./start_oanda_practice.sh
```

## How It Works

### Detection Method
Uses `pgrep -f 'oanda/oanda_trading_engine.py'` to find running instances by process name pattern.

### Prevention Logic
```python
1. On startup, check for existing PIDs
2. If found:
   - Display warning with PID list
   - Prompt user for action
   - Execute chosen action
3. Continue with engine initialization
```

### Script Auto-Stop
```bash
1. Count running instances with pgrep
2. If any found:
   - Display count
   - Kill with pkill
   - Wait 2 seconds
3. Start new instance
```

## Benefits

✅ **No More Duplicates** - Prevents accidental multiple launches  
✅ **Clear Feedback** - Shows when instances are detected  
✅ **User Control** - Choose how to handle existing instances  
✅ **Auto-Cleanup** - Script mode handles it automatically  
✅ **Resource Efficient** - Only one engine running at a time

## Examples

### Scenario 1: Script Start (No Running Engines)
```bash
$ ./start_oanda_practice.sh
Starting OANDA Trading Engine in PRACTICE mode...
Press Ctrl+C to stop

=== RBOTZILLA Consolidated ===
Env: practice | PIN: 841921
...
```

### Scenario 2: Script Start (Engine Already Running)
```bash
$ ./start_oanda_practice.sh
⚠️  Found 1 running OANDA engine(s)
Stopping existing instances...
✅ Stopped existing instances

Starting OANDA Trading Engine in PRACTICE mode...
...
```

### Scenario 3: Direct Python Start (Engine Running)
```bash
$ python3 oanda/oanda_trading_engine.py
⚠️  WARNING: 2 OANDA engine(s) already running (PIDs: 12345, 12346)
Do you want to:
  1. Stop existing instances and start fresh
  2. Continue anyway (NOT recommended - will have multiple engines)
  3. Cancel
Enter choice (1/2/3): 1
Stopping existing instances...
✅ Existing instances stopped. Starting fresh...
=== RBOTZILLA Consolidated ===
...
```

## Technical Details

### Files Modified
1. `oanda/oanda_trading_engine.py` - Added duplicate detection at startup
2. `start_oanda_practice.sh` - Added auto-stop before launch

### Dependencies
- `pgrep` - Process detection (standard Linux utility)
- `pkill` - Process termination (standard Linux utility)
- `subprocess` Python module (standard library)

### Process Detection
Searches for processes matching: `oanda/oanda_trading_engine.py`
Excludes current process PID to avoid false detection.

## Testing Performed

✅ Start with no running engines - works normally  
✅ Start with 1 running engine - detected and handled  
✅ Start with multiple (6) running engines - all detected and stopped  
✅ Script auto-stop - works correctly  
✅ Interactive prompt - all options work  
✅ Syntax validation - passes

## Date
Implemented: 2025-12-04  
By: Copilot CLI
