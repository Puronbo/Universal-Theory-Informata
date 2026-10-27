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
    delta_norm_uncertainty, kene_step, mandelbrot_escape,
    attention_trace, conscious_moment, closure_check,
    multi_agent_step, network_closure,
    purge_derivative, canvas_energy, ternary_compose,
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
    x, steps, conv, _ = iterate(lambda x: math.cos(x), 1.0)
    assert conv
    assert abs(x - 0.7390851332151607) < 1e-9

def test_iterate_no_converge_finite():
    x, steps, conv, _ = iterate(lambda x: x + 1.0, 0.0, n=5)
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
    x, steps, conv, _ = iterate(logistic(2.5), 0.5)
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

def test_delta_norm_uncertainty():
    base, unc = delta_norm_uncertainty(-0.75, -0.87, 0.058, 0.25)
    assert unc >= 0
    assert base == delta_norm(1.0, -0.75, -0.87)

def test_mandelbrot_escape():
    # c=0: z stays 0, never escapes
    esc, n = mandelbrot_escape(0+0j)
    assert not esc
    # c=2: escapes immediately
    esc2, n2 = mandelbrot_escape(2+0j)
    assert esc2
    assert n2 == 2

def test_kene_step():
    assert kene_step(1+1j, 0+0j) == (1+1j)**2

def test_attention_trace():
    assert attention_trace([0.1, 0.8, -0.9, 0.0]) == [0, 1, -1, 0]

def test_conscious_moment():
    assert conscious_moment([1,2,3,4,5], 2) == [1, 3, 5]

def test_closure_check():
    assert closure_check([1.0, 2.0], [1.0, 2.0])
    assert not closure_check([1.0], [1.0, 2.0])

def test_multi_agent_step():
    agents = [[0, 0], [1, -1]]
    out = multi_agent_step(agents, [0.9], threshold=0.5, erosion_pairs=0)
    assert len(out) == 2
    assert out[0][-1] == 1
    assert out[1][-1] == 1

def test_network_closure():
    agents = [[1, -1], [1, 1]]
    frac = network_closure(agents)
    assert frac == 0.5

def test_purge_derivative():
    assert purge_derivative([1.0, 1.0, 1.0])
    assert not purge_derivative([1.0, 2.0, 3.0])

def test_canvas_energy():
    assert canvas_energy(2.0) == 0.5
    try:
        canvas_energy(0.0)
        assert False
    except ValueError:
        pass

def test_ternary_compose():
    assert ternary_compose([1, 1, -1, -1]) == 0.0
    assert ternary_compose([1, 1, 1]) == 1.0
    assert ternary_compose([]) == 0.0

def test_iterate_cycle_detection():
    # f(x)=1-x cycles with period 2
    x, steps, conv, cyc = iterate(lambda v: 1.0 - v, 0.0, detect_cycle=True)
    assert not conv
    assert cyc == 2

import random

def test_prop_erosion_preserves_sum():
    random.seed(0)
    for _ in range(200):
        n = random.randint(1, 12)
        states = [random.choice([-1, 0, 1]) for _ in range(n)]
        before = sum(states)
        out = erosion_step(states, pairs=random.randint(1, 5))
        assert sum(out) == before, (states, out)

def test_prop_strobe_length():
    random.seed(1)
    for _ in range(50):
        n = random.randint(1, 50)
        rate = random.randint(1, 7)
        sig = list(range(n))
        out = strobe(sig, rate)
        assert len(out) == (n + rate - 1) // rate

def test_prop_roll_convert_conservation():
    random.seed(2)
    for _ in range(100):
        cd = random.random()
        total = random.uniform(0.5, 2.0)
        p, d = roll_convert(cd, total)
        assert abs(p + d - total) < 1e-9

def test_prop_stretched_monotonic():
    for sf in [0.5, 1.0, 2.0, 10.0]:
        assert stretched_distance(3.0, sf) == 3.0 * sf

def test_prop_delta_zero_at_present():
    for w0, wa in [(-1.0, 0.0), (-0.75, -0.87), (-0.5, 0.5)]:
        assert abs(delta_norm(0.0, w0, wa)) < 1e-12

def test_prop_attention_trace_range():
    import random
    random.seed(3)
    for _ in range(50):
        stim = [random.uniform(-2, 2) for _ in range(20)]
        tr = attention_trace(stim)
        assert all(v in (-1, 0, 1) for v in tr)

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
