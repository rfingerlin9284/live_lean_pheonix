#!/usr/bin/env bash
set -e

# Try to detect git repo root; fall back to current directory
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "🔍 Checking for AGENTS.md in repo:"
echo "    $REPO_ROOT"
echo

if [ -f "$REPO_ROOT/AGENTS.md" ]; then
  echo "✅ AGENTS.md FOUND at:"
  echo "    $REPO_ROOT/AGENTS.md"
  exit 0
else
  echo "❌ AGENTS.md NOT FOUND in repo root."
  echo
  echo "To create it now, run:"
  echo "  nano \"$REPO_ROOT/AGENTS.md\""
  exit 1
fi
