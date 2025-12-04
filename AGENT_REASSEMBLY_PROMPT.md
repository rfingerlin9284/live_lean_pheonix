# Agent Prompt: RICK PHOENIX System Reassembly

## Context
You are tasked with reassembling the complete RICK PHOENIX trading system from a GitHub repository that has been split across multiple branches to handle the large file tree (94GB total).

## Your Mission
Execute the reassembly script to reconstruct the full system file tree by pulling all branches and merging their contents into a complete workspace.

## Repository Information
- **Repository**: `rfingerlin9284/live_lean_pheonix`
- **Main Branch**: `master`
- **Total Size**: ~94GB when fully assembled
- **Branch Strategy**: Code split into feature branches to avoid GitHub size limits

## Step-by-Step Instructions

### 1. Clone the Repository
```bash
git clone git@github.com:rfingerlin9284/live_lean_pheonix.git
cd live_lean_pheonix
```

Or if already cloned:
```bash
cd /path/to/live_lean_pheonix
git checkout master
git pull origin master
```

### 2. Run the Reassembly Script
```bash
chmod +x REASSEMBLE_SYSTEM.sh
./REASSEMBLE_SYSTEM.sh
```

The script will:
- Fetch all remote branches
- Merge content from feature branches:
  - `feature/core-engines` - Trading engines
  - `feature/broker-connectors` - OANDA, Coinbase, IBKR connectors
  - `feature/strategies` - Trading strategies
  - `feature/foundations` - Core logic and charter
  - `feature/dashboards` - Web dashboards
  - `feature/monitoring` - Monitoring and narration
  - `feature/hive-mind` - Consensus system
  - `feature/utilities` - Utility modules
  - `feature/analysis-tools` - Analysis scripts
  - `feature/testing` - Test suites
  - `data/backtest-results` - Historical backtest data
  - `data/archived-simulations` - Simulation results
  - `data/logs-historical` - Historical logs
  - `docs/comprehensive` - Complete documentation
  - `docs/guides` - Setup and operation guides
  - `docs/api-reference` - API documentation

### 3. Verify Assembly
```bash
# Check critical files exist
ls -la foundation/rick_charter.py
ls -la oanda_trading_engine.py
ls -la coinbase_safe_mode_engine.py
ls -la requirements.txt

# Check directory structure
tree -L 2 -d .
# or
find . -maxdepth 2 -type d
```

### 4. Complete Setup
```bash
# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.paper .env
nano .env  # Add your API credentials
```

### 5. Verify System Integrity
```bash
# Run system check
python3 check_system_status.py

# Verify charter
python3 -c "from foundation.rick_charter import RickCharter; print(RickCharter.validate())"
```

## Expected File Tree Structure

After reassembly, you should have:

```
RICK_PHOENIX/
├── foundation/              # Core trading logic & charter
├── brokers/                 # OANDA, Coinbase, IBKR connectors
├── strategies/              # Trading strategies (bullish, bearish, sideways wolf)
├── engines/                 # Trading engines
├── hive/                    # Hive mind consensus system
├── dashboard/               # Web dashboards (Flask & Streamlit)
├── util/ & utils/          # Utility modules
├── logic/                   # Advanced trading logic
├── tests/                   # Test suites
├── data/                    # Market data and backtest results
├── logs/                    # Trading logs and narration
├── docs/                    # Documentation
├── backups/                 # System backups
├── ROLLBACK_SNAPSHOTS/      # Rollback points
├── .env files              # Environment configuration
├── requirements.txt         # Python dependencies
└── README.md               # Main documentation
```

## Troubleshooting

### If reassembly fails:
```bash
# Reset to clean state
git checkout master
git reset --hard origin/master
git clean -fd

# Try again
./REASSEMBLE_SYSTEM.sh
```

### If branches are missing:
```bash
# List all branches
git branch -a

# Manually checkout specific branch content
git checkout origin/feature/core-engines -- engines/
```

### If files are too large for GitHub:
Some files (legacy_code.tar.gz, large snapshots) may need to be downloaded separately:
- Check for download links in branch README files
- Look for alternative storage references (Google Drive, etc.)

## Important Notes

1. **Credentials**: The `.env` files are NOT included in the repository for security. You must configure them manually.

2. **Large Files**: Some archived data may be stored in Git LFS or external storage due to GitHub's 100MB file limit.

3. **Protected Files**: Critical files like `foundation/rick_charter.py` are read-only (444 permissions) and require PIN 841921 to modify.

4. **System Requirements**:
   - Python 3.11+
   - 4GB RAM minimum
   - 100GB+ disk space for complete system
   - Linux or WSL Ubuntu

5. **Branch Strategy**: Each branch contains a specific component of the system. The reassembly script merges them intelligently without conflicts.

## Validation Checklist

After reassembly, verify:

- [ ] All Python files have proper syntax
- [ ] requirements.txt installs successfully
- [ ] Charter file exists and validates (PIN: 841921)
- [ ] Trading engines are executable
- [ ] Dashboard files are present
- [ ] Broker connectors are intact
- [ ] Strategies directory is populated
- [ ] Tests can be imported
- [ ] Documentation is readable

## Final Steps

Once reassembled and verified:

1. Read the main README.md for system overview
2. Follow QUICK_START_GUIDE.md for setup
3. Start with paper trading using `./start_paper_trading.sh`
4. Monitor with `python3 narration_to_english.py`
5. Access dashboard at `http://localhost:8501`

## Support

If you encounter issues:
- Check the README.md troubleshooting section
- Review branch-specific README files
- Verify all branches were fetched: `git branch -r`
- Ensure adequate disk space: `df -h`

Good luck! The RICK PHOENIX system is powerful once fully assembled. 🚀
