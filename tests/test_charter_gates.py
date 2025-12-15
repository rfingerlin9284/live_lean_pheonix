#!/usr/bin/env python3
"""Charter gate smoke tests.

This file exists primarily to support the VS Code task "Run Charter Gate Tests".
It should stay lightweight and offline (no broker calls).
"""

from foundation.rick_charter import RickCharter
from foundation.agent_charter import AgentCharter


def test_rick_charter_import_validation_passes():
    # Import-time validation already ran; this asserts the module is in a good state.
    assert RickCharter.validate() is True


def test_rick_charter_core_constants_sane():
    assert RickCharter.validate_pin(841921) is True
    assert RickCharter.MIN_NOTIONAL_USD in (10000, 15000)
    assert RickCharter.MIN_EXPECTED_PNL_USD in (35.0, 100.0)
    assert RickCharter.validate_timeframe("M15") is True
    assert RickCharter.validate_timeframe("M1") is False


def test_agent_charter_enforce_does_not_raise():
    # Should raise only if the repo violates charter rules.
    AgentCharter.enforce()


if __name__ == "__main__":
    # Allow running as a plain python script (used as a fallback in the VS Code task).
    RickCharter.validate("test")
    AgentCharter.enforce()
    print("OK")
