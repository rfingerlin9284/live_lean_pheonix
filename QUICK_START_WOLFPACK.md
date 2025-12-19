# Wolfpack EdgePack Choice 1 - Quick Start

## ✅ All Features Are ACTIVE By Default

When you start the trading engine, **ALL** anti-churn and edge-preserving features are automatically active. No manual configuration needed!

## What's Active When You Start

### Anti-Churn Protection (Automatic)
- **Spread Guard**: Rejects orders with spread > 1.2 pips
- **30-Second Hold Time**: Prevents rapid-fire trades
- **Cost Logging**: Records spread, cost, R:R for every trade

### Edge-Preserving Features (Automatic)
- **Regime Gate**: Blocks signals with ML confidence < 0.65
- **Quant Hedge Recovery**: Safe loss recovery (max 1 layer per trade)
- **Surgeon Exit Harmony**: Delays trailing until +0.8R profit

### Charter Limits (Enforced)
- Max Spread: 1.2 pips
- Daily Loss Breaker: 3%
- Max Margin: 25%
- Max Positions: 12 total, 4 per symbol

## How to Start the Engine

Simply run:
```bash
python3 oanda_trading_engine.py
```

That's it! All features are active automatically.

## Verify Features Are Active

To confirm everything is working:
```bash
./tools/verify_wolfpack_edgepack.sh
```

Or see startup confirmation:
```bash
./tools/startup_confirmation.sh
```

## Expected Behavior

When the engine starts, you'll see:
- ✅ Anti-churn features initialized (30s min hold)
- ✅ Spread guard active (1.2 pips max)
- ✅ Regime gate active (0.65 min confidence)
- ✅ All features loaded from config/features.json

## Narration Events to Monitor

Watch for these events in `narration.jsonl`:
- `ANTI_CHURN_BLOCK` - Trade blocked due to 30s hold time
- `GATE_REJECTION` - Trade blocked due to spread > 1.2 pips
- `REGIME_GATE_BLOCKED` - Signal blocked due to low ML confidence
- `COST_ANALYSIS` - Cost logging for each trade

## Configuration File

All features are enabled in `config/features.json`:
```json
{
  "wolfpack_edgepack_choice1": true,
  "regime_gate": true,
  "spread_guard": true,
  "quant_hedge_recovery": true,
  "surgeon_exit_harmony": true
}
```

**No changes needed** - this is the default configuration.

## Disable Features (If Needed)

If you need to disable a feature, edit `config/features.json` and set it to `false`:
```json
{
  "spread_guard": false  // Disables spread guard
}
```

Then restart the engine.

## VSCode Tasks

For convenience, you can also use VSCode tasks:
1. Open Command Palette (Ctrl+Shift+P)
2. Select "Tasks: Run Task"
3. Choose "RBOTzilla: Apply Wolfpack EdgePack Choice 1"

## Troubleshooting

**Q: Are features active when I start?**
A: Yes! All features in `config/features.json` are enabled by default.

**Q: How do I know anti-churn is working?**
A: Watch `narration.jsonl` for `ANTI_CHURN_BLOCK` events, or run `./tools/verify_wolfpack_edgepack.sh`

**Q: Can I adjust the 30s hold time?**
A: Yes, edit `min_hold_seconds` in `oanda_trading_engine.py` (default: 30)

**Q: Can I adjust the spread limit?**
A: Yes, edit `MAX_SPREAD_PIPS` in `rick_hive/rick_charter.py` (default: 1.2)

## Summary

🎉 **Everything is ready!** Just start the engine and all anti-churn features will be active automatically.

No scripts to run, no manual configuration needed. The system is designed to work out of the box with all protections enabled.
