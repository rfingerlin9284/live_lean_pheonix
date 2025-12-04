#!/bin/bash
################################################################################
# RICK PHOENIX System Reassembly Script
# This script pulls all branches and reconstructs the complete file tree
################################################################################

set -e  # Exit on error

echo "=========================================="
echo "RICK PHOENIX System Reassembly"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Error: Not in a git repository. Please run from RICK_PHOENIX root.${NC}"
    exit 1
fi

# Get the repository root
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

echo -e "${BLUE}Repository root: $REPO_ROOT${NC}"
echo ""

# Fetch all branches
echo -e "${GREEN}Step 1: Fetching all remote branches...${NC}"
git fetch --all

# List all remote branches
echo ""
echo -e "${GREEN}Step 2: Available branches:${NC}"
git branch -r | grep -v '\->' | sed 's/origin\///' | grep -v 'master'

echo ""
echo -e "${GREEN}Step 3: Merging branches into current workspace...${NC}"

# Define branch groups
CORE_BRANCHES=(
    "feature/core-engines"
    "feature/broker-connectors"
    "feature/strategies"
    "feature/foundations"
)

DASHBOARD_BRANCHES=(
    "feature/dashboards"
    "feature/monitoring"
    "feature/hive-mind"
)

UTIL_BRANCHES=(
    "feature/utilities"
    "feature/analysis-tools"
    "feature/testing"
)

DATA_BRANCHES=(
    "data/backtest-results"
    "data/archived-simulations"
    "data/logs-historical"
)

DOC_BRANCHES=(
    "docs/comprehensive"
    "docs/guides"
    "docs/api-reference"
)

# Function to safely merge or checkout branch content
merge_branch_content() {
    local branch=$1
    echo -e "${BLUE}  → Processing branch: $branch${NC}"
    
    if git show-ref --verify --quiet "refs/remotes/origin/$branch"; then
        # Branch exists, checkout files from it
        git checkout "origin/$branch" -- . 2>/dev/null || {
            echo -e "${YELLOW}    ⚠ Could not checkout all files from $branch${NC}"
        }
        echo -e "${GREEN}    ✓ Merged content from $branch${NC}"
    else
        echo -e "${YELLOW}    ⚠ Branch $branch not found, skipping${NC}"
    fi
}

# Process each branch group
echo ""
echo -e "${GREEN}Processing Core Branches...${NC}"
for branch in "${CORE_BRANCHES[@]}"; do
    merge_branch_content "$branch"
done

echo ""
echo -e "${GREEN}Processing Dashboard Branches...${NC}"
for branch in "${DASHBOARD_BRANCHES[@]}"; do
    merge_branch_content "$branch"
done

echo ""
echo -e "${GREEN}Processing Utility Branches...${NC}"
for branch in "${UTIL_BRANCHES[@]}"; do
    merge_branch_content "$branch"
done

echo ""
echo -e "${GREEN}Processing Data Branches...${NC}"
for branch in "${DATA_BRANCHES[@]}"; do
    merge_branch_content "$branch"
done

echo ""
echo -e "${GREEN}Processing Documentation Branches...${NC}"
for branch in "${DOC_BRANCHES[@]}"; do
    merge_branch_content "$branch"
done

# Return to master branch
echo ""
echo -e "${GREEN}Step 4: Returning to master branch...${NC}"
git checkout master

# Restore any accidentally deleted critical files
echo ""
echo -e "${GREEN}Step 5: Verifying critical files...${NC}"
CRITICAL_FILES=(
    "README.md"
    "requirements.txt"
    "foundation/rick_charter.py"
    "oanda_trading_engine.py"
    "coinbase_safe_mode_engine.py"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${YELLOW}  ⚠ Restoring critical file: $file${NC}"
        git checkout master -- "$file" 2>/dev/null || echo -e "${YELLOW}    Could not restore $file${NC}"
    else
        echo -e "${GREEN}  ✓ $file present${NC}"
    fi
done

# Create directory structure if needed
echo ""
echo -e "${GREEN}Step 6: Ensuring directory structure...${NC}"
mkdir -p logs
mkdir -p data
mkdir -p backups
mkdir -p ROLLBACK_SNAPSHOTS
mkdir -p exports
mkdir -p reports
mkdir -p tmp

# Set proper permissions
echo ""
echo -e "${GREEN}Step 7: Setting permissions...${NC}"
chmod +x *.sh 2>/dev/null || true
chmod 444 foundation/rick_charter.py 2>/dev/null || true

# Display summary
echo ""
echo "=========================================="
echo -e "${GREEN}✓ Reassembly Complete!${NC}"
echo "=========================================="
echo ""
echo "File tree structure:"
tree -L 2 -d . 2>/dev/null || ls -la

echo ""
echo "Next steps:"
echo "1. Verify .env files are configured"
echo "2. Install dependencies: pip install -r requirements.txt"
echo "3. Run system check: python3 check_system_status.py"
echo "4. Start paper trading: ./start_paper_trading.sh"
echo ""
echo -e "${GREEN}Happy Trading! 🚀${NC}"
