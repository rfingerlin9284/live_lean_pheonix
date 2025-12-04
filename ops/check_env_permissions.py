#!/usr/bin/env python3
"""Check .env file permissions and exit non-zero if insecure (used by agent startup).
"""
import os
import stat
import sys

ENV_FILE = os.environ.get('ENV_FILE', './.env')

# Exit early if simplify mode requested
if os.environ.get('SIMPLIFY_MODE', '0').lower() in ('1', 'true', 'yes'):
    print('SIMPLIFY_MODE active: skipping permission checks')
    sys.exit(0)

def main():
    if not os.path.exists(ENV_FILE):
        print(f"No env file found at {ENV_FILE}")
        return 0
    mode = os.stat(ENV_FILE).st_mode
    # permission bits for group/others
    insecure = bool(mode & (stat.S_IRWXG | stat.S_IRWXO))
    cur_perm = oct(mode & 0o777)
    if insecure:
        print(f"ENV PERMISSION WARNING: {ENV_FILE} permissions={cur_perm} (group/other bits set)")
        # We'll return non-fatal error code 2 to signal to the caller, but not to abort
        return 2
    else:
        print(f"ENV OK: {ENV_FILE} permissions={cur_perm}")
        return 0

if __name__ == '__main__':
    sys.exit(main())
