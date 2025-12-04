#!/usr/bin/env bash
set -euo pipefail
OUTDIR=${1:-"export_rebuild"}
ARCHIVE_NAME="package.tar.gz"
echo "Writing embedded archive to $ARCHIVE_NAME and extracting to $OUTDIR..."
mkdir -p "$OUTDIR"
BASE64_PAYLOAD_FILE="$(mktemp)"
cat > "$BASE64_PAYLOAD_FILE" <<'PAYLOAD'
$(base64 "$DEST/package.tar.gz")
PAYLOAD
base64 -d "$BASE64_PAYLOAD_FILE" > "$ARCHIVE_NAME"
tar -xzf "$ARCHIVE_NAME" -C "$OUTDIR"
echo "Extracted to $OUTDIR"
if [ -f "$OUTDIR/tools/validate_and_snapshot.sh" ]; then
  bash "$OUTDIR/tools/validate_and_snapshot.sh" "$OUTDIR"
fi
rm -f "$ARCHIVE_NAME" "$BASE64_PAYLOAD_FILE"
echo "Done."
