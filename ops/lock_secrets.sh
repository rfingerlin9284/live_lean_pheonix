#!/usr/bin/env bash
set -euo pipefail

# Lock .env file(s) permissions and report status
# If an explicit file path is provided as the first argument, lock that file
# Otherwise, lock all files matching .env*

ENV_FILE=${1:-}

# If user requested a simplified run, do nothing
if [[ "${SIMPLIFY_MODE:-0}" == '1' ]]; then
  echo "SIMPLIFY_MODE active: skipping lock_secrets operations"
  exit 0
fi

if [[ -n "$ENV_FILE" ]]; then
  echo "Checking env file: $ENV_FILE"
  if [[ ! -f "$ENV_FILE" ]]; then
    echo "No env file found at $ENV_FILE. Nothing to do."
    exit 0
  fi
  PERMS=$(stat -c '%a' "$ENV_FILE")
  echo "Current permissions: $PERMS"
  if [[ "$PERMS" != "600" ]]; then
    echo "Locking env file to 600"
    chmod 600 "$ENV_FILE"
    NEW_PERMS=$(stat -c '%a' "$ENV_FILE")
    echo "Updated permissions: $NEW_PERMS"
  else
    echo "Permissions already secure (600)."
  fi
else
  echo "Locking secrets in repo: setting 600 permissions on .env* files"
  for f in .env*; do
    if [[ -f "$f" ]]; then
      echo "Setting permissions for $f"
      chmod 600 "$f" || true
    fi
  done
  echo "Secrets locked."
fi

exit 0
