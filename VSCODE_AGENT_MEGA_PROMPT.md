# RBOTZILLA PHOENIX — VS CODE AGENT REBUILD MEGA PROMPT

**PURPOSE**: This document is written for a VS Code AI agent to rebuild the complete RBOTZILLA trading system on a brand-new local computer using only proven, debugged code that already exists in the GitHub repos listed below. The agent must read every instruction carefully and work through each step in order. No new code is to be invented. No placeholders. No simulation modes. Every connection must be live and real.

**HOW TO TALK TO THE USER**: Always reply in simple plain English. Do not paste JSON blocks, code snippets, or terminal output into the chat. When something works, say "Done — that step is complete." When something fails, describe what went wrong in plain English and ask what you need from the user to continue.

---

## QUICK REFERENCE — ALL SOURCE REPOS

All code must come from these GitHub repositories owned by `rfingerlin9284`:

| Repo Name | What It Provides |
|---|---|
| `rick_clean_live` | Primary working codebase — brokers, wolf packs, strategies, monitoring scripts |
| `Rbotzilla_pheonix_v1` | All five strategy files, .env template, additional scripts |
| `RBOTZILLA_FINAL_v001` | Foundation charter, risk management, swarm bot, utility modules, canary/ghost engines |
| `FROZEN-V2` | Research-grade backtest engine with CI, regime detection |
| `multi_broker_rbtz` | Production deployment v2.0 tarball (128 files), deployment docs |
| `MULTIBROKER_ESSENTIALS_ONLY` | Build tools, deployment scripts, verification tooling |
| `RICK_LIVE_CLEAN_FROZEN` | Golden frozen version — additional utility scripts |
| `FROZEN-V2` | Canonical backtest engine, Risk Brain, pack runner |

---

## PHASE 1 — COMPUTER SETUP

### Step 1 — Install Python

Tell the user: "We need Python 3.11 or newer on your computer. I will check if it is already there."

Run this check: `python3 --version`

If Python 3.11 or newer is already installed, move to Step 2. If it is not installed, tell the user: "Please download Python 3.11 from python.org and run the installer. Make sure to check the box that says 'Add Python to PATH' during installation. Let me know when that is done and I will continue."

### Step 2 — Install Git

Check if git is installed: `git --version`

If git is not installed, tell the user: "Please download Git from git-scm.com and install it with default settings. Let me know when done."

### Step 3 — Create the Main Project Folder

Create the working folder:
```
mkdir -p ~/RBOTZILLA_PHOENIX
cd ~/RBOTZILLA_PHOENIX
```

Tell the user: "I have created your main project folder at your home directory under RBOTZILLA_PHOENIX."

---

## PHASE 2 — CLONE ALL SOURCE REPOS

Clone every repo we need into a temporary source folder so we can extract the best files from each:

```bash
cd ~/RBOTZILLA_PHOENIX
mkdir -p _source_repos
cd _source_repos

git clone https://github.com/rfingerlin9284/rick_clean_live.git
git clone https://github.com/rfingerlin9284/Rbotzilla_pheonix_v1.git
git clone https://github.com/rfingerlin9284/RBOTZILLA_FINAL_v001.git
git clone https://github.com/rfingerlin9284/FROZEN-V2.git
git clone https://github.com/rfingerlin9284/multi_broker_rbtz.git
git clone https://github.com/rfingerlin9284/MULTIBROKER_ESSENTIALS_ONLY.git
git clone https://github.com/rfingerlin9284/RICK_LIVE_CLEAN_FROZEN.git
git clone https://github.com/rfingerlin9284/R_H_UNI.git
```

Tell the user: "All source repositories have been downloaded to your computer. Now I will begin assembling the final system."

---

## PHASE 3 — BUILD THE FINAL SYSTEM FOLDER STRUCTURE

Create this exact folder structure inside `~/RBOTZILLA_PHOENIX`:

```bash
cd ~/RBOTZILLA_PHOENIX

mkdir -p brokers
mkdir -p strategies
mkdir -p wolf_packs
mkdir -p foundation
mkdir -p risk
mkdir -p swarm
mkdir -p util
mkdir -p scripts
mkdir -p backtest
mkdir -p backtest/wolf_pack_runner
mkdir -p backtest/systems
mkdir -p dashboard
mkdir -p logs
mkdir -p configs
```

---

## PHASE 4 — COPY BROKER CONNECTORS

These are the live API connection files. They have been tested and confirmed working with real OANDA and Coinbase accounts.

**Source: `rick_clean_live`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/rick_clean_live

cp $SRC/brokers/oanda_connector.py ~/RBOTZILLA_PHOENIX/brokers/oanda_connector.py
cp $SRC/brokers/oanda_connector_enhanced.py ~/RBOTZILLA_PHOENIX/brokers/oanda_connector_enhanced.py
cp $SRC/brokers/coinbase_connector.py ~/RBOTZILLA_PHOENIX/brokers/coinbase_connector.py
cp $SRC/brokers/ib_connector.py ~/RBOTZILLA_PHOENIX/brokers/ib_connector.py
```

Tell the user: "OANDA, Coinbase, and Interactive Brokers connector files are in place."

---

## PHASE 5 — COPY ALL FIVE TRADING STRATEGIES

These are the proven strategies that went through backtesting. Copy all five from `Rbotzilla_pheonix_v1` which has the complete set with quality-scoring logic.

**Source: `Rbotzilla_pheonix_v1`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/Rbotzilla_pheonix_v1

cp $SRC/strategies/base.py                   ~/RBOTZILLA_PHOENIX/strategies/base.py
cp $SRC/strategies/fabio_aaa_full.py         ~/RBOTZILLA_PHOENIX/strategies/fabio_aaa_full.py
cp $SRC/strategies/price_action_holy_grail.py ~/RBOTZILLA_PHOENIX/strategies/price_action_holy_grail.py
cp $SRC/strategies/trap_reversal_scalper.py  ~/RBOTZILLA_PHOENIX/strategies/trap_reversal_scalper.py
cp $SRC/strategies/institutional_sd.py       ~/RBOTZILLA_PHOENIX/strategies/institutional_sd.py
cp $SRC/strategies/ema_scalper.py            ~/RBOTZILLA_PHOENIX/strategies/ema_scalper.py
cp $SRC/strategies/registry.py              ~/RBOTZILLA_PHOENIX/strategies/registry.py
cp $SRC/strategies/bearish_wolf.py           ~/RBOTZILLA_PHOENIX/strategies/bearish_wolf.py
cp $SRC/strategies/bullish_wolf.py           ~/RBOTZILLA_PHOENIX/strategies/bullish_wolf.py
cp $SRC/strategies/sideways_wolf.py          ~/RBOTZILLA_PHOENIX/strategies/sideways_wolf.py
cp $SRC/strategies/liquidity_sweep.py        ~/RBOTZILLA_PHOENIX/strategies/liquidity_sweep.py
cp $SRC/strategies/fib_confluence_breakout.py ~/RBOTZILLA_PHOENIX/strategies/fib_confluence_breakout.py
cp $SRC/strategies/crypto_breakout.py        ~/RBOTZILLA_PHOENIX/strategies/crypto_breakout.py
```

If a file does not exist in that repo, try the fallback from `rick_clean_live`:

```bash
SRC2=~/RBOTZILLA_PHOENIX/_source_repos/rick_clean_live
# Only copy if not already present
[ ! -f ~/RBOTZILLA_PHOENIX/strategies/bearish_wolf.py ] && cp $SRC2/strategies/bearish_wolf.py ~/RBOTZILLA_PHOENIX/strategies/
[ ! -f ~/RBOTZILLA_PHOENIX/strategies/bullish_wolf.py ] && cp $SRC2/strategies/bullish_wolf.py ~/RBOTZILLA_PHOENIX/strategies/
[ ! -f ~/RBOTZILLA_PHOENIX/strategies/sideways_wolf.py ] && cp $SRC2/strategies/sideways_wolf.py ~/RBOTZILLA_PHOENIX/strategies/
```

Tell the user: "All five trading strategies and three wolf pack regime strategies are in place."

---

## PHASE 6 — COPY WOLF PACK REGIME ORCHESTRATION

The wolf pack system detects whether the market is trending up (bullish), trending down (bearish), or moving sideways, then routes signals to the right strategy.

**Source: `rick_clean_live`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/rick_clean_live

cp $SRC/wolf_packs/__init__.py          ~/RBOTZILLA_PHOENIX/wolf_packs/__init__.py
cp $SRC/wolf_packs/_base.py             ~/RBOTZILLA_PHOENIX/wolf_packs/_base.py
cp $SRC/wolf_packs/extracted_oanda.py  ~/RBOTZILLA_PHOENIX/wolf_packs/extracted_oanda.py
cp $SRC/wolf_packs/orchestrator.py     ~/RBOTZILLA_PHOENIX/wolf_packs/orchestrator.py
cp $SRC/wolf_packs/stochastic_config.py ~/RBOTZILLA_PHOENIX/wolf_packs/stochastic_config.py
```

Tell the user: "Wolf pack regime detection and orchestration files are in place."

---

## PHASE 7 — COPY FOUNDATION AND CHARTER

The charter enforces the non-negotiable trading rules. Nothing trades without passing the charter gates.

**Source: `RBOTZILLA_FINAL_v001`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/RBOTZILLA_FINAL_v001

cp $SRC/foundation/rick_charter.py ~/RBOTZILLA_PHOENIX/foundation/rick_charter.py
touch ~/RBOTZILLA_PHOENIX/foundation/__init__.py
```

**Charter Rules (hardcoded — do not change):**
- Charter PIN: `841921`
- Minimum Risk-to-Reward Ratio: `3.2:1`
- Allowed Timeframes: `M15`, `M30`, `H1` only
- Maximum Hold Time per Trade: `6 hours`
- 4 Guardian Gates validate every single trade

Tell the user: "Trading charter and guardian gate rules are in place."

---

## PHASE 8 — COPY RISK MANAGEMENT SYSTEM

This is the stop loss, take profit, position sizing, and drawdown protection layer.

**Source: `RBOTZILLA_FINAL_v001`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/RBOTZILLA_FINAL_v001

cp $SRC/risk/risk_control_center.py ~/RBOTZILLA_PHOENIX/risk/risk_control_center.py
cp $SRC/risk/dynamic_sizing.py      ~/RBOTZILLA_PHOENIX/risk/dynamic_sizing.py
cp $SRC/risk/oco_validator.py       ~/RBOTZILLA_PHOENIX/risk/oco_validator.py
touch ~/RBOTZILLA_PHOENIX/risk/__init__.py
```

**Risk Parameters (from verified deployment):**
- Daily loss limit: 2.0% of account (emergency stop at 3.0%)
- Max drawdown: 10%
- Max consecutive losses: 5
- Trailing stops: Active on all positions on both OANDA and Coinbase
- Position time limit: 6 hours maximum (auto-closed)
- OANDA instruments: micro/nano lots only during testing
- Coinbase: nano lots only, 10 trades/day max, $50 daily loss max

Tell the user: "Risk management, stop loss, take profit, and dynamic position sizing are in place."

---

## PHASE 9 — COPY SWARM BOT AND HIVE AGENT INTEGRATION

The swarm bot coordinates all strategies. The hive agent uses three AI models to validate signals before execution.

**Source: `RBOTZILLA_FINAL_v001`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/RBOTZILLA_FINAL_v001

cp $SRC/swarm/swarm_bot.py ~/RBOTZILLA_PHOENIX/swarm/swarm_bot.py
touch ~/RBOTZILLA_PHOENIX/swarm/__init__.py
```

**Also copy the hive agent files from `multi_broker_rbtz` deployment package:**

```bash
SRC_MULTI=~/RBOTZILLA_PHOENIX/_source_repos/multi_broker_rbtz

# Extract the deployment tarball first
cd ~/RBOTZILLA_PHOENIX/_source_repos/multi_broker_rbtz
tar -xzf MULTI_BROKER_PHOENIX_DEPLOYMENT_20260107_095025.tar.gz 2>/dev/null || echo "Tarball extraction attempted"
```

If the tarball extracts, copy these hive agent files into the project:

```bash
EXTRACTED=~/RBOTZILLA_PHOENIX/_source_repos/multi_broker_rbtz/MULTI_BROKER_PHOENIX/multi_broker_phoenix

for f in autonomous_hive_agent.py engine_startup_bootstrap.py live_extreme_autonomous_integration.py startup_autonomous_hive.py unified_hive_scanner.py hive_cost_control.py; do
    [ -f $EXTRACTED/$f ] && cp $EXTRACTED/$f ~/RBOTZILLA_PHOENIX/swarm/$f
done
```

Tell the user: "Swarm bot and AI hive agent files are in place."

---

## PHASE 10 — COPY UTILITY MODULES

**Source: `RBOTZILLA_FINAL_v001`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/RBOTZILLA_FINAL_v001

cp $SRC/util/mode_manager.py     ~/RBOTZILLA_PHOENIX/util/mode_manager.py
cp $SRC/util/narration_logger.py ~/RBOTZILLA_PHOENIX/util/narration_logger.py
cp $SRC/util/logging.py          ~/RBOTZILLA_PHOENIX/util/logging.py
cp $SRC/util/timezone_manager.py ~/RBOTZILLA_PHOENIX/util/timezone_manager.py
touch ~/RBOTZILLA_PHOENIX/util/__init__.py
```

Also copy the progress tracker from `rick_clean_live`:

```bash
SRC2=~/RBOTZILLA_PHOENIX/_source_repos/rick_clean_live
[ -f $SRC2/util/progress_tracker.py ] && cp $SRC2/util/progress_tracker.py ~/RBOTZILLA_PHOENIX/util/progress_tracker.py
```

Tell the user: "Utility modules including the narration logger and mode manager are in place."

---

## PHASE 11 — COPY MAIN ENGINE FILES

**Source: `RBOTZILLA_FINAL_v001`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/RBOTZILLA_FINAL_v001

cp $SRC/canary_trading_engine.py   ~/RBOTZILLA_PHOENIX/canary_trading_engine.py
cp $SRC/ghost_trading_engine.py    ~/RBOTZILLA_PHOENIX/ghost_trading_engine.py
cp $SRC/capital_manager.py         ~/RBOTZILLA_PHOENIX/capital_manager.py
```

Also copy additional main-engine files from `rick_clean_live`:

```bash
SRC2=~/RBOTZILLA_PHOENIX/_source_repos/rick_clean_live

for f in run_headless.py autonomous_trading.py system_audit.sh RBOTZILLA_LAUNCH.sh verify_system.py verify_system_ready.py; do
    [ -f $SRC2/$f ] && cp $SRC2/$f ~/RBOTZILLA_PHOENIX/$f
done
```

Tell the user: "Main engine files including launch scripts are in place."

---

## PHASE 12 — COPY SELF-MONITORING AND POSITION MANAGEMENT SCRIPTS

These scripts watch all open positions and automatically act when positions are going against you.

**Source: `rick_clean_live`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/rick_clean_live

for f in monitor_positions.py canary_to_live.py position_monitor.py \
         view_live_narration.sh view_tmux_session.sh verify_live_safety.sh \
         verify_paper_mode.sh narration_daemon.py dashboard_supervisor.py; do
    [ -f $SRC/$f ] && cp $SRC/$f ~/RBOTZILLA_PHOENIX/$f
done
```

**Source: `RBOTZILLA_FINAL_v001`**

```bash
SRC2=~/RBOTZILLA_PHOENIX/_source_repos/RBOTZILLA_FINAL_v001

cp $SRC2/scripts/monitor_ghost_session.py ~/RBOTZILLA_PHOENIX/scripts/monitor_ghost_session.py
cp $SRC2/scripts/oanda_paper.py           ~/RBOTZILLA_PHOENIX/scripts/oanda_paper.py
cp $SRC2/start_ghost_trading.sh           ~/RBOTZILLA_PHOENIX/scripts/start_ghost_trading.sh
```

Tell the user: "Position monitoring and self-management scripts are in place."

---

## PHASE 13 — COPY DASHBOARD

**Source: `rick_clean_live`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/rick_clean_live

[ -d $SRC/dashboard ] && cp -r $SRC/dashboard/ ~/RBOTZILLA_PHOENIX/dashboard/ 2>/dev/null
[ -f $SRC/dashboard/advanced_multi_window_dashboard.html ] && cp $SRC/dashboard/advanced_multi_window_dashboard.html ~/RBOTZILLA_PHOENIX/dashboard/
[ -f $SRC/dashboard/dashboard.html ] && cp $SRC/dashboard/dashboard.html ~/RBOTZILLA_PHOENIX/dashboard/
```

Tell the user: "Dashboard files are in place."

---

## PHASE 14 — COPY BACKTEST ENGINE

The canonical research backtest engine comes from `FROZEN-V2`. It supports bar-by-bar simulation, partial take-profits, trailing stop loss, fees, and slippage. This is the only backtesting module used — no new one is created.

**Source: `FROZEN-V2`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/FROZEN-V2

# Copy all backtest-related directories
[ -d $SRC/backtest ] && cp -r $SRC/backtest/ ~/RBOTZILLA_PHOENIX/backtest/ 2>/dev/null
[ -d $SRC/systems ] && cp -r $SRC/systems/ ~/RBOTZILLA_PHOENIX/backtest/systems/ 2>/dev/null

# Copy the pack backtest runner
for f in run_pack_backtest.py demo_pack_backtest.py pack_backtest.py research_backtest.py; do
    [ -f $SRC/$f ] && cp $SRC/$f ~/RBOTZILLA_PHOENIX/backtest/$f
done

# Copy Risk Brain for drawdown management
for d in risk_brain risk; do
    [ -d $SRC/$d ] && cp -r $SRC/$d/ ~/RBOTZILLA_PHOENIX/backtest/$d/ 2>/dev/null
done
```

**Backtest Engine Parameters (from FROZEN-V2):**
- Mode: bar-by-bar simulation
- Stop Loss Maximum: 15 pips (MAX_SL_PIPS)
- Winner R:R Threshold: 2.5 (moves SL to breakeven)
- Fees and slippage: included in every trade calculation
- Partial take-profits: supported
- Trailing stop loss: supported

Tell the user: "Backtest engine from FROZEN-V2 is in place."

---

## PHASE 15 — COPY ML INTELLIGENCE COMPONENTS

These are pre-trained models and ML stack components that were tested and verified working in `rick_clean_live`.

**Source: `rick_clean_live`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/rick_clean_live

# Copy ML models directory
[ -d $SRC/ml ] && cp -r $SRC/ml/ ~/RBOTZILLA_PHOENIX/ml/ 2>/dev/null

# Copy intelligence scripts
for f in ml_intelligence.py intelligence_stack.py pattern_learner.py regime_detector.py; do
    [ -f $SRC/$f ] && cp $SRC/$f ~/RBOTZILLA_PHOENIX/$f
done
```

**Also from `RBOTZILLA_FINAL_v001`:**

```bash
SRC2=~/RBOTZILLA_PHOENIX/_source_repos/RBOTZILLA_FINAL_v001
for f in ml_intelligence.py regime_detector.py pattern_learner.py; do
    [ -f $SRC2/$f ] && [ ! -f ~/RBOTZILLA_PHOENIX/$f ] && cp $SRC2/$f ~/RBOTZILLA_PHOENIX/$f
done
```

**Verified ML Stack Components (from rick_clean_live README):**
- ML Model A: Forex trading signals
- ML Model B: Crypto trading signals
- ML Model C: Derivatives trading signals
- Pattern Learner: Stores up to 10,000 patterns
- Regime Detector: Detects BULL / BEAR / SIDEWAYS / CRASH / TRIAGE

Tell the user: "Machine learning intelligence stack is in place."

---

## PHASE 16 — COPY STOCHASTIC AND TECHNICAL INDICATOR FILES

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/rick_clean_live

[ -f $SRC/stochastic.py ] && cp $SRC/stochastic.py ~/RBOTZILLA_PHOENIX/stochastic.py
[ -f $SRC/wolf_packs/stochastic_config.py ] && cp $SRC/wolf_packs/stochastic_config.py ~/RBOTZILLA_PHOENIX/wolf_packs/stochastic_config.py
```

Also from `R_H_UNI`:

```bash
SRC2=~/RBOTZILLA_PHOENIX/_source_repos/R_H_UNI
[ -f $SRC2/stochastic.py ] && [ ! -f ~/RBOTZILLA_PHOENIX/stochastic.py ] && cp $SRC2/stochastic.py ~/RBOTZILLA_PHOENIX/stochastic.py
```

---

## PHASE 17 — COPY REQUIREMENTS AND CONFIG FILES

**Source: `rick_clean_live`**

```bash
SRC=~/RBOTZILLA_PHOENIX/_source_repos/rick_clean_live
cp $SRC/requirements.txt ~/RBOTZILLA_PHOENIX/requirements.txt
[ -f $SRC/.gitignore ] && cp $SRC/.gitignore ~/RBOTZILLA_PHOENIX/.gitignore
```

**Source: `Rbotzilla_pheonix_v1` — the .env template:**

```bash
SRC2=~/RBOTZILLA_PHOENIX/_source_repos/Rbotzilla_pheonix_v1
cp $SRC2/.env.example ~/RBOTZILLA_PHOENIX/.env.example
[ -f $SRC2/.env.live.example ] && cp $SRC2/.env.live.example ~/RBOTZILLA_PHOENIX/.env.live.example
```

---

## PHASE 18 — CREATE PYTHON VIRTUAL ENVIRONMENT AND INSTALL DEPENDENCIES

```bash
cd ~/RBOTZILLA_PHOENIX
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

If any package fails to install, tell the user which package failed and ask if they want to skip it or if they have a specific version to try. Do not stop the whole install for one optional package.

Tell the user: "All Python packages are installed and ready."

---

## PHASE 19 — CREATE THE .env CONFIGURATION FILE

This is the most important step for the user. All API keys go here. Tell the user:

"I have created a template file called .env in your RBOTZILLA_PHOENIX folder. You need to open it and fill in your API keys. I will walk you through each one."

Create the .env file from the template:

```bash
cd ~/RBOTZILLA_PHOENIX
cp .env.example .env
```

Then tell the user each section they need to fill in:

---

**SECTION 1 — OANDA Forex Broker**

Tell the user: "For OANDA, you need two things: your Account ID and your API Token. Log into your OANDA account at oanda.com, go to Manage API Access, and generate a token. Your Account ID appears at the top of your account dashboard. Fill in these two lines in the .env file:

```
OANDA_ACCOUNT_ID=your-account-id-here
OANDA_API_KEY=your-api-token-here
OANDA_ENV=live
OANDA_API_BASE=https://api-fxtrade.oanda.com
```

If you want to test first with OANDA's paper (practice) account, use:
```
OANDA_ENV=practice
OANDA_API_BASE=https://api-fxpractice.oanda.com
```"

---

**SECTION 2 — Coinbase Advanced Trade**

Tell the user: "For Coinbase, log into your Coinbase Advanced Trade account, go to Settings then API, and create a new API key with trading permissions. You will get an API Key and a Private Key (which is a long multi-line string). Fill in:

```
COINBASE_API_KEY=organizations/your-org-id/apiKeys/your-key-id
COINBASE_PRIVATE_KEY=-----BEGIN EC PRIVATE KEY-----
your-private-key-content-here
-----END EC PRIVATE KEY-----
```"

---

**SECTION 3 — AI Hive Models (Optional but Recommended)**

Tell the user: "The AI Hive uses three AI models to verify trades before execution. These are optional but strongly recommended. Fill in as many as you have:

```
OPENAI_API_KEY=sk-your-openai-key-here
XAI_API_KEY=your-grok-xai-key-here
DEEPSEEK_API_KEY=your-deepseek-key-here
```

The daily AI cost budget is set to ten dollars. The system is strategy-first — AI only activates after a strategy signal fires, so most hours cost nothing."

---

**SECTION 4 — System Settings (Pre-filled, Do Not Change)**

```
RICK_PIN=841921
RICK_DEV_MODE=0
MIN_RISK_REWARD=3.2
MAX_HOLD_HOURS=6
HIVE_DAILY_BUDGET=10.00
MAX_DRAWDOWN_PCT=10.0
DAILY_LOSS_LIMIT_PCT=2.0
EMERGENCY_STOP_PCT=3.0
MAX_CONSECUTIVE_LOSSES=5
BOT_MAX_TRADES=20
RICK_DEMO_MODE=false
USE_GHOST_MODE=false
SIMULATED=false
```

---

## PHASE 20 — MAKE SHELL SCRIPTS EXECUTABLE

```bash
cd ~/RBOTZILLA_PHOENIX
chmod +x *.sh scripts/*.sh 2>/dev/null
chmod +x RBOTZILLA_LAUNCH.sh 2>/dev/null
```

---

## PHASE 21 — VERIFY THE SYSTEM IS READY

Run the system verification script:

```bash
cd ~/RBOTZILLA_PHOENIX
source venv/bin/activate
python3 verify_system.py 2>/dev/null || python3 verify_system_ready.py 2>/dev/null
```

Also run the audit:

```bash
bash system_audit.sh 2>/dev/null || echo "Audit script not present, skipping"
```

Tell the user each thing that passed and each thing that failed. For failures, explain in plain English what is missing and how to fix it.

---

## PHASE 22 — LAUNCH THE SYSTEM

Tell the user: "Your system is assembled. Here is how to start it."

**Option A — Use the Master Launch Script (Recommended)**

```bash
cd ~/RBOTZILLA_PHOENIX
source venv/bin/activate
bash RBOTZILLA_LAUNCH.sh
```

When the menu appears, the options are:
1. Canary Mode — Coinbase crypto, real money, nano lots (small test)
2. OANDA Forex — Paper account, live API data (safest first run)
3. Multi-Asset — All brokers, all strategies, full power
4. Strategy Test — Backtest only, no live trading
5. AI Hive Only — Catalyst scanning, no trades
6. Full Audit — Health check everything
7. Emergency Stop — Kill all running processes immediately
8. Exit

Tell the user: "For your very first run, choose Option 2 to test with OANDA on your practice account. Once you are confident everything works correctly, choose Option 3 for full multi-asset live trading."

**Option B — Run Directly**

```bash
cd ~/RBOTZILLA_PHOENIX
source venv/bin/activate
python3 canary_trading_engine.py --continuous
```

---

## PHASE 23 — MONITORING LIVE POSITIONS

These commands let you watch what the system is doing in real time:

**Watch live trading narration:**
```bash
bash view_live_narration.sh
```

**Watch position monitor:**
```bash
python3 monitor_positions.py
```

**Watch live logs:**
```bash
tail -f logs/*.log
```

**Check session performance:**
```bash
python3 scripts/monitor_ghost_session.py
```

**Emergency stop everything:**
```bash
bash RBOTZILLA_LAUNCH.sh
# Then choose Option 7
```

Or immediate kill:
```bash
pkill -9 -f canary_trading_engine
pkill -9 -f autonomous_trading
pkill -9 -f run_headless
```

---

## PHASE 24 — RUN A BACKTEST

To validate strategy performance before trading live money:

```bash
cd ~/RBOTZILLA_PHOENIX
source venv/bin/activate

# Run pack backtest
python3 backtest/run_pack_backtest.py 2>/dev/null || python3 backtest/demo_pack_backtest.py
```

**FABIO AAA Backtest Parameters (verified results):**
- RSI Threshold: 40 (proven best)
- Trades generated: 167 over backtest period
- Win rate: 64.7%
- ROI: 369% over backtest period
- Risk-based stops: 1–8% volatility stops

Tell the user the backtest results in plain English when it finishes.

---

## WHAT THE SYSTEM DOES EVERY TICK

This is what happens automatically in the background from the moment you start it:

**Step 1 — Strategy Scanning (free, local, instant)**
Every tick (every 60 seconds), the system checks:
- FABIO AAA Full: Is RSI below 40? (RSI threshold proven to generate 64.7% win rate)
- Holy Grail: Is there multi-timeframe trend alignment? (30% portfolio weight)
- EMA Scalper: Are the fast EMA lines crossing? (15% portfolio weight)
- Institutional SD: Is price reaching supply or demand zones? (20% portfolio weight)
- Trap Reversal: Is there a liquidity trap spike reversing? (20% portfolio weight)

**Step 2 — Wolf Pack Regime Detection**
Before acting on any signal, the wolf pack system checks the market regime:
- BULL market: Routes signals to bullish_wolf.py strategy weighting
- BEAR market: Routes signals to bearish_wolf.py strategy weighting
- SIDEWAYS: Routes signals to sideways_wolf.py strategy weighting

**Step 3 — Charter Gate Check**
Every signal must pass all four guardian gates:
- Gate 1: Risk-to-reward ratio must be at least 3.2 to 1
- Gate 2: Timeframe must be M15, M30, or H1
- Gate 3: Trade quality score must meet strategy minimum (65–80 depending on strategy)
- Gate 4: No conflicting open positions in same direction

**Step 4 — AI Hive Validation (only if signal passes all gates)**
If a signal passes the charter gates, three AI models vote on it:
- Grok (XAI): Checks for major economic events (Fed, GDP, employment reports)
- OpenAI (GPT-4): Analyzes news sentiment from Bloomberg, Reuters, CNBC
- DeepSeek: Analyzes Reddit and social media sentiment
At least 2 of 3 AI models must agree before a trade is placed.

**Step 5 — Trade Execution**
If all gates and AI validation pass:
- Calculates position size using dynamic sizing (micro/nano lots)
- Sets stop loss based on strategy type (volatility-adaptive for FABIO, fixed for others)
- Sets take profit at 2x or 3.2x the risk
- Enables trailing stop immediately
- Submits order to broker (OANDA or Coinbase)
- Logs all details

**Step 6 — Continuous Position Monitoring**
Every 30 seconds, for every open position:
- Checks current P&L vs stop loss level
- Checks if trailing stop needs to be moved
- Checks if 6-hour time limit is approaching
- Checks daily loss total vs daily limit
- Checks drawdown vs maximum drawdown

**Step 7 — Autonomous Closing Logic**
Positions are automatically closed when:
- Stop loss is hit
- Take profit is hit
- 6-hour time limit expires
- Daily loss limit reached (stops all trading for the day)
- Maximum drawdown reached (emergency close all positions)
- 5 consecutive losses (pauses system for review)

---

## FIVE STRATEGY CHARTERS — DETAILED SPECIFICATIONS

### Strategy 1: FABIO AAA Full
- **What it does**: Identifies oversold conditions where price is likely to bounce
- **Primary indicator**: RSI below 40 (optimized threshold — proven in backtest)
- **Secondary indicators**: Volatility measurement, momentum confirmation
- **Stop loss**: Adaptive, 1–8% based on current volatility
- **Take profit**: 2:1 minimum reward-to-risk
- **Best timeframes**: M30, H1
- **Best market conditions**: Any (works in all regimes)
- **Portfolio weight**: 15%
- **Quality threshold**: 78 out of 100

### Strategy 2: Holy Grail
- **What it does**: Trades the primary trend using multi-timeframe confirmation
- **Primary indicator**: Higher timeframe trend direction (H4 aligns with H1 signal)
- **Secondary indicators**: Momentum, price action confirmation
- **Stop loss**: Fixed 3% of position
- **Take profit**: 3:1 or higher
- **Best timeframes**: H1 is primary signal
- **Best market conditions**: BULL or BEAR (directional trends)
- **Portfolio weight**: 30% (primary strategy)
- **Quality threshold**: 80 out of 100

### Strategy 3: EMA Scalper
- **What it does**: Catches fast momentum moves when EMAs cross
- **Primary indicator**: Fast EMA crossing slow EMA
- **Secondary indicators**: Volume confirmation, spread check
- **Stop loss**: Tight 0.5% of position
- **Take profit**: 1:1 to 1.5:1 (quick trades)
- **Best timeframes**: M15 primarily
- **Best market conditions**: BULL or BEAR trending
- **Portfolio weight**: 15%
- **Quality threshold**: 65 out of 100

### Strategy 4: Institutional Supply and Demand
- **What it does**: Identifies zones where large institutions buy and sell
- **Primary indicator**: Supply zone (for shorts) and demand zone (for longs) detection
- **Secondary indicators**: Confluence with higher timeframe levels
- **Stop loss**: Moderate 1% of position
- **Take profit**: 2:1 to 3:1
- **Best timeframes**: H1, M30
- **Best market conditions**: Any regime (institutions trade in all conditions)
- **Portfolio weight**: 20%
- **Quality threshold**: 70 out of 100

### Strategy 5: Trap Reversal
- **What it does**: Catches false breakout reversals after liquidity grabs
- **Primary indicator**: Price spikes beyond a key level then immediately reverses
- **Secondary indicators**: Volume spike detection, candle pattern confirmation
- **Stop loss**: 0.5x the size of the spike
- **Take profit**: 1.5:1 to 2:1
- **Best timeframes**: M15, M30
- **Best market conditions**: SIDEWAYS or beginning of reversals
- **Portfolio weight**: 20%
- **Quality threshold**: 75 out of 100

---

## SUPPORTED TRADING INSTRUMENTS

### OANDA Forex (all six pairs active)
- EUR/USD — Euro vs US Dollar
- GBP/USD — British Pound vs US Dollar
- USD/JPY — US Dollar vs Japanese Yen
- AUD/USD — Australian Dollar vs US Dollar
- NZD/USD — New Zealand Dollar vs US Dollar
- USD/CAD — US Dollar vs Canadian Dollar

### Coinbase Crypto (two pairs)
- BTC-USD — Bitcoin vs US Dollar
- ETH-USD — Ethereum vs US Dollar

### Interactive Brokers (optional — equities, futures, options)
- Requires IBKR TWS or Gateway running locally on port 7497 (paper) or 7496 (live)

---

## HIVE AGENT AI COST CONTROL

The AI budget is pre-configured at ten dollars per day. The system is strategy-first:
- Local strategy scanning costs nothing
- AI only activates when a strategy signal passes all four charter gates
- Actual cost measured at 0.001 dollars per call during testing
- Expected monthly AI cost: between 25 cents and thirteen dollars

If the AI budget runs out for the day, the system continues trading based on strategy signals alone, without AI validation.

---

## TROUBLESHOOTING IN PLAIN ENGLISH

**"OANDA connection refused"**
Check that OANDA_ENV is set to either "practice" or "live" and that the API key and account ID are correct in your .env file.

**"Coinbase authentication failed"**
The Coinbase private key must be the full text including the BEGIN and END lines. Make sure the key has trading permissions enabled on the Coinbase website.

**"No trading signals firing"**
This is normal during low-volatility periods. The system is selective and will reject 75-80% of all possible setups. Wait for market conditions that match strategy criteria. This could be a few hours during quiet Asian session.

**"Daily loss limit hit"**
The system automatically stopped trading for today. This is the protection working correctly. It will resume automatically tomorrow.

**"AI Hive not responding"**
Check your OpenAI, Grok, and DeepSeek API keys in the .env file. The system continues trading on strategy signals alone if AI is unavailable.

**"Can't find file [name]"**
Some files may not exist in every repo. The copy commands above use conditional checks (the `[ -f file ] &&` syntax) so missing files are skipped gracefully. Only worry if a core file is missing (broker connectors, strategies, or main engine files).

---

## FINAL VERIFICATION CHECKLIST

Before starting live trading, confirm every item below:

- [ ] All five strategies copied and present in ~/RBOTZILLA_PHOENIX/strategies/
- [ ] Three wolf pack files copied (bullish_wolf.py, bearish_wolf.py, sideways_wolf.py)
- [ ] OANDA connector present and API keys filled in .env
- [ ] Coinbase connector present and API keys filled in .env
- [ ] Rick charter in place (foundation/rick_charter.py)
- [ ] Risk control center in place (risk/risk_control_center.py)
- [ ] Swarm bot in place (swarm/swarm_bot.py)
- [ ] Mode manager in place (util/mode_manager.py)
- [ ] Narration logger in place (util/narration_logger.py)
- [ ] Backtest engine in place (backtest/ directory)
- [ ] Python virtual environment active
- [ ] All packages from requirements.txt installed
- [ ] RICK_DEMO_MODE=false in .env
- [ ] USE_GHOST_MODE=false in .env
- [ ] SIMULATED=false in .env
- [ ] System audit passes

---

*This document references only existing, tested, deployed code from rfingerlin9284's GitHub repositories. No new code has been invented. Every file path, parameter, and configuration value comes directly from proven deployments documented in the repositories listed above.*
