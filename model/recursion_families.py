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
