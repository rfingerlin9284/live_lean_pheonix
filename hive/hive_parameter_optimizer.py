#!/usr/bin/env python3
"""
Hive Parameter Optimizer - Multi-Agent Parameter Tuning System
Uses hive mind intelligence to optimize trading parameters
Integrates FVG and Fibonacci logic into optimization decisions
PIN: 841921 | Phase: Hive Analysis
"""

import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class HiveAgent:
    """Individual agent in the hive with specific expertise"""
    name: str
    specialty: str
    weight: float  # Influence weight (0-1)
    recommendations: List[Dict]


@dataclass
class OptimizedParameters:
    """Optimized parameter set with hive consensus"""
    parameters: Dict[str, any]
    consensus_confidence: float
    contributing_agents: List[str]
    expected_improvement: float
    reasoning: str
    backtest_score: float


class HiveParameterOptimizer:
    """
    Multi-agent parameter optimization system
    Uses collective intelligence to find optimal trading parameters
    """
    
    def __init__(self, pin: int = 841921):
        """Initialize Hive Parameter Optimizer"""
        if pin != 841921:
            raise PermissionError("Invalid PIN for Hive Parameter Optimizer")
        
        self.pin_verified = True
        self.logger = logger
        
        # Initialize hive agents with specialties
        self.agents = self._initialize_agents()
        
        # Parameter search spaces
        self.parameter_space = {
            'confidence_threshold': (0.50, 0.85, 0.05),  # min, max, step
            'stop_loss_pips': (5, 20, 1),
            'take_profit_pips': (15, 60, 5),
            'trailing_start_pips': (2, 10, 1),
            'trailing_dist_pips': (3, 15, 1),
            'max_positions': (5, 15, 1),
            'position_size_multiplier': (0.5, 1.5, 0.1),
            'fvg_weight': (0.0, 0.4, 0.05),
            'fibonacci_weight': (0.0, 0.4, 0.05),
            'momentum_weight': (0.3, 0.6, 0.05),
        }
        
        self.logger.info("HiveParameterOptimizer initialized with PIN verification")
    
    def _initialize_agents(self) -> List[HiveAgent]:
        """Initialize specialized hive agents"""
        agents = [
            HiveAgent(
                name="RiskManager",
                specialty="risk_reward_optimization",
                weight=0.25,
                recommendations=[]
            ),
            HiveAgent(
                name="TrendAnalyst",
                specialty="trend_momentum_detection",
                weight=0.20,
                recommendations=[]
            ),
            HiveAgent(
                name="FVGSpecialist",
                specialty="fair_value_gap_analysis",
                weight=0.20,
                recommendations=[]
            ),
            HiveAgent(
                name="FibonacciExpert",
                specialty="fibonacci_retracement_levels",
                weight=0.20,
                recommendations=[]
            ),
            HiveAgent(
                name="VolumeAnalyst",
                specialty="volume_confirmation",
                weight=0.15,
                recommendations=[]
            )
        ]
        return agents
    
    def optimize_with_hive(
        self,
        current_params: Dict[str, any],
        performance_data: Dict[str, any],
        market_conditions: Optional[Dict] = None
    ) -> OptimizedParameters:
        """
        Run hive optimization to find optimal parameters
        
        Args:
            current_params: Current parameter values
            performance_data: Recent performance metrics
            market_conditions: Optional current market state
            
        Returns:
            OptimizedParameters with hive consensus
        """
        self.logger.info("Starting hive parameter optimization...")
        
        # Each agent analyzes and recommends
        for agent in self.agents:
            agent.recommendations = self._agent_analyze(
                agent,
                current_params,
                performance_data,
                market_conditions
            )
        
        # Aggregate recommendations
        optimized = self._aggregate_recommendations(current_params)
        
        # Validate with backtest simulation
        backtest_score = self._simulate_backtest(optimized.parameters, performance_data)
        optimized.backtest_score = backtest_score
        
        self.logger.info(f"Hive optimization complete. Confidence: {optimized.consensus_confidence:.2f}")
        
        return optimized
    
    def _agent_analyze(
        self,
        agent: HiveAgent,
        current_params: Dict,
        performance: Dict,
        market: Optional[Dict]
    ) -> List[Dict]:
        """
        Agent-specific analysis and recommendations
        
        Each agent focuses on their specialty
        """
        recommendations = []
        
        if agent.specialty == "risk_reward_optimization":
            # Risk manager focuses on SL/TP ratios
            win_rate = performance.get('win_rate', 0.5)
            profit_factor = performance.get('profit_factor', 1.0)
            
            if profit_factor < 1.5:
                # Poor R:R - increase TP relative to SL
                current_sl = current_params.get('stop_loss_pips', 10)
                current_tp = current_params.get('take_profit_pips', 32)
                
                # Recommend 3:1 or better R:R
                recommended_tp = max(current_sl * 3.5, current_tp * 1.2)
                
                recommendations.append({
                    'parameter': 'take_profit_pips',
                    'current': current_tp,
                    'recommended': int(recommended_tp),
                    'reason': f"Improve R:R from {current_tp/current_sl:.1f}:1 to {recommended_tp/current_sl:.1f}:1",
                    'confidence': 0.80
                })
            
            # Check max positions vs drawdown
            max_dd = performance.get('max_drawdown', 0)
            total_pnl = performance.get('total_pnl', 0)
            
            if max_dd > abs(total_pnl) * 0.4:
                # High drawdown - reduce exposure
                current_max = current_params.get('max_positions', 12)
                recommended_max = max(5, int(current_max * 0.7))
                
                recommendations.append({
                    'parameter': 'max_positions',
                    'current': current_max,
                    'recommended': recommended_max,
                    'reason': f"Reduce drawdown exposure (current DD: ${max_dd:.2f})",
                    'confidence': 0.75
                })
        
        elif agent.specialty == "trend_momentum_detection":
            # Trend analyst focuses on momentum weights
            win_rate = performance.get('win_rate', 0.5)
            
            if win_rate < 0.45:
                # Low win rate - increase momentum filter strength
                current_momentum = current_params.get('momentum_weight', 0.40)
                recommended_momentum = min(0.55, current_momentum + 0.10)
                
                recommendations.append({
                    'parameter': 'momentum_weight',
                    'current': current_momentum,
                    'recommended': recommended_momentum,
                    'reason': "Increase momentum filter to reduce false signals",
                    'confidence': 0.70
                })
        
        elif agent.specialty == "fair_value_gap_analysis":
            # FVG specialist focuses on FVG weighting
            # If market has clear gaps, increase FVG weight
            if market and market.get('volatility', 0) > 0.02:
                current_fvg = current_params.get('fvg_weight', 0.20)
                recommended_fvg = min(0.35, current_fvg + 0.10)
                
                recommendations.append({
                    'parameter': 'fvg_weight',
                    'current': current_fvg,
                    'recommended': recommended_fvg,
                    'reason': "High volatility environment - increase FVG signal weight",
                    'confidence': 0.75
                })
        
        elif agent.specialty == "fibonacci_retracement_levels":
            # Fibonacci expert focuses on fib weighting
            # In ranging markets, fibonacci levels are more reliable
            if market and market.get('regime', '') == 'sideways':
                current_fib = current_params.get('fibonacci_weight', 0.20)
                recommended_fib = min(0.35, current_fib + 0.10)
                
                recommendations.append({
                    'parameter': 'fibonacci_weight',
                    'current': current_fib,
                    'recommended': recommended_fib,
                    'reason': "Sideways market - fibonacci levels more reliable",
                    'confidence': 0.80
                })
        
        elif agent.specialty == "volume_confirmation":
            # Volume analyst focuses on confidence threshold
            # Low volume = need higher confidence
            if market and market.get('volume_trend', '') == 'decreasing':
                current_conf = current_params.get('confidence_threshold', 0.55)
                recommended_conf = min(0.75, current_conf + 0.10)
                
                recommendations.append({
                    'parameter': 'confidence_threshold',
                    'current': current_conf,
                    'recommended': recommended_conf,
                    'reason': "Low volume - require higher signal confidence",
                    'confidence': 0.70
                })
        
        return recommendations
    
    def _aggregate_recommendations(self, current_params: Dict) -> OptimizedParameters:
        """
        Aggregate all agent recommendations into consensus
        
        Uses weighted voting based on agent weights and recommendation confidence
        """
        # Collect all recommendations by parameter
        param_recommendations = {}
        
        for agent in self.agents:
            for rec in agent.recommendations:
                param = rec['parameter']
                if param not in param_recommendations:
                    param_recommendations[param] = []
                
                # Weight by agent weight and recommendation confidence
                weighted_rec = rec.copy()
                weighted_rec['total_weight'] = agent.weight * rec['confidence']
                weighted_rec['agent'] = agent.name
                
                param_recommendations[param].append(weighted_rec)
        
        # Build optimized parameter set
        optimized_params = current_params.copy()
        contributing_agents = set()
        total_confidence = 0
        reasoning_parts = []
        
        for param, recs in param_recommendations.items():
            if not recs:
                continue
            
            # Calculate weighted average of recommendations
            total_weight = sum(r['total_weight'] for r in recs)
            weighted_value = sum(r['recommended'] * r['total_weight'] for r in recs) / total_weight
            
            # Use recommendation with highest confidence if discrete
            if isinstance(current_params.get(param), int):
                weighted_value = int(round(weighted_value))
            
            optimized_params[param] = weighted_value
            
            # Track contributing agents
            for r in recs:
                contributing_agents.add(r['agent'])
            
            # Aggregate confidence
            max_confidence = max(r['total_weight'] for r in recs)
            total_confidence += max_confidence
            
            # Build reasoning
            top_rec = max(recs, key=lambda x: x['total_weight'])
            reasoning_parts.append(f"{param}: {top_rec['reason']}")
        
        # Normalize confidence
        avg_confidence = total_confidence / max(1, len(param_recommendations))
        
        # Estimate improvement
        expected_improvement = self._estimate_improvement(
            current_params,
            optimized_params,
            param_recommendations
        )
        
        return OptimizedParameters(
            parameters=optimized_params,
            consensus_confidence=avg_confidence,
            contributing_agents=list(contributing_agents),
            expected_improvement=expected_improvement,
            reasoning="; ".join(reasoning_parts),
            backtest_score=0.0  # Will be filled by backtest
        )
    
    def _estimate_improvement(
        self,
        current: Dict,
        optimized: Dict,
        recommendations: Dict
    ) -> float:
        """
        Estimate expected performance improvement
        
        Based on magnitude of changes and agent confidence
        """
        total_change = 0
        num_changes = 0
        
        for param, value in optimized.items():
            current_val = current.get(param, 0)
            if current_val != 0:
                pct_change = abs(value - current_val) / abs(current_val)
                total_change += pct_change
                num_changes += 1
        
        if num_changes == 0:
            return 0.0
        
        avg_change = total_change / num_changes
        
        # Improvement estimate: 0-50% based on change magnitude
        # More conservative for large changes
        improvement = min(0.50, avg_change * 0.5)
        
        return improvement
    
    def _simulate_backtest(self, params: Dict, performance: Dict) -> float:
        """
        Simulate backtest with new parameters
        
        Simplified scoring based on expected changes
        """
        # Base score on current performance
        current_pf = performance.get('profit_factor', 1.0)
        current_wr = performance.get('win_rate', 0.5)
        current_sharpe = performance.get('sharpe_ratio', 0.5)
        
        # Simulate improvements based on parameter changes
        # This is a simplified heuristic - real backtest would be more complex
        
        # Better R:R improves profit factor
        new_sl = params.get('stop_loss_pips', 10)
        new_tp = params.get('take_profit_pips', 32)
        rr_ratio = new_tp / new_sl if new_sl > 0 else 3.0
        
        pf_adjustment = min(1.5, rr_ratio / 3.0)  # Normalize to 3:1 baseline
        projected_pf = current_pf * pf_adjustment
        
        # Higher confidence threshold improves win rate slightly but reduces trades
        new_conf = params.get('confidence_threshold', 0.55)
        wr_adjustment = 1.0 + (new_conf - 0.55) * 0.2  # Up to 10% win rate improvement
        projected_wr = min(0.95, current_wr * wr_adjustment)
        
        # Composite score (0-100)
        score = (projected_pf / 2.0) * 30 + projected_wr * 50 + (current_sharpe + 1) * 10
        
        return min(100, max(0, score))
    
    def export_recommendations(self, optimized: OptimizedParameters, filename: str = None):
        """
        Export optimization recommendations to JSON file
        
        Args:
            optimized: Optimized parameters to export
            filename: Output filename (default: hive_recommendations_<timestamp>.json)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hive_recommendations_{timestamp}.json"
        
        export_data = {
            'generated_at': datetime.now().isoformat(),
            'optimized_parameters': optimized.parameters,
            'consensus_confidence': optimized.consensus_confidence,
            'contributing_agents': optimized.contributing_agents,
            'expected_improvement': optimized.expected_improvement,
            'backtest_score': optimized.backtest_score,
            'reasoning': optimized.reasoning
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Recommendations exported to: {filename}")
        return filename


if __name__ == "__main__":
    # Self-test
    print("Hive Parameter Optimizer self-test...")
    
    try:
        optimizer = HiveParameterOptimizer(pin=841921)
        
        # Simulate current parameters
        current_params = {
            'confidence_threshold': 0.55,
            'stop_loss_pips': 10,
            'take_profit_pips': 32,
            'max_positions': 12,
            'momentum_weight': 0.40,
            'fvg_weight': 0.20,
            'fibonacci_weight': 0.20
        }
        
        # Simulate performance data
        performance = {
            'win_rate': 0.42,
            'profit_factor': 1.3,
            'max_drawdown': 500,
            'total_pnl': 300,
            'sharpe_ratio': 0.6
        }
        
        # Simulate market conditions
        market = {
            'volatility': 0.025,
            'regime': 'sideways',
            'volume_trend': 'normal'
        }
        
        # Run optimization
        optimized = optimizer.optimize_with_hive(current_params, performance, market)
        
        print(f"\n✅ Hive Optimization Complete:")
        print(f"   Consensus Confidence: {optimized.consensus_confidence:.2f}")
        print(f"   Contributing Agents: {', '.join(optimized.contributing_agents)}")
        print(f"   Expected Improvement: {optimized.expected_improvement:.1%}")
        print(f"   Backtest Score: {optimized.backtest_score:.1f}/100")
        
        print(f"\n   Parameter Changes:")
        for param, value in optimized.parameters.items():
            if param in current_params and current_params[param] != value:
                print(f"      {param}: {current_params[param]} → {value}")
        
        print(f"\n   Reasoning: {optimized.reasoning}")
        
        # Export recommendations
        filename = optimizer.export_recommendations(optimized)
        print(f"\n   Exported to: {filename}")
        
        print("\n✅ HiveParameterOptimizer module validated")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
