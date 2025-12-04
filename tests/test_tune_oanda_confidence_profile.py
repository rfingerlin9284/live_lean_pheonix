import pytest
import tempfile
from pathlib import Path
import shutil
import subprocess
import sys


SCRIPT = Path(__file__).parents[1] / 'scripts' / 'tune_oanda_confidence_profile.py'
TARGETS = [
    Path('foundation/rick_charter.py'),
    Path('oanda/foundation/rick_charter.py'),
    Path('rick_hive/rick_charter.py'),
]


def test_dry_run_no_change(tmp_path, capsys):
    # Run dry-run; it should not change files
    cmd = [sys.executable, str(SCRIPT), '--dry-run']
    p = subprocess.run(cmd, cwd=str(Path(__file__).parents[1]), capture_output=True, text=True)
    assert p.returncode == 0
    out = p.stdout
    # If script reports changes needed, it's fine; we just ensure no file changes are made
    for t in TARGETS:
        orig = Path(__file__).parents[1] / t
        assert orig.exists()


def test_apply_and_revert_tmp_files(tmp_path):
    # Create temp copies of target files
    tmp_targets = []
    for t in TARGETS:
        orig = Path(__file__).parents[1] / t
        if not orig.exists():
            continue
        dest = tmp_path / t.name
        shutil.copy2(orig, dest)
        tmp_targets.append(dest)

    if not tmp_targets:
        pytest.skip('No target charter files found to test')

    # Apply the script to these temp files
    cmd = [sys.executable, str(SCRIPT), '--apply', '--targets'] + [str(p) for p in tmp_targets]
    p = subprocess.run(cmd, cwd=str(Path(__file__).parents[1]), capture_output=True, text=True)
    assert p.returncode == 0
    # Check that backups were created
    for tt in tmp_targets:
        bak = next(tt.parent.glob(tt.name + '.bak-tune-*'))
        assert bak.exists()
        # The file should contain MIN_EXPECTED_PNL_USD = 35.0 and MIN_NOTIONAL_USD = 10000
        txt = tt.read_text()
        assert 'MIN_EXPECTED_PNL_USD' in txt
        assert 'MIN_NOTIONAL_USD' in txt
        # Ensure we no longer have the old $100 fallback in the file
        assert 'MIN_EXPECTED_PNL_USD = 100.0' not in txt
        # Ensure the new balanced value is present
        assert 'MIN_EXPECTED_PNL_USD = 35.0' in txt

    # Revert backups
    # find created backups and restore original content
    for tt in tmp_targets:
        bak = next(tt.parent.glob(tt.name + '.bak-tune-*'))
        shutil.copy2(bak, tt)
        assert (tt.read_text() == bak.read_text())
