#!/usr/bin/env bash
# Mega script to recreate the gemini export directory from an embedded tarball or an archive next to it.
set -euo pipefail

ARCHIVE=${1:-"package.tar.gz"}
OUTDIR=${2:-"export_rebuild"}

if [ ! -f "$ARCHIVE" ]; then
  echo "Archive $ARCHIVE not found. Expect it in the same folder as this script or provide path." >&2
  exit 1
fi

mkdir -p "$OUTDIR"

echo "Extracting $ARCHIVE to $OUTDIR..."
tar -xzf "$ARCHIVE" -C "$OUTDIR"

# Run validation and snapshot script
if [ -f "$OUTDIR/tools/validate_and_snapshot.sh" ]; then
  echo "Running validation in $OUTDIR..."
  bash "$OUTDIR/tools/validate_and_snapshot.sh" "$OUTDIR"
else
  echo "Validation script not found; skipping validation." >&2
fi

echo "Rebuild complete. Snapshot saved in $OUTDIR/snapshot_status.json if validation completed."
