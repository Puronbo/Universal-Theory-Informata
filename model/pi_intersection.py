"""Pi as the intersection of nested rational intervals.

Archimedes bounds a circle of radius one between regular inscribed and
circumscribed polygons. Let ``a_n`` be the half-side of the inscribed ``n``-gon
and ``b_n`` the half-side of the circumscribed ``n``-gon. Then

    n * a_n < pi < n * b_n.

Starting from the hexagon,

    a_6 = 1/2,    b_6 = 1/sqrt(3),

and doubling the number of sides uses

    a_{2n} = a_n / sqrt(2 * (1 + sqrt(1 - a_n**2))),
    b_{2n} = b_n / (1 + sqrt(1 + b_n**2)).

Every square root is enclosed by rational bounds computed with ``math.isqrt``,
and every operation rounds outward. The returned intervals therefore contain
``pi`` rigorously. The intervals are intersected as they are produced, so the
family is nested by construction.

The infinite intersection is the single point ``{pi}``. A finite intersection
is a rational interval; the module never pretends that ``pi`` is rational.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

__all__ = [
    "PiInterval",
    "PiIntersection",
    "archimedes_interval",
    "archimedes_intervals",
    "archimedes_intersection",
]

DEFAULT_DIGITS = 30


def _index(value: int, minimum: int, name: str) -> int:
    """Return ``value`` after checking that it is an integer of at least ``minimum``."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}, got {value}")
    return value


def _sqrt_bounds(value: Fraction, digits: int) -> tuple[Fraction, Fraction]:
    """Return rational ``(lower, upper)`` bounds on ``sqrt(value)``.

    The bounds have denominator ``10**digits``. The lower bound is the floor of
    the scaled square root; the upper bound is the next grid point, unless the
    root is exact.
    """
    if value < 0:
        raise ValueError("value must be non-negative")
    if value == 0:
        return (Fraction(0), Fraction(0))
    scale = 10**digits
    numerator = value.numerator
    denominator = value.denominator
    lower_int = isqrt((numerator * scale * scale) // denominator)
    lower = Fraction(lower_int, scale)
    if lower * lower == value:
        return (lower, lower)
    return (lower, Fraction(lower_int + 1, scale))


def _sqrt_interval(lower: Fraction, upper: Fraction, digits: int) -> tuple[Fraction, Fraction]:
    """Return rational bounds on ``sqrt(x)`` for every ``x`` in ``[lower, upper]``."""
    root_lower, _ = _sqrt_bounds(lower, digits)
    _, root_upper = _sqrt_bounds(upper, digits)
    return (root_lower, root_upper)


@dataclass(frozen=True)
class PiInterval:
    """A rational interval known to contain ``pi``.

    Attributes:
        sides: Number of sides of the Archimedes polygons.
        lower: Rational lower bound.
        upper: Rational upper bound.
    """

    sides: int
    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        if self.sides < 3:
            raise ValueError("sides must be at least three")
        if self.lower > self.upper:
            raise ValueError("lower must not exceed upper")

    @property
    def width(self) -> Fraction:
        """Return ``upper - lower``."""
        return self.upper - self.lower

    @property
    def midpoint(self) -> Fraction:
        """Return the rational midpoint ``(lower + upper) / 2``."""
        return (self.lower + self.upper) / 2

    def contains(self, value: Fraction | int) -> bool:
        """Return whether ``value`` lies in the closed interval."""
        return self.lower <= Fraction(value) <= self.upper


@dataclass(frozen=True)
class PiIntersection:
    """A nested family of rational intervals whose intersection contains ``pi``.

    Attributes:
        intervals: Nested intervals, outermost first.
    """

    intervals: tuple[PiInterval, ...]

    def __post_init__(self) -> None:
        if not self.intervals:
            raise ValueError("intervals must not be empty")
        for earlier, later in zip(self.intervals[:-1], self.intervals[1:], strict=True):
            if later.lower < earlier.lower or later.upper > earlier.upper:
                raise ValueError("intervals must be nested")

    def __len__(self) -> int:
        return len(self.intervals)

    @property
    def lower(self) -> Fraction:
        """Return the greatest lower bound of the family."""
        return max(interval.lower for interval in self.intervals)

    @property
    def upper(self) -> Fraction:
        """Return the least upper bound of the family."""
        return min(interval.upper for interval in self.intervals)

    @property
    def width(self) -> Fraction:
        """Return ``upper - lower`` for the finite intersection."""
        return self.upper - self.lower

    @property
    def sides(self) -> int:
        """Return the polygon side count of the last interval."""
        return self.intervals[-1].sides


def archimedes_intervals(doublings: int, digits: int = DEFAULT_DIGITS) -> tuple[PiInterval, ...]:
    """Return the nested Archimedes intervals up to ``doublings``.

    Args:
        doublings: Number of side doublings after the hexagon, at least zero.
        digits: Decimal digits used for rational square-root bounds, at least one.

    Returns:
        A tuple of ``doublings + 1`` nested intervals, starting with the hexagon.

    Raises:
        ValueError: If an index is invalid or a square root is negative.
    """
    doublings = _index(doublings, 0, "doublings")
    digits = _index(digits, 1, "digits")

    a_lower = a_upper = Fraction(1, 2)
    sqrt_three_lower, sqrt_three_upper = _sqrt_bounds(Fraction(3), digits)
    b_lower = Fraction(1) / sqrt_three_upper
    b_upper = Fraction(1) / sqrt_three_lower

    sides = 6
    lower = sides * a_lower
    upper = sides * b_upper
    intervals: list[PiInterval] = []

    for step in range(doublings + 1):
        raw_lower = sides * a_lower
        raw_upper = sides * b_upper
        lower = max(lower, raw_lower)
        upper = min(upper, raw_upper)
        intervals.append(PiInterval(sides=sides, lower=lower, upper=upper))

        if step < doublings:
            x_lower = 1 - a_upper * a_upper
            x_upper = 1 - a_lower * a_lower
            sqrt_x_lower, sqrt_x_upper = _sqrt_interval(x_lower, x_upper, digits)
            denominator_lower = 2 * (1 + sqrt_x_lower)
            denominator_upper = 2 * (1 + sqrt_x_upper)
            sqrt_denominator_lower, sqrt_denominator_upper = _sqrt_interval(
                denominator_lower, denominator_upper, digits
            )
            a_lower, a_upper = (
                a_lower / sqrt_denominator_upper,
                a_upper / sqrt_denominator_lower,
            )

            y_lower = 1 + b_lower * b_lower
            y_upper = 1 + b_upper * b_upper
            sqrt_y_lower, sqrt_y_upper = _sqrt_interval(y_lower, y_upper, digits)
            b_lower = b_lower / (1 + sqrt_y_upper)
            b_upper = b_upper / (1 + sqrt_y_lower)

            sides *= 2

    return tuple(intervals)


def archimedes_interval(doublings: int, digits: int = DEFAULT_DIGITS) -> PiInterval:
    """Return the nested intersection up to ``doublings``.

    Args:
        doublings: Number of side doublings after the hexagon, at least zero.
        digits: Decimal digits used for rational square-root bounds, at least one.

    Returns:
        The last (tightest) interval in :func:`archimedes_intervals`.

    Raises:
        ValueError: If an index is invalid.
    """
    return archimedes_intervals(doublings, digits)[-1]


def archimedes_intersection(doublings: int, digits: int = DEFAULT_DIGITS) -> PiIntersection:
    """Return the nested family of Archimedes intervals.

    The finite intersection is a rational interval. As ``doublings`` grows, the
    width tends to zero, so the infinite intersection is ``{pi}``.

    Args:
        doublings: Number of side doublings after the hexagon, at least zero.
        digits: Decimal digits used for rational square-root bounds, at least one.

    Returns:
        A :class:`PiIntersection` holding the nested family.

    Raises:
        ValueError: If an index is invalid.
    """
    return PiIntersection(archimedes_intervals(doublings, digits))
