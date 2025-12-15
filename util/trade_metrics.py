import os
import json
from datetime import datetime, timezone
from pathlib import Path

def record_trade_event(venue, symbol, direction, entry_price, stop_loss, take_profit, size, pnl_usd=None, pnl_pips=None, meta=None):
    """Append a trade event as JSON to metrics/trades.jsonl"""
    metrics_dir = Path('metrics')
    metrics_dir.mkdir(exist_ok=True)
    event = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'venue': venue,
        'symbol': symbol,
        'direction': direction,
        'entry_price': entry_price,
        'stop_loss': stop_loss,
        'take_profit': take_profit,
        'size': size,
        'pnl_usd': pnl_usd,
        'pnl_pips': pnl_pips,
        'meta': meta or {}
    }
    with open(metrics_dir / 'trades.jsonl', 'a') as f:
        f.write(json.dumps(event) + '\n')

def summarize_metrics(window_days=None):
    """Prints a summary of trades in metrics/trades.jsonl (optionally filter by days)"""
    from collections import Counter, defaultdict
    import pandas as pd
    metrics_file = Path('metrics/trades.jsonl')
    if not metrics_file.exists():
        print('No metrics found.')
        return
    rows = []
    with open(metrics_file) as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    if not rows:
        print('No trades found.')
        return
    df = pd.DataFrame(rows)
    if window_days:
        cutoff = pd.Timestamp.utcnow() - pd.Timedelta(days=window_days)
        df = df[pd.to_datetime(df['timestamp']) >= cutoff]
    print(f"Total trades: {len(df)}")
    print("Trades by venue:")
    print(df['venue'].value_counts())
    print("Win rate (if PnL available):")
    if 'pnl_usd' in df:
        wins = df['pnl_usd'].dropna() > 0
        print(f"Win rate: {wins.mean()*100:.1f}%")
    print("Top 5 symbols:")
    print(df['symbol'].value_counts().head(5))
    if 'pnl_usd' in df:
        print(f"Total PnL: ${df['pnl_usd'].dropna().sum():.2f}")
