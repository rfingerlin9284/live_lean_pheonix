#!/usr/bin/env python3
"""
Hive Opportunity Scanner - Proactive Market Analysis
Uses hive agents to scan for optimal trading opportunities
Integrates FVG, Fibonacci, and momentum analysis
PIN: 841921 | Phase: Opportunity Discovery
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hive.quant_hedge_rules import QuantHedgeRules

# Import simplified versions to avoid dependencies
class FVGWolf:
    """Simplified FVG detector"""
    def __init__(self):
        self.name = "FVGWolf"
    
    def get_signal(self, df):
        if len(df) < 3:
            return "NEUTRAL", 0.0
        
        last_candle = df.iloc[-1]
        third_candle = df.iloc[-3]
        
        # Bullish FVG (gap up)
        if last_candle['low'] > third_candle['high']:
            return "BUY", 0.75
        
        # Bearish FVG (gap down)
        if last_candle['high'] < third_candle['low']:
            return "SELL", 0.75
        
        return "NEUTRAL", 0.0


class FibonacciWolf:
    """Simplified Fibonacci detector"""
    def __init__(self):
        self.name = "FibonacciWolf"
    
    def get_signal(self, df):
        high = df['high'].max()
        low = df['low'].min()
        current = df['close'].iloc[-1]
        
        retracement = (current - low) / (high - low) if (high - low) != 0 else 0
        
        # Golden pocket (0.618 - 0.65)
        if 0.618 <= retracement <= 0.65:
            return "BUY", 0.85
        elif 0.35 <= retracement <= 0.382:
            return "SELL", 0.85
        
        return "NEUTRAL", 0.0

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TradingOpportunity:
    """Identified trading opportunity"""
    symbol: str
    direction: str  # BUY or SELL
    confidence: float
    entry_price: float
    stop_loss: float
    take_profit: float
    reasoning: str
    signals: Dict[str, any]
    risk_reward_ratio: float
    timeframe: str
    detected_at: datetime


class HiveOpportunityScanner:
    """
    Scans markets for high-probability trading opportunities
    Uses multiple hive agents with different specialties
    """
    
    def __init__(self, pin: int = 841921):
        """Initialize Opportunity Scanner"""
        if pin != 841921:
            raise PermissionError("Invalid PIN for Hive Opportunity Scanner")
        
        self.pin_verified = True
        self.logger = logger
        
        # Initialize analysis agents
        self.quant_hedge = QuantHedgeRules(pin=pin)
        self.fvg_wolf = FVGWolf()
        self.fibonacci_wolf = FibonacciWolf()
        
        # Scanner configuration
        self.min_confidence = 0.60  # Minimum confidence to report
        self.min_rr_ratio = 2.0  # Minimum R:R ratio
        
        # Currency pairs to scan
        self.pairs = [
            'EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD', 'USD_CAD',
            'NZD_USD', 'EUR_GBP', 'EUR_JPY', 'GBP_JPY'
        ]
        
        # Timeframes to analyze
        self.timeframes = ['M15', 'H1', 'H4']
        
        self.logger.info("HiveOpportunityScanner initialized")
    
    def scan_markets(
        self,
        pairs: Optional[List[str]] = None,
        timeframes: Optional[List[str]] = None
    ) -> List[TradingOpportunity]:
        """
        Scan markets for trading opportunities
        
        Args:
            pairs: List of currency pairs to scan (default: all configured)
            timeframes: List of timeframes to analyze (default: all configured)
            
        Returns:
            List of identified opportunities
        """
        if pairs is None:
            pairs = self.pairs
        if timeframes is None:
            timeframes = self.timeframes
        
        self.logger.info(f"Scanning {len(pairs)} pairs across {len(timeframes)} timeframes...")
        
        opportunities = []
        
        for pair in pairs:
            for timeframe in timeframes:
                try:
                    opportunity = self._analyze_pair_timeframe(pair, timeframe)
                    if opportunity and opportunity.confidence >= self.min_confidence:
                        opportunities.append(opportunity)
                        self.logger.info(
                            f"✓ Opportunity found: {pair} {timeframe} "
                            f"{opportunity.direction} (conf: {opportunity.confidence:.2f})"
                        )
                except Exception as e:
                    self.logger.debug(f"Error analyzing {pair} {timeframe}: {e}")
        
        # Sort by confidence
        opportunities.sort(key=lambda x: x.confidence, reverse=True)
        
        self.logger.info(f"Scan complete. Found {len(opportunities)} opportunities.")
        
        return opportunities
    
    def _analyze_pair_timeframe(
        self,
        pair: str,
        timeframe: str
    ) -> Optional[TradingOpportunity]:
        """
        Analyze a specific pair and timeframe
        
        Returns:
            TradingOpportunity if suitable setup found, None otherwise
        """
        # Simulate market data (in production, fetch from broker)
        prices, volume = self._get_market_data(pair, timeframe)
        
        if prices is None or len(prices) < 50:
            return None
        
        # Convert to DataFrame for wolf strategies
        import pandas as pd
        df = pd.DataFrame({
            'close': prices,
            'high': prices * 1.0005,  # Simplified
            'low': prices * 0.9995,
            'volume': volume
        })
        
        # Analyze with multiple agents
        signals = {}
        
        # 1. Quant Hedge Analysis (market regime and conditions)
        try:
            quant_analysis = self.quant_hedge.analyze_market_conditions(
                prices=prices,
                volume=volume,
                account_nav=10000,
                margin_used=1000,
                open_positions=2
            )
            signals['regime'] = quant_analysis.regime
            signals['volatility'] = quant_analysis.volatility_level
            signals['risk_level'] = quant_analysis.risk_level
            signals['quant_action'] = quant_analysis.primary_action
        except Exception as e:
            self.logger.debug(f"Quant analysis failed: {e}")
            return None
        
        # 2. FVG Analysis
        try:
            fvg_signal, fvg_conf = self.fvg_wolf.get_signal(df)
            signals['fvg_signal'] = fvg_signal
            signals['fvg_confidence'] = fvg_conf
        except Exception as e:
            self.logger.debug(f"FVG analysis failed: {e}")
            signals['fvg_signal'] = 'NEUTRAL'
            signals['fvg_confidence'] = 0.0
        
        # 3. Fibonacci Analysis
        try:
            fib_signal, fib_conf = self.fibonacci_wolf.get_signal(df)
            signals['fib_signal'] = fib_signal
            signals['fib_confidence'] = fib_conf
        except Exception as e:
            self.logger.debug(f"Fibonacci analysis failed: {e}")
            signals['fib_signal'] = 'NEUTRAL'
            signals['fib_confidence'] = 0.0
        
        # 4. Momentum Analysis
        momentum = self._calculate_momentum(prices)
        signals['momentum'] = 'bullish' if momentum > 0.0001 else 'bearish' if momentum < -0.0001 else 'neutral'
        signals['momentum_strength'] = abs(momentum)
        
        # Aggregate signals to determine opportunity
        opportunity = self._aggregate_signals(pair, timeframe, prices, signals)
        
        return opportunity
    
    def _get_market_data(
        self,
        pair: str,
        timeframe: str
    ) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Get market data for analysis
        
        In production, this would fetch real data from the broker
        For now, simulate realistic price action
        """
        # Simulate price data with trend and noise
        np.random.seed(hash(pair + timeframe) % 2**32)
        
        n = 100
        base_price = 1.1000 if 'USD' in pair else 150.0
        
        # Create trend component
        trend = np.linspace(0, np.random.uniform(-0.01, 0.01), n)
        
        # Add noise
        noise = np.random.normal(0, 0.002, n)
        
        # Combine
        prices = base_price * (1 + trend + noise)
        
        # Volume with some variation
        volume = np.random.uniform(1000, 5000, n)
        
        return prices, volume
    
    def _calculate_momentum(self, prices: np.ndarray) -> float:
        """Calculate price momentum (slope)"""
        if len(prices) < 2:
            return 0.0
        
        x = np.arange(len(prices))
        slope, _ = np.polyfit(x, prices, 1)
        
        # Normalize by price level
        return slope / np.mean(prices)
    
    def _aggregate_signals(
        self,
        pair: str,
        timeframe: str,
        prices: np.ndarray,
        signals: Dict
    ) -> Optional[TradingOpportunity]:
        """
        Aggregate signals from all agents to determine opportunity
        
        Uses weighted voting system
        """
        # Extract signals
        fvg_signal = signals.get('fvg_signal', 'NEUTRAL')
        fvg_conf = signals.get('fvg_confidence', 0.0)
        
        fib_signal = signals.get('fib_signal', 'NEUTRAL')
        fib_conf = signals.get('fib_confidence', 0.0)
        
        momentum = signals.get('momentum', 'neutral')
        momentum_strength = signals.get('momentum_strength', 0.0)
        
        quant_action = signals.get('quant_action', 'wait_for_clarity')
        regime = signals.get('regime', 'triage')
        risk_level = signals.get('risk_level', 'moderate')
        
        # Determine direction with weighted votes
        buy_score = 0.0
        sell_score = 0.0
        
        # FVG vote (weight: 0.30)
        if fvg_signal == 'BUY':
            buy_score += 0.30 * fvg_conf
        elif fvg_signal == 'SELL':
            sell_score += 0.30 * fvg_conf
        
        # Fibonacci vote (weight: 0.30)
        if fib_signal == 'BUY':
            buy_score += 0.30 * fib_conf
        elif fib_signal == 'SELL':
            sell_score += 0.30 * fib_conf
        
        # Momentum vote (weight: 0.25)
        if momentum == 'bullish':
            buy_score += 0.25 * min(1.0, momentum_strength * 100)
        elif momentum == 'bearish':
            sell_score += 0.25 * min(1.0, momentum_strength * 100)
        
        # Quant hedge vote (weight: 0.15)
        if 'long' in quant_action.lower():
            buy_score += 0.15
        elif 'short' in quant_action.lower() or 'reduce' in quant_action.lower():
            sell_score += 0.10
        
        # Determine direction and confidence
        if buy_score > sell_score and buy_score >= 0.35:  # Lowered from 0.50 for testing
            direction = 'BUY'
            confidence = buy_score
        elif sell_score > buy_score and sell_score >= 0.35:  # Lowered from 0.50 for testing
            direction = 'SELL'
            confidence = sell_score
        else:
            return None  # No clear signal
        
        # Filter by risk level
        if risk_level in ['critical', 'elevated']:
            confidence *= 0.8  # Reduce confidence in risky conditions
        
        if confidence < self.min_confidence:
            return None
        
        # Calculate entry, SL, TP
        current_price = prices[-1]
        atr = np.std(prices[-14:]) if len(prices) >= 14 else np.std(prices)
        
        if direction == 'BUY':
            entry_price = current_price
            stop_loss = entry_price - (atr * 1.5)
            take_profit = entry_price + (atr * 4.0)  # 2.67:1 R:R minimum
        else:
            entry_price = current_price
            stop_loss = entry_price + (atr * 1.5)
            take_profit = entry_price - (atr * 4.0)
        
        # Calculate R:R ratio
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)
        rr_ratio = reward / risk if risk > 0 else 0
        
        if rr_ratio < self.min_rr_ratio:
            return None  # R:R not good enough
        
        # Build reasoning
        reasoning_parts = []
        if fvg_signal != 'NEUTRAL':
            reasoning_parts.append(f"FVG {fvg_signal.lower()} signal (conf: {fvg_conf:.2f})")
        if fib_signal != 'NEUTRAL':
            reasoning_parts.append(f"Fibonacci {fib_signal.lower()} (conf: {fib_conf:.2f})")
        if momentum != 'neutral':
            reasoning_parts.append(f"{momentum} momentum")
        reasoning_parts.append(f"{regime} regime")
        
        reasoning = "; ".join(reasoning_parts)
        
        return TradingOpportunity(
            symbol=pair,
            direction=direction,
            confidence=confidence,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            reasoning=reasoning,
            signals=signals,
            risk_reward_ratio=rr_ratio,
            timeframe=timeframe,
            detected_at=datetime.now()
        )
    
    def export_opportunities(
        self,
        opportunities: List[TradingOpportunity],
        filename: str = "trading_opportunities.json"
    ):
        """Export opportunities to JSON file"""
        import json
        
        export_data = {
            'generated_at': datetime.now().isoformat(),
            'total_opportunities': len(opportunities),
            'opportunities': [
                {
                    **asdict(opp),
                    'detected_at': opp.detected_at.isoformat()
                }
                for opp in opportunities
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Opportunities exported to: {filename}")
        return filename
    
    def print_opportunities(self, opportunities: List[TradingOpportunity]):
        """Print opportunities in readable format"""
        if not opportunities:
            print("\n❌ No trading opportunities found meeting criteria")
            return
        
        print(f"\n{'='*80}")
        print(f"HIVE TRADING OPPORTUNITIES - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        for i, opp in enumerate(opportunities, 1):
            print(f"{i}. {opp.symbol} - {opp.timeframe} - {opp.direction}")
            print(f"   Confidence: {opp.confidence:.1%}")
            print(f"   Entry: {opp.entry_price:.5f}")
            print(f"   Stop Loss: {opp.stop_loss:.5f}")
            print(f"   Take Profit: {opp.take_profit:.5f}")
            print(f"   Risk:Reward: 1:{opp.risk_reward_ratio:.1f}")
            print(f"   Reasoning: {opp.reasoning}")
            print()
        
        print(f"{'='*80}\n")


if __name__ == "__main__":
    # Run scanner
    print("Starting Hive Opportunity Scanner...")
    print("=" * 60)
    
    try:
        scanner = HiveOpportunityScanner(pin=841921)
        
        # Scan markets
        opportunities = scanner.scan_markets()
        
        # Print results
        scanner.print_opportunities(opportunities)
        
        # Export to file
        if opportunities:
            scanner.export_opportunities(opportunities)
            print(f"✅ Found {len(opportunities)} opportunities - exported to trading_opportunities.json")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
