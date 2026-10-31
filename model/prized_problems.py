"""Prized-problem numerical sectors (evidence only, not proofs)."""

from __future__ import annotations

import math
from functools import lru_cache


def collatz_spine_sum(k: int) -> int:
    """spineSum(k) = (4^(k+1) - 1) / 3."""
    if k < 0:
        raise ValueError("k must be >= 0")
    result: int = (4 ** (k + 1) - 1) // 3
    return result


def collatz_spine_check(k: int) -> bool:
    """Verify 4^(k+1) == 3*spineSum(k) + 1."""
    lhs: int = 4 ** (k + 1)
    rhs: int = 3 * collatz_spine_sum(k) + 1
    return lhs == rhs


@lru_cache(maxsize=64)
def _primes_below(n: int) -> tuple[int, ...]:
    """All primes p with 2 <= p < n (memoized sieve)."""
    if n < 3:
        return ()
    sieve = bytearray(b"\x01") * n
    sieve[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(n - 1) + 1):
        if sieve[i]:
            sieve[i * i : n : i] = b"\x00" * (((n - 1 - i * i) // i) + 1)
    return tuple(i for i in range(2, n) if sieve[i])


def goldbach_check(n: int) -> bool:
    """Check Goldbach for even n >= 4: n = p + q with primes p,q."""
    if n < 4 or n % 2 != 0:
        return False
    pset = set(_primes_below(n))
    for p in pset:
        if p > n // 2:
            continue
        if (n - p) in pset:
            return True
    return False


def zeta_partial(s: float, N: int) -> float:
    """Partial sum sum_{n=1}^N 1/n^s (real s)."""
    if N < 0:
        raise ValueError("N must be >= 0")
    total: float = sum(1.0 / (n**s) for n in range(1, N + 1))
    return total
