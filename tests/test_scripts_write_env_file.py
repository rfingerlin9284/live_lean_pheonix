#!/usr/bin/env python3
from pathlib import Path
import os


def test_write_env_script_exists_and_exec():
    p = Path('scripts/write_env_file.sh')
    assert p.exists(), 'write_env_file.sh must exist'
    assert p.stat().st_mode & 0o111, 'write_env_file.sh must be executable'


def test_write_env_script_dry_run(tmp_path):
    # Copy script into a temp dir and run with --dry-run to ensure it does not write files
    import subprocess
    cwd = Path.cwd()
    try:
        os.chdir(str(tmp_path))
        script_src = Path(cwd) / 'scripts' / 'write_env_file.sh'
        script_dst = tmp_path / 'write_env_file.sh'
        script_dst.write_text(script_src.read_text())
        script_dst.chmod(0o755)
        # Run dry run
        out = subprocess.check_output([str(script_dst), '.env.oanda_only', '.env', '--dry-run'], stderr=subprocess.STDOUT)
        out_text = out.decode('utf-8')
        assert 'DRY RUN' in out_text or 'preview' in out_text
        # Ensure files are not created
        assert not (tmp_path / '.env.oanda_only').exists()
        assert not (tmp_path / '.env').exists()
    finally:
        os.chdir(str(cwd))


def test_write_env_script_no_lock(tmp_path):
    import subprocess
    cwd = Path.cwd()
    try:
        os.chdir(str(tmp_path))
        script_src = Path(cwd) / 'scripts' / 'write_env_file.sh'
        script_dst = tmp_path / 'write_env_file.sh'
        script_dst.write_text(script_src.read_text())
        script_dst.chmod(0o755)
        # Run with --no-lock
        out = subprocess.check_output([str(script_dst), '.env.oanda_only', '.env', '--no-lock'], stderr=subprocess.STDOUT)
        out_text = out.decode('utf-8')
        assert 'Skipping ops/lock_secrets.sh' in out_text or 'Skipping permission hardening' in out_text
        # Basic assertion: script reported skipping lock steps and completed
        assert 'Skipping ops/lock_secrets.sh' in out_text or 'Skipping permission hardening' in out_text
    finally:
        os.chdir(str(cwd))
