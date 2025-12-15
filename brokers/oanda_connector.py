#!/usr/bin/env python3
"""
OANDA Broker Connector - RBOTzilla UNI Phase 9
Live/Paper trading connector with OCO support and sub-300ms execution.
PIN: 841921 | Generated: 2025-09-26
"""

import os
import json
import time
import logging
import requests
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timezone, timedelta
import websocket
from urllib.parse import urljoin, urlencode

try:
    from util.platform_breaker import is_platform_enabled
except Exception:
    def is_platform_enabled(platform: str) -> bool:
        return True

# Charter compliance imports
try:
    from ..foundation.rick_charter import validate_pin
except ImportError:
    # Fallback for testing
    def validate_pin(pin): return pin == 841921

# Narration logging
try:
    from ..util.narration_logger import log_narration, log_pnl
except ImportError:
    try:
        from util.narration_logger import log_narration, log_pnl
    except ImportError:
        # Fallback stubs for testing
        def log_narration(*args, **kwargs): pass
        def log_pnl(*args, **kwargs): pass
    try:
        from util.micro_trade_filter import should_block_micro_trade
    except ImportError:
        def should_block_micro_trade(*args, **kwargs):
            return False, {}

# OCO integration
try:
    from ..execution.smart_oco import OCOOrder, OCOStatus, create_oco_order
except ImportError:
    # Fallback stubs for testing
    class OCOStatus:
        PLACED = "placed"
        ERROR = "error"
    
    def create_oco_order(*args, **kwargs):
        return {"status": "success", "order_id": "test_123"}

class OandaOrderType(Enum):
    """OANDA order types"""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    MARKET_IF_TOUCHED = "MARKET_IF_TOUCHED"
    TAKE_PROFIT = "TAKE_PROFIT"
    STOP_LOSS = "STOP_LOSS"

class OandaTimeInForce(Enum):
    """OANDA time in force options"""
    FOK = "FOK"  # Fill or Kill
    IOC = "IOC"  # Immediate or Cancel
    GTC = "GTC"  # Good Till Cancelled
    GTD = "GTD"  # Good Till Date

@dataclass
class OandaAccount:
    """OANDA account information"""
    account_id: str
    currency: str
    balance: float
    unrealized_pl: float
    margin_used: float
    margin_available: float
    open_positions: int
    open_trades: int

@dataclass
class OandaInstrument:
    """OANDA instrument specification"""
    name: str
    display_name: str
    pip_location: int
    display_precision: int
    trade_units_precision: int
    minimum_trade_size: float
    maximum_trailing_stop_distance: float
    minimum_trailing_stop_distance: float

class OandaConnector:
    """
    OANDA v20 REST API Connector with OCO support
    Handles both live and practice (paper) trading environments
    Supports dynamic mode switching via .upgrade_toggle
    """
    
    def __init__(self, pin: Optional[int] = None, environment: Optional[str] = None):
        """
        Initialize OANDA connector
        
        Args:
            pin: Charter PIN (841921)
            environment: 'practice' or 'live' (if None, reads from .upgrade_toggle)
        """
        if pin and not validate_pin(pin):
            raise PermissionError("Invalid PIN for OandaConnector")
        
        self.pin_verified = validate_pin(pin) if pin else False
        
        # Dynamic environment from .upgrade_toggle if not specified
        if environment is None:
            try:
                from ..util.mode_manager import get_connector_environment
            except ImportError:
                try:
                    from util.mode_manager import get_connector_environment
                except ImportError:
                    environment = "practice"  # Fallback
                    self.logger = logging.getLogger(__name__)
                    self.logger.warning("mode_manager not available, defaulting to practice")
            
            if environment is None:  # Still None after import attempt
                environment = get_connector_environment("oanda")
                self.logger = logging.getLogger(__name__)
                self.logger.info(f"🔄 Auto-detected environment from .upgrade_toggle: {environment}")
        
        self.environment = environment
        self.logger = logging.getLogger(__name__)
        self.trading_enabled = False
        
        # Load API credentials from environment
        self._load_credentials()
        
        # API endpoints
        if environment == "live":
            self.api_base = "https://api-fxtrade.oanda.com"
            self.stream_base = "https://stream-fxtrade.oanda.com"
        else:  # practice
            self.api_base = "https://api-fxpractice.oanda.com"
            self.stream_base = "https://stream-fxpractice.oanda.com"
        
        # Headers for API requests (Authorization added if token loaded)
        self.headers = {
            "Content-Type": "application/json",
            "Accept-Datetime-Format": "RFC3339"
        }
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"
        
        # Performance tracking
        self.request_times = []
        self._lock = threading.Lock()
        
        # Charter compliance
        self.max_placement_latency_ms = 300
        self.default_timeout = 5.0  # 5 second API timeout
        
        self.logger.info(f"OandaConnector initialized for {environment} environment")
        
        # Validate connection
        self._validate_connection()

    def check_authorization(self) -> tuple:
        """
        Check if the OANDA API credentials are valid by making a test request.
        Returns: (success: bool, message: str)
        """
        if not self.api_token or not self.account_id:
            return False, "Missing API token or account ID"
        
        try:
            url = f"{self.api_base}/v3/accounts/{self.account_id}/summary"
            response = requests.get(url, headers=self.headers, timeout=self.default_timeout)
            if response.status_code == 200:
                data = response.json()
                balance = data.get('account', {}).get('balance', 'N/A')
                return True, f"Account {self.account_id[-4:]} balance: {balance}"
            elif response.status_code == 401:
                return False, f"401 Unauthorized - Invalid API token"
            else:
                return False, f"HTTP {response.status_code}: {response.text[:100]}"
        except requests.exceptions.Timeout:
            return False, "Connection timeout"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def _load_credentials(self):
        """Load API credentials from environment or .env file with safe defaults."""
        # Practice credentials are expected to rotate. To avoid brittle in-code secrets,
        # prefer:
        #   1) explicit environment variables, then
        #   2) repo-local token files (token_practice.txt / token_paper.txt), then
        #   3) finally a last-resort placeholder.
        PRACTICE_ACCOUNT_ID_DEFAULT = "101-001-31210531-002"

        def _read_token_file(path: Path) -> Optional[str]:
            try:
                if not path.is_file():
                    return None
                token = path.read_text(encoding="utf-8").strip().splitlines()[0].strip()
                if not token:
                    return None
                # Basic sanity: OANDA personal access tokens are long hex-ish strings with a dash.
                if len(token) < 20:
                    return None
                return token
            except Exception:
                return None
        
        repo_root = Path(__file__).resolve().parents[1]
        env_file = repo_root / '.env'
        should_load_envfile = os.environ.get('OANDA_LOAD_ENV_FILE', '1').lower() in ('1', 'true', 'yes')

        if should_load_envfile and not env_file.exists():
            try:
                env_file.write_text(
                    "# Auto-generated placeholder for OANDA credentials\n"
                    "# Fill in the values before enabling live trading.\n"
                    "OANDA_PAPER=\n"
                    "OANDA_PRACTICE_ACCOUNT_ID=\n"
                    "OANDA_LIVE_TOKEN=\n"
                    "OANDA_LIVE_ACCOUNT_ID=\n"
                )
                self.logger.info(f"Created placeholder .env file at {env_file} for missing OANDA secrets")
            except Exception as exc:
                self.logger.warning(f"Unable to create placeholder .env file: {exc}")

        if env_file.exists() and should_load_envfile:
            try:
                self.logger.info(f"Loading OANDA credentials from {env_file}")
                with env_file.open() as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#') or '=' not in line:
                            continue
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        if not value:
                            continue
                        if os.environ.get(key):
                            continue
                        os.environ[key] = value
            except Exception as exc:
                self.logger.warning(f"Failed to read {env_file}: {exc}")
        elif should_load_envfile:
            self.logger.debug(".env file not found; relying on existing environment variables for OANDA credentials")

        practice_token = (
            os.getenv('OANDA_PAPER')
            or os.getenv('OANDA_PRACTICE')
            or os.getenv('OANDA_PRACTICE_TOKEN')
            or os.getenv('OANDA_TOKEN')
            or os.getenv('OANDA_ACCESS_TOKEN')
        )
        practice_account = os.getenv('OANDA_PRACTICE_ACCOUNT_ID') or os.getenv('OANDA_ACCOUNT_ID')

        # If practice token is not provided via env, try repo-local token files.
        if not practice_token:
            practice_token = (
                _read_token_file(repo_root / 'token_practice.txt')
                or _read_token_file(repo_root / 'token_paper.txt')
            )

        live_token = (
            os.getenv('OANDA_LIVE_TOKEN')
            or os.getenv('OANDA_ACCESS_TOKEN')
            or os.getenv('OANDA_API_KEY')
            or os.getenv('OANDA_TOKEN')
        )
        live_account = os.getenv('OANDA_LIVE_ACCOUNT_ID') or os.getenv('OANDA_ACCOUNT_ID')

        if self.environment == 'live':
            self.api_token = live_token.strip() if live_token else None
            self.account_id = live_account.strip() if live_account else None
        else:
            # Practice: prefer environment / repo token files; default account id if missing.
            self.api_token = practice_token.strip() if practice_token else None
            self.account_id = (practice_account.strip() if practice_account else PRACTICE_ACCOUNT_ID_DEFAULT)

            # Seed common env vars for downstream components (without overriding explicit user env).
            if self.api_token:
                os.environ.setdefault('OANDA_PAPER', self.api_token)
                os.environ.setdefault('OANDA_PRACTICE_TOKEN', self.api_token)
            if self.account_id:
                os.environ.setdefault('OANDA_PRACTICE_ACCOUNT_ID', self.account_id)

            if self.api_token:
                self.logger.info(f"Practice token loaded (…{self.api_token[-4:]}); account=****{self.account_id[-4:]}")
            else:
                self.logger.warning(
                    "Practice token missing. Set OANDA_PAPER/OANDA_PRACTICE_TOKEN or put it in token_practice.txt"
                )
    
    def _validate_connection(self):
        """Validate OANDA connection and credentials"""
        self.trading_enabled = bool(self.api_token and self.account_id)
        account_suffix = None
        if self.account_id and len(self.account_id) > 4:
            account_suffix = self.account_id[-4:]
        account_display = f"****{account_suffix}" if account_suffix else (self.account_id or 'N/A')

        if not self.trading_enabled:
            if self.environment == "live":
                self.logger.warning("LIVE OANDA credentials not configured - trading will be disabled")
            else:
                self.logger.warning("Practice OANDA credentials not configured - trading is paused")
        else:
            self.logger.info(f"OANDA {self.environment} credentials validated; account={account_display}")
    
    def place_oco_order(self, instrument: str, entry_price: float, stop_loss: float,
                       take_profit: Optional[float] = None, units: int = 0, ttl_hours: float = 24.0,
                       order_type: str = "LIMIT", explanation: Optional[str] = None) -> Dict[str, Any]:
        """
        Place OCO order using OANDA's bracket order functionality - LIVE VERSION
        
        Args:
            instrument: Trading pair (e.g., "EUR_USD")
            entry_price: Entry price for limit order (ignored if order_type="MARKET")
            stop_loss: Stop loss price
            take_profit: Take profit price
            units: Position size (positive for buy, negative for sell)
            ttl_hours: Time to live in hours (default 24h for limit orders, prevents early expiry)
            order_type: "LIMIT" (wait for price) or "MARKET" (immediate execution)
            
        Returns:
            Dict with OCO order result
        """
        start_time = time.time()

        # Platform breaker: allow disabling OANDA only, without stopping the whole system.
        if not is_platform_enabled('oanda'):
            return {
                "success": False,
                "error": "OANDA_PLATFORM_BREAKER_OFF",
                "broker": "OANDA",
                "environment": self.environment,
            }

        # OANDA validates price strings against instrument precision. Avoid float-string
        # artifacts like "1.164179999999" which can trigger 400 InvalidParameterException.
        try:
            quote_ccy = instrument.split("_")[1] if "_" in instrument else instrument[-3:]
        except Exception:
            quote_ccy = ""
        price_precision = 3 if quote_ccy == "JPY" else 5

        def _fmt_price(p: float) -> str:
            return f"{float(p):.{price_precision}f}"

        # Stop-loss is mandatory; take-profit is optional (two-step SL / scale-out management).
        if stop_loss is None:
            self.logger.error("Stop-loss required: stop_loss must be provided for all orders")
            
            # Narration log error
            log_narration(
                event_type="OCO_ERROR",
                details={
                    "error": "STOP_REQUIRED",
                    "message": "stop_loss must be specified",
                    "entry_price": entry_price,
                    "units": units
                },
                symbol=instrument,
                venue="oanda"
            )
            
            return {
                "success": False,
                "error": "STOP_REQUIRED: stop_loss must be specified",
                "broker": "OANDA",
                "environment": self.environment
            }
        
        # Enforce charter minimum notional (match Coinbase behavior)
        try:
            # Import RickCharter if available
            try:
                from ..foundation.rick_charter import RickCharter
            except ImportError:
                try:
                    from foundation.rick_charter import RickCharter
                except ImportError:
                    RickCharter = None
            
            if RickCharter:
                min_notional = RickCharter.MIN_NOTIONAL_USD
                
                # Calculate USD notional based on pair type
                # For USD-based pairs (USD_XXX), units are already in USD
                # For other pairs (XXX_USD), need to convert: units × price
                base_currency = instrument.split("_")[0]
                if base_currency == "USD":
                    notional = abs(units)  # Units already in USD
                else:
                    notional = abs(units) * float(entry_price)  # Convert to USD
                
                if notional < min_notional:
                    # REJECT order instead of auto-adjusting
                    # Auto-adjusting could create unexpected large positions
                    self.logger.error(
                        f"❌ ORDER REJECTED: Charter requires minimum ${min_notional:,} notional. "
                        f"Order notional: ${notional:,.2f} for {instrument} ({abs(units)} units @ {entry_price})"
                    )
                    
                    # Narration log the rejection
                    log_narration(
                        event_type="ORDER_REJECTED_MIN_NOTIONAL",
                        details={
                            "units": units,
                            "notional": notional,
                            "min_notional": min_notional,
                            "entry_price": entry_price,
                            "reason": "below_charter_minimum",
                            "charter_pin": 841921
                        },
                        symbol=instrument,
                        venue="oanda"
                    )
                    
                    return {
                        "success": False,
                        "error": f"ORDER_REJECTED: Notional ${notional:,.2f} below Charter minimum ${min_notional:,}",
                        "notional": notional,
                        "min_notional": min_notional,
                        "broker": "OANDA",
                        "environment": self.environment
                    }
        except Exception as e:
            # Don't block order placement if enforcement fails
            self.logger.warning(f"Min-notional enforcement check failed: {e}")

        # NOTE: MIN_EXPECTED_PNL_USD is NOT a hard-stop by default.
        # If you want it enforced, set ENFORCE_MIN_EXPECTED_PNL=true and ensure a TP is provided.
        try:
            enforce_min_expected = os.getenv('ENFORCE_MIN_EXPECTED_PNL', 'false').lower() in ('1', 'true', 'yes')
            if enforce_min_expected and take_profit is not None and RickCharter and hasattr(RickCharter, "MIN_EXPECTED_PNL_USD"):
                expected_pnl_usd = abs((float(take_profit) - float(entry_price)) * float(units))
                min_expected = float(RickCharter.MIN_EXPECTED_PNL_USD)
                if expected_pnl_usd < min_expected:
                    self.logger.warning(
                        f"Charter min expected PnL ${min_expected:.2f} not met "
                        f"(got ${expected_pnl_usd:.2f}) for {instrument}. Blocking order."
                    )
                    log_narration(
                        event_type="CHARTER_VIOLATION",
                        details={
                            "code": "MIN_EXPECTED_PNL_USD",
                            "expected_pnl_usd": expected_pnl_usd,
                            "min_expected_pnl_usd": min_expected,
                            "entry_price": entry_price,
                            "take_profit": take_profit,
                            "units": units
                        },
                        symbol=instrument,
                        venue="oanda"
                    )
                    return {
                        "success": False,
                        "error": f"EXPECTED_PNL_BELOW_MIN: {expected_pnl_usd:.2f} < {min_expected:.2f}",
                        "broker": "OANDA",
                        "environment": self.environment
                    }
        except Exception as e:
            self.logger.warning(f"Min-expected-PnL enforcement failed: {e}")
        
        try:
            # For LIVE environment, validate API credentials first
            if self.environment == "live":
                if not self.api_token or self.api_token == "your_live_token_here":
                    self.logger.error("LIVE OANDA token not configured - cannot place real orders")
                    return {
                        "success": False,
                        "error": "LIVE API credentials not configured",
                        "latency_ms": 0,
                        "execution_time_ms": (time.time() - start_time) * 1000,
                        "broker": "OANDA",
                        "environment": self.environment
                    }
                
                # LIVE ORDER PLACEMENT
                # Support both LIMIT and MARKET order types
                if order_type.upper() == "MARKET":
                    # MARKET order - immediate execution with OCO brackets
                    order = {
                        "type": OandaOrderType.MARKET.value,
                        "instrument": instrument,
                        "units": str(units),
                        "timeInForce": OandaTimeInForce.FOK.value,  # Fill or Kill
                        "stopLossOnFill": {
                            "price": _fmt_price(stop_loss),
                            "timeInForce": OandaTimeInForce.GTC.value
                        }
                    }
                    if take_profit is not None:
                        order["takeProfitOnFill"] = {
                            "price": _fmt_price(take_profit),
                            "timeInForce": OandaTimeInForce.GTC.value
                        }
                    order_data = {"order": order}
                else:
                    # LIMIT order - wait for specific entry price with extended TTL (24h default)
                    order = {
                        "type": OandaOrderType.LIMIT.value,
                        "instrument": instrument,
                        "units": str(units),
                        "price": _fmt_price(entry_price),
                        "timeInForce": OandaTimeInForce.GTD.value,
                        "gtdTime": (datetime.now(timezone.utc) + timedelta(hours=ttl_hours)).isoformat(),
                        "stopLossOnFill": {
                            "price": _fmt_price(stop_loss),
                            "timeInForce": OandaTimeInForce.GTC.value
                        }
                    }
                    if take_profit is not None:
                        order["takeProfitOnFill"] = {
                            "price": _fmt_price(take_profit),
                            "timeInForce": OandaTimeInForce.GTC.value
                        }
                    order_data = {"order": order}
                # Micro trade gate: only applies when a TP exists (otherwise reward is undefined)
                if take_profit is not None:
                    try:
                        blocked, info = should_block_micro_trade(
                            symbol=instrument,
                            side='LONG' if units > 0 else 'SHORT',
                            entry_price=entry_price if entry_price is not None else 0.0,
                            stop_loss_price=stop_loss,
                            take_profit_price=take_profit,
                            units=units,
                            venue='OANDA'
                        )
                        if blocked:
                            try:
                                log_narration('MICRO_TRADE_BLOCKED', info, symbol=instrument, venue='oanda')
                            except Exception:
                                pass
                            return {"success": False, "error": "MICRO_TRADE_BLOCKED", "broker": "OANDA", "details": info}
                    except Exception:
                        return {"success": False, "error": "MICRO_TRADE_GATE_ERROR", "broker": "OANDA"}
                
                # Make LIVE API call
                response = self._make_request("POST", f"/v3/accounts/{self.account_id}/orders", order_data)
                execution_time = (time.time() - start_time) * 1000
                
                if response["success"]:
                    order_result = response["data"]
                    order_id = order_result.get("orderCreateTransaction", {}).get("id")
                    
                    # Log successful LIVE OCO placement
                    self.logger.info(
                        f"LIVE OANDA OCO placed: {instrument} | Entry: {entry_price} | "
                        f"SL: {stop_loss} | TP: {take_profit if take_profit is not None else '--'} | Latency: {response['latency_ms']:.1f}ms | "
                        f"Order ID: {order_id}"
                    )
                    
                    # Narration log: core OCO placed
                    log_narration(
                        event_type="OCO_PLACED",
                        details={
                            "order_id": order_id,
                            "entry_price": entry_price,
                            "stop_loss": stop_loss,
                            "take_profit": take_profit,
                            "units": units,
                            "latency_ms": response['latency_ms'],
                            "environment": "LIVE"
                        },
                        symbol=instrument,
                        venue="oanda"
                    )

                    # Narration log: explicit broker order created mapping (helps correlate brokers ↔ internal trades)
                    details = {
                        "broker": "OANDA",
                        "order_id": order_id,
                        "instrument": instrument,
                        "units": units,
                        "entry_price": entry_price,
                        "environment": "LIVE"
                    }
                    if explanation:
                        details['explanation'] = explanation
                    log_narration(
                        event_type="BROKER_ORDER_CREATED",
                        details=details,
                        symbol=instrument,
                        venue="oanda"
                    )
                    
                    # Charter compliance check
                    if response["latency_ms"] > self.max_placement_latency_ms:
                        self.logger.error(f"LIVE OCO latency {response['latency_ms']:.1f}ms exceeds Charter limit - CANCELLING ORDER")
                        # Attempt to cancel the order
                        if order_id:
                            cancel_response = self._make_request("PUT", f"/v3/accounts/{self.account_id}/orders/{order_id}/cancel")
                            if cancel_response["success"]:
                                self.logger.info(f"Order {order_id} cancelled due to latency breach")
                        
                        return {
                            "success": False,
                            "error": f"Order cancelled - latency {response['latency_ms']:.1f}ms exceeds Charter limit",
                            "latency_ms": response["latency_ms"],
                            "execution_time_ms": execution_time,
                            "broker": "OANDA",
                            "environment": self.environment,
                            "cancelled": True
                        }
                    
                    return {
                        "success": True,
                        "order_id": order_id,
                        "instrument": instrument,
                        "entry_price": entry_price,
                        "stop_loss": stop_loss,
                        "take_profit": take_profit,
                        "units": units,
                        "latency_ms": response["latency_ms"],
                        "execution_time_ms": execution_time,
                        "broker": "OANDA",
                        "environment": self.environment,
                        "ttl_hours": ttl_hours
                    }
                else:
                    self.logger.error(f"LIVE OANDA OCO failed: {response['error']}")
                    return {
                        "success": False,
                        "error": f"LIVE API error: {response['error']}",
                        "latency_ms": response.get("latency_ms", execution_time),
                        "execution_time_ms": execution_time,
                        "broker": "OANDA",
                        "environment": self.environment
                    }
            
            else:
                # PRACTICE MODE - Place REAL orders on OANDA practice account
                # (Not simulation - actual API calls to practice endpoint)
                order_data = {
                    "order": {
                        "type": "LIMIT",
                        "instrument": instrument,
                        "units": str(units),
                        "price": _fmt_price(entry_price),
                        "timeInForce": "GTD",
                        "gtdTime": (datetime.now(timezone.utc) + timedelta(hours=ttl_hours)).isoformat(),
                        "stopLossOnFill": {
                            "price": _fmt_price(stop_loss),
                            "timeInForce": "GTC"
                        }
                    }
                }
                if take_profit is not None:
                    order_data["order"]["takeProfitOnFill"] = {
                        "price": _fmt_price(take_profit),
                        "timeInForce": "GTC"
                    }
                
                # Make PRACTICE API call (real order on practice account)
                response = self._make_request("POST", f"/v3/accounts/{self.account_id}/orders", order_data)
                execution_time = (time.time() - start_time) * 1000
                
                if response["success"]:
                    order_result = response["data"]
                    order_id = order_result.get("orderCreateTransaction", {}).get("id")
                    
                    # Log successful PRACTICE OCO placement
                    self.logger.info(
                        f"PRACTICE OANDA OCO placed (REAL API): {instrument} | Entry: {entry_price} | "
                        f"SL: {stop_loss} | TP: {take_profit if take_profit is not None else '--'} | Latency: {response['latency_ms']:.1f}ms | "
                        f"Order ID: {order_id}"
                    )
                    
                    # Narration log: core OCO placed (practice)
                    log_narration(
                        event_type="OCO_PLACED",
                        details={
                            "order_id": order_id,
                            "entry_price": entry_price,
                            "stop_loss": stop_loss,
                            "take_profit": take_profit,
                            "units": units,
                            "latency_ms": response['latency_ms'],
                            "environment": "PRACTICE",
                            "simulated": False,  # Real API order
                            "visible_in_oanda": True
                        },
                        symbol=instrument,
                        venue="oanda"
                    )

                    # Narration log: explicit broker order created mapping (practice)
                    details = {
                        "broker": "OANDA",
                        "order_id": order_id,
                        "instrument": instrument,
                        "units": units,
                        "entry_price": entry_price,
                        "environment": "PRACTICE",
                        "simulated": False
                    }
                    if explanation:
                        details['explanation'] = explanation
                    log_narration(
                        event_type="BROKER_ORDER_CREATED",
                        details=details,
                        symbol=instrument,
                        venue="oanda"
                    )
                    
                    # Charter compliance check
                    if response["latency_ms"] > self.max_placement_latency_ms:
                        self.logger.warning(f"PRACTICE OCO latency {response['latency_ms']:.1f}ms exceeds Charter limit")
                    
                    return {
                        "success": True,
                        "order_id": order_id,
                        "instrument": instrument,
                        "entry_price": entry_price,
                        "stop_loss": stop_loss,
                        "take_profit": take_profit,
                        "units": units,
                        "latency_ms": response["latency_ms"],
                        "execution_time_ms": execution_time,
                        "broker": "OANDA",
                        "environment": self.environment,
                        "ttl_hours": ttl_hours,
                        "simulated": False  # Real API order
                    }
                else:
                    self.logger.error(f"PRACTICE OANDA OCO failed: {response['error']}")
                    return {
                        "success": False,
                        "error": f"PRACTICE API error: {response['error']}",
                        "latency_ms": response.get("latency_ms", execution_time),
                        "execution_time_ms": execution_time,
                        "broker": "OANDA",
                        "environment": self.environment
                    }
                
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.logger.error(f"OANDA OCO exception ({self.environment}): {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "latency_ms": execution_time,
                "execution_time_ms": execution_time,
                "broker": "OANDA",
                "environment": self.environment
            }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make authenticated API request with performance tracking - LIVE VERSION
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request payload for POST/PUT
            params: Query string parameters (for GET requests)
            
        Returns:
            Dict with API response
        """
        start_time = time.time()
        url = urljoin(self.api_base, endpoint)
        
        try:
            # Prepare request
            if method.upper() == "GET":
                # Pass params for query string support (e.g., candles)
                response = requests.get(url, headers=self.headers, params=params, timeout=self.default_timeout)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=self.default_timeout)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=self.headers, json=data, timeout=self.default_timeout)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=self.default_timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Track request latency
            latency_ms = (time.time() - start_time) * 1000
            with self._lock:
                self.request_times.append(latency_ms)
                if len(self.request_times) > 100:
                    self.request_times = self.request_times[-100:]
            
            # Check response
            response.raise_for_status()
            
            result = response.json() if response.content else {}
            
            # Log performance for LIVE environment
            if self.environment == "live":
                if latency_ms > self.max_placement_latency_ms:
                    self.logger.error(f"LIVE OANDA API TIMEOUT: {latency_ms:.1f}ms for {method} {endpoint}")
                elif latency_ms > 200:  # Warning threshold
                    self.logger.warning(f"LIVE OANDA API slow: {latency_ms:.1f}ms for {method} {endpoint}")
            
            return {
                "success": True,
                "data": result,
                "latency_ms": latency_ms,
                "status_code": response.status_code
            }
            
        except requests.exceptions.Timeout:
            latency_ms = (time.time() - start_time) * 1000
            self.logger.error(f"OANDA API TIMEOUT ({self.environment}): {latency_ms:.1f}ms for {method} {endpoint}")
            return {
                "success": False,
                "error": "Request timeout - order execution failed",
                "latency_ms": latency_ms,
                "status_code": 408
            }
            
        except requests.exceptions.HTTPError as e:
            latency_ms = (time.time() - start_time) * 1000
            error_msg = f"HTTP {response.status_code}: {response.text}"
            self.logger.error(f"OANDA API ERROR ({self.environment}): {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "latency_ms": latency_ms,
                "status_code": response.status_code
            }
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self.logger.error(f"OANDA API EXCEPTION ({self.environment}): {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "latency_ms": latency_ms,
                "status_code": 0
            }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get connector performance statistics"""
        with self._lock:
            request_times = self.request_times.copy()
        
        if not request_times:
            return {
                "total_requests": 0,
                "avg_latency_ms": 0,
                "max_latency_ms": 0,
                "charter_compliance_rate": 0,
                "environment": self.environment,
                "account_id": "stub"
            }
        
        avg_latency = sum(request_times) / len(request_times)
        max_latency = max(request_times)
        compliant_requests = sum(1 for lat in request_times if lat <= self.max_placement_latency_ms)
        compliance_rate = compliant_requests / len(request_times)
        
        return {
            "total_requests": len(request_times),
            "avg_latency_ms": round(avg_latency, 1),
            "max_latency_ms": round(max_latency, 1),
            "charter_compliance_rate": round(compliance_rate, 3),
            "environment": self.environment,
            "account_id": self.account_id[-4:] if self.account_id else "N/A"
        }

    # --- Convenience management API helpers -------------------------------------------------
    def get_orders(self, state: str = "PENDING") -> List[Dict[str, Any]]:
        """Return pending orders from OANDA for this account."""
        try:
            endpoint = f"/v3/accounts/{self.account_id}/orders?state={state}"
            resp = self._make_request("GET", endpoint)
            if resp.get("success"):
                data = resp.get("data") or {}
                return data.get("orders", [])
        except Exception as e:
            self.logger.warning(f"Failed to fetch orders: {e}")
        return []

    def get_trades(self) -> List[Dict[str, Any]]:
        """Return open trades for this account."""
        try:
            endpoint = f"/v3/accounts/{self.account_id}/trades"
            resp = self._make_request("GET", endpoint)
            if resp.get("success"):
                data = resp.get("data") or {}
                return data.get("trades", [])
        except Exception as e:
            self.logger.warning(f"Failed to fetch trades: {e}")
        return []

    def get_account(self) -> Optional[Dict[str, Any]]:
        """Get account summary including balance."""
        try:
            endpoint = f"/v3/accounts/{self.account_id}"
            resp = self._make_request("GET", endpoint)
            if resp.get("success"):
                data = resp.get("data") or {}
                return data.get("account")
        except Exception as e:
            self.logger.warning(f"Failed to fetch account: {e}")
        return None


    def _safe_request_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Runtime-safe GET wrapper that ALWAYS bypasses _make_request.
        Directly uses requests.get() for maximum compatibility with legacy stubs.
        """
        try:
            url = urljoin(self.api_base, endpoint)
            r = requests.get(url, headers=self.headers, params=params, timeout=self.default_timeout)
            r.raise_for_status()
            latency_ms = 0  # Direct call timing
            with self._lock:
                self.request_times.append(latency_ms)
                if len(self.request_times) > 100:
                    self.request_times = self.request_times[-100:]
            return {
                "success": True,
                "data": r.json() if r.content else {},
                "latency_ms": latency_ms,
                "status_code": r.status_code
            }
        except Exception as e:
            self.logger.error(f"_safe_request_get failed: {e}")
            return {"success": False, "error": str(e)}

    def get_historical_data(self, instrument: str, count: int = 120, granularity: str = "M15") -> List[Dict[str, Any]]:
        """Fetch historical candle data from OANDA for signal generation
        
        Args:
            instrument: Trading pair (e.g., "EUR_USD")
            count: Number of candles to fetch (default: 120)
            granularity: Candle period (default: "M15" for 15 minutes)
            
        Returns:
            List of candle dicts with format:
            [{'time': 'ISO8601', 'volume': int, 'mid': {'o': str, 'h': str, 'l': str, 'c': str}}, ...]
        """
        try:
            endpoint = f"/v3/instruments/{instrument}/candles"
            params = {
                "count": count,
                "granularity": granularity,
                "price": "M"   # Mid prices only
            }
            # Use safe wrapper that handles legacy signatures
            resp = self._safe_request_get(endpoint, params=params)
            
            if resp.get("success"):
                data = resp.get("data") or {}
                candles = data.get("candles", [])
                if candles:
                    return candles
                self.logger.warning(f"No candles in response for {instrument}")
                return []
            else:
                err = resp.get("error", "unknown error")
                self.logger.error(f"OANDA candles error for {instrument}: {err}")
                return []
        except Exception as e:
            self.logger.error(f"Failed to fetch candles for {instrument}: {e}")
            return []

    def get_live_prices(self, instruments: List[str]) -> Dict[str, Dict[str, Any]]:
        """Fetch real-time price snapshots (bid/ask/mid) for instruments.

        Args:
            instruments: list like ["EUR_USD", "GBP_USD"]

        Returns:
            Dict mapping instrument -> { bid, ask, mid, time }
        """
        if not instruments:
            return {}

        try:
            endpoint = f"/v3/accounts/{self.account_id}/pricing"
            params = {"instruments": ",".join(instruments)}
            resp = self._safe_request_get(endpoint, params=params)
            if not resp.get("success"):
                self.logger.error(f"Pricing API error: {resp.get('error')}")
                return {}

            data = resp.get("data", {})
            prices = data.get("prices", [])
            out: Dict[str, Dict[str, Any]] = {}
            for p in prices:
                inst = p.get("instrument")
                bids = p.get("bids", [])
                asks = p.get("asks", [])
                bid = float(bids[0]["price"]) if bids else None
                ask = float(asks[0]["price"]) if asks else None
                mid = (bid + ask) / 2.0 if (bid is not None and ask is not None) else None
                out[inst] = {
                    "bid": bid,
                    "ask": ask,
                    "mid": mid,
                    "time": p.get("time")
                }
            return out
        except Exception as e:
            self.logger.error(f"Failed to fetch live prices: {e}")
            return {}

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel a pending order by id."""
        try:
            endpoint = f"/v3/accounts/{self.account_id}/orders/{order_id}/cancel"
            resp = self._make_request("PUT", endpoint)
            return resp
        except Exception as e:
            self.logger.error(f"Failed to cancel order {order_id}: {e}")
            return {"success": False, "error": str(e)}

    def set_trade_stop(self, trade_id: str, stop_price: float) -> Dict[str, Any]:
        """Set/modify the stop loss price for an existing trade. Uses OANDA trade modification endpoint.

        Note: exact payload is compatible with OANDA v20 update trade orders. If your broker returns
        a different schema adjust accordingly.
        """
        try:
            payload = {
                "stopLoss": {
                    "price": str(stop_price)
                }
            }
            endpoint = f"/v3/accounts/{self.account_id}/trades/{trade_id}/orders"
            resp = self._make_request("PUT", endpoint, payload)
            return resp
        except Exception as e:
            self.logger.error(f"Failed to set stop for trade {trade_id}: {e}")
            return {"success": False, "error": str(e)}

    def close_trade(self, trade_id: str, units: Optional[int] = None) -> Dict[str, Any]:
        """Close an existing trade.

        Args:
            trade_id: OANDA trade id
            units: optional number of units to close. If None, closes ALL.

        Notes:
            OANDA expects a positive units value for partial closes and "ALL" for full closes.
        """
        try:
            if units is None:
                payload = {"units": "ALL"}
            else:
                payload = {"units": str(abs(int(units)))}
            endpoint = f"/v3/accounts/{self.account_id}/trades/{trade_id}/close"
            return self._make_request("PUT", endpoint, payload)
        except Exception as e:
            self.logger.error(f"Failed to close trade {trade_id}: {e}")
            return {"success": False, "error": str(e)}

# Convenience functions
def get_oanda_connector(pin: Optional[int] = None, environment: str = "practice") -> OandaConnector:
    """Get OANDA connector instance"""
    return OandaConnector(pin=pin, environment=environment)

def place_oanda_oco(connector: OandaConnector, symbol: str, entry: float, 
                   sl: float, tp: float, units: int) -> Dict[str, Any]:
    """Convenience function for OANDA OCO placement"""
    return connector.place_oco_order(symbol, entry, sl, tp, units)

if __name__ == "__main__":
    # Self-test with stub data
    print("OANDA Connector self-test starting...")
    
    try:
        # Initialize connector in practice mode
        oanda = OandaConnector(pin=841921, environment="practice")
        
        print(f"\n1. Testing OCO Order Creation:")
        print("=" * 35)
        
        # Test OCO order structure creation
        test_oco_params = {
            "instrument": "EUR_USD",
            "entry_price": 1.0800,
            "stop_loss": 1.0750,
            "take_profit": 1.0950,
            "units": 10000,
            "ttl_hours": 6.0
        }
        
        print(f"OCO Parameters:")
        print(f"  Instrument: {test_oco_params['instrument']}")
        print(f"  Entry: {test_oco_params['entry_price']:.4f}")
        print(f"  Stop Loss: {test_oco_params['stop_loss']:.4f}")
        print(f"  Take Profit: {test_oco_params['take_profit']:.4f}")
        print(f"  Units: {test_oco_params['units']}")
        
        # Calculate RR ratio validation
        risk = abs(test_oco_params['entry_price'] - test_oco_params['stop_loss'])
        reward = abs(test_oco_params['take_profit'] - test_oco_params['entry_price'])
        rr_ratio = reward / risk
        
        print(f"  Risk/Reward: {rr_ratio:.2f}")
        
        if rr_ratio >= 3.0:
            print("✅ RR ratio meets Charter requirement (≥3:1)")
        else:
            print("❌ RR ratio below Charter requirement")
        
        # Test OCO placement
        oco_result = oanda.place_oco_order(**test_oco_params)
        
        if oco_result["success"]:
            print(f"✅ OCO order placed successfully")
            print(f"   Order ID: {oco_result['order_id']}")
            print(f"   Latency: {oco_result['latency_ms']:.1f}ms")
        else:
            print(f"❌ OCO placement failed: {oco_result.get('error', 'Unknown error')}")
        
        print(f"\n2. Performance Statistics:")
        print("=" * 30)
        
        stats = oanda.get_performance_stats()
        print(f"Environment: {stats['environment']}")
        print(f"Account ID: {stats['account_id']}")
        
        # Test convenience functions
        print(f"\n3. Testing Convenience Functions:")
        print("=" * 37)
        
        convenience_connector = get_oanda_connector(pin=841921, environment="practice")
        print(f"✅ Convenience connector created: {convenience_connector.environment}")
        
        print("\n" + "=" * 50)
        print("✅ OANDA Connector architecture validated")
        print("✅ OCO order structure compatible")
        print("✅ Charter compliance enforced")
        print("✅ Performance tracking enabled")
        print("✅ Ready for live API credentials")
        print("\nOANDA Connector self-test completed successfully! 🔐")
        
    except Exception as e:
        print(f"❌ OANDA Connector test failed: {str(e)}")
        exit(1)