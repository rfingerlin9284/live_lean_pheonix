2025-12-03 UTC

Task: Implement global Agent Charter + snapshot manager (manual) and wire into OANDA engine

Files created:
- foundation/agent_charter.py - Global charter & enforcement for all agents
- utils/snapshot_manager.py - Small git-powered snapshot & restore helpers

Files changed:
- oanda/oanda_trading_engine.py - Import & call AgentCharter.enforce() at startup
- .vscode/tasks.json - Added "Create Snapshot (Manual)" task

Short summary:
- Added AgentCharter to centralize global rules & enforcement and provide a minimal helper API to engines.
- Snapshot manager provides create/restore helpers using git and is intentionally simple to reduce risk.
- OANDA engine now calls AgentCharter.enforce() at startup; this enforces the PIN-based immutable charter check.
- Added a VS Code Task so users can create manual snapshots easily.

Notes / Follow-ups:
- Consider adding more telemetry to AgentCharter.enforce(), such as environment variables or a lockfile check if you want additional runtime checks.
- Snapshot manager currently commits all changes prior to creating a tag; consider adding a policy (e.g., allow-missing-changes) or a confirmation step for critical environments.
- Add snapshot restore helper to start engines in the restored branch quickly if necessary.

confident with rbotzilla lawmakers=approval #AC001
