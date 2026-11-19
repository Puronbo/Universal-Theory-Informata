"""The Fold corpus's exact core, made executable.

``The-Fold`` (github.com/Puronbo/The-Fold) reads one homothety,

    g_k(P) = P0 + k * (P - P0),

as the source of a scale, a fold, a crease, a twist, and an observer. Its
checkable content is small and this module isolates it:

- the homothety and its determinant ``det(g_k) = k**n``;
- a hyperplane reflection (a fold) and the composition of two folds, which is
  a rotation by twice the angle between the creases;
- the midpoint and division maps, whose collapse scale is ``(t-1)/t``;
- the observer split: for a unit complex scale ``k = exp(i*theta)``, the
  midpoint modulus is ``cos(theta/2)`` and the division-collapse modulus is
  ``2*sin(theta/2)``, so their squares sum to one and the second is the
  solid-angle fraction;
- the orthogonal projection onto the crease, ``(I + reflection)/2``;
- the cap/puncture ledger: equal Euler characteristic, different surfaces;
- the wheel's closure after ``m`` turns and doubling's bijectivity iff odd;
- the exterior solid-angle fraction and the Schwarzschild ratio.

What is **not** here: the corpus's theta/Mellin derivation of the functional
equation, its zeta checks, and its physics readings. Those are documented in
``FOLD_CORPUS.md`` with their status; the theta modular identity is exact, the
derivation is a reformulation, and the rhymes are not claims. The one
determinant is the whole engine: heights scale like ``k``, areas like
``k**2``, volumes like ``abs(k)**3``.

The corpus's own rule applies: a rhyme is a place to look, never a proof.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from model.spacebar import SPEED_OF_LIGHT

__all__ = [
    "SurfaceLedger",
    "compose_reflections",
    "division_collapse_scale",
    "division_point",
    "doubling_agrees_with_negation",
    "doubling_is_bijective",
    "fold_orbit",
    "horizon_ratio",
    "midpoint_map",
    "midpoint_scale",
    "observer_split",
    "projection_onto_crease",
    "reflect_point",
    "reflection_matrix",
    "rotation_matrix",
    "scale_determinant",
    "scale_point",
    "schwarzschild_radius",
    "solid_angle_fraction",
    "two_fold_rotation_angle",
    "wheel_turn",
    "wheel_turns",
]

Matrix2 = tuple[tuple[float, float], tuple[float, float]]

# CODATA 2018, m^3 kg^-1 s^-2. Kept private so the public vocabulary of the
# module stays the Fold's, not a second constants table.
_GRAVITATIONAL_CONSTANT = 6.674_30e-11


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive(value: float, name: str) -> float:
    value = _finite(value, name)
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0")
    return value


def _nonnegative(value: float, name: str) -> float:
    value = _finite(value, name)
    if value < 0.0:
        raise ValueError(f"{name} must be >= 0")
    return value


def _point(values: Sequence[float], name: str) -> tuple[float, ...]:
    point = tuple(float(value) for value in values)
    if not point:
        raise ValueError(f"{name} must have at least one coordinate")
    if not all(math.isfinite(value) for value in point):
        raise ValueError(f"{name} must have finite coordinates")
    return point


def _datum(point: tuple[float, ...], datum: Sequence[float] | None) -> tuple[float, ...]:
    if datum is None:
        return (0.0,) * len(point)
    origin = _point(datum, "datum")
    if len(origin) != len(point):
        raise ValueError("datum and point must have the same dimension")
    return origin


def _integer(value: int, name: str, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return value


def _unit(normal: Sequence[float]) -> tuple[float, ...]:
    vector = _point(normal, "normal")
    length = math.sqrt(sum(value * value for value in vector))
    if length == 0.0:
        raise ValueError("normal must be nonzero")
    return tuple(value / length for value in vector)


# Scale ---------------------------------------------------------------------


def scale_point(
    k: float, point: Sequence[float], datum: Sequence[float] | None = None
) -> tuple[float, ...]:
    """Return ``g_k(P) = P0 + k*(P - P0)``, the homothety about ``datum``.

    With ``datum=None`` the origin is used. The map is a group action for
    ``k != 0``; ``k = 0`` collapses every point to the datum and is outside
    the group.

    Raises:
        ValueError: If ``k`` is not finite, a point is empty or non-finite, or
            ``datum`` and ``point`` disagree in dimension.
    """
    k = _finite(k, "k")
    target = _point(point, "point")
    origin = _datum(target, datum)
    return tuple(o + k * (p - o) for p, o in zip(target, origin, strict=True))


def scale_determinant(k: float, dimension: int) -> float:
    """Return ``det(g_k) = k**dimension``, the signed volume factor.

    The determinant carries the sign; a *volume* scales by its absolute value,
    which is why heights keep a sign that areas lose. In three dimensions a
    negative ``k`` reverses orientation.

    Raises:
        ValueError: If ``k`` is not finite or ``dimension`` is less than one.
    """
    k = _finite(k, "k")
    dimension = _integer(dimension, "dimension", 1)
    return k**dimension


# Fold and crease -----------------------------------------------------------


def reflect_point(
    point: Sequence[float], normal: Sequence[float], offset: float = 0.0
) -> tuple[float, ...]:
    """Reflect ``point`` across the hyperplane ``normal . x = offset``.

    The normal is normalized, so any nonzero vector may be passed. A point on
    the hyperplane is fixed; the reflection is an involution.

    Raises:
        ValueError: If the point or normal is empty, non-finite, or of a
            different dimension, if the normal is zero, or if ``offset`` is not
            finite.
    """
    target = _point(point, "point")
    unit = _unit(normal)
    if len(unit) != len(target):
        raise ValueError("normal and point must have the same dimension")
    offset = _finite(offset, "offset")
    distance = sum(value * direction for value, direction in zip(target, unit, strict=True))
    shift = 2.0 * (distance - offset)
    return tuple(value - shift * direction for value, direction in zip(target, unit, strict=True))


def reflection_matrix(normal: Sequence[float]) -> Matrix2:
    """Return the 2x2 matrix of the reflection across a line through the origin.

    The line is spanned by ``normal``'s perpendicular; equivalently the matrix
    is ``I - 2*n*n^T`` for the unit normal ``n``.

    Raises:
        ValueError: If ``normal`` is not a finite, nonzero 2-vector.
    """
    unit = _unit(normal)
    if len(unit) != 2:
        raise ValueError("normal must be two-dimensional")
    x, y = unit
    return ((1.0 - 2.0 * x * x, -2.0 * x * y), (-2.0 * x * y, 1.0 - 2.0 * y * y))


def rotation_matrix(angle: float) -> Matrix2:
    """Return the 2x2 rotation by ``angle`` radians.

    Raises:
        ValueError: If ``angle`` is not finite.
    """
    angle = _finite(angle, "angle")
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return ((cosine, -sine), (sine, cosine))


def _multiply(first: Matrix2, second: Matrix2) -> Matrix2:
    return (
        (
            first[0][0] * second[0][0] + first[0][1] * second[1][0],
            first[0][0] * second[0][1] + first[0][1] * second[1][1],
        ),
        (
            first[1][0] * second[0][0] + first[1][1] * second[1][0],
            first[1][0] * second[0][1] + first[1][1] * second[1][1],
        ),
    )


def compose_reflections(first_normal: Sequence[float], second_normal: Sequence[float]) -> Matrix2:
    """Return ``R(second) . R(first)``, the composition of two folds.

    Two reflections whose creases meet at angle ``alpha`` compose to a rotation
    by ``2*alpha``. The rotations are applied in the order given: ``first``
    then ``second``.

    Raises:
        ValueError: If either normal is not a finite, nonzero 2-vector.
    """
    return _multiply(reflection_matrix(second_normal), reflection_matrix(first_normal))


def two_fold_rotation_angle(first_normal: Sequence[float], second_normal: Sequence[float]) -> float:
    """Return the rotation angle produced by two reflections, normalized.

    The result is ``2*(theta_2 - theta_1)`` reduced to ``(-pi, pi]``.

    Raises:
        ValueError: If either normal is not a finite, nonzero 2-vector.
    """
    first = _unit(first_normal)
    second = _unit(second_normal)
    if len(first) != 2 or len(second) != 2:
        raise ValueError("normals must be two-dimensional")
    difference = 2.0 * (math.atan2(second[1], second[0]) - math.atan2(first[1], first[0]))
    return math.atan2(math.sin(difference), math.cos(difference))


# Midpoint and division -----------------------------------------------------


def midpoint_scale(k: float) -> float:
    """Return ``(1 + k)/2``, the scale of the midpoint map.

    Raises:
        ValueError: If ``k`` is not finite.
    """
    return 0.5 * (1.0 + _finite(k, "k"))


def midpoint_map(
    k: float, point: Sequence[float], datum: Sequence[float] | None = None
) -> tuple[float, ...]:
    """Return ``(P + g_k(P))/2``, which equals ``g_((1+k)/2)(P)``.

    The midpoint map's determinant vanishes only at ``k = -1``, where every
    midpoint lands on the datum. For an honest reflection ``R``, the average
    ``(P + R(P))/2`` is the projection onto the crease instead; that is
    ``projection_onto_crease``, a different map.

    Raises:
        ValueError: If ``k`` is not finite, the point is empty or non-finite,
            or ``datum`` and ``point`` disagree in dimension.
    """
    return scale_point(midpoint_scale(k), point, datum)


def division_point(
    t: float, k: float, point: Sequence[float], datum: Sequence[float] | None = None
) -> tuple[float, ...]:
    """Return the point a fraction ``t`` of the way from ``P`` to ``g_k(P)``.

    The map is again a homothety about the datum, with factor
    ``1 - t + t*k``; it collapses at ``k = (t-1)/t``.

    Raises:
        ValueError: If ``t`` or ``k`` is not finite, the point is empty or
            non-finite, or ``datum`` and ``point`` disagree in dimension.
    """
    t = _finite(t, "t")
    k = _finite(k, "k")
    factor = 1.0 - t + t * k
    return scale_point(factor, point, datum)


def division_collapse_scale(t: float) -> float:
    """Return ``(t - 1)/t``, the scale at which the ``t``-division collapses.

    Every ``k != 1`` is owned by exactly one ``t = 1/(1-k)``, and ``t`` paired
    with ``1 - t`` pairs ``k`` with ``1/k``.

    Raises:
        ValueError: If ``t`` is not finite or is zero.
    """
    t = _finite(t, "t")
    if t == 0.0:
        raise ValueError("t must be nonzero")
    return (t - 1.0) / t


def observer_split(k: complex) -> tuple[float, float]:
    """Return the crease and sky fractions of a unit complex scale ``k``.

    Write ``k = exp(i*theta)``. The midpoint and division maps then have the
    moduli

        |(1 + k)/2|   = cos(theta/2),
        |(k - 1)/k|   = 2*sin(theta/2).

    Squaring gives ``crease = cos(theta/2)**2`` and
    ``sky = |(k - 1)/k|**2 / 4 = sin(theta/2)**2``, so ``crease + sky = 1``.
    The sky fraction is the solid-angle fraction of a sphere of angular radius
    ``theta``: ``(1 - cos theta)/2 = sin(theta/2)**2``.

    At ``k = i`` the split is ``(1/2, 1/2)``, the observer on the surface; at
    ``k = -1`` it is ``(0, 1)``, the observer inside.

    This is an identity between the corpus's two elementary maps and the
    solid-angle formula, not a derivation of observation.

    Raises:
        ValueError: If ``k`` is not finite, is zero, or does not lie on the
            unit circle.
    """
    k = complex(k)
    if not (math.isfinite(k.real) and math.isfinite(k.imag)) or k == 0:
        raise ValueError("k must be finite and nonzero")
    if abs(abs(k) - 1.0) > 1e-12:
        raise ValueError("k must lie on the unit circle")
    crease = abs(0.5 * (1.0 + k)) ** 2
    sky = abs((k - 1.0) / k) ** 2 / 4.0
    return crease, sky


def projection_onto_crease(
    point: Sequence[float], normal: Sequence[float], offset: float = 0.0
) -> tuple[float, ...]:
    """Return the orthogonal projection of ``point`` onto the crease.

    The projection is ``(P + reflection(P))/2``, the midpoint map of the fold.

    Raises:
        ValueError: If the point or normal is invalid, or ``offset`` is not
            finite.
    """
    target = _point(point, "point")
    unit = _unit(normal)
    if len(unit) != len(target):
        raise ValueError("normal and point must have the same dimension")
    offset = _finite(offset, "offset")
    distance = sum(value * direction for value, direction in zip(target, unit, strict=True))
    shift = distance - offset
    return tuple(value - shift * direction for value, direction in zip(target, unit, strict=True))


def fold_orbit(
    point: Sequence[float], fold: Callable[[tuple[float, ...]], tuple[float, ...]]
) -> tuple[tuple[float, ...], ...]:
    """Return the orbit of ``point`` under an involution.

    A fixed point has a one-element orbit; every other point has a two-element
    orbit. Equality is exact, which is appropriate for constructed folds.

    Raises:
        ValueError: If ``point`` is empty or non-finite.
    """
    target = _point(point, "point")
    image = tuple(float(value) for value in fold(target))
    return (target,) if image == target else (target, image)


# Cap/puncture ledger -------------------------------------------------------


@dataclass(frozen=True)
class SurfaceLedger:
    """The three invariants the cap/puncture argument uses.

    This is not a topological space; it is the triple
    ``(chi, boundary, punctures)`` that the ledger tracks. Capping raises
    ``chi`` and consumes a boundary; puncturing lowers ``chi`` and creates a
    puncture. On ``chi`` alone they cancel; on the triple they do not.

    Raises:
        ValueError: If ``boundary`` or ``punctures`` is negative.
    """

    chi: int
    boundary: int
    punctures: int

    def __post_init__(self) -> None:
        if self.boundary < 0:
            raise ValueError("boundary must be >= 0")
        if self.punctures < 0:
            raise ValueError("punctures must be >= 0")

    def cap(self) -> SurfaceLedger:
        """Glue a disk to a boundary circle.

        Raises:
            ValueError: If there is no boundary component to cap.
        """
        if self.boundary < 1:
            raise ValueError("cap requires a boundary component")
        return SurfaceLedger(self.chi + 1, self.boundary - 1, self.punctures)

    def uncap(self) -> SurfaceLedger:
        """Remove an open disk, creating a boundary component."""
        return SurfaceLedger(self.chi - 1, self.boundary + 1, self.punctures)

    def puncture(self) -> SurfaceLedger:
        """Remove a point, lowering ``chi`` and creating a puncture."""
        return SurfaceLedger(self.chi - 1, self.boundary, self.punctures + 1)

    def fill(self) -> SurfaceLedger:
        """Fill a puncture, raising ``chi``.

        Raises:
            ValueError: If there is no puncture to fill.
        """
        if self.punctures < 1:
            raise ValueError("fill requires a puncture")
        return SurfaceLedger(self.chi + 1, self.boundary, self.punctures - 1)


# Closure -------------------------------------------------------------------


def wheel_turn(m: int, n: int) -> int:
    """Return one turn of an ``m``-spoke wheel, ``(n + 1) % m``.

    Raises:
        ValueError: If ``m`` is less than one or ``n`` is negative.
    """
    m = _integer(m, "m", 1)
    n = _integer(n, "n", 0)
    return (n + 1) % m


def wheel_turns(m: int, steps: int, n: int) -> int:
    """Return the mark after ``steps`` turns of an ``m``-spoke wheel.

    Raises:
        ValueError: If ``m`` is less than one, ``steps`` is negative, or ``n``
            is negative.
    """
    m = _integer(m, "m", 1)
    steps = _integer(steps, "steps", 0)
    n = _integer(n, "n", 0)
    return (n + steps) % m


def doubling_is_bijective(n: int) -> bool:
    """Return whether ``x -> 2x`` is a permutation of ``Z/n``.

    Doubling is injective exactly when ``n`` is odd.

    Raises:
        ValueError: If ``n`` is less than one.
    """
    n = _integer(n, "n", 1)
    return n % 2 == 1


def doubling_agrees_with_negation(n: int) -> bool:
    """Return whether ``2x == -x`` on ``Z/n``, which holds iff ``n`` divides 3.

    The divisibility includes the trivial ``n = 1``; the non-trivial case is
    ``n = 3``, where ``2 = -1``.

    Raises:
        ValueError: If ``n`` is less than one.
    """
    n = _integer(n, "n", 1)
    return 3 % n == 0


# Observer and horizon ------------------------------------------------------


def solid_angle_fraction(radius: float, distance: float) -> float:
    """Return the fraction of the sky a sphere subtends from ``distance``.

    For an exterior observer,

        Omega/(4*pi) = (1 - sqrt(1 - (r/d)**2)) / 2.

    An observer on the surface sees a half-space (``1/2``); an observer inside
    sees the whole sky (``1``).

    Raises:
        ValueError: If ``radius`` or ``distance`` is not finite and
            nonnegative.
    """
    radius = _nonnegative(radius, "radius")
    distance = _nonnegative(distance, "distance")
    if radius == 0.0:
        return 0.0
    if distance < radius:
        return 1.0
    return 0.5 * (1.0 - math.sqrt(1.0 - (radius / distance) ** 2))


def schwarzschild_radius(mass: float) -> float:
    """Return ``2*G*M/c**2``, the Schwarzschild radius.

    Raises:
        ValueError: If ``mass`` is not finite and nonnegative.
    """
    mass = _nonnegative(mass, "mass")
    return 2.0 * _GRAVITATIONAL_CONSTANT * mass / SPEED_OF_LIGHT**2


def horizon_ratio(mass: float, radius: float) -> float:
    """Return ``r_s/R = 2*G*M/(c**2*R)``, the collapse stage ``k*``.

    A body reaches its own horizon at ``k*``; values far below one are ordinary
    bodies (Earth is about ``1.4e-9``).

    Raises:
        ValueError: If ``mass`` is not finite and nonnegative, or ``radius`` is
            not finite and positive.
    """
    mass = _nonnegative(mass, "mass")
    radius = _positive(radius, "radius")
    return schwarzschild_radius(mass) / radius
