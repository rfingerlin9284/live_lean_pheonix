# 🔥 RICK Phoenix V2 Trading System

**Institutional-Grade Autonomous Trading System**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Overview

RICK Phoenix V2 is a sophisticated autonomous trading system featuring:

- **Multi-Broker Support**: OANDA (Forex), Coinbase Advanced (Crypto), IBKR (Stocks/Options)
- **HiveMind AI**: Multi-agent consensus system with GPT/Grok/DeepSeek integration
- **WolfPack Strategies**: 5 battle-tested strategies with voting consensus
- **Immutable Charter**: PIN-protected risk management (841921)
- **Amplifier Protocol**: 12 concurrent positions, 70% margin utilization
- **Real-time Monitoring**: Supervisor pattern with health checks

## 📊 Performance

Based on 1-year historical backtest (see `backtest_results/`):

- **Initial Capital**: $5,000
- **Monthly Deposits**: $1,000
- **Charter Compliance**: 100%
- **Risk Management**: 2% per trade, 3:1 R:R minimum

## 🚀 Quick Start

### Prerequisites

```bash
python >= 3.8
pandas
numpy
requests
python-dotenv
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rfingerlin9284/Rbotzilla_pheonix_v1.git
cd Rbotzilla_pheonix_v1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.template .env
# Edit .env with your API credentials
```

4. Start the system:
```bash
./start_phoenix_v2.sh
```

## 🏗️ Architecture

```
PhoenixV2/
├── brain/              # Strategy aggregation (HiveMind + WolfPack)
├── config/             # Charter and trading pairs
├── core/               # Authentication and state management
├── execution/          # Broker connectors (OANDA, Coinbase, IBKR)
├── gate/               # Risk management and validation
├── operations/         # Position management (Surgeon)
└── logic/              # Technical indicators and regime detection
```

### Key Components

**Charter System** (`config/charter.py`):
- Immutable risk rules
- PIN protection (841921)
- Position limits and margin caps

**HiveMind** (`brain/hive_mind.py`):
- Multi-AI agent delegation
- Consensus-based signals
- 3:1 R:R enforcement

**WolfPack** (`brain/wolf_pack.py`):
- 5 strategy voting system
- Confidence-weighted decisions
- Learning-driven allocation

**Risk Gate** (`gate/risk_gate.py`):
- Final trade validation
- Correlation monitoring
- Charter compliance enforcement

## 📈 Trading Strategy

1. **Signal Generation**:
   - HiveMind checks for ML-validated setups (3:1 R:R minimum)
   - WolfPack generates consensus from 5 strategies
   - Cross-market correlation checks (BTC vs SPX)

2. **Risk Validation**:
   - Charter compliance (position count, margin, R:R)
   - Correlation check (prevents overexposure)
   - Notional size validation

3. **Execution**:
   - OCO orders (Stop Loss + Take Profit mandatory)
   - Position tracking via Surgeon
   - Stagnant winner harvest (6h + $5 profit)

## 🔐 Charter Rules

The Charter enforces institutional-grade risk management:

```python
MAX_CONCURRENT_POSITIONS = 12  # Amplifier Protocol
MAX_MARGIN_UTILIZATION = 0.70  # 70% hard cap
MAX_RISK_PER_TRADE = 0.02      # 2% per trade
MIN_TIMEFRAME = "M15"           # No noise trading
OCO_MANDATORY = True            # Must have SL/TP
```

**Charter modifications require PIN: 841921**

## 🧠 HiveMind Integration

The system delegates analysis to multiple AI agents:

- **GPT-4**: Technical pattern recognition (35% weight)
- **Grok**: Market sentiment analysis (35% weight)
- **DeepSeek**: Cross-asset correlation (30% weight)

Consensus confidence threshold: **65%**

## 📊 Monitoring

Check system status:
```bash
cat PhoenixV2/logs/system_status.json
```

View audit trail:
```bash
tail -f PhoenixV2/logs/audit.log
```

Check portfolio:
```bash
python3 check_portfolio.py
```

## 🧪 Testing

Run backtests:
```bash
python3 comprehensive_1year_backtest.py
```

View results:
```bash
cat backtest_results/*.json | python3 -m json.tool
```

## 🔧 Configuration

### Master Environment File

`paper_acct_env.env` is the **single source of truth**. All updates require:
- PIN verification (841921), OR
- Explicit chat confirmation

### Broker Setup

**OANDA** (Forex):
```bash
OANDA_PRACTICE_ACCOUNT_ID=your_account_id
OANDA_PRACTICE_TOKEN=your_token
OANDA_PRACTICE_BASE_URL=https://api-fxpractice.oanda.com/v3
```

**Coinbase Advanced** (Crypto):
```bash
COINBASE_LIVE_API_KEY=organizations/xxx/apiKeys/xxx
COINBASE_LIVE_API_SECRET=-----BEGIN EC PRIVATE KEY-----...
COINBASE_LIVE_BASE_URL=https://api.coinbase.com
```

**IBKR** (Stocks):
```bash
IB_GATEWAY_HOST=127.0.0.1
IB_GATEWAY_PORT=4002
IB_ACCOUNT_ID=your_account_id
```

## 🐛 Troubleshooting

### No Trading Activity

1. Check processes:
```bash
ps aux | grep -E "supervisor|main.py"
```

2. Verify environment variables:
```bash
cat /proc/$(pgrep -f main.py)/environ | tr '\0' '\n' | grep OANDA
```

3. Test connection:
```bash
python3 -c "from PhoenixV2.core.auth import AuthManager; from PhoenixV2.execution.router import BrokerRouter; auth = AuthManager(); router = BrokerRouter(auth)"
```

See `docs/DIAGNOSIS_NO_TRADING_ACTIVITY.md` for comprehensive troubleshooting.

### Signal Generation Issues

HiveMind requires market data access. Verify:
```bash
python3 -c "from PhoenixV2.brain.aggregator import StrategyBrain; from PhoenixV2.execution.router import BrokerRouter; from PhoenixV2.core.auth import AuthManager; auth = AuthManager(); router = BrokerRouter(auth); brain = StrategyBrain(router); print('OK' if brain.get_signal('EUR_USD') else 'No signal')"
```

## 📚 Documentation

- `docs/AGENT_CHARTER_v2.md` - Charter rules and philosophy
- `docs/ALL_INTERFACES_GUIDE.md` - Complete interface documentation
- `docs/DIAGNOSIS_NO_TRADING_ACTIVITY.md` - Troubleshooting guide
- `docs/COMPLETE_SYSTEM_INVENTORY.md` - Full component inventory

## 🤝 Contributing

This is a personal trading system. Fork at your own risk.

## ⚖️ License

MIT License - See LICENSE file

## ⚠️ Disclaimer

**USE AT YOUR OWN RISK**

This software is for educational purposes. Trading involves substantial risk of loss. Past performance does not guarantee future results. The authors assume no liability for financial losses.

## 📞 Support

- Issues: GitHub Issues
- Documentation: `/docs` folder
- System Status: `PhoenixV2/logs/system_status.json`

---

**Built with institutional discipline. Powered by AI consensus. Protected by immutable charter.**

🔥 RICK Phoenix V2 - The Money Machine
