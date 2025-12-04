# RICK — Quick Cheat Sheet & Task Guide

This file is your one-stop CLI & Task reference. Use VS Code Tasks (Cmd/Ctrl+Shift+P → Tasks: Run Task) to run these commands without remembering code.

---
## Quick Task List (Tasks available in `.vscode/tasks.json`)
- `Check Narration (tools)` — Count and show recent narration events.
- `Run OANDA Engine (Practice)` — Start the engine using practice account in background.
- `Run OANDA Engine (Live)` — Start the engine using live account in background.
- `Run Charter Gate Tests` — Run unit tests for charter gating logic.
- `Tail Narration (follow)` — Tail `narration.jsonl` and follow live events.
- `Open Cheat Sheet` — Opens this file (or prints it) to the terminal.

---
## Copy/Paste CLI Commands (run from repo root)
- Run OANDA engine (practice):

```bash
RICK_ENV=practice python3 oanda/oanda_trading_engine.py
```

- Run OANDA engine (live):

```bash
RICK_ENV=live python3 oanda/oanda_trading_engine.py
```

- Tail narration log (live):

```bash
tail -n 200 -f narration.jsonl
```

- Check narration counts (our helper):

```bash
python3 tools/check_narration_counts.py
```

- Run the charter gate unit tests:

```bash
python3 -m pytest -q tests/test_charter_gates.py || python3 tests/test_charter_gates.py
```

- Run the quick diagnostic monitor:

```bash
python3 auto_diagnostic_monitor.py
```

---
## Organ Groups (High-level responsibilities & files) 

### Brain — "The Engine"
Responsibility: Receives signals, evaluates them against charter/gates, and places/cancels orders.
- `oanda/oanda_trading_engine.py` — OANDA engine entrypoint (Practice/Live) — the consolidated engine.
- `canary_trading_engine.py` / `canary_trading_engine.py.backup` — Canary (test/lab) trading engine.
- `aggressive_money_machine.py` — Aggressive strategy runner.
- `rick_institutional_full.py` — Institutional-grade autonomous agent and five-layer gates.
- `start_with_integrity.sh` — Wrapper to start the whole system safely.

### Eyes — "Sentinel & Watchers"
Responsibility: Monitor positions, account status, and safety conditions to raise events/alerts.
- `active_trade_monitor.py` — Live position & trade monitor.
- `auto_diagnostic_monitor.py` — Periodic system & connectivity checks.
- `check_system_status.py` — Helper to check system/health endpoints.
- `check_ib_balance.py`, `check_ib_gateway.sh`, `check_ibkr_status.sh` — Broker health checks.

### Voice — "Narration & Logging"
Responsibility: Centralized logging / narration that emits `narration.jsonl` events consumed by UI/ops.
- `util/narration_logger.py` — Writes events into `narration.jsonl` — the event stream.
- `util/rick_narrator.py`, `pretty_print_narration.py` — CLI tools to pretty-print narration logs for humans.
- `logs/` and `narration.jsonl` — Event storage for debugging & dashboards.

### Pulse — "Watchdog & Automation"
Responsibility: High-level monitoring and automatic restart/management logic.
- `system_watchdog.py` — Watchdog for running components.
- `bot_health_check.py` — Health & liveliness checks for the autonomous components.
- `safe_shutdown.sh`, `activate_live_trading.sh` — Operational scripts for safe maintenance.

### Gatekeepers / Charter — "Rules Enforcement"
Responsibility: The charter, gating logic, and enforcement mechanisms for trade safety.
- `foundation/rick_charter.py` — The single-source-of-truth Charter (global configuration for the system).
- `oanda/foundation/rick_charter.py` — OANDA-specific Charter (balanced profile; MIN_EXPECTED_PNL = $35, MIN_NOTIONAL = $10k, MAX_MARGIN_UTILIZATION = 175%).
- `rick_institutional_full.py` — Applies the five-layer gate validation in the institutional agent.
- `rick_hive/guardian_gates.py` — Per-signal gate validation in the hive.
- `util/position_police.py` — Minimal enforcement for min-notional and position repairs.
- `oanda/brokers/oanda_connector.py` — Enforces min-notional and expected PnL checks inside the connector.

### Brokers & Bridges — "Connector & Adapter Layer"
Responsibility: Broker-specific connectors and translation between the agent and the broker APIs.
- `oanda/brokers/oanda_connector.py` — OANDA API integration & order placement; logs `OCO_PLACED` events.
- `brokers/coinbase_advanced_connector.py` — Coinbase connector.
- `bridges/oanda_live_bridge.py` & `bridges/oanda_charter_bridge.py` — Helper bridges turning hive signals into broker orders, using Charter rules.

### Tools & Utilities — "Helpers & CLI"
Responsibility: Small CLI utilities to help ops & testing.
- `tools/check_narration_counts.py` — Event counting & quick stats (added by ops).
- `util/terminal_display.py` — Console display helpers.
- `util/confidence.py` — Confidence formatting support.
- `util/position_police.py` — Charter position enforcement.
- `tools/` or `scripts/` — Misc. helpers.

### Config & Scripts
Responsibility: Tunables and shell scripts for starting/stopping and environment config.
- `config/gates.yaml` — Per-connector gate toggles.
- `config/aggressive_machine_config.py` — Strategy & gating config.
- `.env` — Environment variables & API keys.
- `start_with_integrity.sh`, `activate_live_trading.sh`, `safe_shutdown.sh` — Start/stop scripts.

### Tests — "Unit / Integration"
Responsibility: Validation and regression checks.
- `tests/test_charter_gates.py` — Unit tests for Charter gates (added by us).
- `PhoenixV2/tests/` and `tests/` — Additional test suites across the codebase.

---
## Example Shortcuts & 'No Code' Steps — Use Tasks instead of remembering commands
- To run the OANDA engine in practice: Run the task `Run OANDA Engine (Practice)` (Cmd/Ctrl+Shift+P → Tasks: Run Task → Run OANDA Engine (Practice)).
- To monitor events & tail logs: Run the task `Tail Narration (follow)`.
- To print the summary of narrated events: Run the task `Check Narration (tools)`.
- To run tests: Run the task `Run Charter Gate Tests`.

---
## Notes
- Tasks in `.vscode/tasks.json` are the easiest one-click operations. If you want to add more tasks (e.g., a shortcut to run streams for OANDA + tail logs) I can set them up.
- If you use a Python virtualenv, replace `python3` in the example snippets with the venv python like `${workspaceFolder}/.venv/bin/python` or update the tasks to point to the venv.

---
## Quick Commands for Debugging (copy/paste)
- Print the last 50 narration lines with `jq`: 

```bash
tail -n 50 narration.jsonl | jq -r '.event_type + " | " + .symbol + " | " + (.details | tostring)'
```

- Find how many `OCO_PLACED` events:

```bash
grep -c 'OCO_PLACED' narration.jsonl
```

- Check for `CHARTER_VIOLATION` reasons:

```bash
jq -r 'select(.event_type=="CHARTER_VIOLATION") | .details.code' narration.jsonl | sort | uniq -c
```

---
If you'd like, I can add the following features next:
- Auto-detect your venv and update tasks to use it.
- Add additional, per-organ tasks to tail logs or open specific source files.
- Add a small UI panel or README file that automatically builds the organ list and tasks (more advanced).

If this cheat sheet looks good, I’ll add a task to open it directly from VS Code's Task menu and update the README with the instructions.
