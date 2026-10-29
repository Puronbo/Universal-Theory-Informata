"""Tests for model.self_looping."""
from model import cosmological_coupling, portal_journey, uv_ir_inversion


def test_cosmological_coupling():
    assert cosmological_coupling(10.0, 2.0) == 10.0
    assert cosmological_coupling(5.0, 1.0) == 0.0
    assert cosmological_coupling(5.0, 1.5) == 2.5


def test_uv_ir_inversion():
    assert uv_ir_inversion(2.0) == 0.5
    assert uv_ir_inversion(0.5) == 2.0
    assert uv_ir_inversion(1.0) == 1.0
    try:
        uv_ir_inversion(0.0)
        raise AssertionError()
    except ValueError:
        pass
    try:
        uv_ir_inversion(-1.0)
        raise AssertionError()
    except ValueError:
        pass


def test_portal_journey():
    r0 = portal_journey(0.0)
    r1 = portal_journey(0.25)
    r2 = portal_journey(0.75)
    assert r0["phase"] == "compression"
    assert r2["phase"] == "expansion"
    assert r1["scale"] >= 0

    # Test inversion point
    r_mid = portal_journey(0.5)
    assert r_mid["phase"] == "inversion"
    assert r_mid["scale"] == float("inf")
