How to manage local env secrets safely
====================================

This repository contains a sanitized environment file template, but should never contain real secrets committed to Git.

1. Use `scripts/populate_env_from_file.py` to build a local, untracked `.env` file from a local source file:

   - Dry-run to preview (masked):
    python3 scripts/populate_env_from_file.py --source paper_acct_env.env.txt --target .env --dry-run

   - Apply to write the target file (will create a backup):
    python3 scripts/populate_env_from_file.py --source paper_acct_env.env.txt --target .env --apply

   - Revert to restore the most recent backup:
    python3 scripts/populate_env_from_file.py --target .env --revert

2. Never commit .env files or real secrets. Add them to your OS-level environment or a secret manager for CI.

3. Add the following to gitignore (already present in this repo):
   .env
  # .env.oanda_only

4. Scan your changes before committing using the repo scanner:
   python3 scripts/find_secrets.py
