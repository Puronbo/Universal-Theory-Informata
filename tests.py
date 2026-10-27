"""Tests for engine.py. Run: python tests.py"""
import math
from engine import (
    net_zero, ternarize, iterate, purge_if_flat,
    cusp_roots, bifurcation_value, on_cusp, crease_density_proxy,
    w_cpl, rho_lambda_ratio, check_predictions, DESI_REFERENCE,
    delta_norm, delta_derivative_present, Playhead,
)

def test_ternary_net_zero():
    assert net_zero([1, -1, 0])
    assert net_zero([1, 1, -1, -1])
    assert not net_zero([1, 1, 0])

def test_ternarize():
    assert ternarize(0.9) == 1
    assert ternarize(-0.9) == -1
    assert ternarize(0.0) == 0

def test_iterate_fixed_point():
    x, steps, conv = iterate(lambda x: math.cos(x), 1.0)
    assert conv
    assert abs(x - 0.7390851332151607) < 1e-9

def test_iterate_no_converge_finite():
    x, steps, conv = iterate(lambda x: x + 1.0, 0.0, n=5)
    assert not conv
    assert steps == 5

def test_purge_flat():
    assert purge_if_flat([1.0, 1.0])
    assert not purge_if_flat([1.0, 2.0])

def test_cusp_bifurcation():
    # on cusp: 8a^3 = 27b^2 -> e.g. a=3, b=2*sqrt? let's use a= (27/8)^{1/3}... use known: a=3, b=2*sqrt(2)? 8*27=216, 27*8=216 yes b^2=8 -> b=2*sqrt2
    a, b = 3.0, 2*math.sqrt(2)
    assert on_cusp(a, b)
    assert abs(bifurcation_value(a, b)) < 1e-9

def test_cusp_three_real_roots_inside():
    # inside cusp: bifurcation_value > 0 (three real roots)
    a, b = 3.0, 1.0
    assert bifurcation_value(a, b) > 0
    roots = cusp_roots(a, b)
    assert all(abs(r.imag) < 1e-9 for r in roots)

def test_cusp_one_real_root_outside():
    a, b = 1.0, 3.0
    assert bifurcation_value(a, b) < 0
    roots = cusp_roots(a, b)
    real_count = sum(1 for r in roots if abs(r.imag) < 1e-9)
    assert real_count == 1

def test_crease_density_proxy():
    rho = crease_density_proxy(3.0, 1.0, [1.88, -0.35, 5.0], eps=0.05)
    assert 0.0 <= rho <= 1.0
    assert rho > 0.0

def test_w_cpl_lambda():
    # Lambda: w0=-1, wa=0 -> w=-1 everywhere
    assert abs(w_cpl(0.3, -1.0, 0.0) + 1.0) < 1e-12
    assert abs(w_cpl(1.0, -1.0, 0.0) + 1.0) < 1e-12

def test_rho_lambda_lambda_constant():
    # For Lambda, rho(z)/rho0 = 1 for all z
    for z in [0.0, 0.5, 1.0, 2.0]:
        assert abs(rho_lambda_ratio(z, -1.0, 0.0) - 1.0) < 1e-9

def test_check_predictions_quintom():
    r = check_predictions(-0.75, -0.87, 0.058, 0.25)
    assert r["quintom_B_quadrant"] is True
    assert r["P3_phantom_sign_flip_needed"] is False

def test_check_predictions_phantom():
    r = check_predictions(-1.2, -0.5, 0.1, 0.2)
    assert r["P3_phantom_sign_flip_needed"] is True

def test_desi_reference_ranges():
    lo, hi = DESI_REFERENCE["w0_range"]
    assert lo < hi
    lo2, hi2 = DESI_REFERENCE["wa_range"]
    assert lo2 < hi2 < 0

def test_delta_norm_present_zero():
    assert abs(delta_norm(0.0, -0.75, -0.87)) < 1e-12

def test_delta_norm_past_positive_quintom():
    assert delta_norm(1.0, -0.75, -0.87) > 0.0

def test_delta_derivative_present_positive():
    assert delta_derivative_present(-0.75, -0.87) > 0.0

def test_playhead_index_and_step():
    ph = Playhead(["a", "b", "c"], tau=1.0)
    assert ph.read(0.0) == "a"
    assert ph.read(0.5) == "a"
    assert ph.read(1.0) == "b"
    assert ph.read(10.0) == "c"  # clamped
    assert ph.step() == "a"
    assert ph.step() == "b"
    assert ph.step() == "c"
    assert ph.step() is None

def test_playhead_read_all():
    ph = Playhead([1, 2, 3])
    assert ph.read_all() == [1, 2, 3]
    assert ph.index == 3

if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except Exception as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests)-failed}/{len(tests)} passed")
    if failed:
        raise SystemExit(1)
