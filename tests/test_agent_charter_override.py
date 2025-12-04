#!/usr/bin/env python3
import os
import time
import hmac
import hashlib
from foundation.agent_charter import AgentCharter

def make_token(secret: str, ts: int) -> str:
    return hmac.new(secret.encode('utf-8'), msg=str(ts).encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

def test_override_token_success(monkeypatch, tmp_path):
    secret = 'testsecret'
    ts = int(time.time())
    token = make_token(secret, ts)
    monkeypatch.setenv('UNLOCK_SECRET', secret)
    monkeypatch.setenv('PROTOCOL_UNCHAINED', '1')
    monkeypatch.setenv('PROTOCOL_UNCHAINED_TS', str(ts))
    monkeypatch.setenv('PROTOCOL_UNCHAINED_TOKEN', token)
    monkeypatch.setenv('ALLOW_PRACTICE_ORDERS', '1')
    monkeypatch.setenv('CONFIRM_PRACTICE_ORDER', '1')
    assert AgentCharter._verify_unlocked_token() is True
    # Also ensure practice_allowed returns True
    assert AgentCharter.practice_allowed() is True

def test_override_token_expired(monkeypatch):
    secret = 'testsecret'
    ts = int(time.time()) - 10000
    token = make_token(secret, ts)
    monkeypatch.setenv('UNLOCK_SECRET', secret)
    monkeypatch.setenv('PROTOCOL_UNCHAINED', '1')
    monkeypatch.setenv('PROTOCOL_UNCHAINED_TS', str(ts))
    monkeypatch.setenv('PROTOCOL_UNCHAINED_TOKEN', token)
    monkeypatch.setenv('ALLOW_PRACTICE_ORDERS', '1')
    monkeypatch.setenv('CONFIRM_PRACTICE_ORDER', '1')
    assert AgentCharter._verify_unlocked_token() is False

def test_override_token_invalid(monkeypatch):
    secret = 'testsecret'
    ts = int(time.time())
    token = 'deadbeef'
    monkeypatch.setenv('UNLOCK_SECRET', secret)
    monkeypatch.setenv('PROTOCOL_UNCHAINED', '1')
    monkeypatch.setenv('PROTOCOL_UNCHAINED_TS', str(ts))
    monkeypatch.setenv('PROTOCOL_UNCHAINED_TOKEN', token)
    monkeypatch.setenv('ALLOW_PRACTICE_ORDERS', '1')
    monkeypatch.setenv('CONFIRM_PRACTICE_ORDER', '1')
    assert AgentCharter._verify_unlocked_token() is False

def test_override_writes_log(monkeypatch, tmp_path):
    secret = 'testsecret'
    ts = int(time.time())
    token = hmac.new(secret.encode('utf-8'), msg=str(ts).encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
    monkeypatch.setenv('UNLOCK_SECRET', secret)
    monkeypatch.setenv('PROTOCOL_UNCHAINED', '1')
    monkeypatch.setenv('PROTOCOL_UNCHAINED_TS', str(ts))
    monkeypatch.setenv('PROTOCOL_UNCHAINED_TOKEN', token)
    monkeypatch.setenv('ALLOW_PRACTICE_ORDERS', '1')
    monkeypatch.setenv('CONFIRM_PRACTICE_ORDER', '1')
    # Monkeypatch audit log path to tmp
    monkeypatch.setattr(AgentCharter, 'OVERRIDE_AUDIT_LOG', str(tmp_path / 'override_audit.log'))
    assert AgentCharter._verify_unlocked_token() is True
    # Verify log file was written
    p = tmp_path / 'override_audit.log'
    assert p.exists()
    content = p.read_text()
    assert 'OVERRIDE' in content
