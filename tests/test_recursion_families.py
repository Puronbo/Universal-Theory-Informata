"""Tests for model.recursion_families."""
from model import kene_step, mandelbrot_escape


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
