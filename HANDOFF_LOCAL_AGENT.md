# HANDOFF TO LOCAL AGENT - Coinbase Test Order

## 📋 Summary
This handoff provides a ready-to-execute script for placing a small Coinbase test order to verify authentication and trading capabilities.

---

## 🎯 Objective
Place a small live test order ($10 BTC) to confirm:
1. Coinbase API authentication works
2. Order placement is functional
3. OCO (Take-Profit + Stop-Loss) orders work
4. System is ready for production trading

---

## 📁 Files Created

### 1. `place_test_order.py`
**Purpose**: Execute a small test trade on Coinbase
**Location**: `/home/runner/work/live_lean_pheonix/live_lean_pheonix/place_test_order.py`

**Features**:
- ✅ PIN-protected (requires 841921)
- ✅ Configurable test order parameters
- ✅ Shows account balances before trading
- ✅ Fetches current market price
- ✅ Calculates TP/SL automatically
- ✅ Requires "EXECUTE" confirmation
- ✅ Places market order + OCO orders
- ✅ Full error handling

---

## ⚙️ Configuration

Edit the `TEST_ORDER_CONFIG` section in `place_test_order.py`:

```python
TEST_ORDER_CONFIG = {
    "product": "BTC-USD",           # Change to ETH-USD, SOL-USD, etc.
    "side": "BUY",                  # or "SELL"
    "amount_usd": 10.0,             # Minimum ~$10
    "take_profit_pct": 2.0,         # Take profit at 2% gain
    "stop_loss_pct": 1.0,           # Stop loss at 1% loss
}
```

---

## 🚀 Execution Instructions

### Prerequisites
1. **Internet connection** (to reach api.coinbase.com)
2. **Valid .env file** with Coinbase credentials:
   ```
   COINBASE_LIVE_API_KEY=organizations/.../apiKeys/...
   COINBASE_LIVE_API_SECRET=-----BEGIN EC PRIVATE KEY-----
   ...
   -----END EC PRIVATE KEY-----
   ```
3. **Python libraries**:
   ```bash
   pip install PyJWT cryptography requests
   ```

### Steps to Execute

1. **Navigate to repository**:
   ```bash
   cd /path/to/live_lean_pheonix
   ```

2. **Run the script**:
   ```bash
   python3 place_test_order.py
   ```

3. **Follow prompts**:
   - Enter PIN: `841921`
   - Review order details (price, TP, SL)
   - Type `EXECUTE` to confirm
   - Wait for confirmation

### Expected Output

```
================================================================================
                    🔐 COINBASE TEST ORDER SCRIPT                    
================================================================================

✅ PIN verified: 841921
✅ Credentials loaded
   API Key: organizations/5ae72c85-48da-48...

Current Account Balances:
   USD      - Available: $      1000.00
   BTC      - Available: $         0.00

================================================================================
                     📊 TEST ORDER CONFIGURATION                     
================================================================================

Product: BTC-USD
Side: BUY
Amount: $10.00 USD
Take Profit: 2.0%
Stop Loss: 1.0%

Fetching current price...
✅ Current BTC-USD Price: $42,350.00

Order Details:
  Entry: $42,350.00
  Take Profit: $43,197.00 (+$847.00)
  Stop Loss: $41,926.50 (-$423.50)
  Size: 0.000236 BTC

⚠️  WARNING: This will place a REAL order with REAL MONEY!

Type 'EXECUTE' to place this order: EXECUTE

Placing market order...
✅ MARKET ORDER PLACED!
   Order ID: abc123-def456-...

Placing take-profit order...
✅ Take-Profit order placed at $43,197.00
   Order ID: xyz789-...

Placing stop-loss order...
✅ Stop-Loss order placed at $41,926.50
   Order ID: qwe456-...

🎉 TEST ORDER COMPLETE!

Position opened with OCO (One-Cancels-Other) protection:
  - Entry: $42,350.00
  - TP: $43,197.00
  - SL: $41,926.50

✅ Test order successful - authentication verified!
```

---

## 🔐 Security Notes

**PIN Protection**: Script requires PIN 841921 to execute
**Confirmation Required**: Must type "EXECUTE" to proceed
**Amount Configurable**: Default is $10 USD (minimum safe amount)
**Stop Loss Included**: Automatically sets protective stop-loss
**Take Profit Included**: Automatically sets profit target

---

## 🛠️ Customization Options

### Change Product
```python
"product": "ETH-USD",  # Ethereum instead of Bitcoin
```

### Adjust Order Size
```python
"amount_usd": 20.0,  # $20 instead of $10
```

### Modify Risk/Reward
```python
"take_profit_pct": 3.0,  # 3% TP instead of 2%
"stop_loss_pct": 0.5,    # 0.5% SL instead of 1%
```

---

## ⚠️ Important Warnings

1. **Real Money**: This uses your actual Coinbase account with real funds
2. **Market Orders**: Fills at current market price (slight slippage possible)
3. **Fees Apply**: Coinbase charges trading fees (~0.6%)
4. **Minimum Size**: Each crypto has minimum order sizes:
   - BTC-USD: ~$10
   - ETH-USD: ~$10
   - SOL-USD: ~$5
5. **Network Required**: Must have internet access to api.coinbase.com

---

## 🔍 Verification Steps

After execution:

1. **Check Coinbase App/Web**:
   - Login to coinbase.com
   - View "Portfolio" → Check new position
   - View "Orders" → Verify TP and SL orders

2. **Check narration.jsonl**:
   ```bash
   tail -20 narration.jsonl
   ```
   Should show order events

3. **Verify in Trading Engine**:
   - Start Coinbase engine
   - Check for position in monitoring terminal

---

## 🐛 Troubleshooting

### "Invalid PIN"
- Ensure you enter exactly `841921`

### "Credentials not found"
- Check .env file exists
- Verify COINBASE_LIVE_API_KEY is set
- Verify COINBASE_LIVE_API_SECRET has full private key

### "Failed to get price"
- Check internet connection
- Verify api.coinbase.com is accessible
- Try different product (ETH-USD, SOL-USD)

### "Order failed: 400"
- Order size too small (increase amount_usd)
- Product not available (check Coinbase for valid pairs)
- Insufficient balance (add funds to account)

### "Missing libraries"
- Run: `pip install PyJWT cryptography requests`

---

## 📊 Next Steps After Successful Test

1. **Verify Order Filled**:
   - Check Coinbase portfolio
   - Confirm TP and SL orders are active

2. **Monitor Position**:
   - Use VSCode task: "🎯 Start Two Persistent Terminals"
   - Watch narration feed for updates

3. **Start Live Trading**:
   - Use VSCode task: "💰 Coinbase Trading Engine (Safe Mode)" first
   - After validation, switch to "🔴 Coinbase Trading Engine (LIVE)"

4. **Enable OANDA** (optional):
   - Run both engines simultaneously (crypto + forex)
   - Shared monitoring terminals show both

---

## 📝 Test Order Checklist

- [ ] Script created (`place_test_order.py`)
- [ ] Configuration reviewed and adjusted
- [ ] .env file verified with credentials
- [ ] Libraries installed (PyJWT, cryptography, requests)
- [ ] Internet connection confirmed
- [ ] Sufficient balance in Coinbase account
- [ ] PIN ready (841921)
- [ ] User understands this uses real money
- [ ] Execute script on local machine
- [ ] Confirm order placement
- [ ] Verify TP/SL orders set
- [ ] Check position in Coinbase
- [ ] Ready for full trading system

---

## 💡 Script Highlights

**Safety Features**:
- Requires PIN entry
- Shows all details before execution
- Requires explicit "EXECUTE" confirmation
- Sets protective stop-loss automatically
- Error handling throughout

**Transparency**:
- Shows current balances
- Displays market price
- Calculates TP/SL levels
- Shows exact order size
- Reports all order IDs

**Completeness**:
- Places market entry order
- Places take-profit limit order
- Places stop-loss order
- OCO configuration (one cancels other)
- Full order lifecycle

---

## 🎓 What This Proves

✅ **Authentication**: Coinbase API credentials are valid and working
✅ **Connectivity**: Can reach Coinbase servers successfully  
✅ **Order Placement**: Can execute market orders
✅ **Risk Management**: Can set TP and SL orders
✅ **Production Ready**: System is ready for live trading

---

**Status**: Ready for local execution
**Created**: 2025-12-04
**PIN**: 841921
**Risk Level**: Low ($10 minimum test)
**Approval**: Granted by user

---

## 🤝 Handoff Complete

The script is configured and ready. Execute on your local machine with internet access to verify Coinbase trading is fully functional.

**Good luck!** 🚀
