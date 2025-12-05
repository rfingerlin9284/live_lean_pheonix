# Hive Analysis & Parameter Optimization System

## Overview

This system provides comprehensive trading analysis and parameter optimization using a multi-agent "hive mind" approach. It integrates Fair Value Gap (FVG) detection, Fibonacci retracement analysis, and momentum detection to optimize trading strategies.

## Components

### 1. Strategic Hedge Manager (`oanda/strategic_hedge_manager.py`)

Monitors losing positions and automatically executes strategic hedges or position flips based on momentum reversal detection.

**Features:**
- Detects momentum shifts using price action analysis
- Integrates FVG and Fibonacci reversal signals
- Automatic hedge ratio calculation based on confidence
- Position flip recommendations for strong reversals

**Usage:**
```python
from oanda.strategic_hedge_manager import StrategicHedgeManager

manager = StrategicHedgeManager(pin=841921)

# Check if a losing position should be hedged
position = {
    'entry_price': 1.1000,
    'direction': 'long',
    'size': 10000,
    'unrealized_pnl': -200
}

decision = manager.maybe_open_hedge(position, current_price, prices)
if decision and decision.should_hedge:
    print(f"Hedge recommended: {decision.reasoning}")
```

### 2. Log Analyzer (`util/log_analyzer.py`)

Analyzes narration logs to extract performance metrics and identify weaknesses in trading strategies.

**Metrics Calculated:**
- Win rate, profit factor, Sharpe ratio
- Maximum drawdown
- Best/worst performing pairs
- Parameter insights

**Usage:**
```python
from util.log_analyzer import LogAnalyzer

analyzer = LogAnalyzer()
report = analyzer.generate_report(
    strategies=['wolfpack', 'quant_hedge'],
    hours_back=24
)
```

### 3. Hive Parameter Optimizer (`hive/hive_parameter_optimizer.py`)

Uses multiple specialized agents to optimize trading parameters through collective intelligence.

**Hive Agents:**
- **RiskManager**: Optimizes stop-loss/take-profit ratios
- **TrendAnalyst**: Adjusts momentum detection weights
- **FVGSpecialist**: Tunes Fair Value Gap parameters
- **FibonacciExpert**: Optimizes Fibonacci level weights
- **VolumeAnalyst**: Adjusts confidence thresholds based on volume

**Usage:**
```python
from hive.hive_parameter_optimizer import HiveParameterOptimizer

optimizer = HiveParameterOptimizer(pin=841921)

optimized = optimizer.optimize_with_hive(
    current_params=current_params,
    performance_data=performance,
    market_conditions=market
)

print(f"Expected improvement: {optimized.expected_improvement:.1%}")
```

### 4. Hive Opportunity Scanner (`hive/hive_opportunity_scanner.py`)

Proactively scans markets for high-probability trading opportunities using multiple analysis agents.

**Features:**
- Multi-timeframe analysis (M15, H1, H4)
- FVG detection for reversal points
- Fibonacci retracement level identification
- Momentum strength analysis
- Automatic risk/reward calculation

**Usage:**
```python
from hive.hive_opportunity_scanner import HiveOpportunityScanner

scanner = HiveOpportunityScanner(pin=841921)
opportunities = scanner.scan_markets()

scanner.print_opportunities(opportunities)
```

### 5. Strategy Optimization Orchestrator (`optimize_strategies.py`)

Master orchestrator that coordinates all analysis and optimization components.

**Workflow:**
1. Analyzes logs to understand current performance
2. Engages hive agents to identify weaknesses
3. Generates optimized parameters
4. Validates with backtest simulations
5. Produces actionable recommendations

**Usage:**
```python
from optimize_strategies import StrategyOptimizationOrchestrator

orchestrator = StrategyOptimizationOrchestrator(pin=841921)
report = orchestrator.run_full_optimization(
    strategies=['wolfpack', 'quant_hedge', 'strategic_hedge'],
    hours_back=24,
    output_dir='optimization_results'
)
```

### 6. Command-Line Interface (`hive_cli.py`)

User-friendly CLI for accessing all analysis tools.

## CLI Usage

### Analyze Trading Logs

```bash
# Analyze last 24 hours
python hive_cli.py analyze

# Analyze last 48 hours
python hive_cli.py analyze --hours 48

# Analyze specific strategies
python hive_cli.py analyze --strategies wolfpack quant_hedge
```

**Output:**
- Trade statistics for each strategy
- Win rate, profit factor, total PNL
- Best/worst performing pairs
- Parameter recommendations

### Optimize Parameters

```bash
# Run full optimization
python hive_cli.py optimize

# Optimize with custom settings
python hive_cli.py optimize --strategies wolfpack --hours 48 --output-dir results
```

**Output:**
- Executive summary of performance
- Hive agent recommendations
- Optimized parameter values
- Expected performance improvement
- Comprehensive JSON report
- Human-readable markdown summary

**Generated Files:**
- `optimization_results/comprehensive_optimization_report.json` - Full analysis
- `optimization_results/OPTIMIZATION_SUMMARY.md` - Readable summary
- `optimization_results/log_analysis.json` - Log analysis data
- `optimization_results/<strategy>_optimization.json` - Per-strategy results

### Scan for Opportunities

```bash
# Scan all configured pairs and timeframes
python hive_cli.py scan

# Scan specific pairs
python hive_cli.py scan --pairs EUR_USD GBP_USD

# Scan specific timeframes
python hive_cli.py scan --timeframes H1 H4

# Combine filters
python hive_cli.py scan --pairs EUR_USD GBP_USD USD_JPY --timeframes M15 H1
```

**Output:**
- High-confidence trading opportunities
- Entry price, stop-loss, take-profit levels
- Risk/reward ratio
- Confluence reasoning (FVG, Fibonacci, momentum)
- JSON export of all opportunities

## Integration with Existing System

### Adding Strategic Hedge to Trading Engine

```python
from oanda.strategic_hedge_manager import StrategicHedgeManager

# In your trading engine initialization
self.hedge_manager = StrategicHedgeManager(pin=841921)

# After detecting a losing position
for position in losing_positions:
    decision = self.hedge_manager.maybe_open_hedge(
        position=position,
        current_price=current_price,
        prices=recent_prices
    )
    
    if decision:
        if decision.flip_position:
            # Execute complete reversal
            self.close_position(position)
            self.open_position(opposite_direction)
        elif decision.should_hedge:
            # Open partial hedge
            hedge_size = position.size * decision.hedge_ratio
            self.open_hedge(position, hedge_size)
```

### Using Optimized Parameters

After running optimization, apply recommended parameters:

```python
import json

# Load optimization results
with open('optimization_results/wolfpack_optimization.json') as f:
    results = json.load(f)

optimized_params = results['optimized_parameters']

# Apply to your strategy
strategy.confidence_threshold = optimized_params['confidence_threshold']
strategy.stop_loss_pips = optimized_params['stop_loss_pips']
strategy.take_profit_pips = optimized_params['take_profit_pips']
# ... etc
```

### Automated Opportunity Trading

```python
from hive.hive_opportunity_scanner import HiveOpportunityScanner

scanner = HiveOpportunityScanner(pin=841921)

# Scan periodically (e.g., every 15 minutes)
opportunities = scanner.scan_markets()

for opp in opportunities:
    if opp.confidence >= 0.75:  # High confidence threshold
        # Execute trade
        self.place_trade(
            symbol=opp.symbol,
            direction=opp.direction,
            entry=opp.entry_price,
            stop_loss=opp.stop_loss,
            take_profit=opp.take_profit
        )
```

## FVG and Fibonacci Logic

### Fair Value Gap (FVG)

FVG detection identifies price gaps that often act as support/resistance:

- **Bullish FVG**: Price gaps up, leaving unfilled area below (potential support)
- **Bearish FVG**: Price gaps down, leaving unfilled area above (potential resistance)

**Implementation:**
```python
# Detect bullish FVG
if current_low > previous_high:
    # Gap up detected - bullish signal
    
# Detect bearish FVG
if current_high < previous_low:
    # Gap down detected - bearish signal
```

### Fibonacci Retracements

Key levels used for entry and reversal detection:

- **Golden Pocket (0.618 - 0.65)**: Strongest reversal zone
- **0.5 Level**: Equilibrium point
- **0.382 Level**: Shallow retracement zone

**Implementation:**
```python
# Calculate retracement
retracement = (current_price - swing_low) / (swing_high - swing_low)

# Check for golden pocket
if 0.618 <= retracement <= 0.65:
    # High-probability reversal zone
```

## Parameter Recommendations

### Confidence Threshold
- **Default**: 0.55
- **High Win Rate (>60%)**: Can lower to 0.50 for more trades
- **Low Win Rate (<45%)**: Increase to 0.65+ to filter weak signals

### Stop Loss / Take Profit
- **Default**: 10 pips SL, 32 pips TP (3.2:1 R:R)
- **High Volatility**: Widen stops (15 pips SL, 50 pips TP)
- **Low Profit Factor (<1.5)**: Increase TP target or tighten SL

### Position Sizing
- **Default**: Max 12 positions
- **High Drawdown**: Reduce to 6-8 positions
- **Low Volatility**: Can increase to 15 positions

### FVG/Fibonacci Weights
- **Volatile Markets**: Increase FVG weight to 0.30-0.35
- **Ranging Markets**: Increase Fibonacci weight to 0.30-0.35
- **Trending Markets**: Increase momentum weight to 0.50-0.55

## Monitoring and Maintenance

### Daily Routine

1. **Morning Analysis**:
   ```bash
   python hive_cli.py analyze --hours 24
   ```

2. **Weekly Optimization**:
   ```bash
   python hive_cli.py optimize --hours 168
   ```

3. **Continuous Scanning**:
   ```bash
   python hive_cli.py scan
   ```

### Performance Tracking

Monitor these key metrics:
- Win rate trend over time
- Profit factor consistency
- Maximum drawdown relative to profits
- Best/worst performing pairs

## Troubleshooting

### No Opportunities Found

If scanner returns no results:
1. Check `min_confidence` parameter (default: 0.60)
2. Verify `min_rr_ratio` isn't too high (default: 2.0)
3. Expand pairs or timeframes scanned
4. Review market conditions (low volatility = fewer opportunities)

### Low Win Rate

If strategies show low win rates:
1. Run `python hive_cli.py optimize` to get recommendations
2. Increase `confidence_threshold` to filter weak signals
3. Review and potentially blacklist underperforming pairs
4. Adjust FVG/Fibonacci weights based on market regime

### High Drawdown

If drawdown is excessive:
1. Reduce `max_positions` parameter
2. Tighten stop losses
3. Increase position sizing restrictions
4. Consider enabling strategic hedge manager

## Files Created

- `oanda/strategic_hedge_manager.py` - Strategic hedging system
- `util/log_analyzer.py` - Log analysis tool
- `hive/hive_parameter_optimizer.py` - Multi-agent optimizer
- `hive/hive_opportunity_scanner.py` - Market scanner
- `optimize_strategies.py` - Main orchestrator
- `hive_cli.py` - Command-line interface
- `optimization_results/` - Generated reports directory

## Next Steps

1. Review generated optimization reports
2. Apply recommended parameter changes
3. Backtest optimized parameters
4. Enable strategic hedge manager for losing positions
5. Set up automated opportunity scanning
6. Monitor performance and iterate

## Support

For questions or issues:
1. Check `optimization_results/OPTIMIZATION_SUMMARY.md` for insights
2. Review narration logs for detailed trade history
3. Run `python hive_cli.py --help` for usage information
