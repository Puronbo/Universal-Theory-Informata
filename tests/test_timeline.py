"""Tests for model.timeline."""
from datetime import date

from model import (
    ANCHOR_DATE,
    MILESTONE_YEARS,
    logistic,
    milestone_date,
    milestone_reached,
    years_since_anchor,
)


def test_timeline_anchor():
    assert ANCHOR_DATE.isoformat() == "2000-10-26"
    assert MILESTONE_YEARS == 26
    assert milestone_date().isoformat() == "2026-10-26"


def test_timeline_reached():
    assert milestone_reached(date(2026, 10, 27)) is True
    assert milestone_reached(date(2000, 10, 26)) is False
    assert milestone_reached(date(2026, 10, 26)) is True


def test_years_since_anchor():
    assert abs(years_since_anchor(date(2001, 10, 26)) - 1.0) < 0.01


def test_logistic_fixed_point():
    from model import iterate
    # r=2.5 has stable fixed point at 1 - 1/r = 0.6
    x, steps, conv, _ = iterate(logistic(2.5), 0.5)
    assert conv
    assert abs(x - 0.6) < 1e-9


def test_logistic_function():
    f = logistic(2.0)
    assert f(0.5) == 0.5
    assert f(0.0) == 0.0
    assert f(1.0) == 0.0
