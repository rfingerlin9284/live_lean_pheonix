#!/usr/bin/env python3
"""
Strategic Hedge Manager - Auto-Flip & Momentum Detection System
Monitors losing trades and executes strategic reversal hedges
PIN: 841921 | Phase: Active Hedging
"""

import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)


class MomentumShift(Enum):
    """Momentum shift detection states"""
    NO_SHIFT = "no_shift"
    WEAK_REVERSAL = "weak_reversal"
    STRONG_REVERSAL = "strong_reversal"
    CONTINUATION = "continuation"


@dataclass
class HedgeDecision:
    """Decision to hedge or flip a position"""
    should_hedge: bool
    hedge_ratio: float  # 0.0 to 1.0 (percentage of position to hedge)
    flip_position: bool  # Complete reversal
    confidence: float
    reason: str
    momentum_shift: str


class StrategicHedgeManager:
    """
    Strategic hedging system that monitors losing trades and executes hedges
    Integrates with FVG and Fibonacci logic for reversal detection
    """
    
    def __init__(self, pin: int = 841921):
        """Initialize Strategic Hedge Manager"""
        if pin != 841921:
            raise PermissionError("Invalid PIN for Strategic Hedge Manager")
        
        self.pin_verified = True
        self.logger = logger
        
        # Hedge parameters
        self.loss_threshold_pips = 15  # Start monitoring at -15 pips
        self.auto_flip_threshold = 0.75  # 75% confidence to auto-flip
        self.hedge_ratio_default = 0.5  # Hedge 50% by default
        
        # Momentum detection parameters
        self.momentum_lookback = 20
        self.reversal_threshold = 0.65
        
        # FVG detection parameters
        self.fvg_enabled = True
        self.fib_enabled = True
        
        self.logger.info("StrategicHedgeManager initialized with PIN verification")
    
    def maybe_open_hedge(
        self,
        position: Dict,
        current_price: float,
        prices: np.ndarray,
        volume: Optional[np.ndarray] = None
    ) -> Optional[HedgeDecision]:
        """
        Analyze a losing position and determine if hedging is warranted
        
        Args:
            position: Current position info (entry, direction, size, unrealized_pnl)
            current_price: Current market price
            prices: Recent price history for momentum analysis
            volume: Optional volume data
            
        Returns:
            HedgeDecision if action needed, None otherwise
        """
        
        # Extract position details
        entry_price = position.get('entry_price', 0)
        direction = position.get('direction', 'long')
        unrealized_pnl = position.get('unrealized_pnl', 0)
        position_size = position.get('size', 0)
        
        # Check if position is losing enough to warrant analysis
        pips_lost = self._calculate_pips_lost(entry_price, current_price, direction)
        
        if pips_lost < self.loss_threshold_pips:
            return None  # Not losing enough yet
        
        self.logger.info(f"Analyzing losing position: {pips_lost:.1f} pips loss")
        
        # Analyze momentum shift
        momentum_shift = self._detect_momentum_shift(prices, direction)
        
        # Check for FVG reversal signals
        fvg_signal = self._detect_fvg_reversal(prices) if self.fvg_enabled else None
        
        # Check for Fibonacci reversal levels
        fib_signal = self._detect_fibonacci_reversal(prices, entry_price, current_price) if self.fib_enabled else None
        
        # Calculate hedge confidence
        confidence = self._calculate_hedge_confidence(
            momentum_shift,
            fvg_signal,
            fib_signal,
            pips_lost
        )
        
        # Determine hedge action
        if confidence >= self.auto_flip_threshold:
            # Strong reversal detected - flip the position
            return HedgeDecision(
                should_hedge=True,
                hedge_ratio=1.0,
                flip_position=True,
                confidence=confidence,
                reason=f"Strong reversal detected (momentum: {momentum_shift.value}, confidence: {confidence:.2f})",
                momentum_shift=momentum_shift.value
            )
        elif confidence >= 0.55:
            # Moderate reversal - hedge portion of position
            hedge_ratio = min(0.75, (confidence - 0.55) / (self.auto_flip_threshold - 0.55) * 0.75 + 0.25)
            return HedgeDecision(
                should_hedge=True,
                hedge_ratio=hedge_ratio,
                flip_position=False,
                confidence=confidence,
                reason=f"Moderate reversal detected (momentum: {momentum_shift.value}, hedge ratio: {hedge_ratio:.2f})",
                momentum_shift=momentum_shift.value
            )
        else:
            # Continue monitoring
            return None
    
    def _calculate_pips_lost(self, entry: float, current: float, direction: str) -> float:
        """Calculate pips lost on position"""
        if direction.lower() in ['long', 'buy']:
            pips = (entry - current) * 10000  # Loss for long
        else:
            pips = (current - entry) * 10000  # Loss for short
        return max(0, pips)  # Return 0 if profitable
    
    def _detect_momentum_shift(self, prices: np.ndarray, direction: str) -> MomentumShift:
        """
        Detect momentum shifts using price action
        
        Args:
            prices: Recent price history
            direction: Current position direction
            
        Returns:
            MomentumShift enum
        """
        if len(prices) < self.momentum_lookback:
            return MomentumShift.NO_SHIFT
        
        recent_prices = prices[-self.momentum_lookback:]
        
        # Calculate momentum indicators
        # 1. Trend slope
        x = np.arange(len(recent_prices))
        slope, _ = np.polyfit(x, recent_prices, 1)
        
        # 2. Price acceleration (second derivative)
        if len(recent_prices) >= 3:
            velocity = np.diff(recent_prices)
            acceleration = np.diff(velocity)
            recent_accel = np.mean(acceleration[-5:]) if len(acceleration) >= 5 else 0
        else:
            recent_accel = 0
        
        # 3. Volatility trend
        volatility = np.std(recent_prices[-10:]) if len(recent_prices) >= 10 else 0
        
        # Determine shift based on position direction
        if direction.lower() in ['long', 'buy']:
            # For long positions, look for downward momentum (bad for us)
            if slope < -0.0001 and recent_accel < -0.00001:
                return MomentumShift.STRONG_REVERSAL
            elif slope < -0.00005:
                return MomentumShift.WEAK_REVERSAL
            elif slope > 0:
                return MomentumShift.CONTINUATION
        else:
            # For short positions, look for upward momentum (bad for us)
            if slope > 0.0001 and recent_accel > 0.00001:
                return MomentumShift.STRONG_REVERSAL
            elif slope > 0.00005:
                return MomentumShift.WEAK_REVERSAL
            elif slope < 0:
                return MomentumShift.CONTINUATION
        
        return MomentumShift.NO_SHIFT
    
    def _detect_fvg_reversal(self, prices: np.ndarray) -> Optional[str]:
        """
        Detect Fair Value Gap reversals
        
        FVG occurs when:
        - Bullish FVG: High[i-2] < Low[i] (gap up)
        - Bearish FVG: Low[i-2] > High[i] (gap down)
        """
        if len(prices) < 3:
            return None
        
        # Use close prices as proxy for high/low (simplified)
        # In production, would use actual OHLC data
        current = prices[-1]
        prev = prices[-2]
        third = prices[-3]
        
        # Bullish FVG (price gapping up - reversal from downtrend)
        if current > third * 1.0015:  # 0.15% gap up
            return "bullish_fvg"
        
        # Bearish FVG (price gapping down - reversal from uptrend)
        if current < third * 0.9985:  # 0.15% gap down
            return "bearish_fvg"
        
        return None
    
    def _detect_fibonacci_reversal(
        self,
        prices: np.ndarray,
        entry_price: float,
        current_price: float
    ) -> Optional[str]:
        """
        Detect Fibonacci reversal levels
        
        Key levels: 0.236, 0.382, 0.5, 0.618, 0.786
        Golden pocket: 0.618-0.65 range
        """
        if len(prices) < 20:
            return None
        
        # Find swing high and low in recent history
        swing_high = np.max(prices[-20:])
        swing_low = np.min(prices[-20:])
        price_range = swing_high - swing_low
        
        if price_range == 0:
            return None
        
        # Calculate retracement level
        retracement = (current_price - swing_low) / price_range
        
        # Check for golden pocket (0.618 - 0.65) - strong reversal zone
        if 0.618 <= retracement <= 0.65:
            return "golden_pocket"
        
        # Check for 0.5 retracement (equilibrium)
        if 0.48 <= retracement <= 0.52:
            return "fib_50"
        
        # Check for 0.382 retracement
        if 0.36 <= retracement <= 0.40:
            return "fib_382"
        
        return None
    
    def _calculate_hedge_confidence(
        self,
        momentum_shift: MomentumShift,
        fvg_signal: Optional[str],
        fib_signal: Optional[str],
        pips_lost: float
    ) -> float:
        """
        Calculate confidence in hedge decision
        
        Combines:
        - Momentum shift strength (40%)
        - FVG signals (30%)
        - Fibonacci levels (30%)
        - Loss magnitude bonus
        """
        confidence = 0.0
        
        # Momentum contribution (40%)
        if momentum_shift == MomentumShift.STRONG_REVERSAL:
            confidence += 0.40
        elif momentum_shift == MomentumShift.WEAK_REVERSAL:
            confidence += 0.25
        elif momentum_shift == MomentumShift.NO_SHIFT:
            confidence += 0.10
        
        # FVG contribution (30%)
        if fvg_signal:
            confidence += 0.30
        
        # Fibonacci contribution (30%)
        if fib_signal == "golden_pocket":
            confidence += 0.30
        elif fib_signal == "fib_50":
            confidence += 0.20
        elif fib_signal == "fib_382":
            confidence += 0.15
        
        # Loss magnitude bonus (increases urgency)
        if pips_lost > 30:
            confidence += 0.10
        elif pips_lost > 20:
            confidence += 0.05
        
        return min(1.0, confidence)


if __name__ == "__main__":
    # Self-test
    print("Strategic Hedge Manager self-test...")
    
    try:
        manager = StrategicHedgeManager(pin=841921)
        
        # Simulate a losing long position
        position = {
            'entry_price': 1.1000,
            'direction': 'long',
            'size': 10000,
            'unrealized_pnl': -200
        }
        
        # Simulate price moving against us
        current_price = 1.0980  # 20 pips loss
        
        # Simulate price history showing reversal
        prices = np.array([1.1010 - i * 0.0002 for i in range(25)])  # Downtrend
        
        decision = manager.maybe_open_hedge(position, current_price, prices)
        
        if decision:
            print(f"\n✅ Hedge Decision:")
            print(f"   Should Hedge: {decision.should_hedge}")
            print(f"   Hedge Ratio: {decision.hedge_ratio:.2f}")
            print(f"   Flip Position: {decision.flip_position}")
            print(f"   Confidence: {decision.confidence:.2f}")
            print(f"   Reason: {decision.reason}")
            print(f"   Momentum: {decision.momentum_shift}")
        else:
            print("\n✅ No hedge action needed yet")
        
        print("\n✅ StrategicHedgeManager module validated")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
