import sys
sys.path.insert(0, '.')
from util.trade_metrics import summarize_metrics

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Summarize trade metrics')
    parser.add_argument('--days', type=int, default=None, help='Window (days) to summarize')
    args = parser.parse_args()
    summarize_metrics(window_days=args.days)
