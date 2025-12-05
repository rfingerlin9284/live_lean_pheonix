#!/usr/bin/env python3
"""
Strategy Optimization Orchestrator
Coordinates log analysis, hive optimization, and parameter tuning
PIN: 841921 | Phase: Comprehensive Optimization
"""

import sys
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from util.log_analyzer import LogAnalyzer, StrategyPerformance
from hive.hive_parameter_optimizer import HiveParameterOptimizer, OptimizedParameters
from hive.quant_hedge_rules import QuantHedgeRules
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StrategyOptimizationOrchestrator:
    """
    Master orchestrator for strategy optimization
    
    Workflow:
    1. Analyze logs to understand current performance
    2. Engage hive agents to analyze weaknesses
    3. Generate optimized parameters
    4. Validate with simulations
    5. Produce actionable recommendations
    """
    
    def __init__(self, pin: int = 841921):
        """Initialize Orchestrator"""
        if pin != 841921:
            raise PermissionError("Invalid PIN for Orchestrator")
        
        self.pin_verified = True
        self.logger = logger
        
        # Initialize components
        self.log_analyzer = LogAnalyzer()
        self.hive_optimizer = HiveParameterOptimizer(pin=pin)
        self.quant_hedge = QuantHedgeRules(pin=pin)
        
        self.logger.info("StrategyOptimizationOrchestrator initialized")
    
    def run_full_optimization(
        self,
        strategies: List[str] = None,
        hours_back: int = 24,
        output_dir: str = "optimization_results"
    ) -> Dict:
        """
        Run complete optimization cycle
        
        Args:
            strategies: List of strategies to optimize
            hours_back: Hours of log history to analyze
            output_dir: Directory for output files
            
        Returns:
            Comprehensive optimization report
        """
        if strategies is None:
            strategies = ['wolfpack', 'quant_hedge', 'strategic_hedge']
        
        self.logger.info(f"Starting full optimization for strategies: {strategies}")
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Step 1: Analyze current performance
        self.logger.info("Step 1: Analyzing performance from logs...")
        log_report = self.log_analyzer.generate_report(
            strategies=strategies,
            hours_back=hours_back
        )
        
        # Save log analysis
        log_file = output_path / "log_analysis.json"
        with open(log_file, 'w') as f:
            json.dump(log_report, f, indent=2)
        self.logger.info(f"Log analysis saved to: {log_file}")
        
        # Step 2: Run hive optimization for each strategy
        self.logger.info("Step 2: Running hive parameter optimization...")
        optimization_results = {}
        
        for strategy in strategies:
            self.logger.info(f"Optimizing {strategy}...")
            
            # Extract performance data
            strategy_data = log_report['strategies'].get(strategy, {})
            performance = strategy_data.get('performance', {})
            
            if performance.get('total_trades', 0) == 0:
                self.logger.warning(f"No trades found for {strategy}, skipping optimization")
                continue
            
            # Get current parameters (defaults)
            current_params = self._get_default_params(strategy)
            
            # Get market conditions
            market_conditions = self._analyze_market_conditions()
            
            # Run hive optimization
            optimized = self.hive_optimizer.optimize_with_hive(
                current_params=current_params,
                performance_data=performance,
                market_conditions=market_conditions
            )
            
            optimization_results[strategy] = {
                'current_params': current_params,
                'optimized_params': optimized.parameters,
                'consensus_confidence': optimized.consensus_confidence,
                'contributing_agents': optimized.contributing_agents,
                'expected_improvement': optimized.expected_improvement,
                'backtest_score': optimized.backtest_score,
                'reasoning': optimized.reasoning
            }
            
            # Export individual strategy recommendations
            strategy_file = output_path / f"{strategy}_optimization.json"
            self.hive_optimizer.export_recommendations(optimized, str(strategy_file))
        
        # Step 3: Generate unified recommendations
        self.logger.info("Step 3: Generating unified recommendations...")
        unified_recommendations = self._generate_unified_recommendations(
            optimization_results,
            log_report
        )
        
        # Step 4: Create executive summary
        self.logger.info("Step 4: Creating executive summary...")
        executive_summary = self._create_executive_summary(
            log_report,
            optimization_results,
            unified_recommendations
        )
        
        # Save comprehensive report
        final_report = {
            'generated_at': log_report['generated_at'],
            'analysis_period_hours': hours_back,
            'log_analysis': log_report,
            'optimization_results': optimization_results,
            'unified_recommendations': unified_recommendations,
            'executive_summary': executive_summary
        }
        
        report_file = output_path / "comprehensive_optimization_report.json"
        with open(report_file, 'w') as f:
            json.dump(final_report, f, indent=2)
        
        # Create human-readable summary
        summary_file = output_path / "OPTIMIZATION_SUMMARY.md"
        self._write_markdown_summary(final_report, summary_file)
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info("OPTIMIZATION COMPLETE")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"Reports saved to: {output_dir}/")
        self.logger.info(f"  - {report_file.name}")
        self.logger.info(f"  - {summary_file.name}")
        self.logger.info(f"{'='*60}\n")
        
        return final_report
    
    def _get_default_params(self, strategy: str) -> Dict:
        """Get default parameters for a strategy"""
        # These are the current defaults from the codebase
        base_params = {
            'confidence_threshold': 0.55,
            'stop_loss_pips': 10,
            'take_profit_pips': 32,
            'trailing_start_pips': 3,
            'trailing_dist_pips': 5,
            'max_positions': 12,
            'position_size_multiplier': 1.0,
            'fvg_weight': 0.20,
            'fibonacci_weight': 0.20,
            'momentum_weight': 0.40
        }
        
        # Strategy-specific adjustments
        if 'hedge' in strategy.lower():
            base_params.update({
                'loss_threshold_pips': 15,
                'hedge_ratio_default': 0.5,
                'auto_flip_threshold': 0.75
            })
        
        return base_params
    
    def _analyze_market_conditions(self) -> Dict:
        """Analyze current market conditions"""
        # Simplified - in production would use real market data
        # This would integrate with the quant_hedge regime detector
        
        try:
            # Simulate price data for regime detection
            prices = np.random.normal(1.1000, 0.005, 50)
            volume = np.random.uniform(1000, 5000, 50)
            
            # Use quant hedge to analyze
            analysis = self.quant_hedge.analyze_market_conditions(
                prices=prices,
                volume=volume,
                account_nav=10000,
                margin_used=2000,
                open_positions=3
            )
            
            return {
                'regime': analysis.regime,
                'volatility': analysis.volatility_value,
                'volatility_level': analysis.volatility_level,
                'risk_level': analysis.risk_level,
                'volume_trend': 'normal'  # Simplified
            }
        except Exception as e:
            self.logger.warning(f"Could not analyze market conditions: {e}")
            return {
                'regime': 'triage',
                'volatility': 0.015,
                'volatility_level': 'moderate',
                'risk_level': 'moderate',
                'volume_trend': 'normal'
            }
    
    def _generate_unified_recommendations(
        self,
        optimization_results: Dict,
        log_report: Dict
    ) -> Dict:
        """Generate unified recommendations across all strategies"""
        recommendations = {
            'immediate_actions': [],
            'parameter_updates': {},
            'strategic_changes': []
        }
        
        # Aggregate across strategies
        for strategy, result in optimization_results.items():
            current = result['current_params']
            optimized = result['optimized_params']
            
            # Track parameter changes
            for param, new_value in optimized.items():
                old_value = current.get(param)
                if old_value != new_value:
                    if param not in recommendations['parameter_updates']:
                        recommendations['parameter_updates'][param] = []
                    
                    recommendations['parameter_updates'][param].append({
                        'strategy': strategy,
                        'from': old_value,
                        'to': new_value,
                        'confidence': result['consensus_confidence']
                    })
        
        # Generate immediate actions based on critical issues
        for strategy, data in log_report['strategies'].items():
            perf = data['performance']
            
            if perf['win_rate'] < 0.40:
                recommendations['immediate_actions'].append(
                    f"URGENT: {strategy} win rate critically low ({perf['win_rate']:.1%}) - consider pausing until optimized"
                )
            
            if perf['max_drawdown'] > abs(perf['total_pnl']) * 2:
                recommendations['immediate_actions'].append(
                    f"WARNING: {strategy} drawdown exceeds profits - reduce position sizing immediately"
                )
        
        # Strategic recommendations
        recommendations['strategic_changes'].extend([
            "Integrate FVG detection into all wolf strategies",
            "Apply Fibonacci levels for take-profit targets",
            "Implement hive-driven entry confirmation",
            "Enable strategic hedge manager for losing positions"
        ])
        
        return recommendations
    
    def _create_executive_summary(
        self,
        log_report: Dict,
        optimization_results: Dict,
        recommendations: Dict
    ) -> str:
        """Create executive summary of findings"""
        summary_parts = []
        
        summary_parts.append("EXECUTIVE SUMMARY")
        summary_parts.append("=" * 60)
        summary_parts.append("")
        
        # Overall performance
        total_trades = sum(
            s['performance']['total_trades']
            for s in log_report['strategies'].values()
        )
        total_pnl = sum(
            s['performance']['total_pnl']
            for s in log_report['strategies'].values()
        )
        
        summary_parts.append(f"Analysis Period: {log_report['analysis_period_hours']} hours")
        summary_parts.append(f"Total Trades Analyzed: {total_trades}")
        summary_parts.append(f"Total PnL: ${total_pnl:.2f}")
        summary_parts.append("")
        
        # Strategy breakdown
        summary_parts.append("Strategy Performance:")
        for strategy, data in log_report['strategies'].items():
            perf = data['performance']
            summary_parts.append(f"  {strategy.upper()}:")
            summary_parts.append(f"    - Trades: {perf['total_trades']}")
            summary_parts.append(f"    - Win Rate: {perf['win_rate']:.1%}")
            summary_parts.append(f"    - PnL: ${perf['total_pnl']:.2f}")
            summary_parts.append(f"    - Profit Factor: {perf['profit_factor']:.2f}")
        
        summary_parts.append("")
        
        # Optimization results
        if optimization_results:
            summary_parts.append("Hive Optimization Results:")
            for strategy, result in optimization_results.items():
                summary_parts.append(f"  {strategy.upper()}:")
                summary_parts.append(f"    - Confidence: {result['consensus_confidence']:.1%}")
                summary_parts.append(f"    - Expected Improvement: {result['expected_improvement']:.1%}")
                summary_parts.append(f"    - Backtest Score: {result['backtest_score']:.1f}/100")
        
        summary_parts.append("")
        
        # Critical actions
        if recommendations['immediate_actions']:
            summary_parts.append("IMMEDIATE ACTIONS REQUIRED:")
            for action in recommendations['immediate_actions']:
                summary_parts.append(f"  ! {action}")
            summary_parts.append("")
        
        return "\n".join(summary_parts)
    
    def _write_markdown_summary(self, report: Dict, filename: Path):
        """Write human-readable markdown summary"""
        with open(filename, 'w') as f:
            f.write("# Trading Strategy Optimization Report\n\n")
            f.write(f"**Generated:** {report['generated_at']}\n\n")
            f.write(f"**Analysis Period:** {report['analysis_period_hours']} hours\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write(report['executive_summary'])
            f.write("\n\n")
            
            f.write("## Unified Recommendations\n\n")
            
            recs = report['unified_recommendations']
            
            if recs['immediate_actions']:
                f.write("### ⚠️ Immediate Actions\n\n")
                for action in recs['immediate_actions']:
                    f.write(f"- {action}\n")
                f.write("\n")
            
            if recs['parameter_updates']:
                f.write("### 📊 Parameter Updates\n\n")
                for param, changes in recs['parameter_updates'].items():
                    f.write(f"**{param}:**\n")
                    for change in changes:
                        f.write(f"- {change['strategy']}: {change['from']} → {change['to']} "
                               f"(confidence: {change['confidence']:.1%})\n")
                    f.write("\n")
            
            if recs['strategic_changes']:
                f.write("### 🎯 Strategic Changes\n\n")
                for change in recs['strategic_changes']:
                    f.write(f"- {change}\n")
                f.write("\n")
            
            f.write("## Detailed Analysis\n\n")
            f.write("See `comprehensive_optimization_report.json` for full details.\n")
        
        self.logger.info(f"Markdown summary written to: {filename}")


if __name__ == "__main__":
    # Run optimization
    print("Starting Strategy Optimization Orchestrator...")
    print("=" * 60)
    
    try:
        orchestrator = StrategyOptimizationOrchestrator(pin=841921)
        
        # Run full optimization
        report = orchestrator.run_full_optimization(
            strategies=['wolfpack', 'quant_hedge', 'strategic_hedge'],
            hours_back=24,
            output_dir="optimization_results"
        )
        
        print("\n" + report['executive_summary'])
        
        print("\n✅ Optimization complete! Check optimization_results/ directory")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
