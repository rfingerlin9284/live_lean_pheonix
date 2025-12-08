# Files Organized by Category - live_lean_pheonix

This document provides a categorized view of all files in the repository for easier navigation and understanding.

## 📊 Repository Statistics

- **Total Files**: 6,681
- **Python Files**: 2,664
- **Documentation Files**: 778 (Markdown)
- **Configuration Files**: 283 (JSON) + 13 (YAML)
- **Shell Scripts**: 275
- **Test Files**: Extensive test coverage across multiple directories

---

## 🐍 Python Files by Component

### Trading Engines
- `oanda_trading_engine.py` - OANDA trading platform integration
- `rick_trading_engine.py` - Rick autonomous trading system
- `canary_trading_engine.py` - Canary/staging environment engine
- `rbotzilla_engine.py` - RBotZilla trading automation
- `ghost_trading_engine.py` - Ghost trading mode
- `live_ghost_engine.py` - Live ghost trading
- `safe_trading_engine.py` - Safety-focused trading
- `paper_trading_engine.py` - Paper trading simulation
- `multi_broker_engine.py` - Multi-broker orchestration

### Core Systems
- `systems/momentum_signals.py` - Momentum-based signal generation
- `systems/` directory - Various trading systems and strategies
- `core/` - Core system functionality
- `foundation/` - Foundational modules

### Risk Management
- `risk/session_breaker.py` - Session breaker for risk control
- `risk/session_breaker_integration.py` - Session breaker integration
- `position_manager.py` - Position sizing and management
- `capital_manager.py` - Capital allocation
- `execution_gate.py` - Trade execution gating

### Monitoring & Dashboard
- `dashboard.py` - Main monitoring dashboard
- `dashboard_smart.py` - Smart dashboard with AI
- `dashboard_supervisor.py` - Dashboard supervision
- `hive_mind_bridge.py` - Hive mind connection
- `system_watchdog.py` - System health monitoring
- `live_monitor.py` - Live trading monitor

### Backtesting & Analysis
- `comprehensive_backtest_engine.py` - Comprehensive backtesting
- `analyze_trades.py` - Trade analysis
- `analyze_opportunities.py` - Opportunity analysis
- `analyze_full_performance.py` - Performance metrics

### Utilities & Tools
- `safe_mode_manager.py` - Safe mode controls
- `rollback_manager_interactive.py` - System rollback
- `auth_manager.py` - Authentication management
- `load_env.py` - Environment loader
- `progress_manager.py` - Progress tracking

---

## 📚 Documentation Files

### Quick Start & Guides
- `README.md` - Main repository documentation
- `START_HERE.md` - Getting started guide
- `QUICK_START_GUIDE.md` - Quick reference
- `QUICK_REFERENCE.md` - Command reference
- `TEAM_QUICK_START.md` - Team onboarding

### Architecture & Design
- `PHOENIX_V2_ARCHITECTURE.md` - Phoenix V2 architecture
- `MULTI_BROKER_ARCHITECTURE.md` - Multi-broker design
- `SYSTEM_DIAGRAM.md` - System architecture diagram
- `COMPLETE_ALGORITHM_WORKFLOW_DECISION_BLUEPRINT.md` - Algorithm workflow

### Deployment & Operations
- `DEPLOYMENT_READINESS.md` - Deployment checklist
- `LIVE_TRADING_ACTIVATED.md` - Live trading setup
- `PAPER_TRADING_ACTIVE.md` - Paper trading configuration
- `AUTOMATED_TRADING_SETUP_GUIDE.md` - Setup instructions

### Analysis & Reports
- `COMPREHENSIVE_SYSTEM_AUDIT_REPORT.md` - System audit
- `CURRENT_SYSTEM_STATE_REPORT.md` - Current state
- `SESSION_ACTIVITY_REPORT_*.md` - Session reports
- `BACKTEST_ANALYSIS_EXECUTIVE_SUMMARY.md` - Backtest results

### Agent & AI
- `AGENT_CHARTER_v2.md` - Agent charter
- `AGENT_CODELESS_MANDATE.md` - Codeless control mandate
- `RICK_PERSONALITY_HARDWIRING.md` - Rick AI personality
- `INSTITUTIONAL_CHARTER_DEPLOYMENT.md` - Institutional rules

---

## ⚙️ Configuration Files

### Environment Configuration
- `.env` - Main environment variables
- `.env.live` - Live trading environment
- `.env.paper` - Paper trading environment
- `.env.ci_temp` - CI/CD temporary config

### System Configuration
- `config/` - Configuration directory
- `configs/` - Additional configurations
- Various `.json` files for system settings
- `.yaml` files for structured configuration

---

## 🧪 Test Files

### Test Directories
- `tests/` - Main test suite
- `PhoenixV2/tests/` - Phoenix V2 tests
- `config/tests/` - Configuration tests

### Specific Test Files
- `test_oanda_session_fix.py` - OANDA session tests
- `test_oanda_enhanced.py` - Enhanced OANDA tests
- `test_live_auth.py` - Authentication tests
- `test_integration.py` - Integration tests
- `tests/test_session_breaker.py` - Session breaker tests

---

## 🔧 Shell Scripts

### System Control
- `start_paper_trading.sh` - Start paper trading
- `start_phoenix.sh` - Start Phoenix system
- `stop_phoenix.sh` - Stop Phoenix system
- `safe_shutdown.sh` - Safe system shutdown

### Monitoring
- `monitor_narration.sh` - Monitor narration logs
- `monitor_paper_trading.sh` - Monitor paper trading
- `view_live_narration.sh` - View live logs

### Deployment
- `deploy_institutional_charter.py` - Deploy charter
- `launch_*.sh` - Various launch scripts
- `install_*.sh` - Installation scripts

### Utilities
- `check_system_status.py` - System status check
- `diagnose_ib_connection.sh` - IB diagnostics
- `verify_*.sh` - Verification scripts

---

## 📁 Backup & Archive Files

### Rollback Snapshots
- `ROLLBACK_SNAPSHOTS/crypto_live_backup_*/` - Crypto backups
- `ROLLBACK_SNAPSHOTS/live_backup_*/` - Live system backups
- `.progress_backups/` - Progress snapshots

### Archived Code
- `_archive_docs/` - Archived documentation
- `_archive_scripts/` - Archived scripts
- `_legacy_code/` - Legacy implementations

---

## 🔍 Session Management Files

**Critical for resolving session-related issues:**

1. **Session Breaker System**
   - `risk/session_breaker.py`
   - `risk/session_breaker_integration.py`
   - `tests/test_session_breaker.py`

2. **Session Monitoring**
   - `scripts/monitor_ghost_session.py`
   - `test_oanda_session_fix.py`

3. **Session in External Packages**
   - `a_zip_file_segments/rick_system_zip/openalgo-openalgo-theme/openalgo-openalgo-theme/utils/session.py`
   - `a_zip_file_segments/rick_system_zip/openalgo-openalgo-theme/openalgo-main/utils/session.py`

**Note:** No standalone `session.py` module found in main source tree, which explains the `ModuleNotFoundError: No module named 'session'` error.

---

## 🎯 Files Needing Attention (Based on Error Reports)

### Session Module Issues
- **Error**: `ModuleNotFoundError: No module named 'session'`
- **Affected File**: Likely `oanda_trading_engine.py`
- **Action Needed**: Create session module or fix import path

### RuntimeProfile Issues  
- **Error**: `'RuntimeProfile' object has no attribute 'is_session_active'`
- **Affected Component**: Runtime profile management
- **Action Needed**: Add `is_session_active` attribute/method to RuntimeProfile class

---

## 📋 Additional Inventory Files

This document is part of a comprehensive file organization effort:

1. `FILE_INVENTORY_SORTED.md` - Comprehensive file statistics and categorization
2. `ALL_FILES_ALPHABETICAL.txt` - Complete alphabetical file listing
3. `DIRECTORY_TREE.txt` - Directory structure visualization
4. `FILES_BY_CATEGORY.md` - This file (categorical organization)

---

*Generated: 2025-12-08 for repository navigation and issue resolution*
