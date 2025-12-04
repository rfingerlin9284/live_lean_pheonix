#!/usr/bin/env python3
import os
import pytest

from foundation.agent_charter import AgentCharter


def test_agent_charter_enforce_skip_permissions(monkeypatch, tmp_path):
    # Ensure that when SIMPLIFY_MODE is set, enforce() skips permission check and does not raise.
    monkeypatch.setenv('SIMPLIFY_MODE', '1')
    # Should not raise even if no .env file exists or if perms are insecure
    AgentCharter.enforce()


def test_agent_charter_enforce_normal(monkeypatch):
    # When SIMPLIFY_MODE is not set, enforce still runs but should not raise if default conditions met
    monkeypatch.delenv('SIMPLIFY_MODE', raising=False)
    AgentCharter.enforce()
