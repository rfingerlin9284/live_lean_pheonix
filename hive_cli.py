#!/usr/bin/env python3
"""
Hive Analysis CLI - Command-line interface for trading analysis
Provides easy access to log analysis, parameter optimization, and opportunity scanning
PIN: 841921
"""

import sys
import argparse
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from optimize_strategies import StrategyOptimizationOrchestrator
from hive.hive_opportunity_scanner import HiveOpportunityScanner
from util.log_analyzer import LogAnalyzer


def analyze_logs(args):
    """Analyze trading logs"""
    print("\n" + "="*60)
    print("ANALYZING TRADING LOGS")
    print("="*60 + "\n")
    
    analyzer = LogAnalyzer()
    report = analyzer.generate_report(
        strategies=args.strategies,
        hours_back=args.hours
    )
    
    # Print summary
    print(f"Analysis Period: {args.hours} hours")
    print(f"Total Log Entries: {report['total_log_entries']}\n")
    
    for strategy, data in report['strategies'].items():
        perf = data['performance']
        print(f"{strategy.upper()}:")
        print(f"  Trades: {perf['total_trades']}")
        print(f"  Win Rate: {perf['win_rate']:.1%}")
        print(f"  Total PNL: ${perf['total_pnl']:.2f}")
        print(f"  Profit Factor: {perf['profit_factor']:.2f}")
        
        if perf['best_pairs']:
            best_pair, best_wr = perf['best_pairs'][0]
            print(f"  Best Pair: {best_pair} ({best_wr:.1%} win rate)")
        
        recs = data['recommendations']
        if recs:
            print(f"  Recommendations: {len(recs)}")
            for rec in recs[:3]:  # Show top 3
                print(f"    - {rec['parameter_name']}: {rec['current_value']} → {rec['recommended_value']}")
        print()
    
    # Save report
    output_file = "log_analysis_report.json"
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Full report saved to: {output_file}\n")


def optimize_parameters(args):
    """Run parameter optimization"""
    print("\n" + "="*60)
    print("RUNNING HIVE PARAMETER OPTIMIZATION")
    print("="*60 + "\n")
    
    orchestrator = StrategyOptimizationOrchestrator(pin=841921)
    
    report = orchestrator.run_full_optimization(
        strategies=args.strategies,
        hours_back=args.hours,
        output_dir=args.output_dir
    )
    
    print("\n" + report['executive_summary'])
    
    # Show key recommendations
    recs = report.get('unified_recommendations', {})
    
    if recs.get('immediate_actions'):
        print("\n⚠️  IMMEDIATE ACTIONS:")
        for action in recs['immediate_actions']:
            print(f"  • {action}")
    
    if recs.get('parameter_updates'):
        print("\n📊 RECOMMENDED PARAMETER UPDATES:")
        for param, changes in recs['parameter_updates'].items():
            print(f"\n  {param}:")
            for change in changes:
                print(f"    {change['strategy']}: {change['from']} → {change['to']} "
                      f"(confidence: {change['confidence']:.1%})")
    
    print(f"\n✅ Full results saved to: {args.output_dir}/\n")


def scan_opportunities(args):
    """Scan for trading opportunities"""
    print("\n" + "="*60)
    print("SCANNING MARKETS FOR OPPORTUNITIES")
    print("="*60 + "\n")
    
    scanner = HiveOpportunityScanner(pin=841921)
    
    # Parse pairs and timeframes
    pairs = args.pairs if args.pairs else None
    timeframes = args.timeframes if args.timeframes else None
    
    opportunities = scanner.scan_markets(pairs=pairs, timeframes=timeframes)
    
    # Print results
    scanner.print_opportunities(opportunities)
    
    # Export
    if opportunities:
        filename = scanner.export_opportunities(opportunities, args.output)
        print(f"✅ Opportunities exported to: {filename}\n")
    else:
        print("ℹ️  No high-confidence opportunities found at this time.\n")
        print("Try adjusting scanner parameters or checking different pairs/timeframes.\n")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Hive Analysis CLI - Trading analysis and optimization tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze logs from last 48 hours
  python hive_cli.py analyze --hours 48
  
  # Optimize parameters for specific strategies
  python hive_cli.py optimize --strategies wolfpack quant_hedge
  
  # Scan for trading opportunities
  python hive_cli.py scan
  
  # Scan specific pairs
  python hive_cli.py scan --pairs EUR_USD GBP_USD --timeframes H1 H4
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze trading logs')
    analyze_parser.add_argument(
        '--strategies',
        nargs='+',
        default=['wolfpack', 'quant_hedge', 'strategic_hedge'],
        help='Strategies to analyze'
    )
    analyze_parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Hours of history to analyze (default: 24)'
    )
    
    # Optimize command
    optimize_parser = subparsers.add_parser('optimize', help='Optimize parameters using hive')
    optimize_parser.add_argument(
        '--strategies',
        nargs='+',
        default=['wolfpack', 'quant_hedge', 'strategic_hedge'],
        help='Strategies to optimize'
    )
    optimize_parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Hours of history to analyze (default: 24)'
    )
    optimize_parser.add_argument(
        '--output-dir',
        default='optimization_results',
        help='Output directory for results'
    )
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan for trading opportunities')
    scan_parser.add_argument(
        '--pairs',
        nargs='+',
        help='Currency pairs to scan (default: all configured)'
    )
    scan_parser.add_argument(
        '--timeframes',
        nargs='+',
        help='Timeframes to analyze (default: M15 H1 H4)'
    )
    scan_parser.add_argument(
        '--output',
        default='trading_opportunities.json',
        help='Output filename for opportunities'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'analyze':
            analyze_logs(args)
        elif args.command == 'optimize':
            optimize_parameters(args)
        elif args.command == 'scan':
            scan_opportunities(args)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
