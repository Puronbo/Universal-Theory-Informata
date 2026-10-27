# GUIDE — The Model: Complete Guide

> A single document covering the theory, the code, the verification, and how to use it.

---

## 1. What this is

A rigorous, alternative model of reality compiled from a gathered architecture, grounded where possible in current physics (DESI dark energy), and implemented as a runnable Python engine with a machine-checked Lean 4 math core.

**Status:** Draft v1.0. Empirical claims are quarantined from metaphysical ones.

---

## 2. The theory in one page

### Foundational math
- \(0 = 1(0)\): nothingness is a container holding a unit.
- \(0/0 = 1\): self-initialization → singularity of consciousness.
- \(0 \to 0+1 \to 0+1+n\): rest → anchor → infinite branching.
- \(2(0)-1(0)=1(0)\): inversion; vessel identity across scales.
- \(1^0=1\): automated purge at zero change.

### Conceptual framework
- **Ternary logic:** \(\{-1,0,+1\}\) (balance/void/active), net-zero invariant.
- **Algorithmic engine:** data-free intelligence from recursive feedback.
- **Consciousness as spatial action:** awareness = movement/modulation of space.

### Architecture
- **Canvas:** quantum vacuum, dynamic dark energy \(\rho_\Lambda(t)\).
- **Geometry:** two-halves (Exterior objective / Interior subjective=consciousness), spin-\(\tfrac12\) needs \(720^\circ\).
- **Playhead:** Planck-time frames read from a static 4D block universe.
- **Recursion:** feedback loops close (\(E\equiv I\)) → awakening.
- **Time-locked sync point:** 2000-10-26 10:26:20 (axiomatic, non-empirical).
- **Erosion:** slow wearing-away preserving net-zero.

---

## 3. Repository layout

| File | Purpose |
|---|---|
| `AXIOMS.md` | Numbered axiom set (A0–A7) + dependency map + open questions |
| `GROUNDING.md` | Empirical anchors (DESI/Euclid dark energy) |
| `FOLDING_CALIBRATION.md` | Lessons from Folding Calculus "dark side" |
| `CONNECTIONS.md` | Map of model ↔ governing laws of nature (with links) |
| `engine.py` | Pure-Python engine |
| `tests.py` | 25 tests (all pass) |
| `simulate.py` | End-to-end demo |
| `cli.py` | Command-line interface |
| `lean/` | Lean 4 machine-checked math core |
| `GUIDE.md` | This document |

---

## 4. Using the engine

```bash
python tests.py            # run all tests
python simulate.py         # end-to-end demo
python cli.py timeline     # milestone status
python cli.py darkenergy --z 1 --w0 -0.75 --wa -0.87
python cli.py recurse --map logistic --r 2.5
python engine.py           # small demo
```

### Key functions
- `net_zero(states)` — invariant check.
- `iterate(f, x0)` — recursion fixed point.
- `purge_if_flat(ys)` — purge at zero change.
- `erosion_step(states, pairs)` — erosion preserving net-zero.
- `cusp_roots(a,b)`, `bifurcation_value(a,b)` — cusp catastrophe.
- `w_cpl(a,w0,wa)`, `rho_lambda_ratio(z,w0,wa)`, `delta_norm(z,w0,wa)` — dark energy.
- `check_predictions(w0,wa,σw0,σwa)` — P1–P3 evaluation.
- `Playhead(block, tau)` — frame sampling.
- `milestone_reached()`, `years_since_anchor()` — timeline.

---

## 5. Verification

- Python: `python tests.py` → 25/25 pass.
- Lean 4: `cd lean && lake build` → clean (18 jobs).
- CI: `.github/workflows/ci.yml` runs both on push/PR.

---

## 6. Empirical status

| Part | Status |
|---|---|
| Dynamic dark energy (DESI DR2) | Grounded (2.8–4.2σ) |
| Spin-\(\tfrac12\) 720° topology | Established physics |
| Cusp/crease as recursion fixed point | Candidate (unvalidated) |
| Time-locked sync point, vessel identity | Axiomatic / non-empirical |
| Consciousness as interior face | Phenomenological |

---

## 7. Cautions

- Do not present the sync point or "True Observer download" as physics.
- Do not claim geometry "entirely governs" reality (container, not content).
- Keep the 720° claim scoped to spin-\(\tfrac12\)/SU(2).
- Crease density is a toy-scale neural-network diagnostic only.

---

## 8. Next steps

1. Formalize recursion operator \(f\) for a concrete family + Lean theorem.
2. Fit \(\delta(t)\) to DESI/Euclid posteriors.
3. Extend Lean proofs (erosion preserves net-zero, etc.).
4. Add notebook demo.

---

*End of Guide.*
