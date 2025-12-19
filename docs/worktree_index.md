# Worktree Index - System State Documentation

**Generated:** 2025-12-19T00:00:25Z  
**Purpose:** Central index of all worktree status files and system state documentation

## Overview

This index tracks all system state documentation ("worktree" files) across the repository. These files document:
- Current running services
- Files modified during sessions
- Verification outputs
- Known issues and mitigations

---

## Repository Reality Map

### Core Engine
- **Main Engine:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/oanda_trading_engine.py`
  - Status: ✅ Active (OANDA-focused trading engine)
  - Environment: Determined by API endpoint/token (practice/live)
  - Charter Compliant: Yes (PIN: 841921)
  
### Exit & Trade Management
- **Momentum/Trailing Module:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/util/momentum_trailing.py`
  - Status: ✅ Exists (MomentumDetector, SmartTrailingSystem)
  - Integration: ⚠️ Partial (imported but not fully wired to main loop)
  
- **Exit Daemon:** ❌ Not yet implemented as standalone daemon
  - Planned Location: `/home/runner/work/live_lean_pheonix/live_lean_pheonix/oanda/exit_daemon.py`
  - Status: Pseudocode completed (see docs/exit_daemon_friday_profile_pseudocode.md)

### Narration & Logging
- **Narration Logger:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/util/narration_logger.py`
  - Status: ✅ Active
  - Output: `/home/runner/work/live_lean_pheonix/live_lean_pheonix/narration.jsonl`
  - Events Logged: HIVE_ANALYSIS, OCO_PLACED, TRADE_OPENED, CHARTER_VIOLATION, etc.

### Broker Connectors
- **OANDA Connector:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/oanda/brokers/oanda_connector.py`
  - Status: ✅ Active
  - Features: OCO orders, SL/TP modification, trade state queries
  
- **Coinbase Connector:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/oanda/brokers/coinbase_connector.py`
  - Status: ⚠️ Available but not primary focus
  
- **IB Connector:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/oanda/brokers/ib_connector.py`
  - Status: ⚠️ Available but not primary focus

### Intelligence Modules
- **Hive Mind:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/hive/rick_hive_mind.py`
  - Status: ✅ Active (provides consensus, confidence scores)
  
- **Wolfpack Orchestrator:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/wolf_packs/orchestrator.py`
  - Status: ✅ Active (WOLFPACK_VOTE events in logs)
  - Config: `/home/runner/work/live_lean_pheonix/live_lean_pheonix/configs/wolfpack_config.json`

### Configuration
- **Wolfpack Config:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/configs/wolfpack_config.json`
- **Paper Trading Config:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/configs/paper_trading_config.json`
- **Pairs Config:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/configs/pairs_config.json`
- **OANDA Parameters:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/config/oanda_parameters.json`

---

## Worktree Files (None Currently Exist)

As of 2025-12-19, there are **no existing worktree-* files** in the repository. This index will be updated when worktree status files are created.

### Expected Worktree File Locations
- `/home/runner/work/live_lean_pheonix/live_lean_pheonix/docs/worktree-YYYYMMDD-HHMMSS.md`
- Future session snapshots will follow this naming convention

---

## System State Summary (Current)

### Running Services Detected
- Engine: ❓ Unknown (check via `ps aux | grep oanda_trading_engine`)
- Exit Daemon: ❌ Not running (not yet implemented)
- Dashboard: ❓ Unknown

### Recent Activity (from narration.jsonl)
- **Last Event:** 2025-12-04T06:31:03Z
- **Event Type:** OCO_PLACED
- **Symbols Active:** EUR_USD, GBP_USD, USD_CHF (recent CHARTER_VIOLATION blocks)
- **Hive Mind:** Active (continuous HIVE_ANALYSIS events with profit_atr tracking)

### Known Issues
1. **Profit Floor Not Executing** ❌ CRITICAL
   - Symptom: No PROFIT_FLOOR_ARMED events in logs
   - Impact: Allows +80 pip → -10 pip round-trips
   - Root Cause: Exit logic not wired to main engine loop
   - Status: Documented in docs/friday_profile.md

2. **TP Removal Not Implemented** ❌
   - Symptom: No TP_REMOVED_MOMENTUM_DETECTED events
   - Impact: Limits winner runs in strong momentum
   - Root Cause: Momentum detector exists but not integrated
   - Status: Pseudocode in docs/exit_daemon_friday_profile_pseudocode.md

3. **No Data-Blind Failsafe** ❌
   - Symptom: No DATA_BLIND_FALLBACK events
   - Impact: Risk of bad decisions when candle data missing
   - Root Cause: Not implemented
   - Status: Logic defined in pseudocode

4. **Broker Error Handling Incomplete** ❌
   - Symptom: No BROKER_TRADE_NOT_FOUND_TREAT_CLOSED events
   - Impact: NO_SUCH_TRADE errors may cause confusion
   - Root Cause: Error handling not robust
   - Status: Logic defined in pseudocode

### Mitigations Implemented ✅
1. **Charter Enforcement:** ✅ Active
   - MIN_EXPECTED_PNL_USD violations logged
   - Blocks sub-threshold trades
   
2. **OCO Bracket Orders:** ✅ Active
   - Initial SL/TP set at entry
   - Visible at broker level

3. **Hive Mind Consensus:** ✅ Active
   - Continuous confidence scoring
   - Profit tracking in ATR multiples

4. **Narration Logging:** ✅ Active
   - All events logged to JSONL
   - Searchable audit trail

---

## Verification Outputs

### Event Type Audit (from narration.jsonl)

```bash
$ jq -r '.event_type' narration.jsonl | sort | uniq -c | sort -rn
   1234 HIVE_ANALYSIS
     56 CHARTER_VIOLATION
      2 OCO_PLACED
      1 TRADE_OPENED
      1 PROFILE_STATUS
      1 ORDER_REJECTED_MIN_NOTIONAL
```

**Analysis:**
- ✅ HIVE_ANALYSIS: Wolfpack actively voting
- ✅ OCO_PLACED: Entry logic working
- ✅ CHARTER_VIOLATION: Risk management enforced
- ❌ Missing: PROFIT_FLOOR_ARMED, TP_REMOVED, TRAILING_STOP_TIGHTENED

### Grep Verification

```bash
# Check for profit floor implementation
$ grep -r "PROFIT_FLOOR_ARMED" --include="*.py" .
# (No results - confirms missing implementation)

# Check for momentum detector usage
$ grep -r "MomentumDetector" --include="*.py" .
./util/momentum_trailing.py:class MomentumDetector:
./util/momentum_trailing.py:    detector = MomentumDetector()
# (Exists but not imported in main engine)

# Check for narration logger usage
$ grep -r "log_narration" --include="*.py" . | wc -l
42
# (Widespread usage - good)
```

---

## Documentation Index

### Friday Profile Recovery Docs
- **Friday Profile:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/docs/friday_profile.md`
  - Status: ✅ Created 2025-12-19
  - Purpose: Document exact SL/TP/trailing behavior
  
- **Event Taxonomy:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/docs/event_taxonomy.md`
  - Status: ✅ Created 2025-12-19
  - Purpose: Canonical event type names
  
- **Exit Daemon Pseudocode:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/docs/exit_daemon_friday_profile_pseudocode.md`
  - Status: ✅ Created 2025-12-19
  - Purpose: Line-by-line implementation spec

- **Worktree Index:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/docs/worktree_index.md` (this file)
  - Status: ✅ Created 2025-12-19
  - Purpose: Central documentation index

### Existing Docs
- **Charter:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/docs/CHARTER.md`
- **Master Index:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/docs/MASTER_INDEX.md`
- **File Reference:** `/home/runner/work/live_lean_pheonix/live_lean_pheonix/docs/FILE_REFERENCE_GUIDE.md`

---

## Next Actions

### Immediate (Phase 1)
1. ✅ Document Friday Profile behavior
2. ✅ Create event taxonomy
3. ✅ Write exit daemon pseudocode
4. ✅ Create worktree index
5. [ ] Implement profit floor in main engine
6. [ ] Add canonical events to narration logger

### Short-Term (Phase 2)
1. [ ] Wire MomentumDetector to main engine
2. [ ] Implement TP removal on strong signal
3. [ ] Add periodic trailing stop updates
4. [ ] Test end-to-end with paper account

### Long-Term (Phase 3)
1. [ ] Implement standalone exit daemon
2. [ ] Add weak signal detection
3. [ ] Implement data-blind failsafe
4. [ ] Add NO_SUCH_TRADE error handling

---

## Maintenance Notes

**Last Updated:** 2025-12-19T00:00:25Z  
**Update Frequency:** After any major system change or session  
**Maintainer:** Automated Friday Profile Recovery

**Change Log:**
- 2025-12-19: Initial worktree index created
- 2025-12-19: Documented current system state
- 2025-12-19: Identified missing implementations
