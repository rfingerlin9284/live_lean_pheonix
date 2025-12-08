# Comprehensive File Inventory - live_lean_pheonix Repository

**Generated:** 2025-12-08  
**Total Files:** 6,681 (excluding .git directory)  
**File Types:** 86 different extensions

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total Files | 6,681 |
| File Types | 86 |
| Python Files (.py) | 2,664 |
| Markdown Files (.md) | 778 |
| JSON Files (.json) | 283 |
| Shell Scripts (.sh) | 275 |

---

## Files by Type (Top 20)

| Extension | Count | Description |
|-----------|-------|-------------|
| .py | 2,664 | Python source files |
| .identifier | 1,922 | Zone identifier files |
| .md | 778 | Markdown documentation |
| .json | 283 | JSON configuration/data files |
| .sh | 275 | Shell scripts |
| .html | 163 | HTML files |
| .txt | 103 | Text files |
| no_extension | 46 | Files without extensions |
| .png | 46 | PNG images |
| .js | 45 | JavaScript files |
| .bru | 42 | Bruno API test files |
| .zip | 30 | Compressed archives |
| .tsx | 28 | TypeScript React files |
| .ts | 23 | TypeScript files |
| .css | 20 | Cascading Style Sheets |
| .svelte | 15 | Svelte framework files |
| .yaml | 13 | YAML configuration files |
| .csv | 10 | CSV data files |
| .jsonl | 8 | JSON Lines files |
| .gz | 8 | Gzip compressed files |

---

## Key Directories Structure

### Root Level
- **Documentation**: Extensive markdown documentation (778+ .md files)
- **Scripts**: Shell scripts for automation (275+ .sh files)
- **Python Modules**: 2,664 Python source files
- **Configuration**: JSON, YAML, and environment files

### Main Components

#### `/oanda/`
- OANDA trading platform integration
- Session management
- Trading engine implementations

#### `/systems/`
- Trading systems and strategies
- Signal generation
- Algorithm implementations

#### `/tests/`
- Comprehensive test suites
- Unit and integration tests
- Test fixtures and utilities

#### `/brokers/`
- Multi-broker support
- Connector implementations
- API integrations

#### `/risk/`
- Risk management modules
- Session breakers
- Position sizing

#### `/dashboard/`
- Web-based monitoring interfaces
- Real-time data visualization
- System status displays

#### `/scripts/`
- Utility scripts
- Deployment automation
- Monitoring tools

#### `/PhoenixV2/` and `/PHOENIX_V2/`
- Version 2 implementation
- Enhanced architecture
- Modular components

#### `/ROLLBACK_SNAPSHOTS/`
- System state backups
- Configuration snapshots
- Recovery points

---

## Critical Files

### Trading Engine
- `oanda_trading_engine.py` - Main OANDA trading engine
- `rick_trading_engine.py` - Rick trading system
- `canary_trading_engine.py` - Canary mode engine
- `rbotzilla_engine.py` - RBotZilla trading system

### Configuration
- `.env` - Environment variables
- `.env.live` - Live trading configuration
- `.env.paper` - Paper trading configuration
- `requirements.txt` - Python dependencies

### System Management
- `dashboard.py` - Main dashboard application
- `system_watchdog.py` - System monitoring
- `safe_mode_manager.py` - Safety controls

### Documentation
- `README.md` - Main documentation
- `START_HERE.md` - Getting started guide
- `QUICK_START_GUIDE.md` - Quick reference

---

## Session Management Files

Based on the analysis request, here are the session-related files:

1. `test_oanda_session_fix.py` - OANDA session fix tests
2. `risk/session_breaker.py` - Session breaker risk management
3. `risk/session_breaker_integration.py` - Session breaker integration
4. `tests/test_session_breaker.py` - Session breaker tests
5. `scripts/monitor_ghost_session.py` - Ghost session monitoring

**Note:** The repository does not appear to have a standalone `session.py` module at the root level or in the main source directories, which may be the cause of the "ModuleNotFoundError: No module named 'session'" error reported in the problem statement.

---

## RuntimeProfile Investigation

Files that may contain RuntimeProfile class:
- Check `oanda_trading_engine.py`
- Check profile-related modules in `/core/` and `/foundation/`
- Check runtime management files

---

## Backup and Archive Structure

The repository maintains extensive backups:
- `.progress_backups/` - Progress snapshots
- `ROLLBACK_SNAPSHOTS/` - System rollback points
- Multiple `.bak` and `.backup` files throughout

---

## Next Steps for Issue Resolution

Based on the problem statement mentioning:
1. **ModuleNotFoundError: No module named 'session'**
2. **RuntimeProfile object has no attribute 'is_session_active'**

### Recommendations:
1. Create or locate the missing `session.py` module
2. Update RuntimeProfile class to include `is_session_active` attribute/method
3. Review `oanda_trading_engine.py` for proper session management imports
4. Verify session management integration across all trading engines

---

## File Organization Notes

- **High file count** (6,681 files) suggests comprehensive system
- **Multiple backup versions** indicate active development
- **Extensive documentation** (778 markdown files) shows good practices
- **Test coverage** appears comprehensive with dedicated test directories
- **Multi-platform support** evidenced by both .sh and .bat files

---

*This inventory was generated automatically to provide a comprehensive overview of the repository structure for debugging and development purposes.*
