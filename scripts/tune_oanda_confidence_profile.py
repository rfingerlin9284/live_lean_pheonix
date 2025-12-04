#!/usr/bin/env python3
"""
Set OANDA confidence and charter gating values back to Balanced profile (idempotent)
Usage:
  scripts/tune_oanda_confidence_profile.py --apply  # make changes
  scripts/tune_oanda_confidence_profile.py --dry-run  # show what would change
  scripts/tune_oanda_confidence_profile.py --revert  # revert previous changes from backups

This script updates the canonical charter files used by connectors:
  - foundation/rick_charter.py
  - oanda/foundation/rick_charter.py
  - rick_hive/rick_charter.py

It backups files with a .bak-tune profile.
"""
import argparse
import re
from pathlib import Path
import shutil
import sys
from datetime import datetime


DESIRED_MIN_EXPECTED_PNL = 35.0
DESIRED_MIN_NOTIONAL = 10000
TARGET_FILES = [
    Path("foundation/rick_charter.py"),
    Path("oanda/foundation/rick_charter.py"),
    Path("rick_hive/rick_charter.py"),
]


def backup_file(p: Path) -> Path:
    bak = p.with_suffix(p.suffix + f".bak-tune-{int(datetime.utcnow().timestamp())}")
    shutil.copy2(p, bak)
    return bak


def replace_constant(text: str, const_name: str, value: float) -> (str, bool):
    pattern = re.compile(rf"^(\s*{const_name}\s*=\s*)([0-9]+(?:\.[0-9]+)?)(\s*#?.*)$", re.MULTILINE)
    def repl(m):
        return f"{m.group(1)}{value}{m.group(3)}"
    new_text, count = pattern.subn(repl, text)
    return new_text, count > 0


def ensure_file_changes(path: Path, dry_run: bool = True) -> dict:
    res = {"file": str(path), "changed": False, "backup": None, "notes": []}
    if not path.exists():
        res["notes"].append("file not found")
        return res
    text = path.read_text()
    updated = False

    # MIN_EXPECTED_PNL_USD
    t2, changed1 = replace_constant(text, "MIN_EXPECTED_PNL_USD", DESIRED_MIN_EXPECTED_PNL)
    if changed1:
        text = t2
        updated = True
        res["notes"].append(f"set MIN_EXPECTED_PNL_USD={DESIRED_MIN_EXPECTED_PNL}")

    # MIN_NOTIONAL_USD
    t3, changed2 = replace_constant(text, "MIN_NOTIONAL_USD", DESIRED_MIN_NOTIONAL)
    if changed2:
        text = t3
        updated = True
        res["notes"].append(f"set MIN_NOTIONAL_USD={DESIRED_MIN_NOTIONAL}")

    if updated and not dry_run:
        bak = backup_file(path)
        path.write_text(text)
        res["backup"] = str(bak)
        res["changed"] = True
    else:
        res["changed"] = updated

    return res


def revert_backups() -> list:
    restored = []
    for p in TARGET_FILES:
        # find backups with .bak-tune
        for bak in p.parent.glob(p.name + ".bak-tune-*"):
            orig = p
            shutil.copy2(bak, orig)
            restored.append({"from": str(bak), "to": str(orig)})
    return restored


def main():
    parser = argparse.ArgumentParser(description="Reset OANDA charter gating to Balanced profile")
    parser.add_argument("--apply", action="store_true", help="apply changes in-place (default is dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="show what would be changed; default")
    parser.add_argument("--revert", action="store_true", help="revert previous backups")
    parser.add_argument("--targets", nargs="*", help="explicit targets to operate on (paths)")
    args = parser.parse_args()

    dry_run = not args.apply and args.dry_run
    targets = TARGET_FILES
    if args.targets:
        targets = [Path(t) for t in args.targets]

    if args.revert:
        restored = revert_backups()
        print(f"Restored {len(restored)} backups")
        for r in restored:
            print("  Reverted:", r)
        sys.exit(0)

    results = []
    for t in targets:
        r = ensure_file_changes(t, dry_run=dry_run)
        results.append(r)

    for r in results:
        print(f"File: {r['file']}")
        print(f"  Exists?: {'yes' if Path(r['file']).exists() else 'no'}")
        print(f"  Changes needed?: {'yes' if r['changed'] else 'no'}")
        for n in r['notes']:
            print(f"    - {n}")
        if r.get('backup'):
            print(f"  Backup: {r['backup']}")
        print("")

    # Summary
    changed = [r for r in results if r['changed']]
    print(f"Summary: {len(changed)} files modified or would be modified.")
    if dry_run:
        print("Dry-run mode: no files were modified.")
    else:
        print("Changes applied; backups created with .bak-tune-<timestamp>")


if __name__ == '__main__':
    main()
