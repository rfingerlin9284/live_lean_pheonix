#!/usr/bin/env python3
"""CLI to toggle a single venue on/off.

Examples:
  python3 tools/set_platform_breaker.py oanda on
  python3 tools/set_platform_breaker.py coinbase off "Coinbase API down"
  python3 tools/set_platform_breaker.py ibkr status
"""

from __future__ import annotations

import sys
from util.platform_breaker import load_breakers, set_platform_enabled


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('usage: set_platform_breaker.py <oanda|coinbase|ibkr> <on|off|status> [reason]')
        return 2

    platform = argv[1].lower()
    action = (argv[2].lower() if len(argv) >= 3 else 'status')
    reason = ' '.join(argv[3:]).strip() if len(argv) >= 4 else ''

    if action == 'status':
        br = load_breakers()
        st = br.get(platform)
        if st is None:
            print(f'{platform}: enabled=True (default)')
            return 0
        print(f"{platform}: enabled={st.enabled} updated_utc={st.updated_utc} reason={st.reason}")
        return 0

    if action in ('on', 'enable', 'enabled', 'true', '1'):
        set_platform_enabled(platform, True, reason=reason)
        print(f'{platform}: ENABLED')
        return 0

    if action in ('off', 'disable', 'disabled', 'false', '0'):
        set_platform_enabled(platform, False, reason=reason or 'manual_disable')
        print(f'{platform}: DISABLED')
        return 0

    print('unknown action:', action)
    return 2


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
