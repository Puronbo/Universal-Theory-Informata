"""Tests for model.self_looping."""

import math

import pytest

from model import cosmological_coupling, portal_journey, uv_ir_inversion


def test_cosmological_coupling():
    assert cosmological_coupling(10.0, 2.0) == 10.0
    assert cosmological_coupling(5.0, 1.0) == 0.0
    assert cosmological_coupling(5.0, 1.5) == 2.5


def test_uv_ir_inversion():
    assert uv_ir_inversion(2.0) == 0.5
    assert uv_ir_inversion(0.5) == 2.0
    assert uv_ir_inversion(1.0) == 1.0


@pytest.mark.parametrize("bad", [0.0, -1.0, math.inf, -math.inf, math.nan])
def test_uv_ir_inversion_rejects_non_positive_or_non_finite(bad):
    with pytest.raises(ValueError):
        uv_ir_inversion(bad)


def test_portal_journey():
    r0 = portal_journey(0.0)
    r1 = portal_journey(0.25)
    r2 = portal_journey(0.75)
    assert r0["phase"] == "compression"
    assert r2["phase"] == "expansion"
    assert r1["scale"] >= 0

    r_mid = portal_journey(0.5)
    assert r_mid["phase"] == "inversion"
    assert r_mid["scale"] == float("inf")


def test_portal_journey_normalizes_by_duration():
    short = portal_journey(0.25)
    long = portal_journey(0.5, T=2.0)
    assert short["phase"] == long["phase"] == "compression"
    assert short["scale"] == pytest.approx(long["scale"])


@pytest.mark.parametrize("t", [-0.1, 1.1, math.inf, math.nan])
def test_portal_journey_rejects_out_of_domain(t):
    with pytest.raises(ValueError):
        portal_journey(t)


@pytest.mark.parametrize("duration", [0.0, -1.0, math.inf, math.nan])
def test_portal_journey_rejects_bad_duration(duration):
    with pytest.raises(ValueError):
        portal_journey(0.5, T=duration)
