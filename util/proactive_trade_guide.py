#!/usr/bin/env python3
"""
Proactive Market Scan & Trade Guide Generator
- Aggregates news, indicator, FVG, Fib, and consensus data
- Asks Rick/hive for best pairs and rationale
- Generates actionable trade guides instead of passively waiting for signals
"""
import sys
import os
import pandas as pd
from datetime import datetime
# Ensure project root is in sys.path for imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from util.strategy_aggregator import StrategyAggregator
from util.narration_logger import log_narration
from oanda.oanda_trading_engine import OandaTradingEngine

# Placeholder for news aggregation (to be replaced with real news API)
def get_market_news():
    # Simulate news headlines
    return [
        "USD rallies on strong NFP report",
        "EUR weakens amid ECB dovish tone",
        "JPY gains as risk-off sentiment returns",
    ]

def scan_all_pairs(engine, aggregator):
    guides = []
    for symbol in engine.TRADING_PAIRS:
        candles = engine.oanda.get_historical_data(symbol, count=120, granularity='M15')
        if not candles or len(candles) < 50:
            continue
        # Convert to DataFrame for aggregator
        df = pd.DataFrame([
            {
                'open': float(c.get('mid', {}).get('o', 0)),
                'high': float(c.get('mid', {}).get('h', 0)),
                'low': float(c.get('mid', {}).get('l', 0)),
                'close': float(c.get('mid', {}).get('c', 0)),
            } for c in candles
        ])
        signals = aggregator.aggregate_signals(df, symbol)
        for sig in signals:
            strength = aggregator.evaluate_signal_strength(sig)
            guide = {
                'symbol': symbol,
                'action': sig['action'],
                'confidence': sig['confidence'],
                'strength': strength,
                'entry': sig['entry'],
                'sl': sig['sl'],
                'tp': sig['tp'],
                'rr_ratio': sig['rr_ratio'],
                'strategies': sig['strategy_names'],
                'timestamp': sig['timestamp'],
                'tag': sig['tag'],
            }
            guides.append(guide)
            log_narration(
                event_type="PROACTIVE_TRADE_GUIDE",
                details=guide,
                symbol=symbol,
                venue="oanda"
            )
    return guides

def main():
    print("Proactive Market Scan & Trade Guide Generator\n" + "="*60)
    engine = OandaTradingEngine(environment=os.getenv('RICK_ENV', 'practice'))
    aggregator = StrategyAggregator(signal_vote_threshold=2)
    news = get_market_news()
    print("\n--- Market News Headlines ---")
    for headline in news:
        print("-", headline)
    print("\n--- Scanning All Pairs for Best Opportunities ---")
    guides = scan_all_pairs(engine, aggregator)
    if not guides:
        print("No actionable trade guides found.")
        return
    # Sort by strength/confidence
    guides = sorted(guides, key=lambda g: (g['strength'], g['confidence']), reverse=True)
    print("\n--- Top Trade Guides ---")
    for g in guides[:5]:
        print(f"{g['symbol']} | {g['action'].upper()} | Strength: {g['strength']:.2f} | Conf: {g['confidence']:.2f} | R:R: {g['rr_ratio']:.2f}")
        print(f"  Entry: {g['entry']:.5f} | SL: {g['sl']:.5f} | TP: {g['tp']:.5f}")
        print(f"  Strategies: {g['strategies']} | Tag: {g['tag']}")
        print(f"  Timestamp: {g['timestamp']}")
        print()
    print("\nAsk Rick: Best pairs and why?")
    for g in guides[:3]:
        print(f"- {g['symbol']}: {g['action'].upper()} (Strength: {g['strength']:.2f}) | Rationale: {g['strategies']}")

if __name__ == "__main__":
    main()
