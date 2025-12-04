#!/usr/bin/env bash
set -euo pipefail

# Install project's recommended git hooks into .git/hooks
# Usage: ./scripts/install_git_hooks.sh

HOOKS_DIR="$(pwd)/scripts/git_hooks"
GIT_HOOKS_DIR="$(pwd)/.git/hooks"

if [ ! -d "$GIT_HOOKS_DIR" ]; then
  echo ".git/hooks not found; are you in the repo root?"
  exit 2
fi

for h in "$HOOKS_DIR"/*; do
  base=$(basename "$h")
  dest="$GIT_HOOKS_DIR/$base"
  if [ -L "$dest" ]; then
    echo "Skipping - already a symlink: $dest"
    continue
  fi
  if [ -e "$dest" ]; then
    echo "Backing up existing hook: $dest -> ${dest}.bak"
    mv "$dest" "${dest}.bak"
  fi
  ln -s "$h" "$dest"
  chmod +x "$h"
  echo "Installed hook: $dest -> $h"
done

echo "Installation complete. Run 'git status' to verify hooks are active." 
