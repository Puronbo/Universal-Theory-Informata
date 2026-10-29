"""Prized-problem numerical sectors (evidence only, not proofs)."""

from __future__ import annotations


def collatz_spine_sum(k: int) -> int:
    """spineSum(k) = (4^(k+1) - 1) / 3."""
    result: int = (4 ** (k + 1) - 1) // 3
    return result


def collatz_spine_check(k: int) -> bool:
    """Verify 4^(k+1) == 3*spineSum(k) + 1."""
    lhs: int = 4 ** (k + 1)
    rhs: int = 3 * collatz_spine_sum(k) + 1
    return lhs == rhs


def goldbach_check(n: int) -> bool:
    """Check Goldbach for even n >= 4: n = p + q with primes p,q."""
    if n < 4 or n % 2 != 0:
        return False
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    primes = [i for i in range(2, n) if sieve[i]]
    pset = set(primes)
    for p in primes:
        if (n - p) in pset:
            return True
    return False


def zeta_partial(s: float, N: int) -> float:
    """Partial sum sum_{n=1}^N 1/n^s (real s)."""
    total: float = sum(1.0 / (n**s) for n in range(1, N + 1))
    return total
