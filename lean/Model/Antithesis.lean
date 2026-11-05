module

import Mathlib

/-!
# Antithesis: involutions, contractions, and nilpotents

The framework's core map is the reciprocal involution `f x = x⁻¹`. This file
records the algebraic contrast with the antithesis:

* `f` is an involution: `f (f x) = x`;
* the contraction `g x = r * x` is not, and its orbits grow or decay;
* the nilpotent `N (x, y) = (0, x)` satisfies `N² = 0`.

These are toy algebraic facts, not physical claims.
-/

namespace Model

/-- The framework's core map: reciprocal scale. -/
noncomputable def involution (x : ℝ) : ℝ := x⁻¹

/-- Inversion is its own inverse: `f² = id`. -/
theorem involution_involutive (x : ℝ) : involution (involution x) = x := by
  simp [involution]

/-- The reciprocal of a nonzero scale is nonzero. -/
theorem involution_ne_zero {x : ℝ} (hx : x ≠ 0) : involution x ≠ 0 := by
  simpa [involution] using inv_ne_zero hx

/-- One step of the one-way contraction `g x = r * x`. -/
noncomputable def contraction (r x : ℝ) : ℝ := r * x

/-- The contraction orbit after `n` steps. -/
noncomputable def contractOrbit (r x : ℝ) : ℕ → ℝ
  | 0 => x
  | n + 1 => r * contractOrbit r x n

/-- The `n`-th contraction iterate is `r ^ n * x`. -/
theorem contractOrbit_eq (r x : ℝ) (n : ℕ) :
    contractOrbit r x n = r ^ n * x := by
  induction n with
  | zero => simp [contractOrbit]
  | succ k ih =>
      simp only [contractOrbit, ih, pow_succ]
      ring

/-- The contraction fixes zero. -/
theorem contraction_zero (r : ℝ) : contraction r 0 = 0 := by
  simp [contraction]

/-- The parabolic map `p x = x + s`. -/
noncomputable def translation (s x : ℝ) : ℝ := x + s

/-- A nonzero translation has no fixed point. -/
theorem translation_no_fixed (s : ℝ) (hs : s ≠ 0) (x : ℝ) :
    translation s x ≠ x := by
  intro h
  unfold translation at h
  exact hs (by linarith)

/-- The nilpotent `N (x, y) = (0, x)` on `ℝ × ℝ`. -/
def nilpotent (v : ℝ × ℝ) : ℝ × ℝ := (0, v.1)

/-- `N² = 0`: applying the nilpotent twice collapses every vector. -/
theorem nilpotent_sq_zero (v : ℝ × ℝ) : nilpotent (nilpotent v) = (0, 0) := by
  simp [nilpotent]

/-- Entropy `-log r` increases under a contraction with `0 < r < 1`. -/
theorem entropy_gain_pos (r : ℝ) (hr0 : 0 < r) (hr1 : r < 1) :
    0 < -Real.log r := by
  have h : Real.log r < Real.log 1 := Real.log_lt_log hr0 hr1
  have h0 : Real.log (1 : ℝ) = 0 := by simp
  rw [h0] at h
  linarith

/-- The inversion-invariant quotient `q x = x + x⁻¹`. -/
noncomputable def fold (x : ℝ) : ℝ := x + x⁻¹

/-- The quotient is invariant under inversion: `q (1/x) = q x`. -/
theorem fold_invariant (x : ℝ) : fold x⁻¹ = fold x := by
  unfold fold
  rw [inv_inv]
  ring

/-- The quotient is at least 2 on positive scales. -/
theorem fold_ge_two {x : ℝ} (hx : 0 < x) : 2 ≤ fold x := by
  unfold fold
  have h : 0 ≤ (x - 1) ^ 2 := sq_nonneg (x - 1)
  have hdiv : 0 ≤ (x - 1) ^ 2 / x := div_nonneg h hx.le
  have hEq : (x - 1) ^ 2 / x = x - 2 + x⁻¹ := by
    field_simp [hx.ne']
    ring
  rw [hEq] at hdiv
  linarith

/-- The quotient is not injective: `2` and `1/2` have the same image. -/
theorem fold_not_injective : ¬ Function.Injective fold := by
  intro h
  have h2 : fold (2 : ℝ) = fold (1 / 2) := by
    unfold fold
    norm_num
  have hEq : (2 : ℝ) = 1 / 2 := h h2
  norm_num at hEq

/-- The log coordinate turns contraction into translation. -/
theorem log_contraction (x r : ℝ) (hx : 0 < x) (hr : 0 < r) :
    Real.log (r * x) = Real.log x + Real.log r := by
  rw [Real.log_mul hr.ne' hx.ne']
  ring

/-- The exponential coordinate is the inverse of the log coordinate. -/
theorem exp_log_coordinate {x : ℝ} (hx : 0 < x) :
    Real.exp (Real.log x) = x :=
  Real.exp_log hx

end Model
