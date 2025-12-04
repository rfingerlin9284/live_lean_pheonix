FINAL EVOLUTION - Combined Phase 3 (Reality Bridge) + Phase 4 (Fortress Rick)
=======================================================================

This document summarizes the final phase changes and how to run the system safely.

Overview
--------
- Real connectors are present: OANDA (existing), plus Coinbase and IBKR connectors provided.
- System hardening artifacts: Dockerfile, docker-compose, systemd unit file, ops scripts.
- Explicit environment gating for practice orders to avoid accidental live trades.

Key files added
--------------
- coinbase/brokers/coinbase_connector.py  (safe wrapper, sandbox by default)
- ibkr/brokers/ibkr_connector.py          (safe wrapper, paper mode by default)
- Dockerfile
- docker-compose.yml
- ops/systemd/rbotzilla-backend.service
- ops/start_oanda_practice.sh
- .env.example
- PHASE_FINAL.md (this file)

How to run (local dev)
----------------------
1) Copy `.env.example` to a safe `.env.oanda_only` and add your practice tokens.
2) Verify your practice credentials for OANDA using the read-only verifier:
   PYTHONPATH=$PWD .venv/bin/python tools/verify_oanda_live.py --env practice --env-file .env.oanda_only
3) Start the engine (practice mode):
   export RICK_ENV=practice
   export ALLOW_PRACTICE_ORDERS=1
   export CONFIRM_PRACTICE_ORDER=1
   export PRACTICE_PIN=841921
   export OANDA_FORCE_ENV=practice
   export OANDA_LOAD_ENV_FILE=1
   PYTHONPATH=$PWD .venv/bin/python oanda/oanda_trading_engine.py

Docker
------
Build: docker build -t rbotzilla:latest .
Run: docker run -it --rm -p 8000:8000 -v $PWD:/app rbotzilla:latest

Systemd
-------
Copy `ops/systemd/rbotzilla-backend.service` to your systemd directory and adjust paths and user accordingly. Then run:
  sudo systemctl daemon-reload
  sudo systemctl enable rbotzilla-backend
  sudo systemctl start rbotzilla-backend

Security and safety
-------------------
- Live trading requires explicit environment overrides and keys. Practice mode is default with safety gating.
- Never check in secrets; `.env.example` is a template and should not contain real tokens.
