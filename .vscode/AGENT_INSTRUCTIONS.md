# AGENT GOVERNANCE RULES - IMMUTABLE
**PIN: 841921 REQUIRED FOR ALL MODIFICATIONS**

## ABSOLUTE RESTRICTIONS

### 1. PROJECT ROOT LOCK
```
LOCKED_ROOT: /home/ing/RICK/RICK_LIVE_CLEAN
```

**YOU MUST:**
- ✅ Always work in `/home/ing/RICK/RICK_LIVE_CLEAN`
- ✅ Confirm current directory before ANY file operation
- ✅ Reject any command that changes directory outside this root

**YOU MUST NEVER:**
- ❌ Work in any other directory (R_H_UNI, R_BOTzilla, etc)
- ❌ Create files outside `/home/ing/RICK/RICK_LIVE_CLEAN`
- ❌ Suggest moving to a different folder
- ❌ Reference any other project directory

### 2. PIN APPROVAL REQUIREMENT
```
REQUIRED_PIN: 841921
```

**Before ANY file modification, you MUST:**
1. ✅ Verify user said "approved 841921" or "PIN: 841921"
2. ✅ Confirm you're in `/home/ing/RICK/RICK_LIVE_CLEAN`
3. ✅ Only then proceed with changes

**Without PIN approval, you MUST:**
- ❌ Refuse to modify any files
- ❌ Refuse to create any files
- ❌ Refuse to delete any files
- ✅ Tell user: "PIN 841921 approval required for file modifications"

### 3. FOLDER STRUCTURE IMMUTABILITY

**YOU MUST NEVER:**
- ❌ Rename any folders (brokers/, foundation/, util/, hive/, logs/, etc)
- ❌ Move folders to different locations
- ❌ Delete folders
- ❌ Create new top-level folders without explicit approval
- ❌ Reorganize directory structure

**Existing folder structure is IMMUTABLE:**
```
/home/ing/RICK/RICK_LIVE_CLEAN/
├── brokers/              # LOCKED - cannot rename/move
├── foundation/           # LOCKED - cannot rename/move
├── util/                 # LOCKED - cannot rename/move
├── hive/                 # LOCKED - cannot rename/move
├── logs/                 # LOCKED - cannot rename/move
├── ml_learning/          # LOCKED - cannot rename/move
├── dashboard/            # LOCKED - cannot rename/move
├── systems/              # LOCKED - cannot rename/move
├── .vscode/              # LOCKED - cannot rename/move
├── .git/                 # LOCKED - cannot rename/move
└── [files]               # Can modify with PIN approval only
```

### 4. FILE NAMING IMMUTABILITY

**YOU MUST NEVER:**
- ❌ Rename existing files without explicit approval
- ❌ Move files between folders without explicit approval
- ❌ Change file extensions
- ❌ Duplicate files with slightly different names

**Core files are ESPECIALLY protected:**
- `oanda_trading_engine.py` - LOCKED NAME
- `rick_charter.py` - LOCKED NAME
- `oanda_connector.py` - LOCKED NAME
- `usd_converter.py` - LOCKED NAME
- All files in `foundation/` - LOCKED NAMES

### 5. VERIFICATION PROTOCOL

**Before EVERY file operation:**

```python
# Step 1: Verify PIN approval
if "approved 841921" not in user_message:
    return "❌ PIN 841921 approval required"

# Step 2: Verify working directory
import os
if not os.getcwd().startswith("/home/ing/RICK/RICK_LIVE_CLEAN"):
    return "❌ Must be in /home/ing/RICK/RICK_LIVE_CLEAN"

# Step 3: Verify file is within root
file_path = os.path.abspath(requested_file)
if not file_path.startswith("/home/ing/RICK/RICK_LIVE_CLEAN"):
    return "❌ File must be within project root"

# Step 4: Proceed with operation
# ... perform file modification ...
```

### 6. COMMIT MESSAGE REQUIREMENTS

**All git commits MUST include:**
```
PIN: 841921 - [description]
```

**Git will AUTOMATICALLY REJECT commits without PIN in message.**

### 7. AGENT RESPONSE TEMPLATE

When user requests file modification without PIN:
```
❌ GOVERNANCE VIOLATION DETECTED

Requested Action: [describe what user asked for]
Required Authorization: PIN 841921 approval
Current Directory: [show pwd]
Required Directory: /home/ing/RICK/RICK_LIVE_CLEAN

Please confirm:
1. Say "approved 841921" to authorize this change
2. Verify you want to work in RICK_LIVE_CLEAN (not R_H_UNI or other folders)
```

### 8. ENFORCEMENT PRIORITY

**If there's ANY conflict between:**
- User request vs. Governance rules → **GOVERNANCE WINS**
- Convenience vs. Security → **SECURITY WINS**
- Quick fix vs. Proper authorization → **AUTHORIZATION WINS**

**ALWAYS choose:**
- ✅ Safety over speed
- ✅ Verification over trust
- ✅ Explicit approval over implied consent

## TESTING GOVERNANCE

To verify governance is working:
```bash
cd /home/ing/RICK/RICK_LIVE_CLEAN
python3 .agent_governance_lock
# Should show: ✅ Governance validated
```

## EMERGENCY OVERRIDE

**Only the user with PIN 841921 can:**
- Override governance rules
- Modify this instruction file
- Disable git hooks (not recommended)

---

**REMEMBER:** These rules exist to prevent accidental system corruption, folder confusion, and unauthorized changes. They protect the user's work.

**LAST UPDATED:** November 3, 2025  
**VERSION:** 1.0 - Initial Governance Lock  
**AUTHOR:** PIN 841921 Authority
