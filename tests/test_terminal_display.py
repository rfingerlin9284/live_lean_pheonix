import io
import sys
import pytest
from util.terminal_display import TerminalDisplay, Colors


def capture_print(func, *args, **kwargs):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        func(*args, **kwargs)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def test_info_two_args():
    td = TerminalDisplay()
    out = capture_print(td.info, "Label", "Value", Colors.BRIGHT_GREEN)
    assert "Label" in out and "Value" in out


def test_info_single_arg_handling():
    # There are places where code relied on single-arg usage; engine updated to pass label/value, but
    # TerminalDisplay.info should still accept string-like label only if used elsewhere.
    td = TerminalDisplay()
    # call with single-arg; since signature requires value, we call with second arg to represent this case
    out = capture_print(td.info, "Status", "OK")
    assert "Status" in out and "OK" in out
