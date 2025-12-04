<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# RICK PHOENIX: Autonomous Multi-Broker Trading System

**Version**: 2.0  
**PIN**: 841921  
**Status**: PRODUCTION READY ✅  
**Last Updated**: December 2025

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Quick Start](#quick-start)
3. [Architecture & Components](#architecture--components)
4. [Multi-Broker Support](#multi-broker-support)
5. [Trading Features](#trading-features)
6. [Charter Compliance](#charter-compliance)
7. [Dashboard & Monitoring](#dashboard--monitoring)
8. [Installation & Setup](#installation--setup)
9. [Safe Mode Progression](#safe-mode-progression)
10. [Control Tasks](#control-tasks)
11. [Troubleshooting](#troubleshooting)
12. [Documentation Index](#documentation-index)

---

## 🌳 Repository Branch Structure

Due to GitHub's file size limitations, the complete RICK PHOENIX system (94GB) is organized across multiple branches:

### Main Branch
- **master** - Core system, documentation, and reassembly scripts

### Feature Branches
- **feature/core-engines** - Trading engines (OANDA, Coinbase, Ghost, Canary)
- **feature/broker-connectors** - Broker API integrations
- **feature/strategies** - Trading strategies (Bullish Wolf, Bearish Wolf, Sideways Wolf)
- **feature/foundations** - Core logic, charter enforcement, smart logic
- **feature/dashboards** - Web dashboards (Flask & Streamlit)
- **feature/monitoring** - Monitoring, narration, and logging systems
- **feature/hive-mind** - Consensus decision-making system
- **feature/utilities** - Utility modules and helper functions
- **feature/analysis-tools** - Performance analysis scripts
- **feature/testing** - Test suites and validation scripts

### Data Branches
- **data/backtest-results** - Historical backtest data and results
- **data/archived-simulations** - Simulation archives
- **data/logs-historical** - Historical trading logs

### Documentation Branches
- **docs/comprehensive** - Complete system documentation
- **docs/guides** - Setup and operation guides
- **docs/api-reference** - API and integration documentation

### Reassembly Tools
- **REASSEMBLE_SYSTEM.sh** - Automated reassembly script
- **AGENT_REASSEMBLY_PROMPT.md** - Complete instructions for agents/developers

**To get the complete system**: Run `./REASSEMBLE_SYSTEM.sh` after cloning

---

RICK PHOENIX is a charter-compliant, autonomous trading platform that combines advanced algorithmic trading with institutional-grade risk management across multiple brokers and asset classes.

### Core Capabilities

**Multi-Broker Integration**
- ✅ OANDA (Forex/CFDs) - Primary platform
- ✅ Coinbase Advanced (Crypto)
- ✅ Interactive Brokers (Stocks/Options/Futures) - Stub ready

**Trading Intelligence**
- ✅ 130+ Advanced Features (Fibonacci, FVG, Mass Behavior)
- ✅ Stochastic Signal Generation (No TALIB dependencies)
- ✅ Dynamic Leverage (2x-25x based on volatility)
- ✅ ATR-Based Stops with Progressive Trailing
- ✅ OCO Order Management (<300ms latency)
- ✅ Hive Mind Consensus System
- ✅ Machine Learning Model Integration

**Safety & Compliance**
- ✅ Charter Enforcement (Immutable Rules)
- ✅ Guardian Gates & Smart Logic Filters
- ✅ Safe Mode Progression (Paper → Validation → Live)
- ✅ Double PIN Protection (841921)
- ✅ Real-Time Narration & Audit Trail
- ✅ Emergency Shutdown & Position Closure

**Monitoring & Control**
- ✅ Streamlit Dashboard (Real-time metrics & charts)
- ✅ Flask Dashboard (AI narration)
- ✅ VS Code Tasks (Codeless control)
- ✅ WebSocket Streaming
- ✅ Auto-Diagnostic Monitor
- ✅ Daily Performance Audit

---

## 🚀 Quick Start

### System Reassembly (If Cloning from GitHub)

**Important**: This repository is split across multiple branches due to its size (94GB total). To get the complete system:

```bash
# Clone the repository
git clone git@github.com:rfingerlin9284/live_lean_pheonix.git
cd live_lean_pheonix

# Run the reassembly script
chmod +x REASSEMBLE_SYSTEM.sh
./REASSEMBLE_SYSTEM.sh
```

The script will automatically:
- Fetch all feature branches
- Merge core engines, strategies, and utilities
- Restore dashboards and monitoring tools
- Reconstruct the complete file tree

**For detailed reassembly instructions**, see [AGENT_REASSEMBLY_PROMPT.md](AGENT_REASSEMBLY_PROMPT.md)

### Prerequisites
- Python 3.11+ (3.11.9 recommended)
- WSL Ubuntu or Linux
- 4GB RAM minimum
- 100GB disk space (for complete system)

### Step 1: Navigate to Repository
```bash
cd /path/to/live_lean_pheonix
```

### Step 2: Create Virtual Environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.paper .env
nano .env

# Required variables:
OANDA_ACCESS_TOKEN=your_practice_token
OANDA_ACCOUNT_ID=your_account_id
COINBASE_API_KEY=your_key_here
COINBASE_API_SECRET=your_secret_here
```

### Step 5: Start Paper Trading (Safe Mode)
```bash
# OANDA Paper Trading
python3 oanda_trading_engine.py

# OR Coinbase Safe Mode
python3 coinbase_safe_mode_engine.py

# OR Unified System
./start_paper_trading.sh
```

### Step 6: Monitor in Real-Time
```bash
# Plain English Narration
python3 narration_to_english.py

# Live Dashboard
streamlit run dashboard.py
# Opens at: http://localhost:8501
```

### Step 7: Setup Persistent Monitoring Terminals (VSCode)

For the best monitoring experience with auto-refreshing terminals:

```bash
# Quick start guide
./quick_start_terminals.sh

# Verify OANDA scanning
python3 verify_scanning.py

# Verify Coinbase system
python3 verify_coinbase.py
```

**In VSCode**:
1. Open Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Select "Tasks: Run Task"
3. Choose "🎯 Start Two Persistent Terminals"

This sets up:
- **Terminal 1**: System Watchdog (auto-refresh every 30s)
- **Terminal 2**: Live Narration Feed (auto-refresh every 10s)

**Available Engines**:
- 🚀 OANDA Trading Engine (Practice/Live) - Forex trading
- 💰 Coinbase Trading Engine (Safe Mode/Live) - Crypto trading

See [TERMINAL_SETUP_GUIDE.md](TERMINAL_SETUP_GUIDE.md) for OANDA documentation.
See [COINBASE_SETUP_GUIDE.md](COINBASE_SETUP_GUIDE.md) for Coinbase documentation.

**Environment Toggle** (Practice ↔ Live):
- Use VSCode task: "⚙️ Toggle Practice/Live Environment"
- Or edit `.env`: `RICK_ENV=practice` or `RICK_ENV=live`
- Then restart the trading engine

---

## 🏗️ Architecture & Components

### Core System Structure

```
RICK_PHOENIX/
├── foundation/              # Core Trading Logic
│   ├── rick_charter.py     # Immutable charter enforcement (PIN: 841921)
│   ├── margin_correlation_gate.py  # Advanced risk logic
│   └── smart_logic.py      # Intelligent trade filtering
│
├── brokers/                 # Broker Connectors
│   ├── oanda_connector.py  # OANDA API integration
│   ├── coinbase_connection.py  # Coinbase Advanced API
│   └── ib_connector.py     # Interactive Brokers (stub)
│
├── strategies/              # Trading Strategies
│   ├── bullish_wolf.py     # Trend-following long
│   ├── bearish_wolf.py     # Trend-following short
│   └── sideways_wolf.py    # Range-bound trading
│
├── engines/                 # Trading Engines
│   ├── oanda_trading_engine.py     # OANDA autonomous engine
│   ├── coinbase_safe_mode_engine.py  # Coinbase with safe mode
│   ├── ghost_trading_engine.py     # Paper trading simulator
│   └── canary_trading_engine.py    # Extended validation
│
├── hive/                    # Hive Mind System
│   ├── rick_hive_mind.py   # Consensus decision-making
│   └── hive_position_advisor.py  # Position recommendations
│
├── dashboard/               # Web Interfaces
│   ├── app.py              # Flask dashboard (AI narration)
│   └── dashboard_smart.py  # Streamlit dashboard (metrics)
│
├── util/                    # Utilities
│   ├── narration_logger.py # Event logging
│   ├── rick_narrator.py    # Ollama LLM narration
│   ├── mode_manager.py     # System mode control
│   └── rick_live_monitor.py  # Real-time monitoring
│
└── logic/                   # Advanced Logic
    ├── execution_gate.py   # Trade execution validation
    ├── capital_manager.py  # Capital allocation
    └── position_manager.py # Position tracking
```

### Data Flow Architecture

```
Market Data → Stochastic Engine → Charter Validation → Risk Manager
                                                            ↓
                                                    Hive Mind Consensus
                                                            ↓
                                                    Smart Logic Filter
                                                            ↓
                                                    OCO Order Generator
                                                            ↓
                                                    Broker Execution
                                                            ↓
                                            Live Monitor → Dashboard
                                                    ↓
                                            RICK Narrator (LLM)
```

---

## 🌐 Multi-Broker Support

### OANDA (Primary Platform)
**Asset Classes**: Forex (28 pairs), CFDs  
**Features**: Sub-millisecond execution, guaranteed stops, 50:1 leverage  
**Modes**: Practice (paper trading) and Live  

**Configuration**:
```bash
# .env.oanda_only or .env.paper
OANDA_ACCESS_TOKEN=your_practice_token
OANDA_ACCOUNT_ID=your_account_id
OANDA_ENVIRONMENT=practice  # or 'live'
```

**Quick Start**:
```bash
python3 oanda_trading_engine.py
```

### Coinbase Advanced
**Asset Classes**: Crypto (BTC, ETH, SOL, etc.)  
**Features**: Advanced trading API, real-time data, portfolio management  
**Modes**: Paper and Live  

**Configuration**:
```bash
# .env.coinbase_advanced
COINBASE_API_KEY=your_api_key
COINBASE_API_SECRET=your_api_secret
```

**Safe Mode Start**:
```bash
python3 coinbase_safe_mode_engine.py
```

### Interactive Brokers (Coming Soon)
**Asset Classes**: Stocks, Options, Futures, Forex  
**Features**: IB Gateway integration, TWS support  
**Status**: Stub ready for integration  

**Configuration**:
```bash
IB_GATEWAY_HOST=127.0.0.1
IB_GATEWAY_PORT=7497  # Paper: 7497, Live: 7496
```

---

## ⚡ Trading Features

### 1. Advanced Algorithmic Analysis (130+ Features)

**Fibonacci Levels**
- Retracement (23.6%, 38.2%, 50%, 61.8%, 78.6%)
- Extension (127.2%, 161.8%, 200%)
- Auto-detection of swing highs/lows

**Fair Value Gaps (FVG)**
- Bullish/Bearish gap detection
- Volume profile analysis
- Support/resistance confirmation

**Mass Behavior Patterns**
- Crowd psychology indicators
- Sentiment analysis
- Contrarian signal detection

**Momentum Indicators**
- Rate of change (ROC)
- Relative strength
- Divergence detection

### 2. Stochastic Signal Generation

**Pure Stochastic Approach** (No TALIB)
```python
from stochastic_engine import StochasticSignalGenerator

generator = StochasticSignalGenerator()
signal = generator.generate_signal()

# Returns:
{
  'signal': 'BUY',
  'regime': 'bullish',
  'confidence': 0.82,
  'entry_price': 1.0945,
  'stop_loss': 1.0925,
  'take_profit': 1.0985
}
```

**Market Regime Detection**:
- Bullish (35%): Higher probability of BUY signals
- Bearish (25%): Higher probability of SELL signals
- Sideways (40%): Increased HOLD signals

### 3. Dynamic Leverage System

**Formula**:
```
final_leverage = base_leverage × volatility_multiplier × size_multiplier
```

**Volatility Adjustment**:
- High volatility (>60 pips ATR): 0.5x
- Medium volatility (40-60 pips): 0.75x
- Low volatility (<40 pips): 1.0x

**Account Size Adjustment**:
- Account > $50K: 1.2x
- Account > $25K: 1.0x
- Account < $25K: 0.8x

**Hard Limits**:
- Maximum leverage: 20:1
- Minimum leverage: 2:1

### 4. Trailing Stop Logic

**Activation**: On profitable positions with >2x ATR profit

**Progressive Tightening**:
1. Initial: 1.2x ATR
2. At +2x ATR profit: 1.0x ATR
3. At +3x ATR profit: 0.75x ATR
4. At +5x ATR profit: 0.5x ATR

**Take-Profit Cancellation**: TP orders canceled when trailing activates

### 5. OCO Order Management

**Guaranteed Protection**: Every trade includes One-Cancels-Other orders

**Execution Requirements**:
- OCO placement latency: ≤ 300ms
- Guaranteed stop-loss on all positions
- Automatic take-profit targets

**Example**:
```python
# Entry: BUY EUR/USD @ 1.0945
# Stop Loss: 1.0925 (-20 pips, $200 risk)
# Take Profit: 1.0985 (+40 pips, $640 profit)
# Risk:Reward = 3.2:1 ✅
```

### 6. Hive Mind Consensus

**Multi-Agent Decision System**:
- ML Model predictions
- Technical analysis consensus
- Sentiment analysis
- Historical pattern matching

**Consensus Thresholds**:
- 85%+ agreement: Auto-execute (Option A/B)
- 70-84% agreement: Recommend (manual approval)
- <70% agreement: Hold position

**Example Output**:
```
The hive mind analyzed BTC-USD using fresh ML predictions, current market 
data, and news sentiment. Models suggest taking partial profits because 
resistance level reached with increased reversal probability. Recommended 
action is to sell 50% of position to lock in gains while leaving runner 
for potential upside. This maintains charter compliance with 85% confidence.
```

---

## 🔐 Charter Compliance (PIN: 841921)

### Immutable Rules

All trades MUST pass these validation gates:

| Rule | Value | Enforcement |
|------|-------|-------------|
| **Risk-Reward Ratio** | ≥ 3.2:1 | Pre-trade validation |
| **Minimum Notional** | $15,000 USD | Position sizing |
| **Max Hold Duration** | 6 hours | Auto-close timer |
| **Daily Loss Breaker** | -5% | Circuit breaker halt |
| **Max Concurrent Positions** | 3 | Order gate |
| **Max Daily Trades** | 12 | Daily limit counter |
| **Allowed Timeframes** | M15, M30, H1 | Signal filter |
| **Rejected Timeframes** | M1, M5 | Hard block |
| **OCO Latency** | ≤ 300ms | Order execution |
| **FX Spread Gate** | ≤ 0.15x ATR14 | Pre-trade check |
| **Crypto Spread Gate** | ≤ 0.10x ATR14 | Pre-trade check |
| **FX Stop Loss** | 1.2x ATR | Position protection |
| **Crypto Stop Loss** | 1.5x ATR | Position protection |

### Charter Validation

```python
from foundation.rick_charter import RickCharter

# Validate PIN
assert RickCharter.validate_pin(841921)

# Validate risk-reward
assert RickCharter.validate_risk_reward(3.5)  # True
assert RickCharter.validate_risk_reward(3.0)  # False

# Validate notional
assert RickCharter.validate_notional(15000)  # True
assert RickCharter.validate_notional(14999)  # False

# Validate timeframe
assert RickCharter.validate_timeframe("M15")  # True
assert RickCharter.validate_timeframe("M1")   # False
```

---

## 📊 Dashboard & Monitoring

### Streamlit Dashboard

**URL**: `http://localhost:8501`

**Features**:
- Real-time metrics (7 KPIs)
- Interactive equity curves (Plotly)
- Live log viewer with filtering
- Bot control (Start/Stop)
- Broker account integration
- Configuration management
- Auto-refresh capability

**Launch**:
```bash
streamlit run dashboard.py
```

### Flask Dashboard with AI Narration

**URL**: `http://localhost:8080`

**Features**:
- RICK LLM narration (Ollama)
- Mode control panel (OFF/GHOST/CANARY/LIVE)
- Real-time position tracking
- Performance cards
- Chat-like interface
- Emergency stop button

**Launch**:
```bash
python3 dashboard/app.py
```

### Plain English Narration Stream

**Real-time translation of trading events**:
```bash
python3 narration_to_english.py
```

**Example Output**:
```
💵 LIVE TRADE EXECUTED - REAL MONEY

   WHAT: BUY $15,000 of BTC-USD
   WHY: High-probability setup confirmed by Hive Mind consensus
        Technical confluence: FVG support + Fibonacci retracement
        Risk management: Meets charter requirements (RR: 3.5:1)

   HOW: Market order executed at $101,950
        OCO orders placed automatically:
          - Take Profit: $106,000 ($350 profit)
          - Stop Loss: $101,000 ($100 max loss)

   WHEN: 14:32:15
   TIMING: Entry triggered on bullish FVG sweep
   POSITION: Now holding BTC-USD
   MONEY: $15,000 deployed, $350 target profit
```

### Auto-Diagnostic Monitor

**Continuous health monitoring**:
```bash
python3 auto_diagnostic_monitor.py --interval 600
```

**Checks 10 Critical Systems**:
1. API connectivity (Coinbase, OANDA, IBKR)
2. Authentication tokens
3. Logging systems
4. Charter enforcement
5. Gated logic files
6. OCO logic implementation
7. Algo scanning (Fibonacci, FVG, etc.)
8. Hive mind consensus
9. ML models
10. Safe mode progression

---

## 🛠️ Installation & Setup

### Detailed Installation

See [README_ENV_SETUP.md](README_ENV_SETUP.md) for complete setup instructions.

### Environment Variables

**Required for OANDA**:
```bash
OANDA_ACCESS_TOKEN=your_token
OANDA_ACCOUNT_ID=your_account_id
OANDA_ENVIRONMENT=practice  # or 'live'
```

**Required for Coinbase**:
```bash
COINBASE_API_KEY=your_key
COINBASE_API_SECRET=your_secret
```

**System Configuration**:
```bash
RICK_PIN=841921
RICK_DEV_MODE=1  # 1 = dev, 0 = normal
RICK_AGGRESSIVE_PLAN=0  # 1 = aggressive, 0 = conservative
TRADING_ENVIRONMENT=sandbox  # sandbox or live
```

### Security: Encrypted Environment

**Unlock for viewing**:
```bash
./scripts/unlock_env.sh
```

**Edit securely**:
```bash
./scripts/edit_env.sh
```

Uses GPG symmetric encryption (AES256) with PIN protection.

---

## 📈 Safe Mode Progression

### Stage 1: PAPER TRADING

**Status**: No real money, building track record

**Requirements to advance**:
- Win rate ≥ 65%
- Profit factor ≥ 1.8
- Sharpe ratio ≥ 1.5
- Minimum 50 trades
- 7 consecutive profitable days
- Maximum 15% drawdown
- Minimum $10K paper capital managed
- Average daily profit ≥ $200

### Stage 2: SAFE VALIDATION

**Status**: Stricter requirements, proving consistency

**Additional checks**:
- Charter compliance verification
- OCO logic testing
- Risk management validation

### Stage 3: LIVE READY

**Status**: Met all thresholds, awaiting authorization

**Actions**:
- System displays qualification message
- Waits for PIN 841921 authorization
- User must explicitly approve

### Stage 4: LIVE AUTHORIZED

**Status**: Live trading active, real money at risk

**Safety systems engaged**:
- Charter enforcement strict
- OCO protection enabled
- Hive mind monitoring
- Real-time narration active

**Check progress**:
```bash
python3 safe_mode_progress_interactive.py
```

---

## 🎮 Control Tasks (Codeless Operations)

Access via VS Code: `Ctrl+Shift+P` → `Tasks: Run Task`

### Available Tasks

1️⃣ **Check Bot Status** - Show if engines are running  
2️⃣ **Run Full Diagnostic** - 130+ feature health check  
3️⃣ **Emergency Shutdown** - Stop all & close positions  
4A️⃣ **Toggle Coinbase** - ON/OFF  
4B️⃣ **Toggle OANDA** - ON/OFF  
4C️⃣ **Toggle IBKR Gateway** - ON/OFF  
5️⃣ **Update Environment Secrets** - Double PIN required  
6️⃣ **Reassess All Positions** - Hive Mind analysis  
7️⃣ **Daily Replay/Audit** - Performance report  
🔒 **Lock/Unlock Code** - Double PIN protection  
📊 **View Real-Time Narration** - Plain English stream  
🔧 **10-Min Auto Diagnostic** - Background monitoring  
🚀 **Start Safe Mode Engine** - Paper trading  
📈 **View Safe Mode Progress** - Qualification status  
🔄 **Upgrade Manager** - System updates with rollback  
💾 **Create System Snapshot** - Manual backup  
🧠 **Hive Mind Manual Query** - Symbol analysis

See [CODELESS_CONTROL_README.md](CODELESS_CONTROL_README.md) for complete guide.

---

## 🔧 Troubleshooting

### Engine Won't Start

**Check**:
1. Virtual environment active: `source .venv/bin/activate`
2. Dependencies installed: `pip install -r requirements.txt`
3. Environment file exists: `ls -la .env`
4. Credentials configured: `cat .env`
5. Logs for errors: `tail -50 logs/engine.log`

### Narration Not Updating

**Check**:
1. Engine running: `pgrep -af trading_engine`
2. Narration file exists: `ls -la logs/narration.jsonl`
3. File being written: `tail -f logs/narration.jsonl`

### Dashboard Not Loading

**Flask Dashboard**:
```bash
# Check port 8080
lsof -i :8080

# Kill if needed
kill -9 $(lsof -t -i:8080)

# Restart
python3 dashboard/app.py
```

**Streamlit Dashboard**:
```bash
# Check backend
curl http://127.0.0.1:8000/api/health

# Hard refresh browser
# Ctrl+F5
```

### API Authentication Failing

**OANDA**:
```bash
# Test connection
curl -H "Authorization: Bearer $OANDA_ACCESS_TOKEN" \
     https://api-fxpractice.oanda.com/v3/accounts/$OANDA_ACCOUNT_ID
```

**Coinbase**:
```bash
python3 test_coinbase_auth_fixed.py
```

---

## 📚 Documentation Index

### Quick Start Guides
- [START_HERE.md](START_HERE.md) - Complete delivery summary
- [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Fast setup guide
- [TEAM_QUICK_START.md](TEAM_QUICK_START.md) - Team onboarding

### Setup & Configuration
- [README_ENV_SETUP.md](README_ENV_SETUP.md) - Environment configuration
- [ENV_README.md](ENV_README.md) - Secure env workflow
- [README_DEPLOYMENT.md](README_DEPLOYMENT.md) - Deployment guide
- [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) - Docker setup

### System Documentation
- [README_UNIFIED_SYSTEM.md](README_UNIFIED_SYSTEM.md) - Unified system manual
- [SAFETY_CHARTER.md](SAFETY_CHARTER.md) - Charter rules
- [SYSTEM_PROTECTION_ADDENDUM.md](SYSTEM_PROTECTION_ADDENDUM.md) - Protection rules
- [MULTI_BROKER_ARCHITECTURE.md](MULTI_BROKER_ARCHITECTURE.md) - Broker integration

### Features & Capabilities
- [CODELESS_CONTROL_README.md](CODELESS_CONTROL_README.md) - Control tasks guide
- [ANALYSIS_TOOLS_README.md](ANALYSIS_TOOLS_README.md) - Analysis scripts
- [RBOTZILLA_STREAMLIT_README.md](RBOTZILLA_STREAMLIT_README.md) - Dashboard guide
- [ALL_INTERFACES_GUIDE.md](ALL_INTERFACES_GUIDE.md) - Interface documentation

### Operation Guides
- [PAPER_README.md](PAPER_README.md) - Paper trading setup
- [CANARY_MODE_SETUP.md](CANARY_MODE_SETUP.md) - Validation mode
- [LIVE_TRADING_ACTIVATED.md](LIVE_TRADING_ACTIVATED.md) - Live trading
- [MONITORING_QUICK_REFERENCE.md](MONITORING_QUICK_REFERENCE.md) - Monitoring guide

### Reference
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Complete index
- [FILE_REFERENCE_INDEX.md](FILE_REFERENCE_INDEX.md) - File reference
- [ESSENTIALS_MANIFEST.txt](ESSENTIALS_MANIFEST.txt) - Essential files list

---

## 🎯 System Protection

### Immutable Files (Read-Only)

Protected files require **double PIN** (841921, twice) to modify:
- `foundation/rick_charter.py`
- `coinbase_safe_mode_engine.py`
- `hive/rick_hive_mind.py`
- `logic/smart_logic.py`
- `safe_mode_manager.py`
- `oanda_trading_engine.py`
- `brokers/oanda_connector.py`

**Lock/Unlock**:
```bash
python3 pin_protection.py --lock    # Lock (444 permissions)
python3 pin_protection.py --unlock  # Unlock (644 permissions)
```

### What Agents CANNOT Do

❌ Create/rename/delete files affecting live trading  
❌ Modify code without double PIN  
❌ Execute terminal commands interfering with trading  
❌ Bypass charter enforcement  
❌ Disable logging/narration  
❌ Change environment variables without authorization

### Rollback Protection

**Create snapshot before changes**:
```bash
python3 create_snapshot.py
```

**Restore from snapshot**:
```bash
ls -la ROLLBACK_SNAPSHOTS/
cp -r ROLLBACK_SNAPSHOTS/pre_upgrade_YYYYMMDD/ .
```

---

## 📞 Support & Resources

### Health Checks
```bash
# System status
python3 status_report.py

# Charter compliance
python3 -c "from foundation.rick_charter import RickCharter; print(RickCharter.get_charter_summary())"

# Active positions
python3 check_portfolio.py
```

### Log Locations
```
logs/
├── narration.jsonl              # Event narration
├── engine.log                   # Engine logs
├── oanda_engine.log             # OANDA logs
├── coinbase_engine.log          # Coinbase logs
├── dashboard.log                # Dashboard logs
├── safe_mode_performance.json   # Progress tracking
└── canary_trading_report.json   # Validation results
```

### Emergency Stop
```bash
# Immediate halt
killall python3

# Or use dashboard emergency button
# Or run task: RICK: 3️⃣ Emergency Shutdown
```

---

## 📄 License & Legal

**System**: RICK PHOENIX Autonomous Trading System v2.0  
**Charter PIN**: 841921  
**Classification**: Proprietary Trading System  

⚠️ **Risk Disclaimer**: This system trades financial instruments with real money. Past performance does not guarantee future results. Only trade with capital you can afford to lose.

---

## 🚀 Ready to Trade

**Start with paper trading, build a track record, and graduate to live trading when the system proves itself.**

### Quick Commands
```bash
# Paper Trading
./start_paper_trading.sh

# View Narration
python3 narration_to_english.py

# Dashboard
streamlit run dashboard.py

# Check Status
python3 check_bot_status_interactive.py

# Daily Audit
python3 daily_replay_audit.py
```

**Good luck and happy trading! 🚀📈**

---

**END OF README**  
**Last Updated**: December 4, 2025  
**System Status**: PRODUCTION READY ✅
