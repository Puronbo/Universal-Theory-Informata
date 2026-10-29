# RESEARCH ROADMAP — Prioritized Next Steps

> Companion to `AXIOMS.md` §9. Each item has a concrete task and a success criterion.

---

## Tier 1 — Empirical (highest value, shortest horizon)

### R1. Fit \(\delta(t)\) to DESI DR2 posteriors
- **Task:** Use the DESI DR2 \(w_0,w_a\) covariance to compute \(\delta_{\rm norm}(z)\) with uncertainties; update `GROUNDING.md` §2.4.
- **Success:** \(\delta'_{\rm norm}(0)\) reported with 1σ; P1–P4 evaluated against real posteriors.
- **Tool:** `engine.delta_norm`, `check_predictions`.

### R2. Euclid first cosmology release (expected ~2026–2027)
- **Task:** Re-run P1–P4 against Euclid CLOE constraints; update falsifiability horizon.
- **Success:** `GROUNDING.md` §2.5 upgraded from forecast to measurement.
- **Tool:** `agent-reach` web search for Euclid releases.

### R3. Anisotropy test (Sarkar vs. Vincenzi)
- **Task:** Determine whether acceleration is directional; if so, extend A2.2 with a directional term.
- **Success:** Either A2.2 stands (isotropic) or a new axiom A2.6 (anisotropic canvas) is added.
- **Reference:** `HORIZON_FINDINGS.md`.

---

## Tier 2 — Formal (machine-checkable)

### R4. Formalize recursion operator \(f\)
- **Task:** Pick a concrete family (logistic, Kené, Mandelbrot) and define \(f\) with a fixed-point theorem in Lean.
- **Success:** `lean/Model/Recursion.lean` contains a nontrivial theorem (not just `rfl`/`native_decide`).
- **Tool:** Lean 4 + mathlib.

### R5. Prove erosion preserves net-zero in Lean
- **Status:** Attempted via induction on `sum_erase` helper. Blocked: `List.erase_cons_tail` condition requires converting propositional `x != a` to boolean; `of_decide_eq_true` path stalled. Concrete cases verified with `native_decide`.
- **Task:** Define `erodePairs` on `List Ternary` and prove `listSum (erodePairs xs) = listSum xs`.
- **Success:** Theorem compiles in `lean/Model/Erosion.lean`.

### R6. Upgrade Lean to mathlib
- **Task:** Add mathlib dependency to `lean/lakefile.toml`; rebuild.
- **Success:** `lake build` still clean with mathlib; enables number-theory proofs.

### R7. Meta-audit automation
- **Task:** Extend `validate_claims.py` to also check that every axiom has a cross-reference in `CONNECTIONS.md`.
- **Success:** Script exits 0 on current repo; fails on a deliberately broken copy.

---

## Tier 3 — Conceptual (high risk, high reward)

### R8. Asymptotic-safety canvas
- **Task:** Identify the canvas (A2.3) with the UV fixed point of asymptotic safety; derive testable prediction for Higgs potential flatness.
- **Success:** New open question in `AXIOMS.md` §9 with a falsifiable signature.

### R9. Kené as recursion family
- **Task:** Formalize Kené self-similarity as a specific \(f\) for A5.1; connect to Mandelbrot/Julia sets.
- **Success:** A concrete \(f\) and its fixed-point structure documented.

### R10. Consciousness as stroboscopic alias
- **Task:** Extend A4.6 to argue that conscious "now" is the alias of continuous spatial action; identify the sample rate with neural frame rate.
- **Success:** A new axiom or open question with a measurable prediction.

---

## Tier 4 — Usability

### R11. Package and publish
- **Task:** Add `pyproject.toml`, build wheel, publish to PyPI (optional).
- **Success:** `pip install model` works locally.

### R12. Notebook demo
- **Task:** Create `demo.ipynb` combining simulate.py outputs and plots.
- **Success:** Notebook runs end-to-end.

---

## Tracking

Update `AXIOMS.md` §9 open questions as items are resolved. Re-run `validate_claims.py` and `python tests.py` after every change.
