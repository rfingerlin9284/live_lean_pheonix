#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1
if [[ "${1:-}" == "--show-ghost" || "${1:-}" == "-g" ]]; then
  exec ./util/plain_english_narration.sh --show-ghost
else
  exec ./util/plain_english_narration.sh
fi
