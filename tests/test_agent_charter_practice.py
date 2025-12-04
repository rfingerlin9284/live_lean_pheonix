#!/usr/bin/env python3
import os
import importlib

from foundation.agent_charter import AgentCharter


def test_practice_disallowed_by_default(monkeypatch):
    monkeypatch.delenv('ALLOW_PRACTICE_ORDERS', raising=False)
    monkeypatch.delenv('CONFIRM_PRACTICE_ORDER', raising=False)
    monkeypatch.delenv('PRACTICE_PIN', raising=False)
    assert not AgentCharter.practice_allowed()


def test_practice_requires_confirm(monkeypatch):
    monkeypatch.setenv('ALLOW_PRACTICE_ORDERS', '1')
    monkeypatch.delenv('CONFIRM_PRACTICE_ORDER', raising=False)
    monkeypatch.setenv('PRACTICE_PIN', '841921')
    assert not AgentCharter.practice_allowed()


def test_practice_requires_pin_when_required(monkeypatch):
    monkeypatch.setenv('ALLOW_PRACTICE_ORDERS', '1')
    monkeypatch.setenv('CONFIRM_PRACTICE_ORDER', '1')
    monkeypatch.delenv('PRACTICE_PIN', raising=False)
    assert not AgentCharter.practice_allowed()


def test_practice_allowed_with_env_pin(monkeypatch):
    monkeypatch.setenv('ALLOW_PRACTICE_ORDERS', '1')
    monkeypatch.setenv('CONFIRM_PRACTICE_ORDER', '1')
    monkeypatch.setenv('PRACTICE_PIN', str(AgentCharter.PIN))
    assert AgentCharter.practice_allowed()


def test_practice_allowed_with_pin_argument(monkeypatch):
    monkeypatch.setenv('ALLOW_PRACTICE_ORDERS', '1')
    monkeypatch.setenv('CONFIRM_PRACTICE_ORDER', '1')
    monkeypatch.delenv('PRACTICE_PIN', raising=False)
    assert AgentCharter.practice_allowed(pin=int(AgentCharter.PIN))


def test_practice_allowed_with_env_flag(monkeypatch):
    monkeypatch.setenv('ALLOW_PRACTICE_ORDERS', '1')
    monkeypatch.setenv('CONFIRM_PRACTICE_ORDER', '1')
    # Skip the PIN requirement via PRACTICE_TRADING_ALLOWED
    monkeypatch.setenv('PRACTICE_TRADING_ALLOWED', '1')
    monkeypatch.delenv('PRACTICE_PIN', raising=False)
    assert AgentCharter.practice_allowed()
