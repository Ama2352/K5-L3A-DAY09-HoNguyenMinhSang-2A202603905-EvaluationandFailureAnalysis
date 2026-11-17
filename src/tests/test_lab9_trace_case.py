"""Replay the trace case against the locked Day 8 host."""
import pytest
from lab9.trace_case import investigate

pytestmark = pytest.mark.student


def test_lab9_c002_rejects_ticket_override_and_fixed_keeps_db():
    broken = investigate('seeded_regression', 'C-002', 11)['trial']
    fixed = investigate('fixed', 'C-002', 11)['trial']
    assert broken['events'][2]['kind'] == 'model_override'
    assert broken['events'][2]['payload']['delay_days'] == 5
    assert broken['snapshot']['refund_vnd'] == 20000
    assert broken['lab8_pass'] is False
    assert all(e['kind'] != 'model_override' for e in fixed['events'])
    assert fixed['snapshot']['refund_vnd'] == 0
    assert fixed['result']['status'] == 'denied'
    assert fixed['lab8_pass'] is True
