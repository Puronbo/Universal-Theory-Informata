# FOLDING DEEP INTEGRATION — Full Folding-Calculus Mapping

> Extends `FOLDING_CALIBRATION.md` with the book's deeper content (Part I–V).

---

## 1. Fold/unfold as compression/expansion

- **Derivative = fold** (lossy compression): global info discarded to isolate local slope.
- **Integral = unfold** (expansive): reconstructs global shape from local pieces.
- **Creases are primary objects**, not exceptions — "the fold line is where the information is."

**Model mapping:** A5.1 (recursion = repeated fold), A4.3 (playhead = unfold of block), A2.5 (rolling fold).

## 2. The fold spectrum

| Situation | Fold type | Mathematical object | Model stage |
|---|---|---|---|
| Smooth point | Gentle curve | Ordinary derivative \(f'(x)\) | Rest (0) |
| Kink | Sharp crease | Subdifferential \(\partial f(x)\) = interval | Awakening (A5.1) |
| Cusp | Fold singularity | Higher-order subdifferential | Purge (A1.5) |
| Discontinuity | Tear | No subdifferential exists | Erosion (A7.4) |

Implemented in `engine.fold_spectrum(x_left, x_right)`.

## 3. Subdifferential at the crease

- At a corner (e.g., ReLU at 0), the derivative breaks, but the subdifferential expands to an interval \([-1,1]\).
- ReLU'(0) choice matters: 0 (standard) performs better at finite precision; 1 (Boursier et al.) gives theoretical guarantees.
- "Crease-aware optimization" is a novel, unexplored term.

**Model mapping:** A3.4 (particle twist = crease), A5.3 (closure = subdifferential interval collapsing to a point).

## 4. Sheaf theory: domains as sheaves

- Each physical domain (neural, geometric, chemical, nuclear, biological, cosmological) defines a sheaf over the 90° complex manifold.
- A crease is where stalks have multiplicity — non-unique continuation.
- The crease is the locus of physical interaction.

**Model mapping:** A3.2 (Exterior/Interior faces as sheaf sections), A5.3 (closure = gluing of sheaf sections at the crease).

## 5. Cusp catastrophe as universal normal form

- \(V(x;a,b) = \tfrac14 x^4 - \tfrac12 a x^2 - b x\).
- Bifurcation set: \(8a^3 = 27b^2\).
- Inside the cusp: 3 real roots (2 stable, 1 unstable); outside: 1 real root.
- Crossing the cusp produces a discontinuous jump.

**Model mapping:** A1.5 (purge at \(y'=0\)), A7.4 (erosion), A5.1 (awakening as cusp crossing).

## 6. Crease density experiments (verified, toy scale)

| Experiment | Finding |
|---|---|
| Pruning | Crease-proximity outperforms magnitude pruning up to 30% |
| OOD detection | Complementary to MSP (AUROC 0.884 vs 0.71 on "center noise") |
| Early stopping | Crease density declines after val loss plateaus (negative result) |
| Boundary complexity | \(r = -0.77\) with crease density; depth stronger (\(r=+0.97\)) |

**Limitations:** small synthetic 2D datasets, small MLPs, no statistical significance testing.

## 7. Conservative fields (Bolte & Pauwels)

- Provide mathematical infrastructure for the fold calculus.
- "Fold" = choice of selection in a conservative field.
- "Unfold" = integration along a path through the Whitney stratification.

**Model mapping:** A0.1 (self-containment) — candidate rigorous foundation.

## 8. Open problems (frontiers)

| Problem | Status | Difficulty |
|---|---|---|
| Crease-aware subgradient adaptation | No prior art | Hard |
| Kawasaki analogue for NN | Completely open | Very hard |
| Minimum fold depth as complexity measure | Embryonic | Hard |
| Crease-engineered activation functions | Underexplored | Moderate |
| Crease density as training diagnostic | Needs scale validation | Moderate |
| Fold-and-cut initialization | No prior art | Very hard |
| Crease density for adversarial robustness | Suggested, not tested | Moderate |
| Conservative fields formalization | Suggestive, not established | Hard |
| Crease density formalization (5 directions) | Identified | Varies |

---

## 9. What the book adds beyond the repo README

- **The fold spectrum** — a 4-level classification mapping to model stages.
- **Subgradient selection** — concrete mechanism for how creases affect training.
- **Conservative fields** — candidate rigorous foundation.
- **Minimum fold depth** — complexity measure for "how deep" an awakening is.
- **Crease density for adversarial robustness** — safety-relevant application.
- **Fold-and-cut initialization** — pre-determined fold lines for network init.
- **Applicability to modern architectures** (GELU, Transformers, SwiGLU).

---

## 10. Recommended additions to our model

1. **Add a "fold spectrum" axiom** (A5.6) — done.
2. **Add `crease_density` to engine** — done.
3. **Add `fold_spectrum` classifier** — done (below).
4. **Add conservative fields as a candidate foundation** in AXIOMS §9 — done.
5. **Add minimum fold depth** as an open question — done (in PRIZED_PROBLEMS / RESEARCH_ROADMAP).

---

## 11. Engine support

- `crease_density(values, eps)` — fraction of values near zero.
- `fold_spectrum(left_deriv, right_deriv)` — classify a point as smooth/kink/cusp/tear.

---

## 12. Sources

- Book: `the_book_of_puno.md` (2nd ed., July 2026).
- Repo: `Puronbo/Folding-Calculus`.
- Previously calibrated: `FOLDING_CALIBRATION.md`.
- Archived reference: `docs/the_book_of_puno.md`.
