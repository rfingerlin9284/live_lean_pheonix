#!/usr/bin/env python3
import os
import stat
import subprocess
import tempfile
from pathlib import Path

def test_lock_secrets_tmpfile(tmp_path):
    p = tmp_path / '.env.test'
    p.write_text('TEST=1')
    # Create in workspace rather than root intentionally
    cwd = os.getcwd()
    try:
        os.chdir(str(tmp_path))
        # Use the script from ops. Copy it into temp path
        script_src = Path(cwd) / 'ops' / 'lock_secrets.sh'
        script_dst = tmp_path / 'lock_secrets.sh'
        script_dst.write_text(script_src.read_text())
        script_dst.chmod(0o755)
        # Run the script
        subprocess.check_call([str(script_dst)])
        # Check file permission
        st = p.stat().st_mode
        assert stat.S_IMODE(st) & 0o777 == 0o600
    finally:
        os.chdir(cwd)
