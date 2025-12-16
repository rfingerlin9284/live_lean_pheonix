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

# Optional correlation gate (currency bucket anti-duplication)
try:
    from foundation.margin_correlation_gate import MarginCorrelationGate, Position as GatePosition, Order as GateOrder
except Exception:
    MarginCorrelationGate = None
    GatePosition = None
    GateOrder = None

# Additive advanced modules (safe defaults: disabled / classic)
try:
    from systems.signal_fusion import fuse as fuse_signal
except Exception:
    fuse_signal = None

try:
    from util.aggressive_plan import compute_units as compute_aggr_units
except Exception:
    compute_aggr_units = None

try:
    from execution.exit_edge_hybrid import apply as apply_edge_exit
except Exception:
    apply_edge_exit = None

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

            # --- Advanced (additive) knobs ---
            # Exit manager mode:
            # - classic: existing BE + tight trail (+ optional scale-out)
            # - edge_hybrid: ACD (BE/locks) + Chandelier (ATR) with classic fallback
            "exit_mode": "classic",
            "edge_exit_enabled": True,

            # ACD stages (pips)
            "acd_be_pips": 6,
            "acd_partial_pips": 12,
            "acd_full_pips": 24,
            "acd_partial_lock_pips": 4,
            "acd_full_lock_pips": 2,

            # Chandelier (ATR)
            "chandelier_atr_period": 14,
            "chandelier_atr_mult": 2.2,

            # Volatility sanity
            "vol_adr_lookback": 14,
            "vol_adr_cap_pips": 400,

            # Aggressive sizing (PIN-gated) — default OFF
            "aggressive_enabled": False,
            "base_leverage": 1.5,
            "leverage_max": 3.0,
            "leverage_aggressiveness": 1.0,

            # --- Decision narration (plain-English reasons) ---
            "decision_narration_enabled": True,
            "terminal_decision_narration": True,
            "terminal_decision_rate_limit_sec": 20,
            "terminal_narrate_no_signal": False,

            # --- Portfolio posture ---
            # Split the available slots into 2 buckets:
            # - GEM: higher threshold, intended for longer holds
            # - SCALP: faster turnover
            "slot_split_enabled": True,
            "gem_slots": 3,
            "scalp_slots": 9,
            "gem_min_confidence": 0.78,
            "gem_min_confluence": 0.65,
            "scalp_min_confidence": None,
            "scalp_min_confluence": 0.0,

            # --- Anti-duplication / correlation ---
            # Currency bucket correlation gate: blocks entries that increase existing same-direction exposure.
            "correlation_gate_enabled": True,

            # Optional runtime pair universe override
            # Example: ["EUR_USD","GBP_USD","AUD_USD","NZD_USD","USD_JPY","USD_CHF","USD_CAD",...]
            "trading_pairs": None,
        }
        self.toggles = self._load_toggles()
        self._auth_reported_ok = False
        self._auth_reported_fail = False

        # Latest entry confluence (used by aggressive sizing if enabled)
        self._last_confluence = 0.0

        # Decision narration / slot tagging
        self._decision_last_ts: Dict[str, float] = {}
        self._position_bucket_by_symbol: Dict[str, str] = {}

        # Optional correlation gate instance (lazy)
        self._corr_gate = None

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
        self._apply_pairs_from_toggles()
        self._check_auth_guard()
        # Log active profile from config/strategy_toggles.yaml
        try:
            import yaml
            with open('config/strategy_toggles.yaml', 'r') as f:
                toggles = yaml.safe_load(f)
            active_profile = toggles.get('active_profile', 'balanced')
            log_narration(
                event_type="PROFILE_STATUS",
                details={
                    "active_profile": active_profile,
                    "description": f"Profile '{active_profile}' loaded from config/strategy_toggles.yaml"
                },
                symbol='SYSTEM',
                venue='oanda'
            )
        except Exception as e:
            logger.warning(f"Could not log active profile: {e}")

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

    def _apply_pairs_from_toggles(self) -> None:
        """Optionally override trading universe from toggles.

        This does not affect risk/OCO logic; it only changes which instruments are scanned.
        """
        pairs = self.toggles.get('trading_pairs')
        if not isinstance(pairs, list) or not pairs:
            return
        cleaned: List[str] = []
        for p in pairs:
            if not isinstance(p, str):
                continue
            p = p.strip().upper().replace('/', '_')
            if '_' not in p:
                continue
            cleaned.append(p)
        if cleaned:
            self.TRADING_PAIRS = cleaned

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

    def _should_emit_decision(self, symbol: str, key: str) -> bool:
        """Rate-limit terminal decision narration to avoid flooding."""
        try:
            import time
            now = time.time()
        except Exception:
            return True
        rate = self.toggles.get('terminal_decision_rate_limit_sec', 20)
        try:
            rate = float(rate)
        except Exception:
            rate = 20.0
        if rate <= 0:
            return True
        k = f"{symbol}:{key}"
        last = self._decision_last_ts.get(k, 0.0)
        if (now - last) >= rate:
            self._decision_last_ts[k] = now
            return True
        return False

    def _decision_say(self, symbol: str, message: str, key: str = 'decision', warn: bool = False) -> None:
        if not self.toggles.get('terminal_decision_narration', True):
            return
        if not self._should_emit_decision(symbol, key):
            return
        try:
            if warn:
                self.display.warning(f"{symbol}: {message}")
            else:
                self.display.rick_says(f"{symbol}: {message}")
        except Exception:
            pass

    def _narrate(self, event_type: str, symbol: str, details: dict) -> None:
        if not self.toggles.get('decision_narration_enabled', True):
            return
        try:
            log_narration(event_type=event_type, details=details, symbol=symbol, venue='oanda')
        except Exception:
            pass

    def _count_bucket_slots(self, trades: List[dict]) -> Dict[str, int]:
        gem = 0
        scalp = 0
        for t in trades:
            sym = (t.get('instrument') or t.get('symbol') or '').upper()
            if not sym:
                continue
            b = (self._position_bucket_by_symbol.get(sym) or 'SCALP').upper()
            if b == 'GEM':
                gem += 1
            else:
                scalp += 1
        return {'gem': gem, 'scalp': scalp}

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
                self._apply_pairs_from_toggles()
                self._check_auth_guard()
                trades = self.oanda.get_trades() or []
                self.active_positions = {t['id']: t for t in trades}
                self.display.info('Active Positions', str(len(self.active_positions)))

                # Police enforcement
                self._run_police()

                # Place new trades if capacity allows
                if len(self.active_positions) < self.MAX_POSITIONS:
                    bucket_counts = self._count_bucket_slots(trades)
                    gem_slots = int(self.toggles.get('gem_slots', 3) or 0)
                    scalp_slots = int(self.toggles.get('scalp_slots', max(self.MAX_POSITIONS - gem_slots, 0)) or 0)
                    gem_min_conf = float(self.toggles.get('gem_min_confidence', 0.78) or 0.78)
                    gem_min_confl = float(self.toggles.get('gem_min_confluence', 0.65) or 0.0)
                    scalp_min_conf = self.toggles.get('scalp_min_confidence', None)
                    scalp_min_conf = float(scalp_min_conf) if scalp_min_conf is not None else float(self.MIN_CONFIDENCE)
                    scalp_min_confl = float(self.toggles.get('scalp_min_confluence', 0.0) or 0.0)

                    for symbol in self.TRADING_PAIRS:
                        if any((t.get('instrument') or t.get('symbol')) == symbol for t in trades):
                            # Optional: explain skips for duplicates
                            if self.toggles.get('terminal_decision_narration', True) and self._should_emit_decision(symbol, 'already_open'):
                                self._decision_say(symbol, 'skip — already in position', key='already_open')
                            continue
                        candles = self.oanda.get_historical_data(symbol, count=100, granularity='M15')
                        sig = None
                        conf = 0.0
                        confluence = 0.0
                        meta = {}

                        if fuse_signal is not None:
                            try:
                                sig, conf, confluence, meta = fuse_signal(symbol, candles, toggles=self.toggles)
                            except Exception:
                                sig, conf, confluence, meta = None, 0.0, 0.0, {}
                        else:
                            result = generate_signal(symbol, candles)
                            # Handle both 2-tuple and 3-tuple returns
                            if isinstance(result, tuple):
                                sig = result[0]
                                conf = result[1] if len(result) > 1 else 0.0
                                meta = result[2] if len(result) > 2 and isinstance(result[2], dict) else {}
                            else:
                                sig, conf = result, 0.0

                        # If fusion gated volatility, narrate and skip
                        try:
                            if isinstance(meta, dict) and meta.get('vol_gate'):
                                log_narration(
                                    event_type='ENTRY_VOL_GATED',
                                    details={
                                        'symbol': symbol,
                                        'adr_pips': meta.get('adr_pips'),
                                        'adr_cap_pips': meta.get('adr_cap_pips'),
                                    },
                                    symbol=symbol,
                                    venue='oanda'
                                )
                                self._decision_say(symbol, f"rejected — volatility gate (ADR {meta.get('adr_pips')}p > cap {meta.get('adr_cap_pips')}p)", key='vol_gate', warn=True)
                                continue
                        except Exception:
                            pass

                        if not sig:
                            if self.toggles.get('terminal_narrate_no_signal', False):
                                self._decision_say(symbol, 'no signal this scan', key='no_signal')
                            continue

                        # Candidate exists: explain what we saw
                        self._narrate(
                            event_type='ENTRY_CANDIDATE',
                            symbol=symbol,
                            details={
                                'direction': sig,
                                'confidence': float(conf or 0.0),
                                'confluence': float(confluence or 0.0),
                                'meta': meta or {},
                                'min_confidence': float(self.MIN_CONFIDENCE),
                            },
                        )

                        # Confidence/selectivity gate
                        if not self._passes_selectivity(conf):
                            reason = f"confidence {float(conf or 0.0):.2f} < min {float(self.MIN_CONFIDENCE):.2f}"
                            self._narrate('ENTRY_REJECTED', symbol, {
                                'reason_code': 'confidence_below_min',
                                'explanation': reason,
                                'direction': sig,
                                'confidence': float(conf or 0.0),
                                'min_confidence': float(self.MIN_CONFIDENCE),
                            })
                            self._decision_say(symbol, f"rejected — {reason}", key='conf_min', warn=True)
                            continue

                        # Slot split: GEM vs SCALP
                        bucket = 'SCALP'
                        if bool(self.toggles.get('slot_split_enabled', True)):
                            # Prefer GEM only if it clears higher bar and GEM slots remain
                            if float(conf or 0.0) >= gem_min_conf and float(confluence or 0.0) >= gem_min_confl and bucket_counts['gem'] < gem_slots:
                                bucket = 'GEM'
                            else:
                                # Otherwise it must fit SCALP constraints
                                if bucket_counts['scalp'] >= scalp_slots:
                                    reason = f"scalp slots full ({bucket_counts['scalp']}/{scalp_slots})"
                                    self._narrate('ENTRY_REJECTED', symbol, {
                                        'reason_code': 'scalp_slots_full',
                                        'explanation': reason,
                                        'direction': sig,
                                        'confidence': float(conf or 0.0),
                                        'confluence': float(confluence or 0.0),
                                        'bucket_counts': bucket_counts,
                                    })
                                    self._decision_say(symbol, f"rejected — {reason}", key='slots_full', warn=True)
                                    continue
                                if float(conf or 0.0) < scalp_min_conf:
                                    reason = f"scalp conf {float(conf or 0.0):.2f} < {float(scalp_min_conf):.2f}"
                                    self._narrate('ENTRY_REJECTED', symbol, {
                                        'reason_code': 'scalp_conf_below_min',
                                        'explanation': reason,
                                        'direction': sig,
                                        'confidence': float(conf or 0.0),
                                        'scalp_min_confidence': float(scalp_min_conf),
                                    })
                                    self._decision_say(symbol, f"rejected — {reason}", key='scalp_conf', warn=True)
                                    continue
                                if float(confluence or 0.0) < scalp_min_confl:
                                    reason = f"scalp confluence {float(confluence or 0.0):.2f} < {float(scalp_min_confl):.2f}"
                                    self._narrate('ENTRY_REJECTED', symbol, {
                                        'reason_code': 'scalp_confluence_below_min',
                                        'explanation': reason,
                                        'direction': sig,
                                        'confluence': float(confluence or 0.0),
                                        'scalp_min_confluence': float(scalp_min_confl),
                                    })
                                    self._decision_say(symbol, f"rejected — {reason}", key='scalp_confl', warn=True)
                                    continue
                        else:
                            bucket = 'OPEN'

                        # Capacity guard
                        if len(self.active_positions) >= self.MAX_POSITIONS:
                            reason = f"max positions reached ({len(self.active_positions)}/{self.MAX_POSITIONS})"
                            self._narrate('ENTRY_REJECTED', symbol, {
                                'reason_code': 'max_positions',
                                'explanation': reason,
                                'direction': sig,
                            })
                            self._decision_say(symbol, f"rejected — {reason}", key='max_pos', warn=True)
                            continue

                        # Approved by selection gates (correlation gate happens at order-time once we know units)
                        self._narrate('ENTRY_ACCEPTED', symbol, {
                            'direction': sig,
                            'confidence': float(conf or 0.0),
                            'confluence': float(confluence or 0.0),
                            'bucket': bucket,
                            'bucket_counts': bucket_counts,
                        })
                        self._decision_say(symbol, f"accepted — {sig} (bucket={bucket}, conf={float(conf or 0.0):.2f}, confl={float(confluence or 0.0):.2f})", key='accepted')

                        self._last_confluence = float(confluence or 0.0)
                        ok, why = await self._open_trade(
                            symbol,
                            sig,
                            conf,
                            confluence=float(confluence or 0.0),
                            fusion_meta=meta,
                            bucket=bucket,
                        )
                        if ok:
                            # Update local bucket tag for counting/reserving
                            self._position_bucket_by_symbol[symbol] = bucket
                            bucket_counts = self._count_bucket_slots(trades)
                        else:
                            if why:
                                self._decision_say(symbol, f"blocked at order-time — {why}", key='order_blocked', warn=True)
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

    async def _open_trade(self, symbol: str, direction: str, confidence: float, confluence: float = 0.0, fusion_meta: Optional[dict] = None, bucket: str = 'SCALP'):
        prices = self.oanda.get_live_prices([symbol])
        if not prices or symbol not in prices:
            return False, 'missing_price'
        snap = prices[symbol]
        bid = snap.get('bid')
        ask = snap.get('ask')
        entry = ask if direction == 'BUY' else bid
        if entry is None:
            return False, 'missing_entry'
        try:
            entry = float(entry)
        except Exception:
            return False, 'bad_entry'

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
            units_abs = int(min_notional * 1.05)
        else:
            # USD is quote (EUR_USD, AUD_USD, etc.) - each unit = entry price in USD
            units_abs = int((min_notional * 1.05) / max(entry, 1e-9))

        # Round up to nearest 100 for cleaner sizing
        units_abs = max(1, ((units_abs // 100) + 1) * 100)

        # Optional aggressive plan (PIN-gated) — default OFF
        sizing_meta = None
        if compute_aggr_units is not None:
            try:
                units_signed, sizing_meta = compute_aggr_units(
                    pin=841921,
                    price=float(entry),
                    side=direction,
                    base_units_at_1x=int(units_abs),
                    toggles={**self.toggles, "entry_confluence": float(confluence or 0.0)},
                )
                # Keep it clean: nearest 100, but never below 1
                units_abs = max(1, int(abs(units_signed)))
                units_abs = max(1, (units_abs // 100) * 100) or 100
            except Exception:
                sizing_meta = None

        units = units_abs if direction == 'BUY' else -units_abs

        # Correlation/anti-duplication gate (currency bucket) — blocks entries that stack same-direction exposure.
        if bool(self.toggles.get('correlation_gate_enabled', True)) and MarginCorrelationGate is not None and GatePosition is not None and GateOrder is not None:
            try:
                if self._corr_gate is None:
                    # NAV only affects margin checks; correlation check works regardless.
                    nav = float(self.toggles.get('account_nav_usd', 1970.0) or 1970.0)
                    self._corr_gate = MarginCorrelationGate(account_nav=nav)

                positions = []
                for t in (self.active_positions or {}).values():
                    sym = (t.get('instrument') or t.get('symbol') or '').upper()
                    if not sym:
                        continue
                    u = float(t.get('currentUnits', t.get('units', 0)) or 0)
                    side = 'LONG' if u > 0 else 'SHORT'
                    ep = float(t.get('price') or t.get('entryPrice') or 0.0)
                    positions.append(
                        GatePosition(
                            symbol=sym,
                            side=side,
                            units=abs(u),
                            entry_price=ep,
                            current_price=ep,
                            pnl=0.0,
                            pnl_pips=0.0,
                            margin_used=0.0,
                            position_id=str(t.get('id') or ''),
                        )
                    )

                new_order = GateOrder(
                    symbol=symbol,
                    side=direction,
                    units=float(abs(units_abs)),
                    price=float(entry),
                    order_id='PENDING',
                    order_type='MARKET',
                )

                corr = self._corr_gate.correlation_gate_any_ccy(new_order=new_order, current_positions=positions)
                if not getattr(corr, 'allowed', True):
                    reason = getattr(corr, 'reason', 'correlation_gate_blocked')
                    self._narrate('ENTRY_REJECTED', symbol, {
                        'reason_code': 'correlation_gate',
                        'explanation': reason,
                        'direction': direction,
                        'bucket': bucket,
                    })
                    return False, reason
            except Exception:
                # Never fail open order placement due to gate errors; only enforce when it runs cleanly.
                pass
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

        # Optional narration: show confluence + sizing mode
        try:
            log_narration(
                event_type='ENTRY_CONFLUENCE',
                details={
                    'symbol': symbol,
                    'confidence': float(confidence or 0.0),
                    'confluence': float(confluence or 0.0),
                    'fusion_meta': fusion_meta or {},
                    'sizing': sizing_meta,
                    'bucket': bucket,
                },
                symbol=symbol,
                venue='oanda'
            )
        except Exception:
            pass

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
                    'bucket': bucket,
                }
            )
            return True, None
        else:
            self.display.error('Order failed: ' + str(result.get('error')))
            self._narrate('ENTRY_REJECTED', symbol, {
                'reason_code': 'broker_rejected',
                'explanation': str(result.get('error')),
                'direction': direction,
                'bucket': bucket,
            })
            return False, str(result.get('error'))

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

            # Edge exits (ACD -> Chandelier) are additive and toggleable.
            # If enabled, we apply it first; classic BE/trailing remains as fallback.
            exit_mode = str(self.toggles.get('exit_mode', 'classic') or 'classic').lower()
            if apply_edge_exit is not None and exit_mode in ('edge_hybrid', 'edge', 'hybrid'):
                try:
                    recent = None
                    # Only pull candles if we are in/near profit to reduce API load.
                    if profit_pips > 0:
                        recent = self.oanda.get_historical_data(symbol, count=60, granularity='M15')
                    decision = apply_edge_exit(trade=trade, price_snap=snap, toggles=self.toggles, recent_candles=recent)
                    if isinstance(decision, dict) and decision.get('action') == 'MOVE_SL' and decision.get('new_sl') is not None:
                        try:
                            new_sl_raw = decision.get('new_sl')
                            if new_sl_raw is None:
                                return
                            new_sl = float(new_sl_raw)
                        except Exception:
                            return
                        # Never loosen stop
                        if current_sl is None or (is_long and new_sl > current_sl) or ((not is_long) and new_sl < current_sl):
                            self.display.info('SL update', f"{symbol}: {current_sl if current_sl is not None else 0:.5f} -> {new_sl:.5f} ({decision.get('reason','EDGE')})")
                            self.oanda.set_trade_stop(trade.get('id'), new_sl)
                            current_sl = new_sl
                            try:
                                log_narration(
                                    event_type='EXIT_EDGE_SL_MOVED',
                                    details={
                                        'trade_id': trade_id,
                                        'symbol': symbol,
                                        'reason': decision.get('reason'),
                                        'new_sl': new_sl,
                                        'profit_pips': round(float(profit_pips), 2),
                                        'meta': decision.get('meta', {}),
                                    },
                                    symbol=symbol,
                                    venue='oanda'
                                )
                            except Exception:
                                pass
                            # If edge module moved SL, skip further classic changes this loop.
                            return
                except Exception:
                    pass

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
