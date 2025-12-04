import os
import re
from pathlib import Path
import importlib

from foundation.rick_charter import RickCharter as FoundationCharter
from oanda.foundation.rick_charter import RickCharter as OandaCharter
from rick_hive.rick_charter import RickCharter as HiveCharter


def test_foundation_min_expected_pnl():
    assert FoundationCharter.MIN_EXPECTED_PNL_USD == 35.0, "Foundation charter MIN_EXPECTED_PNL_USD must be 35.0"


def test_oanda_min_expected_pnl():
    assert OandaCharter.MIN_EXPECTED_PNL_USD == 35.0, "OANDA charter MIN_EXPECTED_PNL_USD must be 35.0"


def test_rick_hive_min_expected_pnl():
    assert HiveCharter.MIN_EXPECTED_PNL_USD == 35.0, "Rick Hive charter MIN_EXPECTED_PNL_USD must be 35.0"


def test_no_100_fallback_in_code():
    # Scan project files for the string '100.0' used as fallback in MIN_EXPECTED_PNL
    root = Path(".")
    files = [p for p in root.rglob("*.py") if "tests" not in str(p)]
    pattern = re.compile(r"MIN_EXPECTED_PNL_USD.*100\.0|MIN_EXPECTED_PNL_USD.*=\s*100\.0|os\.getenv\(\"MIN_EXPECTED_PNL_USD\",\s*\"100\.0\"\)")
    matches = []
    for f in files:
        try:
            txt = f.read_text()
        except Exception:
            continue
        if pattern.search(txt):
            matches.append(str(f))
    assert not matches, f"Found code files using 100.0 fallback: {matches}"
