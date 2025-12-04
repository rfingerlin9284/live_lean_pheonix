#!/usr/bin/env python3
"""
Scan the repository for likely-secrets (OANDA tokens, UUID-like tokens, long API keys) and print occurrences.
This helper script is intended to be run locally by developers before committing code.
It does NOT attempt to automatically remove secrets. It only warns about locations.
"""
import argparse
import re
from pathlib import Path
import sys

PATTERNS = {
    'oanda_token': re.compile(r'[0-9a-f]{8,}-[0-9a-f]{8,}-[0-9a-f]{8,}-[0-9a-f]{8,}[0-9a-z-]{0,}', re.IGNORECASE),
    'oanda_account': re.compile(r'\b\d{3}-\d{3}-\d{8}-\d{3}\b'),
    'long_secret': re.compile(r'([A-Za-z0-9_\-]{24,})'),
}

IGNORE_PATHS = [
    '.git', 'node_modules', 'dist', 'logs', 'archives', 'backups', 
    'tmp', 'tmp_gemini_export', 'tmp_gemini_export_1764788208', 'export', 
    '.venv', '__pycache__', 'docs'
]

# Files that are expected to contain credentials and are gitignored
IGNORE_FILES = [
    '.env',           # Canonical credentials file (gitignored)
    'envv_new.env',   # Legacy env files to be cleaned up
    'env_new.env',
    'env_new2.env',
    'master.env',
    'master_paper_env.env',
    'paper_acct_env.env',
]

# Archival/conversation files that may contain historical credentials
IGNORE_PATTERNS = [
    'a_convo',
    'a_conversation',
    'no_wsl_days_conv',
    'narration.jsonl',
    'TASKJSON_DROPBOWNS',
    '_conv',
    '_conversation',
]

def search_file(p: Path):
    try:
        text = p.read_text(errors='ignore')
    except Exception:
        return []
    matches = []
    for name, pattern in PATTERNS.items():
        for m in pattern.finditer(text):
            # reduce false-positives: only capture long strings or OANDA like patterns
            if name == 'long_secret' and len(m.group(1)) < 32:
                continue
            matches.append((name, m.group(0)))
    return matches

def should_ignore(p: Path):
    for ig in IGNORE_PATHS:
        if ig in p.parts:
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description='Find likely-secrets in repository')
    parser.add_argument('--strict', action='store_true', help='Exit with non-zero code if high-confidence matches found (oanda_token|oanda_account)')
    args = parser.parse_args()
    base = Path('.')
    files = list(base.rglob('*'))
    total = 0
    all_found = []
    for f in files:
        if not f.is_file():
            continue
        if should_ignore(f):
            continue
        if f.suffix in ('.png', '.jpg', '.jpeg', '.gif', '.ppt', '.pdf', '.zip', '.tar', '.gz', '.log', '.db'):
            continue
        found = search_file(f)
        if found:
            print(f"File: {f}")
            for name, val in found:
                print(f"  - {name}: {val}")
            print("")
            total += len(found)
            all_found.extend([(nm, v, str(f)) for nm, v in found])
    if total == 0:
        print("No obvious secrets found (heuristic scan).")
    else:
        print(f"Scan complete: {total} potential secret matches found. Please review.")
        # In strict mode, only fail CI if we detect oanda account or token matches
        if args.strict:
            high_confidence = [m for m in all_found if m[0] in ('oanda_token', 'oanda_account')]
            if high_confidence:
                print('High confidence secrets found:')
                for t, v, path in high_confidence:
                    print(f"  - {t} at {path}: {v}")
                sys.exit(1)

if __name__ == '__main__':
    main()
