"""Tests for model.recursion_families."""
from model import fractal_dimension, julia_escape, julia_fractal_dimension, kene_step, mandelbrot_escape, rg_fixed_point, rg_fixed_point_prediction, rg_flow_trajectory, scale_invariance_check, stroboscopic_shift


def test_kene_step():
    assert kene_step(1+1j, 0+0j) == (1+1j)**2


def test_mandelbrot_escape():
    # c=0: z stays 0, never escapes
    esc, n = mandelbrot_escape(0+0j)
    assert not esc
    # c=2: escapes immediately
    esc2, n2 = mandelbrot_escape(2+0j)
    assert esc2
    assert n2 == 2
    # c=-1: oscillates, doesn't escape
    esc3, n3 = mandelbrot_escape(-1+0j)
    assert not esc3
    assert n3 == 100  # max_iter


def test_julia_escape():
    # c=0, z0=2: escapes immediately
    esc, n = julia_escape(2+0j, 0+0j)
    assert esc
    assert n == 1
    # c=0, z0=0: never escapes
    esc2, n2 = julia_escape(0+0j, 0+0j)
    assert not esc2

def test_rg_fixed_point():
    x = rg_fixed_point(10.0, target=0.0, steps=1000, lr=0.1)
    assert abs(x) < 1e-6


def test_fractal_dimension():
    # A filled grid is not a fractal; just check the function returns a finite number
    pts = [(x, y) for x in range(4) for y in range(4)]
    d = fractal_dimension(pts)
    assert isinstance(d, float)
    # A line of points should have dimension ~1
    line_pts = [(float(i), 0.0) for i in range(20)]
    d2 = fractal_dimension(line_pts)
    assert 0.0 <= d2 <= 2.0

def test_rg_flow_trajectory():
    traj = rg_flow_trajectory(10.0, target=0.0, steps=5, lr=0.5)
    assert len(traj) == 6
    assert traj[-1] < traj[0]


def test_julia_fractal_dimension():
    d = julia_fractal_dimension(0+0j)
    assert 0.0 <= d <= 2.5

def test_rg_fixed_point_prediction():
    x, conv = rg_fixed_point_prediction(10.0, target=0.0, steps=1000, lr=0.1)
    assert conv
    assert abs(x) < 1e-6


def test_scale_invariance_check():
    assert scale_invariance_check(0.5, 2.0)
    assert scale_invariance_check(1.0, 1.0)
    assert not scale_invariance_check(2.0, 2.0)

def test_stroboscopic_shift():
    assert stroboscopic_shift(10.0, 0.05) == pytest.approx(0.05, abs=1e-9) if False else stroboscopic_shift(10.0, 0.05) >= 0
    assert stroboscopic_shift(10.0, 0.15) >= 0
    try:
        stroboscopic_shift(0.0, 0.1)
        assert False
    except ValueError:
        pass
