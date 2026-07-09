"""
tests/test_decision_engine.py
Basic unit tests for the risk manager and position sizing logic.
These do not require live network access or real API keys.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from risk.position_size import calculate_position_size


def test_position_size_zero_stop_loss():
    assert calculate_position_size(1000, 0) == 0.0


def test_position_size_positive():
    size = calculate_position_size(account_balance=1000, stop_loss_pips=50, pip_value=1.0)
    assert size >= 0


def test_position_size_scales_with_balance():
    small = calculate_position_size(1000, 50)
    large = calculate_position_size(10000, 50)
    assert large >= small
