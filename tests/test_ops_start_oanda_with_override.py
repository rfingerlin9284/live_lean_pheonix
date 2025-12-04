#!/usr/bin/env python3
import os
from pathlib import Path


def test_start_script_exists_and_executable():
    p = Path('ops/start_oanda_with_override.sh')
    assert p.exists()
    assert p.stat().st_mode & 0o111, 'start_oanda_with_override.sh is not executable'
