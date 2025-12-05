#!/usr/bin/env python3
"""
Trading Log Analyzer - Performance Analysis & Parameter Optimization
Analyzes narration logs to identify patterns and optimize parameters
PIN: 841921 | Phase: Analysis & Optimization
"""

import json
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class StrategyPerformance:
    """Performance metrics for a trading strategy"""
    strategy_name: str
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    avg_profit: float
    avg_loss: float
    profit_factor: float
    total_pnl: float
    max_drawdown: float
    sharpe_ratio: float
    avg_hold_time_minutes: float
    best_pairs: List[Tuple[str, float]]  # (pair, win_rate)
    worst_pairs: List[Tuple[str, float]]
    best_timeframes: List[Tuple[str, float]]
    parameter_insights: Dict[str, any]


@dataclass
class ParameterRecommendation:
    """Recommended parameter adjustments"""
    parameter_name: str
    current_value: any
    recommended_value: any
    expected_improvement: float
    confidence: float
    reasoning: str


class LogAnalyzer:
    """
    Analyzes trading logs to extract performance metrics and optimize parameters
    """
    
    def __init__(self, log_path: str = None):
        """Initialize Log Analyzer"""
        if log_path is None:
            # Default to narration.jsonl in repo root
            log_path = Path(__file__).parent.parent / "narration.jsonl"
        
        self.log_path = Path(log_path)
        self.logger = logger
        
        # Performance tracking
        self.trades_by_strategy = defaultdict(list)
        self.trades_by_pair = defaultdict(list)
        self.hedge_events = []
        self.signal_events = []
        
        self.logger.info(f"LogAnalyzer initialized with log: {self.log_path}")
    
    def load_logs(self, hours_back: int = 24) -> List[Dict]:
        """
        Load and parse log entries from the specified time window
        
        Args:
            hours_back: Number of hours of history to analyze
            
        Returns:
            List of parsed log entries
        """
        if not self.log_path.exists():
            self.logger.warning(f"Log file not found: {self.log_path}")
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        logs = []
        
        with open(self.log_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    
                    # Parse timestamp
                    ts_str = entry.get('timestamp', '')
                    if ts_str:
                        ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                        if ts > cutoff_time:
                            logs.append(entry)
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    self.logger.debug(f"Error parsing log entry: {e}")
                    continue
        
        self.logger.info(f"Loaded {len(logs)} log entries from last {hours_back} hours")
        return logs
    
    def analyze_strategy_performance(
        self,
        strategy_name: str,
        logs: List[Dict]
    ) -> StrategyPerformance:
        """
        Analyze performance of a specific strategy
        
        Args:
            strategy_name: Name of strategy (e.g., "wolfpack", "quant_hedge", "strategic_hedge")
            logs: Log entries to analyze
            
        Returns:
            StrategyPerformance object with metrics
        """
        # Filter logs for this strategy
        strategy_logs = [
            log for log in logs
            if strategy_name.lower() in str(log.get('details', {})).lower()
            or strategy_name.lower() in log.get('event_type', '').lower()
        ]
        
        # Extract trade outcomes
        trades = []
        for log in strategy_logs:
            event_type = log.get('event_type', '')
            details = log.get('details', {})
            
            if 'TRADE' in event_type or 'ORDER' in event_type:
                if 'pnl' in details or 'profit' in details:
                    pnl = details.get('pnl', details.get('profit', 0))
                    trades.append({
                        'pnl': float(pnl),
                        'symbol': log.get('symbol', 'UNKNOWN'),
                        'timestamp': log.get('timestamp'),
                        'details': details
                    })
        
        if not trades:
            self.logger.warning(f"No trades found for strategy: {strategy_name}")
            return self._empty_performance(strategy_name)
        
        # Calculate metrics
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['pnl'] > 0])
        losing_trades = len([t for t in trades if t['pnl'] < 0])
        
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        profits = [t['pnl'] for t in trades if t['pnl'] > 0]
        losses = [abs(t['pnl']) for t in trades if t['pnl'] < 0]
        
        avg_profit = np.mean(profits) if profits else 0
        avg_loss = np.mean(losses) if losses else 0
        
        total_profit = sum(profits)
        total_loss = sum(losses)
        profit_factor = total_profit / total_loss if total_loss > 0 else 0
        
        total_pnl = sum(t['pnl'] for t in trades)
        
        # Calculate drawdown
        cumulative_pnl = np.cumsum([t['pnl'] for t in trades])
        running_max = np.maximum.accumulate(cumulative_pnl)
        drawdowns = running_max - cumulative_pnl
        max_drawdown = np.max(drawdowns) if len(drawdowns) > 0 else 0
        
        # Calculate Sharpe ratio (simplified)
        returns = [t['pnl'] for t in trades]
        sharpe_ratio = np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
        
        # Analyze by pair
        pair_performance = defaultdict(lambda: {'wins': 0, 'total': 0})
        for trade in trades:
            pair = trade['symbol']
            pair_performance[pair]['total'] += 1
            if trade['pnl'] > 0:
                pair_performance[pair]['wins'] += 1
        
        best_pairs = sorted(
            [(pair, stats['wins'] / stats['total']) for pair, stats in pair_performance.items()],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        worst_pairs = sorted(
            [(pair, stats['wins'] / stats['total']) for pair, stats in pair_performance.items()],
            key=lambda x: x[1]
        )[:3]
        
        return StrategyPerformance(
            strategy_name=strategy_name,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            avg_profit=avg_profit,
            avg_loss=avg_loss,
            profit_factor=profit_factor,
            total_pnl=total_pnl,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            avg_hold_time_minutes=0,  # Would need more detailed log data
            best_pairs=best_pairs,
            worst_pairs=worst_pairs,
            best_timeframes=[],
            parameter_insights={}
        )
    
    def _empty_performance(self, strategy_name: str) -> StrategyPerformance:
        """Return empty performance object"""
        return StrategyPerformance(
            strategy_name=strategy_name,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0,
            avg_profit=0,
            avg_loss=0,
            profit_factor=0,
            total_pnl=0,
            max_drawdown=0,
            sharpe_ratio=0,
            avg_hold_time_minutes=0,
            best_pairs=[],
            worst_pairs=[],
            best_timeframes=[],
            parameter_insights={}
        )
    
    def optimize_parameters(
        self,
        strategy_name: str,
        performance: StrategyPerformance
    ) -> List[ParameterRecommendation]:
        """
        Generate parameter optimization recommendations
        
        Args:
            strategy_name: Strategy to optimize
            performance: Current performance metrics
            
        Returns:
            List of parameter recommendations
        """
        recommendations = []
        
        # Analyze win rate and suggest adjustments
        if performance.win_rate < 0.45:
            # Low win rate - tighten entry criteria
            recommendations.append(ParameterRecommendation(
                parameter_name="confidence_threshold",
                current_value=0.55,
                recommended_value=0.65,
                expected_improvement=0.15,
                confidence=0.75,
                reasoning="Win rate below 45% - increase confidence threshold to filter weak signals"
            ))
        
        # Analyze profit factor
        if performance.profit_factor < 1.5 and performance.avg_loss > performance.avg_profit * 0.8:
            # Poor risk/reward ratio
            recommendations.append(ParameterRecommendation(
                parameter_name="take_profit_pips",
                current_value=32,
                recommended_value=45,
                expected_improvement=0.20,
                confidence=0.70,
                reasoning="Profit factor low - increase take profit target for better R:R"
            ))
            
            recommendations.append(ParameterRecommendation(
                parameter_name="stop_loss_pips",
                current_value=10,
                recommended_value=8,
                expected_improvement=0.15,
                confidence=0.65,
                reasoning="Average loss too high - tighten stop loss"
            ))
        
        # Analyze drawdown
        if performance.max_drawdown > abs(performance.total_pnl) * 0.3:
            # High drawdown relative to profits
            recommendations.append(ParameterRecommendation(
                parameter_name="max_positions",
                current_value=12,
                recommended_value=8,
                expected_improvement=0.25,
                confidence=0.80,
                reasoning="High drawdown - reduce max positions to limit exposure"
            ))
        
        # Strategy-specific recommendations
        if 'wolfpack' in strategy_name.lower():
            recommendations.extend(self._optimize_wolfpack_params(performance))
        elif 'hedge' in strategy_name.lower():
            recommendations.extend(self._optimize_hedge_params(performance))
        
        return recommendations
    
    def _optimize_wolfpack_params(self, performance: StrategyPerformance) -> List[ParameterRecommendation]:
        """Wolfpack-specific parameter optimization"""
        recommendations = []
        
        # Check if certain pairs consistently underperform
        if performance.worst_pairs:
            worst_pair, worst_wr = performance.worst_pairs[0]
            if worst_wr < 0.35:
                recommendations.append(ParameterRecommendation(
                    parameter_name="pair_blacklist",
                    current_value=[],
                    recommended_value=[worst_pair],
                    expected_improvement=0.10,
                    confidence=0.70,
                    reasoning=f"{worst_pair} has very low win rate ({worst_wr:.1%}) - consider blacklisting"
                ))
        
        return recommendations
    
    def _optimize_hedge_params(self, performance: StrategyPerformance) -> List[ParameterRecommendation]:
        """Hedge-specific parameter optimization"""
        recommendations = []
        
        # If hedge is losing money, may be too aggressive
        if performance.total_pnl < 0:
            recommendations.append(ParameterRecommendation(
                parameter_name="loss_threshold_pips",
                current_value=15,
                recommended_value=20,
                expected_improvement=0.20,
                confidence=0.65,
                reasoning="Hedge showing losses - wait longer before hedging to avoid whipsaws"
            ))
        
        return recommendations
    
    def generate_report(
        self,
        strategies: List[str] = None,
        hours_back: int = 24
    ) -> Dict:
        """
        Generate comprehensive performance report
        
        Args:
            strategies: List of strategy names to analyze
            hours_back: Hours of history to analyze
            
        Returns:
            Report dictionary with performance and recommendations
        """
        if strategies is None:
            strategies = ['wolfpack', 'quant_hedge', 'strategic_hedge']
        
        logs = self.load_logs(hours_back=hours_back)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'analysis_period_hours': hours_back,
            'total_log_entries': len(logs),
            'strategies': {}
        }
        
        for strategy in strategies:
            performance = self.analyze_strategy_performance(strategy, logs)
            recommendations = self.optimize_parameters(strategy, performance)
            
            report['strategies'][strategy] = {
                'performance': asdict(performance),
                'recommendations': [asdict(rec) for rec in recommendations]
            }
        
        return report


if __name__ == "__main__":
    # Self-test
    print("Log Analyzer self-test...")
    
    try:
        analyzer = LogAnalyzer()
        
        # Generate report
        report = analyzer.generate_report(hours_back=24)
        
        print(f"\n✅ Analysis Report Generated:")
        print(f"   Period: {report['analysis_period_hours']} hours")
        print(f"   Log Entries: {report['total_log_entries']}")
        print(f"   Strategies Analyzed: {len(report['strategies'])}")
        
        for strategy, data in report['strategies'].items():
            perf = data['performance']
            print(f"\n   {strategy.upper()}:")
            print(f"      Trades: {perf['total_trades']}")
            print(f"      Win Rate: {perf['win_rate']:.1%}")
            print(f"      Total PNL: ${perf['total_pnl']:.2f}")
            print(f"      Recommendations: {len(data['recommendations'])}")
        
        print("\n✅ LogAnalyzer module validated")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
