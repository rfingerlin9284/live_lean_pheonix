# Hive Analysis System - Quick Start Demo

## What You Asked For

You requested a system that:
1. Analyzes logs from wolfpack, strategic hedge, and quant hedge strategies
2. Uses hive agents to find optimal parameters
3. Integrates FVG (Fair Value Gap) and Fibonacci logic
4. Provides an edge through better parameter tuning

## What Was Built

A complete multi-agent optimization system with 5 specialized "hive" agents that work together to analyze performance and recommend improvements.

## Quick Demo

### 1. Analyze Current Performance

```bash
python hive_cli.py analyze --hours 24
```

**Output:**
- Win rate for each strategy
- Profit factor and total PNL
- Best/worst performing pairs
- Parameter recommendations

### 2. Optimize Parameters

```bash
python hive_cli.py optimize
```

**What Happens:**
1. Loads last 24 hours of trading logs
2. Each hive agent analyzes from their specialty:
   - RiskManager → Checks SL/TP ratios
   - TrendAnalyst → Evaluates momentum filters
   - FVGSpecialist → Reviews gap detection
   - FibonacciExpert → Checks retracement levels
   - VolumeAnalyst → Validates signal quality
3. Agents vote on parameter changes
4. System aggregates recommendations
5. Simulates backtest with new parameters
6. Generates comprehensive report

**Output Files:**
- `optimization_results/OPTIMIZATION_SUMMARY.md` - Human-readable summary
- `optimization_results/comprehensive_optimization_report.json` - Full data
- `optimization_results/wolfpack_optimization.json` - Strategy-specific
- `optimization_results/quant_hedge_optimization.json` - Strategy-specific
- `optimization_results/strategic_hedge_optimization.json` - Strategy-specific

### 3. Scan for Opportunities

```bash
python hive_cli.py scan
```

**What Happens:**
1. Scans 9 currency pairs across 3 timeframes
2. For each pair/timeframe:
   - Detects FVG (Fair Value Gaps)
   - Identifies Fibonacci levels
   - Measures momentum strength
   - Checks market regime
3. Aggregates signals with weighted voting
4. Filters by confidence (>60%) and R:R (>2:1)
5. Calculates entry, SL, TP levels

**Output:**
```
HIVE TRADING OPPORTUNITIES
================================================================================

1. EUR_USD - H1 - BUY
   Confidence: 72%
   Entry: 1.10250
   Stop Loss: 1.10000
   Take Profit: 1.11000
   Risk:Reward: 1:3.0
   Reasoning: FVG buy signal (conf: 0.75); Golden pocket (conf: 0.85); bullish momentum

2. GBP_USD - H4 - SELL
   Confidence: 68%
   Entry: 1.27500
   Stop Loss: 1.27750
   Take Profit: 1.26750
   Risk:Reward: 1:3.0
   Reasoning: Bearish FVG (conf: 0.75); Fibonacci 0.5 level; bear regime
```

## How FVG & Fibonacci Work

### Fair Value Gaps (FVG)

A **Fair Value Gap** occurs when price moves so fast it leaves an unfilled gap:

```
Bullish FVG (Buy Signal):
Price: 1.1000 → 1.1010 → 1.1025
         ^gap^
The gap from 1.1010-1.1025 acts as support

Bearish FVG (Sell Signal):
Price: 1.1025 → 1.1015 → 1.1000
         ^gap^
The gap from 1.1000-1.1015 acts as resistance
```

**Why It Works:** Large institutions often leave gaps when entering positions. Price tends to return to fill these gaps, creating reversal opportunities.

### Fibonacci Retracements

**Golden Pocket (0.618 - 0.65 level):**

```
Swing High: 1.1200
Swing Low:  1.1000
Range:      0.0200

Golden Pocket: 1.1124 - 1.1130 (62-65% retracement)
   ↑ High-probability reversal zone
```

**Why It Works:** Markets naturally retrace. The 0.618 level (golden ratio) is where strong reversals often occur.

## Integration with Trading Engine

### Add Strategic Hedge Manager

In `oanda/oanda_trading_engine.py`:

```python
from oanda.strategic_hedge_manager import StrategicHedgeManager

class OandaTradingEngine:
    def __init__(self):
        # ... existing code ...
        self.hedge_manager = StrategicHedgeManager(pin=841921)
    
    async def monitor_positions(self):
        for position in self.get_losing_positions():
            decision = self.hedge_manager.maybe_open_hedge(
                position=position,
                current_price=self.get_price(position.symbol),
                prices=self.get_price_history(position.symbol)
            )
            
            if decision and decision.flip_position:
                logger.info(f"Flipping position: {decision.reason}")
                await self.close_and_reverse(position)
            elif decision and decision.should_hedge:
                logger.info(f"Opening hedge: {decision.hedge_ratio:.0%}")
                await self.open_hedge(position, decision.hedge_ratio)
```

### Apply Optimized Parameters

After running `python hive_cli.py optimize`:

```python
import json

# Load optimization results
with open('optimization_results/wolfpack_optimization.json') as f:
    results = json.load(f)

params = results['optimized_parameters']

# Apply to trading engine
engine.confidence_threshold = params['confidence_threshold']
engine.stop_loss_pips = params['stop_loss_pips']
engine.take_profit_pips = params['take_profit_pips']
engine.fvg_weight = params['fvg_weight']
engine.fibonacci_weight = params['fibonacci_weight']
```

### Use Opportunity Scanner

```python
from hive.hive_opportunity_scanner import HiveOpportunityScanner

scanner = HiveOpportunityScanner(pin=841921)

# Run every 15 minutes
while True:
    opportunities = scanner.scan_markets()
    
    for opp in opportunities:
        if opp.confidence >= 0.75:  # High confidence only
            # Execute trade
            await engine.place_trade(
                symbol=opp.symbol,
                direction=opp.direction,
                entry=opp.entry_price,
                stop_loss=opp.stop_loss,
                take_profit=opp.take_profit
            )
            
            logger.info(f"Opportunity trade: {opp.reasoning}")
    
    await asyncio.sleep(900)  # 15 minutes
```

## Example Optimization Results

**Before Optimization:**
- Win Rate: 42%
- Profit Factor: 1.3
- Max Drawdown: $500
- Total PNL: $300

**Hive Recommendations:**
1. Increase confidence_threshold: 0.55 → 0.65 (filter weak signals)
2. Adjust take_profit_pips: 32 → 45 (improve R:R from 3.2:1 to 5.6:1)
3. Reduce max_positions: 12 → 8 (limit drawdown exposure)
4. Increase fvg_weight: 0.20 → 0.30 (leverage gap detection)
5. Increase fibonacci_weight: 0.20 → 0.30 (use golden pocket more)

**Expected After Optimization:**
- Win Rate: 48% (+6%)
- Profit Factor: 2.0 (+54%)
- Max Drawdown: $350 (-30%)
- Total PNL: $520 (+73%)

## Monitoring Schedule

**Daily:**
```bash
python hive_cli.py analyze --hours 24
```
Review performance, check for any red flags

**Weekly:**
```bash
python hive_cli.py optimize --hours 168
```
Get updated parameter recommendations

**Continuous (cron job every 15 min):**
```bash
python hive_cli.py scan > opportunities.log
```
Monitor for high-probability setups

## Understanding the Reports

### OPTIMIZATION_SUMMARY.md

Contains:
- Executive summary of performance
- Immediate actions required
- Parameter update recommendations
- Strategic changes needed

### comprehensive_optimization_report.json

Full data including:
- Log analysis for each strategy
- Hive agent recommendations
- Consensus confidence scores
- Expected improvement percentages
- Backtest simulation scores

## Troubleshooting

**Q: No opportunities found when scanning?**
A: Try lowering min_confidence (default 60%) or expanding pairs/timeframes

**Q: Win rate recommendations seem aggressive?**
A: The hive agents balance multiple factors. Start with 50% of recommended change, monitor, then adjust

**Q: How often should I re-optimize?**
A: Weekly is good. Daily if you're actively changing strategies. Monthly at minimum.

## Next Steps

1. Run `python hive_cli.py optimize` to get your first recommendations
2. Review `optimization_results/OPTIMIZATION_SUMMARY.md`
3. Apply top 2-3 recommended parameter changes
4. Monitor performance for 1 week
5. Re-optimize with new data
6. Enable strategic hedge manager
7. Set up automated opportunity scanning

## Support

- Full documentation: `HIVE_OPTIMIZATION_README.md`
- CLI help: `python hive_cli.py --help`
- Strategy tests: `python -m pytest tests/test_*.py -v`
