#!/usr/bin/env python3
"""
Quant Hedge Recovery Module - RBOTzilla Wolfpack EdgePack Choice 1

Loss recovery system with STRICT safety caps.
Only hedges in mean-reversion/chop regimes, never in trend breakouts.

Rules:
- Only 1 hedge layer per parent trade (max_hedge_layers=1)
- Hedge size: 0.35x of parent size
- Hedge direction: opposite of parent
- Hedge must have its own OCO (SL=0.35R, TP=0.70R)
- Trigger: between -0.35R and -0.9R drawdown
- Must not violate MAX_CONCURRENT_POSITIONS, MAX_POSITIONS_PER_SYMBOL, DAILY_LOSS_BREAKER_PCT, MAX_MARGIN_USAGE
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Optional, List, Tuple

logger = logging.getLogger(__name__)


class QuantHedgeRecovery:
    """
    Safe loss recovery via strategic hedging.
    NO MARTINGALE - just intelligent position management.
    """
    
    def __init__(self, charter, oanda_connector):
        """
        Initialize hedge recovery module
        
        Args:
            charter: RickCharter instance for compliance checks
            oanda_connector: OandaConnector for placing orders
        """
        self.charter = charter
        self.oanda = oanda_connector
        
        # Hedge parameters (STRICT)
        self.max_hedge_layers = 1  # Only ONE hedge per parent
        self.hedge_size_ratio = 0.35  # 35% of parent size
        self.trigger_drawdown_min = -0.35  # -0.35R (start watching)
        self.trigger_drawdown_max = -0.9   # -0.9R (last chance)
        self.hedge_stop_loss_r = 0.35  # 0.35R for hedge SL
        self.hedge_take_profit_r = 0.70  # 0.70R for hedge TP
        
        # Track which positions have been hedged
        self.hedged_positions = {}  # {parent_trade_id: hedge_trade_id}
        
        # Allowed regimes for hedging (mean-reversion/chop only)
        self.allowed_regimes = ['mean_revert', 'chop', 'choppy', 'range', 'consolidation']
        
        logger.info("🛡️ Quant Hedge Recovery ACTIVE - Max Layers: 1, Size Ratio: 0.35x")
    
    def is_hedge_eligible(self, position: Dict, regime: str, account_state: Dict) -> Tuple[bool, str]:
        """
        Check if a position is eligible for hedging
        
        Args:
            position: Position dict with unrealizedPL, units, etc.
            regime: Current market regime
            account_state: Account state with margin, positions, etc.
        
        Returns:
            (eligible: bool, reason: str)
        """
        trade_id = position.get('id', 'unknown')
        
        # Check if already hedged
        if trade_id in self.hedged_positions:
            return False, "Already hedged"
        
        # Check regime (only mean-reversion/chop)
        if regime.lower() not in self.allowed_regimes:
            return False, f"Regime '{regime}' not suitable for hedging (trend/breakout)"
        
        # Calculate drawdown in R multiples
        unrealized_pl = float(position.get('unrealizedPL', 0))
        initial_risk = float(position.get('initialRisk', 1))  # Avoid division by zero
        
        if initial_risk <= 0:
            return False, "Invalid initial risk"
        
        drawdown_r = unrealized_pl / initial_risk
        
        # Check if in trigger range
        if drawdown_r > self.trigger_drawdown_min:
            return False, f"Drawdown {drawdown_r:.2f}R not yet in trigger range ({self.trigger_drawdown_min}R)"
        
        if drawdown_r < self.trigger_drawdown_max:
            return False, f"Drawdown {drawdown_r:.2f}R beyond max trigger ({self.trigger_drawdown_max}R)"
        
        # Check concurrent position limits
        current_positions = account_state.get('open_positions', 0)
        max_positions = getattr(self.charter, 'MAX_CONCURRENT_POSITIONS', 12)
        
        if current_positions >= max_positions:
            return False, f"Max concurrent positions reached ({current_positions}/{max_positions})"
        
        # Check margin usage
        margin_used = account_state.get('margin_used', 0)
        nav = account_state.get('nav', 1)
        margin_pct = margin_used / nav if nav > 0 else 1
        max_margin = getattr(self.charter, 'MAX_MARGIN_USAGE', 0.25)
        
        if margin_pct >= max_margin:
            return False, f"Max margin usage reached ({margin_pct:.1%}/{max_margin:.1%})"
        
        # Check daily loss breaker
        daily_pnl_pct = account_state.get('daily_pnl_pct', 0)
        max_loss_pct = abs(getattr(self.charter, 'DAILY_LOSS_BREAKER_PCT', 0.03))
        
        if abs(daily_pnl_pct) >= max_loss_pct:
            return False, f"Daily loss breaker active ({daily_pnl_pct:.1%}/{-max_loss_pct:.1%})"
        
        # Check symbol position limit
        symbol = position.get('instrument', 'UNKNOWN')
        symbol_positions = sum(1 for p in account_state.get('positions', []) 
                              if p.get('instrument') == symbol)
        max_per_symbol = getattr(self.charter, 'MAX_POSITIONS_PER_SYMBOL', 4)
        
        if symbol_positions >= max_per_symbol:
            return False, f"Max positions per symbol reached for {symbol} ({symbol_positions}/{max_per_symbol})"
        
        return True, f"Eligible for hedging at {drawdown_r:.2f}R drawdown"
    
    def calculate_hedge_params(self, parent_position: Dict) -> Dict:
        """
        Calculate hedge order parameters
        
        Args:
            parent_position: Parent position dict
            
        Returns:
            Dict with hedge parameters (symbol, direction, units, sl, tp)
        """
        symbol = parent_position.get('instrument', 'UNKNOWN')
        parent_units = abs(float(parent_position.get('units', 0)))
        parent_direction = 'BUY' if float(parent_position.get('units', 0)) > 0 else 'SELL'
        entry_price = float(parent_position.get('price', 0))
        
        # Hedge direction is opposite
        hedge_direction = 'SELL' if parent_direction == 'BUY' else 'BUY'
        
        # Hedge size is 35% of parent
        hedge_units = int(parent_units * self.hedge_size_ratio)
        
        # Calculate pip size
        pip_size = 0.01 if 'JPY' in symbol else 0.0001
        
        # Calculate initial risk from parent position
        # (assuming parent has SL at 1R distance)
        parent_sl = float(parent_position.get('stopLossOrder', {}).get('price', entry_price))
        parent_risk_pips = abs(entry_price - parent_sl) / pip_size
        one_r_pips = parent_risk_pips  # 1R in pips
        
        # Hedge SL and TP
        if hedge_direction == 'BUY':
            hedge_sl = entry_price - (self.hedge_stop_loss_r * one_r_pips * pip_size)
            hedge_tp = entry_price + (self.hedge_take_profit_r * one_r_pips * pip_size)
        else:  # SELL
            hedge_sl = entry_price + (self.hedge_stop_loss_r * one_r_pips * pip_size)
            hedge_tp = entry_price - (self.hedge_take_profit_r * one_r_pips * pip_size)
        
        return {
            'symbol': symbol,
            'direction': hedge_direction,
            'units': hedge_units,
            'entry_price': entry_price,
            'stop_loss': round(hedge_sl, 5),
            'take_profit': round(hedge_tp, 5),
            'parent_trade_id': parent_position.get('id'),
            'hedge_size_ratio': self.hedge_size_ratio,
            'sl_r': self.hedge_stop_loss_r,
            'tp_r': self.hedge_take_profit_r
        }
    
    def place_hedge(self, parent_position: Dict, regime: str, account_state: Dict, 
                   log_narration_func=None) -> Optional[Dict]:
        """
        Place a hedge order with OCO
        
        Args:
            parent_position: Parent position to hedge
            regime: Current market regime
            account_state: Current account state
            log_narration_func: Narration logging function
            
        Returns:
            Hedge order response or None if failed
        """
        # Check eligibility
        eligible, reason = self.is_hedge_eligible(parent_position, regime, account_state)
        
        if not eligible:
            if log_narration_func:
                log_narration_func(
                    event_type="HEDGE_REJECTED",
                    details={
                        'parent_trade_id': parent_position.get('id'),
                        'reason': reason,
                        'regime': regime
                    },
                    symbol=parent_position.get('instrument', 'UNKNOWN'),
                    venue='oanda'
                )
            return None
        
        # Calculate hedge parameters
        hedge_params = self.calculate_hedge_params(parent_position)
        
        if log_narration_func:
            log_narration_func(
                event_type="HEDGE_ARMED",
                details=hedge_params,
                symbol=hedge_params['symbol'],
                venue='oanda'
            )
        
        try:
            # Place hedge order with OCO
            order_result = self.oanda.place_market_order_with_oco(
                symbol=hedge_params['symbol'],
                direction=hedge_params['direction'],
                units=hedge_params['units'],
                stop_loss=hedge_params['stop_loss'],
                take_profit=hedge_params['take_profit']
            )
            
            if order_result and order_result.get('success'):
                hedge_trade_id = order_result.get('trade_id')
                parent_trade_id = hedge_params['parent_trade_id']
                
                # Track the hedge
                self.hedged_positions[parent_trade_id] = hedge_trade_id
                
                if log_narration_func:
                    log_narration_func(
                        event_type="HEDGE_PLACED",
                        details={
                            'parent_trade_id': parent_trade_id,
                            'hedge_trade_id': hedge_trade_id,
                            'units': hedge_params['units'],
                            'direction': hedge_params['direction'],
                            'sl': hedge_params['stop_loss'],
                            'tp': hedge_params['take_profit']
                        },
                        symbol=hedge_params['symbol'],
                        venue='oanda'
                    )
                    
                    log_narration_func(
                        event_type="HEDGE_OCO_LINKED",
                        details={
                            'hedge_trade_id': hedge_trade_id,
                            'sl_r': self.hedge_stop_loss_r,
                            'tp_r': self.hedge_take_profit_r
                        },
                        symbol=hedge_params['symbol'],
                        venue='oanda'
                    )
                
                logger.info(f"🛡️ HEDGE PLACED: {hedge_params['symbol']} {hedge_params['direction']} "
                          f"{hedge_params['units']} units (parent: {parent_trade_id})")
                
                return order_result
            else:
                if log_narration_func:
                    log_narration_func(
                        event_type="HEDGE_FAILED",
                        details={
                            'parent_trade_id': hedge_params['parent_trade_id'],
                            'error': order_result.get('error', 'Unknown error')
                        },
                        symbol=hedge_params['symbol'],
                        venue='oanda'
                    )
                return None
                
        except Exception as e:
            logger.error(f"❌ Hedge placement error: {e}")
            if log_narration_func:
                log_narration_func(
                    event_type="HEDGE_ERROR",
                    details={
                        'parent_trade_id': hedge_params['parent_trade_id'],
                        'error': str(e)
                    },
                    symbol=hedge_params['symbol'],
                    venue='oanda'
                )
            return None
    
    def on_position_closed(self, trade_id: str):
        """
        Clean up tracking when a position closes
        
        Args:
            trade_id: Trade ID that was closed
        """
        # Remove from hedged positions (whether parent or hedge)
        if trade_id in self.hedged_positions:
            del self.hedged_positions[trade_id]
        
        # Also check if this was a hedge (reverse lookup)
        for parent_id, hedge_id in list(self.hedged_positions.items()):
            if hedge_id == trade_id:
                del self.hedged_positions[parent_id]
                logger.info(f"🛡️ Hedge {trade_id} exited, parent {parent_id} tracking cleared")
                break
