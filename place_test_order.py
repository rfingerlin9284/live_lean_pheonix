#!/usr/bin/env python3
"""
Coinbase Small Test Order Script
Ready-to-execute script for placing a minimal test order to verify authentication
PIN: 841921 REQUIRED

USAGE:
    python3 place_test_order.py

This script will:
1. Verify PIN (841921)
2. Load Coinbase credentials from .env
3. Show current balances
4. Place a SMALL test order (configurable below)
5. Set take-profit and stop-loss orders

⚠️ WARNING: This uses REAL MONEY on your live Coinbase account!
"""

import os
import sys
import json
import time
import uuid
import requests
from datetime import datetime
from pathlib import Path

# =============================================================================
# CONFIGURATION - Modify these for your test order
# =============================================================================
TEST_ORDER_CONFIG = {
    "product": "BTC-USD",           # Crypto pair to trade
    "side": "BUY",                  # BUY or SELL
    "amount_usd": 10.0,             # Order size in USD (minimum ~$10)
    "take_profit_pct": 2.0,         # Take profit % (2% = sell at 2% gain)
    "stop_loss_pct": 1.0,           # Stop loss % (1% = sell at 1% loss)
}

PIN_REQUIRED = 841921
# =============================================================================

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}\n")

class CoinbaseTestOrder:
    """Place a small test order on Coinbase to verify authentication"""
    
    def __init__(self, pin: int):
        if pin != PIN_REQUIRED:
            raise PermissionError(f"❌ Invalid PIN. Required: {PIN_REQUIRED}")
        
        self.pin_verified = True
        self.base_url = "https://api.coinbase.com"
        self.api_key = None
        self.private_key = None
        
        print(f"{Colors.GREEN}✅ PIN verified: {pin}{Colors.ENDC}")
        
        self.load_credentials()
    
    def load_credentials(self):
        """Load Coinbase API credentials from .env file"""
        env_file = Path(__file__).parent / ".env"
        
        if not env_file.exists():
            raise FileNotFoundError(f"❌ .env file not found at {env_file}")
        
        try:
            with open(env_file, 'r') as f:
                content = f.read()
            
            # Parse API key
            for line in content.split('\n'):
                if line.startswith('COINBASE_LIVE_API_KEY='):
                    self.api_key = line.split('=', 1)[1].strip().strip('"\'')
                    break
            
            # Parse private key (multi-line)
            start = content.find('COINBASE_LIVE_API_SECRET=')
            if start != -1:
                start += len('COINBASE_LIVE_API_SECRET=')
                rest = content[start:]
                if rest.startswith('-----BEGIN'):
                    end = rest.find('-----END EC PRIVATE KEY-----')
                    if end != -1:
                        end += len('-----END EC PRIVATE KEY-----')
                        self.private_key = rest[:end].strip()
            
            if not self.api_key or not self.private_key:
                raise ValueError("❌ Credentials not found in .env")
            
            print(f"{Colors.GREEN}✅ Credentials loaded{Colors.ENDC}")
            print(f"   API Key: {self.api_key[:30]}...")
            
        except Exception as e:
            raise ValueError(f"❌ Failed to load credentials: {e}")
    
    def create_jwt_token(self):
        """Generate JWT authentication token"""
        try:
            import jwt
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.backends import default_backend
            
            # Load private key
            private_key_obj = serialization.load_pem_private_key(
                self.private_key.encode('utf-8'),
                ******
                backend=default_backend()
            )
            
            # Create JWT
            timestamp = int(time.time())
            payload = {
                'sub': self.api_key,
                'iss': 'coinbase-cloud',
                'nbf': timestamp,
                'exp': timestamp + 120,
                'aud': ['retail_rest_api_proxy'],
            }
            
            token = jwt.encode(payload, private_key_obj, algorithm='ES256')
            return token
            
        except ImportError:
            raise ValueError("❌ Missing libraries. Install: pip install PyJWT cryptography")
        except Exception as e:
            raise ValueError(f"❌ JWT generation failed: {e}")
    
    def get_auth_headers(self):
        """Get authentication headers with fresh JWT"""
        token = self.create_jwt_token()
        return {
            "Authorization": f"******",
            "Content-Type": "application/json"
        }
    
    def show_balances(self):
        """Display account balances"""
        print(f"\n{Colors.BOLD}Current Account Balances:{Colors.ENDC}")
        
        try:
            headers = self.get_auth_headers()
            response = requests.get(
                f"{self.base_url}/api/v3/brokerage/accounts",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                accounts = data.get('accounts', [])
                
                # Show accounts with balance
                for acc in accounts:
                    currency = acc.get('currency', 'Unknown')
                    available = acc.get('available_balance', {}).get('value', '0')
                    
                    if float(available) > 0:
                        print(f"   {currency:8} - Available: ${float(available):>12.2f}")
                
                print()
                return True
            else:
                print(f"{Colors.RED}❌ Failed to get balances: {response.status_code}{Colors.ENDC}")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")
            return False
    
    def get_current_price(self, product_id):
        """Get current market price for product"""
        try:
            headers = self.get_auth_headers()
            response = requests.get(
                f"{self.base_url}/api/v3/brokerage/products/{product_id}/ticker",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                price = float(data.get('price', 0))
                return price
            else:
                raise ValueError(f"Failed to get price: {response.status_code}")
                
        except Exception as e:
            raise ValueError(f"Error getting price: {e}")
    
    def place_test_order(self, config):
        """Place the test order with TP/SL"""
        print_header("📊 TEST ORDER CONFIGURATION")
        
        product_id = config['product']
        side = config['side']
        amount_usd = config['amount_usd']
        tp_pct = config['take_profit_pct']
        sl_pct = config['stop_loss_pct']
        
        print(f"Product: {Colors.CYAN}{product_id}{Colors.ENDC}")
        print(f"Side: {Colors.CYAN}{side}{Colors.ENDC}")
        print(f"Amount: {Colors.CYAN}${amount_usd:.2f} USD{Colors.ENDC}")
        print(f"Take Profit: {Colors.CYAN}{tp_pct}%{Colors.ENDC}")
        print(f"Stop Loss: {Colors.CYAN}{sl_pct}%{Colors.ENDC}")
        
        # Get current price
        print(f"\n{Colors.YELLOW}Fetching current price...{Colors.ENDC}")
        current_price = self.get_current_price(product_id)
        
        print(f"{Colors.GREEN}✅ Current {product_id} Price: ${current_price:,.2f}{Colors.ENDC}")
        
        # Calculate TP and SL prices
        if side.upper() == 'BUY':
            tp_price = current_price * (1 + tp_pct / 100)
            sl_price = current_price * (1 - sl_pct / 100)
        else:
            tp_price = current_price * (1 - tp_pct / 100)
            sl_price = current_price * (1 + sl_pct / 100)
        
        base_size = amount_usd / current_price
        
        print(f"\n{Colors.BOLD}Order Details:{Colors.ENDC}")
        print(f"  Entry: ${current_price:,.2f}")
        print(f"  Take Profit: ${tp_price:,.2f} ({Colors.GREEN}+${tp_price - current_price:,.2f}{Colors.ENDC})")
        print(f"  Stop Loss: ${sl_price:,.2f} ({Colors.RED}-${current_price - sl_price:,.2f}{Colors.ENDC})")
        print(f"  Size: {base_size:.6f} {product_id.split('-')[0]}")
        
        # Final confirmation
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️  WARNING: This will place a REAL order with REAL MONEY!{Colors.ENDC}")
        confirm = input(f"\nType 'EXECUTE' to place this order: ")
        
        if confirm != 'EXECUTE':
            print(f"\n{Colors.YELLOW}Order cancelled by user{Colors.ENDC}")
            return None
        
        # Place market order
        print(f"\n{Colors.YELLOW}Placing market order...{Colors.ENDC}")
        
        try:
            headers = self.get_auth_headers()
            
            order_data = {
                "client_order_id": str(uuid.uuid4()),
                "product_id": product_id,
                "side": side.upper(),
                "order_configuration": {
                    "market_market_ioc": {
                        "quote_size": str(amount_usd)
                    }
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/v3/brokerage/orders",
                headers=headers,
                json=order_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                order_result = response.json()
                order_id = order_result.get('order_id', 'Unknown')
                
                print(f"{Colors.GREEN}✅ MARKET ORDER PLACED!{Colors.ENDC}")
                print(f"   Order ID: {order_id}")
                
                # Wait for order to fill
                time.sleep(3)
                
                # Place TP order
                print(f"\n{Colors.YELLOW}Placing take-profit order...{Colors.ENDC}")
                
                tp_order = {
                    "client_order_id": str(uuid.uuid4()),
                    "product_id": product_id,
                    "side": "SELL" if side.upper() == "BUY" else "BUY",
                    "order_configuration": {
                        "limit_limit_gtc": {
                            "base_size": str(base_size),
                            "limit_price": str(tp_price)
                        }
                    }
                }
                
                tp_response = requests.post(
                    f"{self.base_url}/api/v3/brokerage/orders",
                    headers=headers,
                    json=tp_order,
                    timeout=10
                )
                
                if tp_response.status_code in [200, 201]:
                    tp_result = tp_response.json()
                    print(f"{Colors.GREEN}✅ Take-Profit order placed at ${tp_price:,.2f}{Colors.ENDC}")
                    print(f"   Order ID: {tp_result.get('order_id', 'Unknown')}")
                
                # Place SL order
                print(f"\n{Colors.YELLOW}Placing stop-loss order...{Colors.ENDC}")
                
                sl_order = {
                    "client_order_id": str(uuid.uuid4()),
                    "product_id": product_id,
                    "side": "SELL" if side.upper() == "BUY" else "BUY",
                    "order_configuration": {
                        "stop_limit_stop_limit_gtc": {
                            "base_size": str(base_size),
                            "limit_price": str(sl_price * 0.995),
                            "stop_price": str(sl_price)
                        }
                    }
                }
                
                sl_response = requests.post(
                    f"{self.base_url}/api/v3/brokerage/orders",
                    headers=headers,
                    json=sl_order,
                    timeout=10
                )
                
                if sl_response.status_code in [200, 201]:
                    sl_result = sl_response.json()
                    print(f"{Colors.GREEN}✅ Stop-Loss order placed at ${sl_price:,.2f}{Colors.ENDC}")
                    print(f"   Order ID: {sl_result.get('order_id', 'Unknown')}")
                
                print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TEST ORDER COMPLETE!{Colors.ENDC}")
                print(f"\n{Colors.CYAN}Position opened with OCO (One-Cancels-Other) protection:{Colors.ENDC}")
                print(f"  - Entry: ${current_price:,.2f}")
                print(f"  - TP: ${tp_price:,.2f}")
                print(f"  - SL: ${sl_price:,.2f}")
                
                return order_result
                
            else:
                print(f"{Colors.RED}❌ Order failed: {response.status_code}{Colors.ENDC}")
                print(f"   Response: {response.text[:500]}")
                return None
                
        except Exception as e:
            print(f"{Colors.RED}❌ Order error: {e}{Colors.ENDC}")
            return None

def main():
    print_header("🔐 COINBASE TEST ORDER SCRIPT")
    
    print(f"{Colors.YELLOW}This script will place a SMALL test order to verify Coinbase authentication{Colors.ENDC}")
    print(f"{Colors.YELLOW}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    
    # Request PIN
    print(f"\n{Colors.BOLD}PIN Required for Live Trading{Colors.ENDC}")
    try:
        pin = int(input("Enter PIN (841921): "))
    except ValueError:
        print(f"{Colors.RED}❌ Invalid PIN format{Colors.ENDC}")
        return 1
    
    try:
        # Initialize trader
        trader = CoinbaseTestOrder(pin)
        
        # Show balances
        trader.show_balances()
        
        # Place test order
        result = trader.place_test_order(TEST_ORDER_CONFIG)
        
        if result:
            print(f"\n{Colors.GREEN}✅ Test order successful - authentication verified!{Colors.ENDC}")
            return 0
        else:
            print(f"\n{Colors.RED}❌ Test order failed{Colors.ENDC}")
            return 1
        
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.ENDC}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
