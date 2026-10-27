# KENÉ RECURSION — Candidate Recursion Family (R9)

> Candidate, not axiom. Formalizes A5.1 using Kené (Shipibo-Konibo) self-similarity.

## Hypothesis
Kené is a concrete instance of the recursion operator \(f\) in A5.1:
- Reflection + fractal self-similarity + recursive motifs.
- *Xao Kené* (merging of opposing forces) mirrors closure \(E \equiv I\) (A5.3).
- The motifs evolve with the environment (rivers, plants, constellations) — recursion is not static but adaptive.

## Candidate \(f\)
A complex quadratic map \(z \mapsto z^2 + c\) (Mandelbrot/Julia family) with
\(c\) drawn from a slowly varying "environment" parameter. Fixed points of this
map are the "awakening" moments (A5.1); the Julia set boundary is the crease
(A5.2, Folding-Calculus §2).

## Testable signature
- **P7 (fractal dimension):** The decision boundary of a ReLU network trained on
  a Kené-like dataset should have fractal dimension matching the Julia set of the
  fitted \(c\).
- **P8 (self-similarity ratio):** Motif sizes should scale by a constant ratio
  (golden-ratio-like) across scales; deviation > 5% would challenge the family.

## Engine support
- `engine.kene_step(z, c)`, `engine.mandelbrot_escape(c)`.

## Status
Candidate (A5.5). Needs a fitted \(c\) and dimension measurement.

## References
- Bow Seat, "Discovering Kené" (2025).
- Folding-Calculus FOUNDATIONS.md.
- `CONNECTIONS.md` (Kené row).
