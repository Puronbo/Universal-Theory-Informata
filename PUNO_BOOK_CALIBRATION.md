# PUNO BOOK CALIBRATION — The Book of Puno (2nd ed., 2026)

> Source: `the_book_of_puno.md` (attached, 1227 lines). Full monograph by Michael Grafiel Sayson Puno.
> Extends `FOLDING_CALIBRATION.md` with the book's deeper content.

---

## 1. Key new insights

### 1.1 Fold/unfold as the core intuition
- **Derivative = fold** (lossy compression): global info discarded to isolate local slope.
- **Integral = unfold** (expansive): reconstructs global shape from local pieces.
- **Creases are primary objects**, not exceptions — "the fold line is where the information is."

### 1.2 The fold spectrum
| Situation | Fold type | Mathematical object |
|---|---|---|
| Smooth point | Gentle curve | Ordinary derivative \(f'(x)\) |
| Kink | Sharp crease | Subdifferential \(\partial f(x)\) = interval |
| Cusp | Fold singularity | Higher-order subdifferential |
| Discontinuity | Tear | No subdifferential |

### 1.3 Subdifferential at the crease
- At a corner (e.g., ReLU at 0), the derivative breaks, but the subdifferential expands to an interval \([-1,1]\).
- ReLU'(0) choice matters: 0 (standard) performs better at finite precision; 1 (Boursier et al.) gives theoretical guarantees.
- "Crease-aware optimization" is a novel, unexplored term.

### 1.4 Origami theorems
- **Kawasaki:** flat-foldability angle-sum condition.
- **Maekawa:** \(M - V = -2\) for flat-foldable vertices.
- **Fold-and-cut:** any polygonal cut from one straight cut after folding → universal approximation.
- **Robertson (1977):** generalizes Kawasaki to N dimensions (alternating volume).
- **No Kawasaki analogue exists for neural networks** — genuinely open.

### 1.5 Crease density experiments (verified)
- Pruning: crease-proximity outperforms magnitude pruning up to 30%.
- OOD detection: complementary to MSP (AUROC 0.884 vs 0.71 on "center noise").
- Early stopping: crease density declines after val loss plateaus (negative result on tested problem).
- Boundary complexity: \(r = -0.77\) with crease density; depth stronger (\(r=+0.97\)).

### 1.6 Conservative fields (Bolte & Pauwels)
- Provide mathematical infrastructure for the fold calculus.
- "Fold" = choice of selection in a conservative field; "unfold" = integration along a path through Whitney stratification.

### 1.7 Open problems (frontiers)
- Crease-aware subgradient adaptation (hard).
- Kawasaki analogue for NN (very hard, completely open).
- Minimum fold depth as complexity measure (hard).
- Crease-engineered activation functions (moderate).
- Crease density as training diagnostic (moderate, needs scale validation).
- Fold-and-cut initialization (very hard).
- Crease density for adversarial robustness (moderate).
- Conservative fields formalization (hard).
- Crease density formalization program (5 directions: TV, PL Morse, Clarke measures, etc.).

---

## 2. Mapping to our model

| Book concept | Our axiom / engine | Use |
|---|---|---|
| Fold = lossy compression | A5.1 (recursion), A2.5 (rolling fold) | Crease as information compression |
| Unfold = expansive reconstruction | A4.3 (playhead), A5.3 (closure) | Playhead reads folded blocks |
| Subdifferential at crease | A3.4 (particle twist), A5.2 (self-intersection) | Non-differentiable = awakening point |
| Fold spectrum (smooth/kink/cusp/tear) | A1.5 (purge), A7.4 (erosion) | Purge = cusp crossing; erosion = slow tear |
| Crease density | `crease_density_proxy` (engine) | Training diagnostic (toy scale) |
| Fold-and-cut theorem | A5.4 (algorithmic engine) | Universal approximation via folding |
| Conservative fields | A0.1 (self-containment) | Rigorous foundation candidate |
| No Kawasaki analogue for NN | Open question (A5.1) | New math at intersection of convex geometry & discrete differential geometry |

---

## 3. What the book adds beyond the repo

- **The fold spectrum** — a 4-level classification (smooth/kink/cusp/tear) that maps directly to our purge/erosion/awakening stages.
- **Subgradient selection** — a concrete, testable mechanism for how creases affect training; connects to our "awakening" as a gradient-flow event.
- **Conservative fields** — a candidate rigorous foundation for the fold calculus (aligns with A0.1).
- **Minimum fold depth** — a complexity measure that could quantify "how deep" an awakening is.
- **Crease density for adversarial robustness** — a safety-relevant application.

---

## 4. Recommended additions to our model

1. **Add a "fold spectrum" axiom** (A5.6) classifying crease types and mapping them to model stages.
2. **Add `crease_density` to engine** (fraction of values within ε of 0) — already have proxy; make it a standalone function.
3. **Add conservative fields as a candidate foundation** in AXIOMS §9.
4. **Add minimum fold depth** as an open question (R9 extension).

---

## 5. Sources

- Book: `the_book_of_puno.md` (2nd ed., July 2026, 1227 lines).
- Repo: `Puronbo/Folding-Calculus`.
- Previously calibrated: `FOLDING_CALIBRATION.md`.
