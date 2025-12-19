#!/bin/bash
# Enhanced Wolfpack EdgePack Verification Script
# Verifies all anti-churn and edge-preserving features are active

echo "======================================================================="
echo "  WOLFPACK EDGEPACK - ENHANCED VERIFICATION"
echo "======================================================================="
echo ""

PROJECT_ROOT="/home/runner/work/live_lean_pheonix/live_lean_pheonix"
PASS_COUNT=0
FAIL_COUNT=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check and report
check_feature() {
    local feature_name="$1"
    local check_command="$2"
    local expected="$3"
    
    result=$(eval "$check_command")
    
    if [[ "$result" == "$expected" ]] || [[ "$result" =~ "$expected" ]]; then
        echo -e "${GREEN}✅ PASS${NC}: $feature_name"
        ((PASS_COUNT++))
    else
        echo -e "${RED}❌ FAIL${NC}: $feature_name (expected: $expected, got: $result)"
        ((FAIL_COUNT++))
    fi
}

echo "Checking Charter Constants..."
echo "-------------------------------------------------------------------"

# Check spread tightened to 1.2 pips
check_feature "Spread Guard Tightened (1.2 pips)" \
    "grep 'MAX_SPREAD_PIPS = ' $PROJECT_ROOT/rick_hive/rick_charter.py | grep -o '[0-9.]*'" \
    "1.2"

# Check anti-churn min hold exists
check_feature "Anti-Churn Min Hold (30s)" \
    "grep -c 'min_hold_seconds = 30' $PROJECT_ROOT/oanda_trading_engine.py" \
    "1"

# Check anti-churn logic in place_trade
check_feature "Anti-Churn Check in place_trade" \
    "grep -c 'ANTI_CHURN_BLOCK' $PROJECT_ROOT/oanda_trading_engine.py" \
    "1"

# Check last_trade_time initialized
check_feature "Last Trade Time Tracking" \
    "grep -c 'self.last_trade_time = ' $PROJECT_ROOT/oanda_trading_engine.py" \
    "2"

echo ""
echo "Checking Wolfpack EdgePack Features..."
echo "-------------------------------------------------------------------"

# Check features.json exists and has correct settings
if [ -f "$PROJECT_ROOT/config/features.json" ]; then
    check_feature "Features Config Exists" \
        "echo 'true'" \
        "true"
    
    check_feature "Spread Guard Enabled" \
        "grep -c '\"spread_guard\": true' $PROJECT_ROOT/config/features.json" \
        "1"
    
    check_feature "Regime Gate Enabled" \
        "grep -c '\"regime_gate\": true' $PROJECT_ROOT/config/features.json" \
        "1"
    
    check_feature "Hedge Recovery Enabled" \
        "grep -c '\"quant_hedge_recovery\": true' $PROJECT_ROOT/config/features.json" \
        "1"
else
    echo -e "${RED}❌ FAIL${NC}: Features config file not found"
    ((FAIL_COUNT++))
fi

# Check hedge recovery module exists
check_feature "Hedge Recovery Module Exists" \
    "[ -f $PROJECT_ROOT/execution/quant_hedge_recovery.py ] && echo 'exists' || echo 'missing'" \
    "exists"

# Check single instance guard
check_feature "Single Instance Guard Script" \
    "[ -f $PROJECT_ROOT/scripts/single_instance_guard.sh ] && echo 'exists' || echo 'missing'" \
    "exists"

echo ""
echo "Checking Surgeon Exit Harmony..."
echo "-------------------------------------------------------------------"

# Check surgeon has exit harmony parameters
check_feature "Surgeon Min Profit for Trail (0.8R)" \
    "grep -c 'min_profit_r_for_trail = 0.8' $PROJECT_ROOT/PhoenixV2/operations/surgeon.py" \
    "1"

check_feature "Surgeon Max Trail Lock (2.5R)" \
    "grep -c 'max_trail_lock_r = 2.5' $PROJECT_ROOT/PhoenixV2/operations/surgeon.py" \
    "1"

echo ""
echo "Checking Charter Values..."
echo "-------------------------------------------------------------------"

# Check concurrent positions
check_feature "Max Concurrent Positions (12)" \
    "grep 'MAX_CONCURRENT_POSITIONS = ' $PROJECT_ROOT/rick_hive/rick_charter.py | grep -o '[0-9]*' | head -1" \
    "12"

# Check daily loss breaker
check_feature "Daily Loss Breaker (3%)" \
    "grep 'DAILY_LOSS_BREAKER_PCT = ' $PROJECT_ROOT/rick_hive/rick_charter.py | grep -o '0.03'" \
    "0.03"

# Check wolf min confidence
check_feature "Wolf Min Confidence (0.65)" \
    "grep 'WOLF_MIN_CONFIDENCE = ' $PROJECT_ROOT/rick_hive/rick_charter.py | grep -o '0.65'" \
    "0.65"

echo ""
echo "======================================================================="
echo "  SUMMARY"
echo "======================================================================="
echo -e "${GREEN}Checks Passed: $PASS_COUNT${NC}"
echo -e "${RED}Checks Failed: $FAIL_COUNT${NC}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL CHECKS PASSED!${NC}"
    echo "Anti-churn features are active. Spread tightened to 1.2 pips."
    echo "System ready for low-churn trading."
    exit 0
else
    echo -e "${YELLOW}⚠️  Some checks failed. Review above for details.${NC}"
    exit 1
fi
