# 📚 File Inventory Index - Quick Navigation Guide

**Repository:** live_lean_pheonix  
**Generated:** 2025-12-08  
**Purpose:** Complete file organization and navigation for troubleshooting and development

---

## 🎯 Quick Access to Inventory Documents

This repository now includes **four comprehensive file inventory documents** to help you navigate the 6,681 files:

### 1️⃣ [FILE_INVENTORY_SORTED.md](FILE_INVENTORY_SORTED.md)
**Best for:** Overview and statistics
- ✅ Summary statistics (file counts, types)
- ✅ Files grouped by extension
- ✅ Key directories explained
- ✅ Critical files highlighted
- ✅ Session management files identified
- ✅ Recommendations for fixing errors

### 2️⃣ [ALL_FILES_ALPHABETICAL.txt](ALL_FILES_ALPHABETICAL.txt)
**Best for:** Finding a specific file
- ✅ Complete list of 6,681 files
- ✅ Alphabetically sorted
- ✅ Numbered list for reference
- ✅ Full relative paths

### 3️⃣ [DIRECTORY_TREE.txt](DIRECTORY_TREE.txt)
**Best for:** Understanding repository structure
- ✅ Visual directory tree
- ✅ Component descriptions
- ✅ Organized by functional area
- ✅ Quick reference for major directories

### 4️⃣ [FILES_BY_CATEGORY.md](FILES_BY_CATEGORY.md)
**Best for:** Finding files by purpose
- ✅ Trading engines categorized
- ✅ Testing files grouped
- ✅ Documentation organized
- ✅ Configuration files listed
- ✅ Scripts by function

---

## 🔍 How to Use This Index

### If you want to...

#### 📊 **See overall statistics**
→ Open [FILE_INVENTORY_SORTED.md](FILE_INVENTORY_SORTED.md)

#### 🔎 **Find a specific file by name**
→ Search in [ALL_FILES_ALPHABETICAL.txt](ALL_FILES_ALPHABETICAL.txt)

#### 🗂️ **Understand the directory structure**
→ Read [DIRECTORY_TREE.txt](DIRECTORY_TREE.txt)

#### 🏷️ **Find files by category or purpose**
→ Browse [FILES_BY_CATEGORY.md](FILES_BY_CATEGORY.md)

#### 🐛 **Debug session-related errors**
→ See "Session Management Files" section in [FILE_INVENTORY_SORTED.md](FILE_INVENTORY_SORTED.md)

#### 🧪 **Locate test files**
→ Check "Test Files" section in [FILES_BY_CATEGORY.md](FILES_BY_CATEGORY.md)

#### 📝 **Find documentation**
→ See "Documentation Files" section in [FILES_BY_CATEGORY.md](FILES_BY_CATEGORY.md)

---

## 🚨 Troubleshooting Issues from Problem Statement

Based on the reported errors, here's what was found:

### ❌ Issue 1: `ModuleNotFoundError: No module named 'session'`

**Finding:** No standalone `session.py` module exists in the main source directories.

**Session-related files found:**
- `risk/session_breaker.py` - Session breaker for risk management
- `risk/session_breaker_integration.py` - Session breaker integration
- `test_oanda_session_fix.py` - OANDA session fix tests
- `tests/test_session_breaker.py` - Session breaker tests
- `scripts/monitor_ghost_session.py` - Ghost session monitoring

**Recommendation:** 
- Check if `oanda_trading_engine.py` is trying to import a non-existent `session` module
- May need to create the module or update import paths
- Session functionality may be embedded in other modules

### ❌ Issue 2: `'RuntimeProfile' object has no attribute 'is_session_active'`

**Finding:** Need to investigate RuntimeProfile class implementation.

**Files to check:**
- `oanda_trading_engine.py` - Main OANDA engine
- Files in `/core/` directory
- Files in `/foundation/` directory
- Profile-related modules

**Recommendation:**
- Add `is_session_active` attribute or method to RuntimeProfile class
- Verify session status management logic
- Check practice mode session handling (per repository memories)

---

## 📈 Repository Statistics

| Metric | Value |
|--------|-------|
| Total Files | 6,681 |
| Python Files (.py) | 2,664 |
| Documentation (.md) | 778 |
| Shell Scripts (.sh) | 275 |
| JSON Configs (.json) | 283 |
| Test Files | 100+ |
| Backup Snapshots | 4 major snapshots |

---

## 🗺️ Major Components Map

### Trading & Execution
- `/oanda/` - OANDA broker integration
- `/brokers/` - Multi-broker support
- `/engines/` - Trading engines
- `/systems/` - Trading systems
- `/strategies/` - Strategy implementations

### Risk & Portfolio
- `/risk/` - Risk management
- `position_manager.py` - Position sizing
- `capital_manager.py` - Capital allocation
- `execution_gate.py` - Trade gating

### Monitoring & Operations
- `/dashboard/` - Web dashboards
- `dashboard.py` - Main dashboard
- `system_watchdog.py` - System monitoring
- `live_monitor.py` - Live monitoring

### Development & Testing
- `/tests/` - Main test suite
- `/PhoenixV2/tests/` - Phoenix V2 tests
- Various test_*.py files throughout

### Configuration & Data
- `/config/` - Configurations
- `/data/` - Data files
- `.env*` files - Environment configs

---

## 🎓 Best Practices for Navigation

1. **Start with the Index** (this file) to understand what's available
2. **Use FILE_INVENTORY_SORTED.md** for high-level overview
3. **Search ALL_FILES_ALPHABETICAL.txt** when you know the filename
4. **Browse FILES_BY_CATEGORY.md** when looking for functionality
5. **Reference DIRECTORY_TREE.txt** to understand relationships

---

## 🔄 Maintenance

These inventory files were generated on 2025-12-08. As the repository grows:

1. Re-run the inventory generation scripts
2. Update statistics in this index
3. Keep categorization current
4. Document new major components

---

## 📞 Need Help?

- For session issues: See [FILE_INVENTORY_SORTED.md](FILE_INVENTORY_SORTED.md) → "Session Management Files"
- For general overview: See [FILE_INVENTORY_SORTED.md](FILE_INVENTORY_SORTED.md)
- For specific file: Search [ALL_FILES_ALPHABETICAL.txt](ALL_FILES_ALPHABETICAL.txt)
- For structure: See [DIRECTORY_TREE.txt](DIRECTORY_TREE.txt)
- For categories: See [FILES_BY_CATEGORY.md](FILES_BY_CATEGORY.md)

---

**All files sorted, categorized, and documented! ✅**

*This inventory suite provides complete visibility into the repository structure for efficient development and troubleshooting.*
