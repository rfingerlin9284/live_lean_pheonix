<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# RICK PHOENIX: OANDA-ONLY ESSENTIALS

## System Overview
This repository is a lean, production-ready version of the RICK PHOENIX trading system, focused exclusively on the OANDA platform. It is designed for robust, autonomous, and auditable live/practice trading, with all legacy, redundant, and non-essential code removed. Stubs for IBKR remain for future integration.

---

## Key Features & Capabilities
- **Autonomous OANDA Trading Engine**: Fully headless, .env-driven, and protocol-enforced.
- **Live & Practice Modes**: Toggle via environment variables and .env files.
- **Sub-millisecond Latency**: Uses `time.perf_counter_ns` for precise timing.
- **Guardian Gates & Smart Logic Filters**: Advanced risk, margin, and compliance enforcement.
- **Self-Healing Narration & Monitoring**: Persistent, auto-repairing narration and watchdog scripts.
- **Task Automation**: VS Code tasks for all major workflows.
- **Audit & Test Coverage**: Charter gate tests, narration checks, and system health monitoring.
- **Upgrade-Ready**: Clean separation of OANDA logic, with stubs for IBKR/Coinbase.

---

## Directory Structure (Post-Cleanup)
```
oanda/                  # OANDA engine, strategies, brokers, foundation
util/, utils/           # Utility modules used by OANDA
.vscode/                # VS Code tasks/settings
ibkr/, coinbase/        # Stubs for future integration
narration_self_repair.py
pretty_print_narration.py
active_trade_monitor.py
system_watchdog.py
start_with_integrity.sh
start_oanda_practice.sh
.env, .env.oanda_only, .env.live, .env.paper
requirements.txt
ESSENTIALS_MANIFEST.txt
```

---

## Workflow & Connection Diagram

![Workflow Diagram](./docs/oanda_workflow.png)

**Diagram Description:**
- **OANDA Engine**: Central logic, connects to OANDA API using credentials from `.env` files.
- **Brokers/Strategies**: Modular, can be extended for IBKR/Coinbase.
- **Utility Modules**: Shared logic for risk, compliance, and data handling.
- **Narration/Monitoring**: Persistent scripts for real-time status and self-repair.
- **VS Code Tasks**: Automate all major workflows (start, monitor, test, repair).

---

## Advanced Logic & Upgrade Candidates
- `foundation/margin_correlation_gate.py`: Advanced margin/risk logic.
- `foundation/rick_charter.py`: Protocol and compliance enforcement.
- `strategies/`: All advanced OANDA strategies (bullish, bearish, sideways wolf, etc).
- `tests/`: Charter gate and system tests.
- `narration_self_repair.py`, `pretty_print_narration.py`: Self-healing, fallback, and monitoring logic.

---

## Audit, Test, and Monitoring Files
- `tests/`
- `active_trade_monitor.py`
- `system_watchdog.py`
- `narration_self_repair.py`
- `pretty_print_narration.py`

---

## Legacy & Redundant Code
All legacy, redundant, or half-finished code has been archived or removed. Only the most advanced, useful logic and strategies remain. See `ESSENTIALS_MANIFEST.txt` for the definitive list of what is kept.

---

## Next Steps
- To upgrade: Add IBKR/Coinbase logic to their respective stubs.
- To restore legacy code: Unzip `old_oanda_legacy.zip` (if present).
- For full system audit, see `tests/` and narration scripts.

---

## File List (Essentials)
See `ESSENTIALS_MANIFEST.txt` for a complete, up-to-date list of all essential files and folders.

---

## PNG Diagram Note
- The workflow diagram should be created and placed at `docs/oanda_workflow.png`.
- It should clearly label: OANDA Engine, Brokers, Utility Modules, Narration/Monitoring, VS Code Tasks, and connection points for IBKR/Coinbase.
- (Diagram not auto-generated here, but this is the expected location and content.)

---

## Contact
For questions or upgrades, see the project owner or open an issue on GitHub.
