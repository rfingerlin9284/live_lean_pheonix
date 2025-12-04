Ops / Deployment helper scripts
================================

Scripts
-------
- lock_secrets.sh: Ensure .env files have correct 600 permission to avoid accidental exposure.
- deploy_systemd.sh: Deploy the systemd unit file (requires sudo/root) for the backend.
- start_oanda_practice.sh: Start the OANDA practice engine with explicit gating flags.

Usage
-----
- Lock secrets:
  - ./ops/lock_secrets.sh
- Deploy systemd (root required):
  - sudo ./ops/deploy_systemd.sh
- Start OANDA engine (practice):
  - ./ops/start_oanda_practice.sh

Security Notes
--------------
- Do not check `.env*` files into git. `.env.example` is a template.
- Use `ops/lock_secrets.sh` to enforce permissions.
# RICK Phoenix Ops (Phase 4)

This folder contains the operational artifacts for running RICK Phoenix as a production service.

Files
- `rick_phoenix.service` — systemd unit to run /app/start_with_integrity.sh as a system service.
- `lock_secrets.sh` — simple script that sets secure permissions on the `.env` file (chmod 600).
- `check_env_permissions.py` — small script to check `.env` file permissions and return non-zero if insecure.

Usage
- Lock secrets before starting the service:
  - `bash ./ops/lock_secrets.sh ./.env`
  - Or use the VS Code task `Lock Secrets`.
 - Lock secrets before starting the service:
   - `bash ./ops/lock_secrets.sh ./.env`
   - Or use the VS Code task `Lock Secrets`.
 - Developer / Simplify Mode: If you are in a development environment and want to skip permission hardening and locking, set `SIMPLIFY_MODE=1` and/or use the simplified tasks:
   - `SIMPLIFY_MODE=1 ./start_with_integrity.sh` or use the `Run OANDA Engine (Practice - Simplify)` task in VS Code.
   - Use the simplified credential writer: `SIMPLIFY_MODE=1 bash ./scripts/write_env_file.sh .env.oanda_only .env --no-lock`

- Install the systemd service (Ubuntu/Debian):
  - `sudo cp ops/rick_phoenix.service /etc/systemd/system/rick_phoenix.service`
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable --now rick_phoenix.service`

Notes
- The service file runs `start_with_integrity.sh` which checks for various integrity conditions before starting the engine.
- For containerized deployments, the `docker-compose.yml` now exposes separate services for each sector (oanda/coinbase/ibkr) with `ENV` variables set for practice/canary/paper modes.

Telemetry & UI Constraints (Phase 4)
- By default, Phase 4 forbids adding new telemetry dashboard or data-emitter changes during core hardening. The MARKET_TICK emitter is present in the OANDA engine for practice/canary testing but is disabled by default.
- To enable the telemetry emitter in local/dev mode, set the environment variable `ENABLE_TELEM_EMITTER=true` prior to starting the agent.

Example:
```bash
export ENABLE_TELEM_EMITTER=true
RICK_ENV=practice ./start_with_integrity.sh
```

Verification Tool
-----------------
We provide a safe, read-only verification tool to confirm OANDA account connectivity and credentials without placing orders.

Run as:
```
python3 tools/verify_oanda_live.py [--env live|practice]
```

This will print a masked account id and the account balance. It does not place orders or modify account state.

NOTE: To actually allow paper execution (placing orders on OANDA practice account), set EXECUTION_ENABLED=true in the environment (or let start_with_integrity.sh auto-enable when a non-placeholder practice token and account are present). By default, EXECUTION_ENABLED is false.
