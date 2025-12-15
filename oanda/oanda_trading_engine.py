#!/usr/bin/env python3
"""
OANDA Trading Engine - RBOTZILLA Consolidated Final (Single file)
This file contains the consolidated engine implementation for the OANDA connector.
It uses momentum-based signals, enforces the charter, and applies Tight SL and trailing stops.
PIN: 841921 | Consolidated: 2025-12-03 | FIXED: Dec 11 (Core Import)
"""

import os
import sys
import asyncio
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Ensure repo root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from foundation.rick_charter import RickCharter
from foundation.agent_charter import AgentCharter
from brokers.oanda_connector import OandaConnector
from util.terminal_display import TerminalDisplay
from util.narration_logger import log_narration
from util.position_police import _rbz_force_min_notional_position_police
from util.alert_notifier import send_system_alert

# --- CRITICAL FIX: Use 'core' instead of 'systems' to restore Dec 5th profitable logic ---
from core.momentum_signals import generate_signal
# ----------------------------------------------------------------------------------------

import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('oanda_consolidated')


class OandaTradingEngine:
    def __init__(self, environment: Optional[str] = None):
        # Enforce Agent Charter at startup
        AgentCharter.enforce()
        if not getattr(RickCharter, 'PIN', None) == 841921:
            raise PermissionError('Invalid Charter PIN')

        self.display = TerminalDisplay()
        # Determine environment: prefer passed environment; then RICK_ENV; then TRADING_ENVIRONMENT; default practice
        if environment is None:
            environment = os.getenv('RICK_ENV') or os.getenv('TRADING_ENVIRONMENT') or 'practice'
        self.environment = environment
        # Only .env is supported for OANDA credentials
        os.environ['OANDA_LOAD_ENV_FILE'] = '1'
        self.oanda = OandaConnector(pin=841921, environment=environment)

        self.toggle_paths = [
            Path(os.getenv('PHX_TOGGLES_PATH') or os.getenv('TOGGLES_PATH') or 'PHOENIX_CLEAN_CUT/config/toggles.json'),
            Path('config/toggles.json')
        ]
        self.default_toggles = {
            "no_simulation_mode": True,
            "tight_trailing": True,
            "two_step_sl": True,
            "tp_for_scalps": False,
            "tp_for_swings": False,
            # Selectivity gate: higher = fewer, better trades.
            # Optional per-venue override supported via "min_confidence_by_venue": {"oanda": 0.65, ...}
            "min_confidence": 0.55,
            "be_trigger_pips": 6,
            "trail_trigger_pips": 12,
            "trail_distance_pips": 6,
            "tight_trail_distance_pips": 3,
            "alert_on_auth": True,
            # Optional scale-out (incremental closes) while running a two-step stop.
            # Format: list of {"pips": <profit_pips_trigger>, "fraction": <0..1>}.
            "scale_out_enabled": True,
            "scale_out_levels": [
                {"pips": 8, "fraction": 0.33},
                {"pips": 16, "fraction": 0.33},
            ],
        }
        self.toggles = self._load_toggles()
        self._auth_reported_ok = False
        self._auth_reported_fail = False

        # Safety constants (MIN_CONFIDENCE is configurable via toggles)
        self.MIN_CONFIDENCE = 0.55
        self.MAX_POSITIONS = 12
        self.STOP_LOSS_PIPS = 10
        self.TAKE_PROFIT_PIPS = 32
        self.TRAILING_START_PIPS = 3
        self.TRAILING_DIST_PIPS = 5
        self.TRADING_PAIRS = ['EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD', 'USD_CAD']

        self.running = False
        self.active_positions: Dict[str, dict] = {}
        # Track which scale-out levels have fired per trade id
        self._scale_out_done: Dict[str, set] = {}
        # Market tick emitter (practice/canary only)
        self.market_tick_task = None
        self.market_tick_symbol = 'EUR_USD'
        self.market_tick_freq = 1.5  # seconds
        self._market_tick_last_price = 1.0845

        self._announce()
        self._apply_selectivity_from_toggles()
        self._check_auth_guard()

    def _apply_selectivity_from_toggles(self) -> None:
        """Apply selectivity knobs (confidence gate) from toggles.

        This intentionally does NOT weaken any risk/OCO/stop-loss enforcement.
        It only controls how picky we are about taking a signal.
        """
        def _clamp01(v: float) -> float:
            try:
                v = float(v)
            except Exception:
                return 0.55
            if v < 0.0:
                return 0.0
            if v > 1.0:
                return 1.0
            return v

        min_conf = self.toggles.get('min_confidence', self.MIN_CONFIDENCE)
        by_venue = self.toggles.get('min_confidence_by_venue', None)
        if isinstance(by_venue, dict):
            min_conf = by_venue.get('oanda', min_conf)
        self.MIN_CONFIDENCE = _clamp01(min_conf)

    def _passes_selectivity(self, confidence: float) -> bool:
        try:
            return float(confidence) >= float(self.MIN_CONFIDENCE)
        except Exception:
            return False

    def _load_toggles(self) -> Dict:
        for path in self.toggle_paths:
            try:
                if path.is_file():
                    return {**self.default_toggles, **json.loads(path.read_text())}
            except Exception as e:
                logger.warning(f"Failed to load toggles from {path}: {e}")
        return self.default_toggles.copy()

    def _check_auth_guard(self):
        ok, msg = self.oanda.check_authorization()
        if ok:
            if self.toggles.get("alert_on_auth", True) and not self._auth_reported_ok:
                try:
                    send_system_alert("OANDA practice connected ✅", msg)
                except Exception:
                    logger.debug('Auth success alert failed', exc_info=True)
            self._auth_reported_ok = True
            self._auth_reported_fail = False
            return
        if not ok:
            if not self._auth_reported_fail and self.toggles.get("alert_on_auth", True):
                try:
                    send_system_alert("❌ Unauthorized 401 — check OANDA_API_KEY", msg, level="ERROR")
                except Exception:
                    logger.debug('Auth failure alert failed', exc_info=True)
            self._auth_reported_fail = True
            if self.toggles.get("no_simulation_mode", True):
                raise SystemExit("Auth failed — refusing to run in simulation (no_simulation_mode=true).")

    def _announce(self):
        self.display.clear_screen()
        self.display.header('RBOTZILLA Consolidated', f'Env: {self.environment} | PIN: {getattr(RickCharter, "PIN", "N/A")}')
        # Log the active profile and critical charter knobs for easier debugging
        try:
            log_narration(
                event_type="PROFILE_STATUS",
                details={
                    "description": "Balanced profile applied",
                    "min_expected_pnl_usd": getattr(RickCharter, 'MIN_EXPECTED_PNL_USD', None),
                    "min_notional_usd": getattr(RickCharter, 'MIN_NOTIONAL_USD', None),
                    "max_margin_utilization_pct": getattr(RickCharter, 'MAX_MARGIN_UTILIZATION_PCT', None),
                },
                symbol='SYSTEM',
                venue='oanda'
            )
        except Exception as e:
            logger.debug('Profile status narration failed: %s', e)

    def _run_police(self):
        try:
            _rbz_force_min_notional_position_police(account_id=self.oanda.account_id, token=self.oanda.api_token, api_base=self.oanda.api_base)
        except Exception as e:
            logger.warning('Position police error: %s', e)

    async def run(self):
        self.running = True
        # Start market tick emitter only for non-live envs AND if opt-in env var is enabled
        if self.environment != 'live' and os.environ.get('ENABLE_TELEM_EMITTER', 'false').lower() in ('1', 'true', 'yes'):
            try:
                self.market_tick_task = asyncio.create_task(self._market_tick_emitter())
            except Exception:
                logger.debug('Market tick emitter initialization failed')
        while self.running:
            try:
                self.toggles = self._load_toggles()
                self._apply_selectivity_from_toggles()
                self._check_auth_guard()
                trades = self.oanda.get_trades() or []
                self.active_positions = {t['id']: t for t in trades}
                self.display.info('Active Positions', str(len(self.active_positions)))

                # Police enforcement
                self._run_police()

                # Place new trades if capacity allows
                if len(self.active_positions) < self.MAX_POSITIONS:
                    for symbol in self.TRADING_PAIRS:
                        if any((t.get('instrument') or t.get('symbol')) == symbol for t in trades):
                            continue
                        candles = self.oanda.get_historical_data(symbol, count=100, granularity='M15')
                        result = generate_signal(symbol, candles)
                        # Handle both 2-tuple and 3-tuple returns
                        if isinstance(result, tuple):
                            sig = result[0]
                            conf = result[1] if len(result) > 1 else 0.0
                        else:
                            sig, conf = result, 0.0
                        if sig and self._passes_selectivity(conf):
                            await self._open_trade(symbol, sig, conf)
                            await asyncio.sleep(1)

                # Manage open trades
                for trade in trades:
                    await self._manage_trade(trade)

                await asyncio.sleep(30)
            except Exception as e:
                logger.error('Engine main loop error: %s', e)
                await asyncio.sleep(5)
            # Graceful shutdown / cancel background tasks
            if self.market_tick_task:
                try:
                    self.market_tick_task.cancel()
                except Exception:
                    pass

    async def _open_trade(self, symbol: str, direction: str, confidence: float):
        prices = self.oanda.get_live_prices([symbol])
        if not prices or symbol not in prices:
            return
        snap = prices[symbol]
        bid = snap.get('bid')
        ask = snap.get('ask')
        entry = ask if direction == 'BUY' else bid
        if entry is None:
            return
        try:
            entry = float(entry)
        except Exception:
            return

        pip = 0.01 if 'JPY' in symbol else 0.0001
        sl = entry - (self.STOP_LOSS_PIPS * pip) if direction == 'BUY' else entry + (self.STOP_LOSS_PIPS * pip)
        strategy_name = os.getenv('ENGINE_STRATEGY', 'momentum')
        is_scalp = strategy_name in {"wolfpack_ema_trend", "fvg_breakout", "scalp"}
        use_tp = self.toggles.get('tp_for_swings', False) if not is_scalp else self.toggles.get('tp_for_scalps', False)
        tp = None
        if use_tp:
            tp = entry + (self.TAKE_PROFIT_PIPS * pip) if direction == 'BUY' else entry - (self.TAKE_PROFIT_PIPS * pip)

        # Calculate units to meet minimum notional with 5% buffer
        # For USD base pairs (USD_XXX): 1 unit = $1 notional
        # For non-USD base pairs (XXX_USD): 1 unit = entry_price USD notional
        min_notional = getattr(RickCharter, 'MIN_NOTIONAL_USD', 15000)
        if symbol.startswith('USD'):
            # USD is base (USD_JPY, USD_CAD, etc.) - each unit = $1
            units = int(min_notional * 1.05)
        else:
            # USD is quote (EUR_USD, AUD_USD, etc.) - each unit = entry price in USD
            units = int((min_notional * 1.05) / max(entry, 1e-9))
        # Round up to nearest 100 for cleaner sizing
        units = ((units // 100) + 1) * 100
        units = units if direction == 'BUY' else -units
        base_ccy, quote_ccy = (symbol.split('_', 1) + [''])[:2]
        if quote_ccy == 'USD':
            risk_usd = abs(entry - sl) * abs(units)
            reward_usd = abs(tp - entry) * abs(units) if tp is not None else 0.0
            notional_usd = abs(units) * entry
        elif base_ccy == 'USD':
            # P/L is denominated in quote currency (JPY/CAD/CHF...). Approx convert to USD by dividing by price.
            risk_usd = (abs(entry - sl) * abs(units)) / max(entry, 1e-9)
            reward_usd = ((abs(tp - entry) * abs(units)) / max(entry, 1e-9)) if tp is not None else 0.0
            notional_usd = abs(units)  # units are USD
        else:
            # Crosses not used by default in this engine; best-effort display.
            risk_usd = 0.0
            reward_usd = 0.0
            notional_usd = None

        tp_text = f"TP: {tp:.5f} (+${reward_usd:.2f})" if tp is not None else "TP: -- (disabled)"
        self.display.info('Placing', f"{symbol} {direction} | SL: {sl:.5f} (-${risk_usd:.2f}) | {tp_text}")
        log_narration(event_type='TRADE_SIGNAL', details={'symbol': symbol, 'direction': direction, 'confidence': confidence})

        # Two-step method: TP is optional; we manage exits via break-even + tight trailing + optional scale-out.
        result = self.oanda.place_oco_order(symbol, entry, sl, tp, units)
        if result.get('success'):
            order_id = result.get('order_id')
            self.display.alert(f"✅ OCO order placed! Order ID: {order_id}", 'SUCCESS')
            target_text = f"{tp:.5f}" if tp is not None else "--"
            notional_text = f"${notional_usd:,.0f}" if isinstance(notional_usd, (int, float)) else "--"
            self.display.trade_open(
                symbol,
                direction,
                entry,
                f"Stop: {sl:.5f} | Target: {target_text} | Size: {abs(units):,} units | Notional: {notional_text}"
            )
            log_narration(
                event_type='TRADE_OPENED',
                details={
                    'symbol': symbol,
                    'entry_price': entry,
                    'stop_loss': sl,
                    'take_profit': tp,
                    'stop_loss_usd': round(risk_usd, 2),
                    'take_profit_usd': round(reward_usd, 2),
                    'notional_usd': round(notional_usd, 2) if isinstance(notional_usd, (int, float)) else None,
                }
            )
        else:
            self.display.error('Order failed: ' + str(result.get('error')))

    async def _manage_trade(self, trade):
        try:
            is_long = float(trade.get('currentUnits', trade.get('units', 0))) > 0
            trade_id = str(trade.get('id') or '')
            entry = float(trade.get('price') or trade.get('entryPrice') or 0)
            sl_order = trade.get('stopLossOrder') or {}
            price_val = sl_order.get('price') if sl_order else None
            current_sl = float(price_val) if price_val is not None else None
            symbol = trade.get('instrument') or trade.get('symbol')
            prices = self.oanda.get_live_prices([symbol])
            if not prices or symbol not in prices:
                return
            snap = prices[symbol]
            curr = snap.get('bid') if is_long else snap.get('ask')
            if curr is None:
                return
            curr = float(curr)
            pip = 0.01 if 'JPY' in symbol else 0.0001
            profit_pips = (curr - entry) / pip if is_long else (entry - curr) / pip

            # Optional scale-out (incremental partial closes)
            try:
                if self.toggles.get('scale_out_enabled', True) and trade_id:
                    done = self._scale_out_done.setdefault(trade_id, set())
                    levels = self.toggles.get('scale_out_levels') or []
                    # Validate levels (avoid weird runtime types from toggles.json)
                    sane_levels = []
                    for i, lvl in enumerate(levels):
                        if not isinstance(lvl, dict):
                            continue
                        p = lvl.get('pips')
                        f = lvl.get('fraction')
                        if p is None or f is None:
                            continue
                        try:
                            p = float(p)
                            f = float(f)
                        except Exception:
                            continue
                        if p > 0 and 0 < f < 1:
                            sane_levels.append((i, p, f))

                    if sane_levels:
                        abs_units = int(abs(float(trade.get('currentUnits', trade.get('units', 0)))))
                        for idx, pips_trigger, fraction in sane_levels:
                            if idx in done:
                                continue
                            if profit_pips >= pips_trigger and abs_units >= 2:
                                close_units = int(abs_units * fraction)
                                # Round to nearest 100 for cleaner sizing, keep at least 1 unit
                                close_units = max(1, (close_units // 100) * 100)
                                if close_units >= abs_units:
                                    continue
                                resp = self.oanda.close_trade(trade_id, close_units)
                                if resp and resp.get('success'):
                                    done.add(idx)
                                    self.display.info('Scale-out', f"{symbol}: closed {close_units} units at +{profit_pips:.1f} pips")
                                    try:
                                        log_narration(
                                            event_type='TRADE_SCALE_OUT',
                                            details={
                                                'trade_id': trade_id,
                                                'symbol': symbol,
                                                'closed_units': close_units,
                                                'profit_pips': round(profit_pips, 2),
                                                'level_index': idx,
                                            },
                                            symbol=symbol,
                                            venue='oanda'
                                        )
                                    except Exception:
                                        pass
            except Exception:
                pass

            be_trigger = self.toggles.get('be_trigger_pips', self.TRAILING_START_PIPS)
            trail_trigger = self.toggles.get('trail_trigger_pips', self.TRAILING_START_PIPS)
            trail_distance = self.toggles.get('tight_trail_distance_pips', self.TRAILING_DIST_PIPS) if self.toggles.get('tight_trailing', True) else self.toggles.get('trail_distance_pips', self.TRAILING_DIST_PIPS)
            # Step 1: move to break-even
            if self.toggles.get('two_step_sl', True) and profit_pips >= be_trigger:
                be_sl = entry
                if current_sl is None or (is_long and be_sl > current_sl) or (not is_long and be_sl < current_sl):
                    self.display.info('SL to BE', f"{symbol}: {current_sl if current_sl is not None else 0:.5f} -> {be_sl:.5f}")
                    self.oanda.set_trade_stop(trade.get('id'), be_sl)
                    current_sl = be_sl
            # Step 2: tight trailing once trigger reached
            if profit_pips >= trail_trigger:
                new_sl = curr - (trail_distance * pip) if is_long else curr + (trail_distance * pip)
                if current_sl is None or (is_long and new_sl > current_sl) or (not is_long and new_sl < current_sl):
                    self.display.info('Trailing', f"{symbol}: {current_sl if current_sl is not None else 0:.5f} -> {new_sl:.5f}")
                    self.oanda.set_trade_stop(trade.get('id'), new_sl)
            elif not self.toggles.get('two_step_sl', True) and profit_pips > self.TRAILING_START_PIPS and current_sl is not None:
                # Fallback to legacy trailing when two_step_sl disabled
                new_sl = curr - (self.TRAILING_DIST_PIPS * pip) if is_long else curr + (self.TRAILING_DIST_PIPS * pip)
                if (is_long and new_sl > current_sl) or (not is_long and new_sl < current_sl):
                    self.display.info('Trailing', f"{symbol}: {current_sl:.5f} -> {new_sl:.5f}")
                    self.oanda.set_trade_stop(trade.get('id'), new_sl)
        except Exception:
            pass

    async def _market_tick_emitter(self):
        """Emit MARKET_TICK events at a steady frequency. If live prices are available, use them; otherwise use last price with minor random walk for testing. Only enabled for practice/canary (non-live) environments to avoid adding noise in production."""
        try:
            while self.running:
                try:
                    prices = self.oanda.get_live_prices([self.market_tick_symbol]) or {}
                    if prices and self.market_tick_symbol in prices:
                        p = prices[self.market_tick_symbol]
                        bid = float(p.get('bid') or p.get('bidPrice') or p.get('b') or 0.0)
                        ask = float(p.get('ask') or p.get('askPrice') or p.get('a') or 0.0)
                    else:
                        # Minor random walk for testing only
                        move = (random.random() - 0.5) * 0.0005
                        self._market_tick_last_price += move
                        bid = round(self._market_tick_last_price - 0.00002, 5)
                        ask = round(self._market_tick_last_price + 0.00002, 5)
                    # Emit a MARKET_TICK narration event
                    try:
                        log_narration(event_type='MARKET_TICK', details={'bid': bid, 'ask': ask}, symbol=self.market_tick_symbol, venue='oanda')
                    except Exception:
                        logger.debug('Failed to log MARKET_TICK', exc_info=True)
                    await asyncio.sleep(self.market_tick_freq)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.debug('Market tick loop error: %s', e)
                    await asyncio.sleep(5)
        except Exception:
            # Best-effort emitter, non-fatal
            pass


if __name__ == '__main__':
    import subprocess
    import time

    # Auto-stop any existing instances before starting
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'oanda/oanda_trading_engine.py'],
            capture_output=True,
            text=True
        )
        existing_pids = [pid for pid in result.stdout.strip().split('\n') if pid and pid != str(os.getpid())]

        if existing_pids:
            print(f"🔄 Stopping {len(existing_pids)} existing OANDA engine(s)...")
            subprocess.run(['pkill', '-f', 'python3.*oanda/oanda_trading_engine.py'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            print("✅ Ready to start")
    except Exception as e:
        logger.warning(f"Could not check for existing instances: {e}")

    engine = OandaTradingEngine(environment=os.getenv('RICK_ENV', 'practice'))
    try:
        asyncio.run(engine.run())
    except KeyboardInterrupt:
        print('\nStopped')
