#!/usr/bin/env bash
set -euo pipefail

# Deploy the systemd unit for RBOTzilla Backend. Edit paths to suit your environment.
UNIT_SRC=ops/systemd/rbotzilla-backend.service
UNIT_DST=/etc/systemd/system/rbotzilla-backend.service

if [ $EUID -ne 0 ]; then
  echo "This script requires root for systemd operations. Please re-run with sudo."
  exit 1
fi

echo "Deploying systemd unit: $UNIT_SRC -> $UNIT_DST"
cp "$UNIT_SRC" "$UNIT_DST"
systemctl daemon-reload
systemctl enable rbotzilla-backend
systemctl restart rbotzilla-backend
systemctl status rbotzilla-backend --no-pager
