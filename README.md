# RBOTZILLA PHOENIX — Full Deployment Rebuild Kit

This repository contains the complete rebuild instructions for the RBOTZILLA PHOENIX autonomous trading system. All code is sourced exclusively from proven, debugged repositories already in the rfingerlin9284 GitHub account.

---

## ⬇️ Download / Get Started

**This is the repo you need to download.**

👉 **https://github.com/rfingerlin9284/live_lean_pheonix**

### How to download it

**Option A — Download as a ZIP (no coding required):**
1. Go to https://github.com/rfingerlin9284/live_lean_pheonix
2. Click the green **Code** button near the top right
3. Click **Download ZIP**
4. Unzip the folder on your computer
5. Open VS Code, then open that unzipped folder (File → Open Folder)

**Option B — Clone with Git (if you have Git installed):**
```
git clone https://github.com/rfingerlin9284/live_lean_pheonix.git
```

Once you have the folder open in VS Code, follow the steps in [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) to rebuild the full trading system.

---

## Start Here — Three Documents

### 1. [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)
**Read this first if you are a non-coder.** Plain-English guide explaining what to do step by step, how to give the VS Code agent its instructions, and what to expect while the system runs.

### 2. [VSCODE_AGENT_MEGA_PROMPT.md](VSCODE_AGENT_MEGA_PROMPT.md)
**The master instruction document for the VS Code AI agent.** Contains 24 phases covering every step from installing Python to launching live trading. References exact file paths in exact repos. No placeholder code — everything comes from verified source repos.

### 3. [REPO_SOURCE_MAP.md](REPO_SOURCE_MAP.md)
**Reference map showing which file comes from which repo.** Used by the agent when assembling the system and when individual files need to be refreshed.

---

## What Gets Built

The rebuilt system includes:

- **5 Proven Trading Strategies**: FABIO AAA Full, Holy Grail, EMA Scalper, Institutional Supply/Demand, Trap Reversal
- **3 Wolf Pack Regime Strategies**: Bullish Wolf, Bearish Wolf, Sideways Wolf (automatically route signals by market regime)
- **3 Broker Connectors**: OANDA Forex, Coinbase Advanced Trade, Interactive Brokers
- **AI Hive Agent**: OpenAI + Grok + DeepSeek — 3 AI models vote on every signal
- **Risk Management**: Dynamic stop loss, trailing stops, drawdown protection, daily loss limits, consecutive loss breaker
- **Position Monitor**: Continuous monitoring of all open positions with autonomous close logic
- **Backtest Engine**: FROZEN-V2 canonical research backtest (bar-by-bar, trailing SL, partial TPs, fees)
- **ML Intelligence Stack**: Forex/Crypto/Derivatives models, Pattern Learner, Regime Detector

---

## Source Repositories (All by rfingerlin9284)

| Repo | Role |
|---|---|
| `rick_clean_live` | Primary codebase — brokers, wolf packs, monitoring |
| `Rbotzilla_pheonix_v1` | All five strategy files, .env template |
| `RBOTZILLA_FINAL_v001` | Foundation charter, risk, swarm bot, utilities |
| `FROZEN-V2` | Research-grade backtest engine |
| `multi_broker_rbtz` | Production v2.0 tarball with hive agent files |
| `MULTIBROKER_ESSENTIALS_ONLY` | Build and verification tools |

---

## Trading Parameters (Verified and Locked)

- **Timeframes**: M15, M30, H1 only
- **Minimum R:R**: 3.2:1 (enforced by charter)
- **Max Hold Time**: 6 hours per trade
- **FABIO RSI Threshold**: 40 (64.7% win rate in backtest)
- **Daily Loss Limit**: 2.0% (emergency stop at 3.0%)
- **Max Drawdown**: 10%
- **OANDA Pairs**: EUR/USD, GBP/USD, USD/JPY, AUD/USD, NZD/USD, USD/CAD
- **Coinbase Pairs**: BTC-USD, ETH-USD

---

## Non-Negotiable Rules

- No simulation, no fallback, no demo mode — live connections only
- No new code invented — every file sourced from existing repos
- All stop losses active on all positions at all times
- Charter PIN 841921 required for mode changes
