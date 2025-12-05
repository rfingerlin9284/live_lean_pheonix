#!/usr/bin/env python3
"""
Tests for Hive Parameter Optimizer
"""

import pytest
from hive.hive_parameter_optimizer import HiveParameterOptimizer


def test_hive_optimizer_init():
    """Test initialization with valid PIN"""
    optimizer = HiveParameterOptimizer(pin=841921)
    assert optimizer.pin_verified is True
    assert len(optimizer.agents) == 5


def test_hive_optimizer_invalid_pin():
    """Test initialization fails with invalid PIN"""
    with pytest.raises(PermissionError):
        HiveParameterOptimizer(pin=12345)


def test_agent_initialization():
    """Test that all agents are properly initialized"""
    optimizer = HiveParameterOptimizer(pin=841921)
    
    agent_names = [agent.name for agent in optimizer.agents]
    assert "RiskManager" in agent_names
    assert "TrendAnalyst" in agent_names
    assert "FVGSpecialist" in agent_names
    assert "FibonacciExpert" in agent_names
    assert "VolumeAnalyst" in agent_names


def test_optimize_with_poor_performance():
    """Test optimization with poor performance data"""
    optimizer = HiveParameterOptimizer(pin=841921)
    
    current_params = {
        'confidence_threshold': 0.55,
        'stop_loss_pips': 10,
        'take_profit_pips': 32,
        'max_positions': 12
    }
    
    performance = {
        'win_rate': 0.35,  # Poor win rate
        'profit_factor': 1.1,  # Poor profit factor
        'max_drawdown': 800,
        'total_pnl': 200,
        'sharpe_ratio': 0.3
    }
    
    optimized = optimizer.optimize_with_hive(current_params, performance)
    
    # Should recommend improvements
    assert optimized.consensus_confidence > 0
    assert optimized.expected_improvement >= 0
    assert len(optimized.contributing_agents) > 0


def test_optimize_with_good_performance():
    """Test optimization with good performance"""
    optimizer = HiveParameterOptimizer(pin=841921)
    
    current_params = {
        'confidence_threshold': 0.65,
        'stop_loss_pips': 8,
        'take_profit_pips': 40,
        'max_positions': 8
    }
    
    performance = {
        'win_rate': 0.65,  # Good win rate
        'profit_factor': 2.5,  # Good profit factor
        'max_drawdown': 200,
        'total_pnl': 1000,
        'sharpe_ratio': 1.2
    }
    
    optimized = optimizer.optimize_with_hive(current_params, performance)
    
    # Should still produce recommendations (even if minor)
    assert optimized is not None
    assert optimized.backtest_score >= 0


def test_agent_analyze_risk_manager():
    """Test RiskManager agent analysis"""
    optimizer = HiveParameterOptimizer(pin=841921)
    
    risk_agent = [a for a in optimizer.agents if a.name == "RiskManager"][0]
    
    current_params = {'stop_loss_pips': 10, 'take_profit_pips': 20, 'max_positions': 12}
    performance = {'win_rate': 0.45, 'profit_factor': 1.2, 'max_drawdown': 600, 'total_pnl': 300}
    
    recommendations = optimizer._agent_analyze(risk_agent, current_params, performance, None)
    
    # RiskManager should make recommendations for poor R:R
    assert len(recommendations) > 0


def test_aggregate_recommendations():
    """Test recommendation aggregation"""
    optimizer = HiveParameterOptimizer(pin=841921)
    
    current_params = {
        'confidence_threshold': 0.55,
        'stop_loss_pips': 10,
        'take_profit_pips': 32
    }
    
    # Manually add recommendations to agents
    optimizer.agents[0].recommendations = [{
        'parameter': 'take_profit_pips',
        'current': 32,
        'recommended': 40,
        'reason': 'Test',
        'confidence': 0.8
    }]
    
    optimized = optimizer._aggregate_recommendations(current_params)
    
    assert 'take_profit_pips' in optimized.parameters


def test_estimate_improvement():
    """Test improvement estimation"""
    optimizer = HiveParameterOptimizer(pin=841921)
    
    current = {'stop_loss_pips': 10, 'take_profit_pips': 32}
    optimized = {'stop_loss_pips': 8, 'take_profit_pips': 45}
    
    improvement = optimizer._estimate_improvement(current, optimized, {})
    
    assert 0 <= improvement <= 1.0


def test_simulate_backtest():
    """Test backtest simulation"""
    optimizer = HiveParameterOptimizer(pin=841921)
    
    params = {
        'stop_loss_pips': 10,
        'take_profit_pips': 40,
        'confidence_threshold': 0.65
    }
    
    performance = {
        'profit_factor': 2.0,
        'win_rate': 0.60,
        'sharpe_ratio': 1.0
    }
    
    score = optimizer._simulate_backtest(params, performance)
    
    assert 0 <= score <= 100


def test_export_recommendations(tmp_path):
    """Test exporting recommendations to file"""
    optimizer = HiveParameterOptimizer(pin=841921)
    
    current_params = {'confidence_threshold': 0.55}
    performance = {'win_rate': 0.50, 'profit_factor': 1.5, 'max_drawdown': 300, 'total_pnl': 500, 'sharpe_ratio': 0.8}
    
    optimized = optimizer.optimize_with_hive(current_params, performance)
    
    output_file = tmp_path / "test_recommendations.json"
    filename = optimizer.export_recommendations(optimized, str(output_file))
    
    assert output_file.exists()
    
    # Verify file content
    import json
    with open(output_file) as f:
        data = json.load(f)
    
    assert 'optimized_parameters' in data
    assert 'consensus_confidence' in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
