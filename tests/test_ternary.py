"""Tests for model.ternary."""
from model import ACTIVE, BALANCE, VOID, is_valid_state, net_zero, ternarize, ternary_compose


def test_ternary_net_zero():
    assert net_zero([1, -1, 0])
    assert net_zero([1, 1, -1, -1])
    assert not net_zero([1, 1, 0])


def test_ternarize():
    assert ternarize(0.9) == ACTIVE
    assert ternarize(-0.9) == BALANCE
    assert ternarize(0.0) == VOID


def test_is_valid_state():
    assert is_valid_state(VOID)
    assert is_valid_state(ACTIVE)
    assert is_valid_state(BALANCE)
    assert not is_valid_state(2)
    assert not is_valid_state(-2)


def test_ternary_compose():
    assert ternary_compose([1, 1, -1, -1]) == 0.0
    assert ternary_compose([1, 1, 1]) == 1.0
    assert ternary_compose([]) == 0.0
    assert ternary_compose([-1, -1]) == -1.0
    # Clamping
    assert ternary_compose([1, 1, 1, 1, 1]) == 1.0
    assert ternary_compose([-1, -1, -1, -1, -1]) == -1.0
