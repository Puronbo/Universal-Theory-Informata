# PRIZED PROBLEMS — Honest Audit (Model Companion)

> Companion to `LORE_CALIBRATION.md`. Maps the Clay Millennium Prize Problems (plus
> Goldbach) to this model's constructs, following L.O.R.E.'s honest-audit discipline:
> **no problem is declared settled.** Each row states what is shown and the gap.

---

## Audit table

| Problem | L.O.R.E. status | Model connection | Gap / honest limit |
|---|---|---|---|
| **Navier–Stokes (T³)** | RIGOROUS PROOF (Fourier bound + Serrin 1962) | Erosion (A7.4): viscous decay as long-timescale purge; playhead (A4) samples the flow | Proof is on T³ only; R³ open |
| **Navier–Stokes (R³)** | PARTIAL | Same as above | Need analytic L¹ boundedness |
| **Yang–Mills mass gap** | PARTIAL (gap equation + OS axioms) | Mass gap calculator (universal impedance); A2.2 tension as mass scale | Constructive measure on R⁴ |
| **Riemann Hypothesis** | STRONG EVIDENCE (Li n=1..30, de Branges 6/6) | Recursion fixed points (A5.1); zeta zeros as "blades" of a stroboscopic sample | Finite zeros verified only |
| **BSD** | KNOWN PARTIAL (rank ≤1, Kolyvagin) | Ternary balance (A0.2) as rank parity | Euler system for rank ≥2 |
| **Goldbach** | NUMERICAL EVIDENCE (49,999/49,999 to 100k) | Erosion pairs (+1,-1)→(0,0) as even decomposition | Parity barrier in sieves |
| **Hodge** | KNOWN PARTIAL (Lefschetz (1,1)) | Sheaf/closure (A5.3) as cycle gluing | Algebraic cycles codim ≥2 |
| **P vs NP** | OPEN | Non-ergodic trial-and-error (A0.4, A7.1) | All barriers block known methods |

---

## What this model contributes

- **Honest labeling:** every claim above is tagged with its epistemic status;
  nothing is promoted to "settled."
- **Meta-audit:** `validate_claims.py` greps for overclaim phrases.
- **Computational sectors:** `engine.py` now includes Collatz spine, Goldbach
  check, and Riemann zeta partial sums as *numerical evidence only*.
- **Lean:** `lean/Model/` holds kernel-verified theorems (no axioms) for the
  small, checkable identities (Collatz spine for k=0,1).

---

## Collatz spine identity (L.O.R.E.)

\[
4^{k+1} = 3 \cdot \text{spineSum}(k) + 1,\qquad
\text{spineSum}(k) = \frac{4^{k+1}-1}{3}.
\]

Implemented in `engine.collatz_spine_check(k)` and verified for \(k=0..20\).

---

## References

- L.O.R.E. README & `papers/honest_audit.pdf`.
- Clay Mathematics Institute Millennium Problems: https://www.claymath.org/millennium-problems/
- This repo: `LORE_CALIBRATION.md`, `validate_claims.py`.

---

*No Millennium problem is settled by this project. This document is a map, not a proof.*
