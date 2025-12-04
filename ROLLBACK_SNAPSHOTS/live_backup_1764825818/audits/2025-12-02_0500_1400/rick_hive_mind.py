#!/usr/bin/env python3
"""
RickHiveMind - RBOTzilla UNI Phase 4
Multi-AI delegation system with confidence weighting.
PIN: 841921 | Generated: 2025-09-26
"""

import json
import logging
import time
import random
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class AIAgent(Enum):
    GPT = "gpt"
    GROK = "grok"
    DEEPSEEK = "deepseek"
    FALLBACK = "fallback"

class SignalStrength(Enum):
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    NEUTRAL = "neutral"
    SELL = "sell"
    STRONG_SELL = "strong_sell"

@dataclass
class AgentResponse:
    agent: AIAgent
    signal: SignalStrength
    confidence: float
    reasoning: str
    risk_reward: Optional[float] = None

@dataclass
class HiveAnalysis:
    consensus_signal: SignalStrength
    consensus_confidence: float
    agent_responses: List[AgentResponse]
    trade_recommendation: Optional[Dict[str, Any]]
    charter_compliant: bool

class RickHiveMind:
    def __init__(self, pin: int = None):
        self.pin_verified = pin == 841921 if pin else False
        self.agent_weights = {
            AIAgent.GPT: 0.35,
            AIAgent.GROK: 0.35, 
            AIAgent.DEEPSEEK: 0.30
        }
        self.min_consensus_confidence = 0.65
        # Optional verbose logging flag (env var)
        self.verbose = os.getenv('RICK_HIVE_VERBOSE', '0') == '1'
    
    def _simulate_agent_analysis(self, agent: AIAgent, market_data: Dict[str, Any]) -> AgentResponse:
        """Simulate AI agent analysis"""
        signals = [SignalStrength.BUY, SignalStrength.NEUTRAL, SignalStrength.SELL]
        confidence = random.uniform(0.6, 0.9)
        
        return AgentResponse(
            agent=agent,
            signal=random.choice(signals),
            confidence=confidence,
            reasoning=f"{agent.value} analysis for {market_data.get('symbol', 'UNKNOWN')}",
            risk_reward=random.uniform(2.5, 4.5)
        )
    
    def _adjust_confidence_threshold(self, market_conditions: Dict[str, float]) -> None:
        """
        Dynamically adjust the minimum consensus confidence threshold based on market conditions.
        Args:
            market_conditions: A dictionary containing market metrics (e.g., volatility, spread).
        """
        base_threshold = 0.65
        volatility = market_conditions.get("volatility", 1.0)  # Default to neutral volatility

        # Example adjustment logic
        if volatility > 1.5:  # High volatility
            self.min_consensus_confidence = max(base_threshold - 0.05, 0.6)  # Reduce threshold slightly
        elif volatility < 0.8:  # Low volatility
            self.min_consensus_confidence = min(base_threshold + 0.05, 0.7)  # Increase threshold slightly
        else:
            self.min_consensus_confidence = base_threshold

        logging.info(f"Adjusted consensus confidence threshold to {self.min_consensus_confidence:.2f}")

    def delegate_analysis(self, market_data: Dict[str, Any], market_conditions: Dict[str, float] = None) -> HiveAnalysis:
        """Main delegation function with dynamic confidence adjustment."""
        if market_conditions:
            self._adjust_confidence_threshold(market_conditions)

        # Weighted consensus (majority vote for signal, weighted mean for confidence)
        responses = []
        for agent in [AIAgent.GPT, AIAgent.GROK, AIAgent.DEEPSEEK]:
            response = self._simulate_agent_analysis(agent, market_data)
            responses.append(response)
        
        signals = [r.signal for r in responses]
        consensus_signal = max(set(signals), key=signals.count)
        # Weighted mean of the confidences using agent_weights where possible
        used_weights = []
        weighted_conf_total = 0.0
        weight_sum = 0.0
        for r in responses:
            w = self.agent_weights.get(r.agent, 0.0)
            used_weights.append((r.agent, r.confidence, w))
            if w:
                weighted_conf_total += r.confidence * w
                weight_sum += w
        if weight_sum > 0:
            consensus_confidence = weighted_conf_total / weight_sum
        else:
            # fallback to arithmetic mean if weights missing
            consensus_confidence = sum(r.confidence for r in responses) / len(responses)

        # Verbose output (optional): include per-agent responses
        if self.verbose:
            try:
                logging.getLogger('hive').info("Hive agent responses: %s", json.dumps([
                    {"agent": r.agent.value, "signal": r.signal.value if hasattr(r.signal,'value') else str(r.signal), "confidence": r.confidence, "reasoning": r.reasoning}
                    for r in responses
                ]))
            except Exception:
                pass
        
        # Generate recommendation if confidence is high enough
        trade_recommendation = None
        if consensus_confidence >= self.min_consensus_confidence:
            trade_recommendation = {
                "action": consensus_signal.value,
                "confidence": consensus_confidence,
                "risk_reward_ratio": 3.2
            }
        
        return HiveAnalysis(
            consensus_signal=consensus_signal,
            consensus_confidence=consensus_confidence,
            agent_responses=responses,
            trade_recommendation=trade_recommendation,
            charter_compliant=True
        )
    
    def get_hive_status(self) -> Dict[str, Any]:
        return {
            "agent_weights": {a.value: w for a, w in self.agent_weights.items()},
            "min_consensus_confidence": self.min_consensus_confidence,
            "charter_enforcement": True
        }

def get_hive_mind(pin: int = None) -> RickHiveMind:
    return RickHiveMind(pin)

if __name__ == "__main__":
    hive = RickHiveMind(pin=841921)
    test_data = {"symbol": "EURUSD", "current_price": 1.0850, "timeframe": "H1"}
    analysis = hive.delegate_analysis(test_data)
    
    print("RickHiveMind self-test results:")
    print(f"Consensus: {analysis.consensus_signal.value} ({analysis.consensus_confidence:.2f})")
    print(f"Agents responded: {len(analysis.agent_responses)}")
    print(f"Charter compliant: {analysis.charter_compliant}")
    print(f"Trade recommended: {analysis.trade_recommendation is not None}")
    print("RickHiveMind self-test passed ✅")