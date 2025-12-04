# Environment Setup for RBOTzilla

This file documents how to use the template `.env.paper` and the live template `.env.live.example`.

Steps to prepare a paper env (safe sandbox):
1. Copy `.env.paper` to `.env` (local only):
```bash
cp .env.paper .env
chmod +x tools/populate_env_from_template.sh
./tools/populate_env_from_template.sh
```
2. Fill the `REPLACE_ME` placeholders in `.env` with your local values.
3. Do not commit `.env` to the repository—it's ignored by `.gitignore`.

To prepare a live env (production):
1. Copy `.env.live.example` to `.env.live` and fill in live credentials.
2. Keep live env in a secure vault and do not commit to the repo.

Safety notes:
Starting the system in paper mode (safe):
1. Prepare `.env` as above.
2. Run the safe start script to launch the full autonomous system in paper mode (logs in `logs/paper_live.log`):
```bash
chmod +x tools/safe_start_paper_trading.sh
./tools/safe_start_paper_trading.sh
```
3. Validate it's running by checking the logs and narration stream:
```bash
tail -n 200 logs/paper_live.log
tail -f narration.jsonl
```

- `.env.paper` is safe to commit (no secrets), and used for local testing and the Dress Rehearsal.
- Always verify `ALLOW_LIVE_TRADING` and `EXECUTION_ENABLED` before enabling live trading.

Additional safety checks:
1. Run `scripts/find_secrets.py` prior to committing to scan for tokens or account IDs in the repository. This is a heuristic scan and should be run if you suspect any secret leakage.
2. Run `scripts/commit_safety_check.sh` in CI or locally as part of pre-commit checks to prevent accidental commits of sensitive keys.

