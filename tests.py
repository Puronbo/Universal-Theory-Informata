"""Tests for engine.py. Run: python tests.py"""
import math
from engine import (
    net_zero, ternarize, iterate, purge_if_flat,
    cusp_roots, bifurcation_value, on_cusp, crease_density_proxy,
    w_cpl, rho_lambda_ratio, check_predictions, DESI_REFERENCE,
    delta_norm, delta_derivative_present, Playhead,
    erosion_step,
    ANCHOR_DATE, MILESTONE_YEARS, milestone_date, years_since_anchor, milestone_reached,
    logistic,
    resonance_w0, impedance_series, schwinger_mass_gap, thirring_gn_mass_gap, grokking_delay,
    roll_orientation, roll_convert,
    stretched_distance, apparent_separation,
    strobe,
    search_text,
    collatz_spine_check, goldbach_check, zeta_partial,
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

def test_erosion_preserves_net_zero():
    s = [1, -1, 1, -1, 0]
    before = sum(s)
    out = erosion_step(s, pairs=2)
    assert sum(out) == before
    assert out.count(1) == 0 and out.count(-1) == 0

def test_erosion_partial():
    s = [1, 1, -1, 0]
    out = erosion_step(s, pairs=5)  # only one opposing pair
    assert out.count(1) == 1
    assert out.count(-1) == 0
    assert sum(out) == sum(s)

def test_timeline_anchor():
    assert ANCHOR_DATE.isoformat() == "2000-10-26"
    assert MILESTONE_YEARS == 26
    assert milestone_date().isoformat() == "2026-10-26"

def test_timeline_reached():
    from datetime import date
    assert milestone_reached(date(2026, 10, 27)) is True
    assert milestone_reached(date(2000, 10, 26)) is False

def test_logistic_fixed_point():
    # r=2.5 has stable fixed point at 1 - 1/r = 0.6
    x, steps, conv = iterate(logistic(2.5), 0.5)
    assert conv
    assert abs(x - 0.6) < 1e-9

def test_playhead_real_block():
    data = list(range(10))
    ph = Playhead(data, tau=2.0)
    assert ph.read(0.0) == 0
    assert ph.read(3.9) == 1  # floor(3.9/2)=1
    assert ph.read(100.0) == 9  # clamped

def test_impedance_resonance():
    R, L, C = 2.0, 1.0, 1.0
    w0 = resonance_w0(L, C)
    Z = impedance_series(R, L, C, w0)
    assert abs(Z.imag) < 1e-9
    assert abs(Z.real - R) < 1e-9

def test_schwinger_mass_gap():
    assert abs(schwinger_mass_gap(math.e) - math.e / math.sqrt(math.pi)) < 1e-12

def test_thirring_gn():
    M = thirring_gn_mass_gap(1.0, 1.0, 2.0)
    assert M > 0
    assert abs(M - 1.0 / math.sinh(2 * math.pi)) < 1e-9

def test_grokking_delay():
    assert abs(grokking_delay(2.0, 4.0, 2.0) - 0.5 * math.log(2.0)) < 1e-12

def test_roll_orientation():
    assert roll_orientation(0) == "photon"
    assert roll_orientation(90) == "dark_energy"
    assert roll_orientation(180) == "photon"
    assert roll_orientation(270) == "dark_energy"

def test_roll_convert_conservation():
    p, d = roll_convert(0.3, 1.0)
    assert abs(p + d - 1.0) < 1e-12
    assert p == 0.3 and d == 0.7

def test_stretched_distance():
    assert stretched_distance(2.0, 3.0) == 6.0
    assert stretched_distance(1.0, 1.0) == 1.0

def test_apparent_separation():
    pts = [0.0, 1.0, 3.0]
    out = apparent_separation(pts, 2.0)
    assert len(out) == 3
    assert out[0] == (0, 1, 2.0)
    assert out[2] == (1, 2, 4.0)

def test_strobe():
    sig = list(range(10))
    assert strobe(sig, 2) == [0, 2, 4, 6, 8]
    assert strobe(sig, 3) == [0, 3, 6, 9]
    try:
        strobe(sig, 0)
        assert False
    except ValueError:
        pass

def test_search_text():
    res = search_text(".", "Rolling-Fold", include="*.md")
    assert len(res) > 0
    assert any("CONNECTIONS" in r[0] or "AXIOMS" in r[0] for r in res)

def test_collatz_spine():
    for k in range(10):
        assert collatz_spine_check(k)

def test_goldbach():
    for n in [4, 6, 8, 10, 100, 1000]:
        assert goldbach_check(n)

def test_zeta_partial():
    # zeta(2) partial should approach pi^2/6 ~ 1.6449
    val = zeta_partial(2.0, 10000)
    assert abs(val - (math.pi**2 / 6.0)) < 1e-3

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
