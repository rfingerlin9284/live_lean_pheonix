import pytest
from hive.rick_hive_mind import RickHiveMind, AIAgent, SignalStrength


def deterministic_simulation(agent, market_data):
    # deterministic responses for testing
    if agent == AIAgent.GPT:
        return type('R', (), {'agent': agent, 'signal': SignalStrength.BUY, 'confidence': 0.90, 'reasoning': 'GPT test', 'risk_reward': 3.2})
    if agent == AIAgent.GROK:
        return type('R', (), {'agent': agent, 'signal': SignalStrength.BUY, 'confidence': 0.80, 'reasoning': 'GROK test', 'risk_reward': 3.2})
    if agent == AIAgent.DEEPSEEK:
        return type('R', (), {'agent': agent, 'signal': SignalStrength.SELL, 'confidence': 0.30, 'reasoning': 'DEEPSEEK test', 'risk_reward': 2.8})


def test_weighted_consensus(monkeypatch):
    hive = RickHiveMind(pin=841921)
    # patch method
    monkeypatch.setattr(hive, '_simulate_agent_analysis', lambda agent, md: deterministic_simulation(agent, md))

    # set custom weights to make the weighted average clear: 0.5, 0.25, 0.25
    hive.agent_weights = {AIAgent.GPT:0.5, AIAgent.GROK:0.25, AIAgent.DEEPSEEK:0.25}
    analysis = hive.delegate_analysis({'symbol':'EURUSD'})

    # consensus should be BUY by majority
    assert analysis.consensus_signal == SignalStrength.BUY
    # expected weighted confidence = 0.9*0.5 + 0.8*0.25 + 0.3*0.25 = 0.45 + 0.2 + 0.075 = 0.725
    assert pytest.approx(analysis.consensus_confidence, rel=1e-3) == 0.725
    # Ensure agent responses included
    assert len(analysis.agent_responses) == 3
    assert analysis.charter_compliant is True
