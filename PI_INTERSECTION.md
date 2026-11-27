# Pi as an Intersection

> **Source:** the instruction "change pi into an intersection" (2026-11-27).
> **Status:** exact rational enclosures with a standard Archimedes limit. The
> finite objects are rational intervals; the infinite intersection is the single
> point \(\{ \pi \}\). Nothing here claims that \(\pi\) is rational.

## 1. The construction

Bounding circle of radius one by regular polygons. Let

- \(a_n\) be the half-side of the inscribed regular \(n\)-gon;
- \(b_n\) be the half-side of the circumscribed regular \(n\)-gon.

Then the half-perimeters satisfy

\[
n a_n < \pi < n b_n.
\]

The hexagon gives

\[
a_6=\frac12,\qquad b_6=\frac{1}{\sqrt3}.
\]

Doubling the number of sides uses the stable half-angle forms

\[
a_{2n}=\frac{a_n}{\sqrt{2\left(1+\sqrt{1-a_n^2}\right)}},
\qquad
b_{2n}=\frac{b_n}{1+\sqrt{1+b_n^2}}.
\]

Both denominators stay away from zero, so the recurrences do not suffer the
cancellation of the naive \(1-\sqrt{1-a^2}\) form.

## 2. Why the intervals are rigorous

Every square root is replaced by rational bounds. For a nonnegative rational
\(x=p/q\),

\[
\left\lfloor \sqrt{x}\,10^k \right\rfloor
=\left\lfloor \sqrt{\frac{p\,10^{2k}}{q}} \right\rfloor
=\left\lfloor \sqrt{\left\lfloor \frac{p\,10^{2k}}{q} \right\rfloor} \right\rfloor.
\]

The numerator is computed with integer `isqrt`. The lower bound is that integer
divided by \(10^k\); the upper bound is the next grid point, unless the root is
exact. Every interval operation then rounds outward. Therefore each returned
interval contains the true value.

The intervals are intersected as they are produced. The finite intersection is

\[
I_d=\bigcap_{j=0}^{d}[\ell_j,u_j]
=[\max_j \ell_j,\ \min_j u_j],
\]

which is again a rational interval. Nesting is enforced by construction, not
assumed from floating-point behaviour.

## 3. The limit

Archimedes' theorem gives

\[
0<\pi-n a_n<\frac{C}{n^2}
\]

for a constant \(C\), and the same order for \(n b_n-\pi\). Hence the widths
of \(I_d\) tend to zero. A nested family of nonempty closed intervals whose
lengths tend to zero has a one-point intersection, and \(\pi\) belongs to every
member. Therefore

\[
\bigcap_{d\ge0} I_d=\{\pi\}.
\]

This is the exact sense in which \(\pi\) has been changed into an intersection.
It is not a rational value and not a finite decimal.

## 4. Values

The table shows the rational endpoints to 18 decimal places. The exact objects
are `Fraction` values; the decimals are display only.

| \(d\) | sides | lower | upper | width |
|---:|---:|---:|---:|---:|
| 0 | 6 | 3.000000000000000000 | 3.464101615137754587 | \(4.641\times10^{-1}\) |
| 1 | 12 | 3.105828541230249148 | 3.215390309173472478 | \(1.096\times10^{-1}\) |
| 2 | 24 | 3.132628613281238197 | 3.159659942097500483 | \(2.703\times10^{-2}\) |
| 3 | 48 | 3.139350203046867207 | 3.146086215131434971 | \(6.736\times10^{-3}\) |
| 4 | 96 | 3.141031950890509638 | 3.142714599645368298 | \(1.683\times10^{-3}\) |
| 5 | 192 | 3.141452472285462075 | 3.141873049979823872 | \(4.206\times10^{-4}\) |
| 6 | 384 | 3.141557607911857646 | 3.141662747056848526 | \(1.051\times10^{-4}\) |
| 10 | 6144 | 3.141592516692157448 | 3.141592927385097034 | \(4.107\times10^{-7}\) |

The width shrinks by approximately a factor of four per doubling, as expected
from the \(n^{-2}\) polygon error.

## 5. What is claimed

- Each finite interval is a rigorous rational enclosure of \(\pi\).
- The intervals are nested by construction.
- The infinite intersection is exactly \(\{\pi\}\).
- The implementation uses only integer square roots and exact rational
  arithmetic.

## 6. What is not claimed

- That \(\pi\) is rational, finite, or equal to any listed endpoint.
- That this is a new proof of the irrationality or transcendence of \(\pi\).
- That the finite table computes all digits of \(\pi\). It computes enclosures;
  the number of correct digits grows with the side count.
- That "intersection" here means an arbitrary set-theoretic intersection. It is
  the intersection of the nested interval family.
- That the construction has a physical or cosmological meaning.

## 7. References

- Archimedes, *Measurement of a Circle*. (The polygon bounds.)
- Euclid, *Elements*, Book XII. (The circle is bounded by polygons.)
- `model/pi_intersection.py`, `tests/test_pi_intersection.py`, and
  `examples/pi_intersection.py` for the executable form.
