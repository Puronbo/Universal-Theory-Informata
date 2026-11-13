"""The Boolean lattice of pole strings over the dual pairs (toy structure).

Each dual pair contributes one binary coordinate: a *pole string* chooses one
pole from every pair. With eight registered pairs there are ``2**8 = 256``
strings, and bitwise OR / AND make them a Boolean lattice:

* ``join`` is bitwise OR (choose the "right" pole if either string does),
* ``meet`` is bitwise AND,
* the involution is bitwise complement (swap every pole for its dual),
* the fold identifies a string with its complement, giving the folded cube.

This is a taxonomy of the framework's dual pairs, not a physical claim.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

from model.duality import DUAL_PAIRS

WIDTH: int = len(DUAL_PAIRS)


@dataclass(frozen=True)
class PoleString:
    """One pole chosen from each dual pair, encoded as a bit tuple."""

    bits: tuple[bool, ...]

    def __post_init__(self) -> None:
        if len(self.bits) != WIDTH:
            raise ValueError(f"a pole string needs {WIDTH} bits")
        if any(not isinstance(bit, bool) for bit in self.bits):
            raise ValueError("pole string bits must be bool")

    @property
    def poles(self) -> tuple[str, ...]:
        """Return the selected pole from each pair, in registration order."""
        return tuple(
            pair.right if bit else pair.left
            for pair, bit in zip(DUAL_PAIRS, self.bits, strict=True)
        )

    @property
    def dual(self) -> PoleString:
        """Return the complement: swap every pole for its dual."""
        return PoleString(tuple(not bit for bit in self.bits))

    @property
    def rank(self) -> int:
        """Return the number of right-pole choices."""
        return sum(self.bits)

    def to_bits(self) -> str:
        """Return the string as ``"0101..."``."""
        return "".join("1" if bit else "0" for bit in self.bits)

    def __str__(self) -> str:
        return self.to_bits()


def from_bits(bits: str) -> PoleString:
    """Build a pole string from a ``"0101..."`` bit string.

    Raises:
        ValueError: If the length is wrong or a character is not ``0``/``1``.
    """
    if len(bits) != WIDTH:
        raise ValueError(f"expected {WIDTH} bits, got {len(bits)}")
    if any(char not in "01" for char in bits):
        raise ValueError("bits must contain only '0' and '1'")
    return PoleString(tuple(char == "1" for char in bits))


def from_poles(poles: tuple[str, ...] | list[str]) -> PoleString:
    """Build a pole string from one pole per pair, in registration order.

    Raises:
        ValueError: If the count is wrong or a pole does not belong to its pair.
    """
    if len(poles) != WIDTH:
        raise ValueError(f"expected {WIDTH} poles, got {len(poles)}")
    bits: list[bool] = []
    for pair, pole in zip(DUAL_PAIRS, poles, strict=True):
        if pole == pair.left:
            bits.append(False)
        elif pole == pair.right:
            bits.append(True)
        else:
            raise ValueError(f"{pole!r} is not a pole of {pair.name!r}")
    return PoleString(tuple(bits))


def join(left: PoleString, right: PoleString) -> PoleString:
    """Return the bitwise OR (least upper bound)."""
    return PoleString(tuple(a or b for a, b in zip(left.bits, right.bits, strict=True)))


def meet(left: PoleString, right: PoleString) -> PoleString:
    """Return the bitwise AND (greatest lower bound)."""
    return PoleString(tuple(a and b for a, b in zip(left.bits, right.bits, strict=True)))


def complement(value: PoleString) -> PoleString:
    """Return the bitwise complement (the duality involution)."""
    return value.dual


def leq(left: PoleString, right: PoleString) -> bool:
    """Return whether every selected pole of ``left`` is also in ``right``."""
    return all((not a) or b for a, b in zip(left.bits, right.bits, strict=True))


def canonical(value: PoleString) -> PoleString:
    """Return the smaller of ``value`` and its dual.

    The fold identifies the two strings in each complement orbit; this is the
    quotient representative in the folded cube.
    """
    return min((value, value.dual), key=lambda item: item.bits)


def same_orbit(left: PoleString, right: PoleString) -> bool:
    """Return whether two strings are equal or complementary."""
    return left == right or left == right.dual


def bottom() -> PoleString:
    """Return the string selecting every left pole."""
    return PoleString(tuple(False for _ in DUAL_PAIRS))


def top() -> PoleString:
    """Return the string selecting every right pole."""
    return PoleString(tuple(True for _ in DUAL_PAIRS))


def atoms() -> tuple[PoleString, ...]:
    """Return the strings of rank one (the lattice atoms)."""
    return tuple(
        PoleString(tuple(index == position for index in range(WIDTH))) for position in range(WIDTH)
    )


def coatoms() -> tuple[PoleString, ...]:
    """Return the strings of rank ``WIDTH - 1``."""
    return tuple(atom.dual for atom in atoms())


def all_strings() -> tuple[PoleString, ...]:
    """Return all ``2**WIDTH`` pole strings in bit order."""
    return tuple(PoleString(bits) for bits in itertools.product((False, True), repeat=WIDTH))


def orbit_count() -> int:
    """Return the number of complement orbits (the folded-cube size)."""
    return 1 << (WIDTH - 1)


def strings_of_rank(rank: int) -> tuple[PoleString, ...]:
    """Return every pole string with exactly ``rank`` right-pole choices.

    The number of such strings is the binomial coefficient ``C(WIDTH, rank)``.

    Raises:
        ValueError: If ``rank`` is not an integer in ``0..WIDTH``.
    """
    if isinstance(rank, bool) or not isinstance(rank, int):
        raise ValueError("rank must be an integer")
    if rank < 0 or rank > WIDTH:
        raise ValueError(f"rank must be in 0..{WIDTH}")
    return tuple(
        PoleString(bits)
        for bits in itertools.product((False, True), repeat=WIDTH)
        if sum(bits) == rank
    )


def rank_counts() -> tuple[int, ...]:
    """Return the number of strings at each rank ``0..WIDTH``.

    The result is row ``WIDTH`` of Pascal's triangle and sums to ``2**WIDTH``.
    """
    return tuple(math.comb(WIDTH, rank) for rank in range(WIDTH + 1))


def orbit_rank_counts() -> tuple[int, ...]:
    """Return the number of complement orbits by their smaller rank.

    Each orbit ``{s, dual(s)}`` is labelled by
    ``min(rank(s), WIDTH - rank(s))``. For ``2*k < WIDTH`` there are
    ``C(WIDTH, k)`` such orbits; when ``2*k == WIDTH`` each orbit pairs two
    rank-``k`` strings, so the count is ``C(WIDTH, k) // 2``.

    The result sums to ``orbit_count()``.
    """
    counts: list[int] = []
    for rank in range(WIDTH // 2 + 1):
        count = math.comb(WIDTH, rank)
        counts.append(count if 2 * rank < WIDTH else count // 2)
    return tuple(counts)
