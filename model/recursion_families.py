"""Recursion families (R4): Mandelbrot / Kené-style complex iteration."""

from __future__ import annotations


def kene_step(z: complex, c: complex) -> complex:
    """One step of the Kené/Mandelbrot-style recursion: z -> z^2 + c."""
    return z * z + c


def mandelbrot_escape(c: complex, max_iter: int = 100, radius: float = 2.0) -> tuple[bool, int]:
    """Iterate z_{n+1}=z_n^2+c from z0=0; return (escaped, n)."""
    z = 0 + 0j
    for n in range(1, max_iter + 1):
        z = z * z + c
        if abs(z) > radius:
            return True, n
    return False, max_iter


def julia_escape(z0, c, max_iter=100, radius=2.0):
    """Iterate z -> z^2 + c from z0 (Julia set); return (escaped, n)."""
    z = z0
    for n in range(1, max_iter + 1):
        z = z * z + c
        if abs(z) > radius:
            return True, n
    return False, max_iter


def rg_fixed_point(g, target=0.0, steps=1000, lr=0.01):
    """Toy RG flow toward a fixed point."""
    x = g
    for _ in range(steps):
        x = x - lr * (x - target)
    return x
