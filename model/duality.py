"""Dual pairs and the involution that swaps them (tooling).

The framework is built from binary poles: UV/IR, exterior/interior,
compression/expansion, photon/dark energy, entropy/structure, becoming/block,
discrete/continuous, and reprocessed/erased. This module makes the pairing
explicit and provides a single swap map. It is a taxonomy, not a physical
claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class DualPair:
    """A pair of poles exchanged by an involution."""

    name: str
    left: str
    right: str

    def __post_init__(self) -> None:
        if not self.name or not self.left or not self.right:
            raise ValueError("dual pair name and poles must be non-empty")
        if self.left == self.right:
            raise ValueError("dual pair poles must differ")

    def other(self, pole: str) -> str:
        """Return the opposite pole.

        Raises:
            ValueError: If ``pole`` is not a member of this pair.
        """
        if pole == self.left:
            return self.right
        if pole == self.right:
            return self.left
        raise ValueError(f"{pole!r} is not a pole of {self.name!r}")


DUAL_PAIRS: Final[tuple[DualPair, ...]] = (
    DualPair("scale", "UV", "IR"),
    DualPair("surface", "exterior", "interior"),
    DualPair("portal", "compression", "expansion"),
    DualPair("fold", "photon", "dark energy"),
    DualPair("brake", "entropy", "structure"),
    DualPair("time", "becoming", "block"),
    DualPair("substrate", "discrete", "continuous"),
    DualPair("information", "reprocessed", "erased"),
)


def dual_pairs() -> tuple[DualPair, ...]:
    """Return the registered dual pairs."""
    return DUAL_PAIRS


def all_poles() -> tuple[str, ...]:
    """Return every registered pole in registration order."""
    return tuple(pole for pair in DUAL_PAIRS for pole in (pair.left, pair.right))


def dual_pair(name: str) -> DualPair:
    """Return the pair with ``name``.

    Raises:
        ValueError: If no pair has that name.
    """
    for pair in DUAL_PAIRS:
        if pair.name == name:
            return pair
    raise ValueError(f"unknown dual pair: {name!r}")


def dual_of(pole: str) -> str:
    """Return the pole opposite ``pole`` across all registered pairs.

    Raises:
        ValueError: If ``pole`` appears in no pair, or in more than one.
    """
    matches = [pair for pair in DUAL_PAIRS if pole in (pair.left, pair.right)]
    if not matches:
        raise ValueError(f"unknown pole: {pole!r}")
    if len(matches) > 1:
        raise ValueError(f"ambiguous pole: {pole!r}")
    return matches[0].other(pole)
