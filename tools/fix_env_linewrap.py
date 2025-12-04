#!/usr/bin/env python3
"""
Fix `.env`-style files with accidental wrapped lines (line breaks mid value).
This script will make a backup and write a cleaned file with each assignment on a single line.

Usage:
    python3 tools/fix_env_linewrap.py .env.oanda_only
"""
import sys, re
from pathlib import Path

def fix_env_file(path: Path):
    if not path.exists():
        print(f"File not found: {path}")
        return 1
    data = path.read_text()
    lines = data.splitlines()
    cleaned = []
    current = None
    for ln in lines:
        if re.match(r'^[A-Z_][A-Z0-9_]+=.*$', ln):
            # new variable
            if current is not None:
                cleaned.append(current)
            current = ln
        else:
            # continuation line - append without spaces
            if current is None:
                # stray line; keep it
                current = ln
            else:
                current = current + ln.strip()
    if current is not None:
        cleaned.append(current)

    if '\n'.join(cleaned) == data.strip():
        print('No changes required')
        return 0
    backup = path.with_suffix(path.suffix + '.bak')
    path.replace(backup)
    path.write_text('\n'.join(cleaned) + '\n')
    print(f'Fixed {path}; backup at {backup}')
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: fix_env_linewrap.py <env_file>')
        raise SystemExit(2)
    raise SystemExit(fix_env_file(Path(sys.argv[1])))
