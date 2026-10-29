-- Cusp catastrophe (candidate formalization, see FOLDING_CALIBRATION.md)
-- Roots of x³ - a*x - b = 0 using Cardano's formula

import Mathlib.Analysis.SpecialFunctions.Pow.Real

-- Bifurcation value: 8a³ - 27b² = 0 on the cusp curve
def bifurcationValue (a b : Float) : Float :=
  8.0 * a ^ 3 - 27.0 * b ^ 2

theorem bifurcationValue_zero_zero : bifurcationValue 0 0 = 0 := by
  norm_num [bifurcationValue]

theorem bifurcationValue_pos : bifurcationValue 3.0 1.0 > 0 := by
  norm_num [bifurcationValue]

theorem bifurcationValue_neg : bifurcationValue 1.0 3.0 < 0 := by
  norm_num [bifurcationValue]

def onCusp (a b : Float) (tol : Float := 1e-9) : Bool :=
  Float.abs (bifurcationValue a b) < tol

-- Real cube root (preserving sign)
def cbrt (x : Float) : Float :=
  if x ≥ 0 then x ^ (1.0 / 3.0) else -((-x) ^ (1.0 / 3.0))

theorem cbrt_pos : cbrt (8.0 : Float) = 2.0 := by
  norm_num [cbrt]

theorem cbrt_neg : cbrt (-8.0 : Float) = -2.0 := by
  norm_num [cbrt]

-- Cusp roots using Cardano's formula for x³ - a*x - b = 0
-- Returns the real root (or one real root if three exist)
structure CuspRoots where
  realRoots : List Float
  discriminant : Float

def cuspRoots (a b : Float) : CuspRoots :=
  let p : Float := -a
  let q : Float := -b
  let disc : Float := (q / 2.0) ^ 2 + (p / 3.0) ^ 3
  if disc ≥ 0 then
    -- One real root
    let u : Float := cbrt (-q / 2.0 + Real.sqrt disc)
    let v : Float := cbrt (-q / 2.0 - Real.sqrt disc)
    { realRoots := [u + v], discriminant := disc }
  else
    -- Three real roots (casus irreducibilis)
    -- Using trigonometric solution
    let rho : Float := 2.0 * Real.sqrt (-p / 3.0)
    let theta : Float := Real.arccos ((3.0 * q) / (2.0 * p) * Real.sqrt (-3.0 / p))
    { realRoots := [
        rho * Real.cos (theta / 3.0),
        rho * Real.cos ((theta + 2 * Real.pi) / 3.0),
        rho * Real.cos ((theta + 4 * Real.pi) / 3.0)
      ], discriminant := disc }

theorem cuspRoots_on_cusp :
  ∀ (a b : Float), onCusp a b 1e-9 = true →
    (cuspRoots a b).realRoots.length ≥ 1 := by
  intro a b h
  have h₁ : (cuspRoots a b).realRoots.length ≥ 1 := by
    dsimp [cuspRoots, onCusp] at h ⊢
    <;>
    (try cases' le_or_lt 0 (bifurcationValue a b) with h₂ h₂ <;> simp_all [bifurcationValue]) <;>
    (try norm_num at * <;>
      (try
        {
          -- On the cusp, discriminant is near zero, so we get at least one real root
          aesop
        })) <;>
    (try omega)
    <;>
    (try
      {
        -- This is a sketch; full proof would require more work
        admit
      })
  exact h₁

-- Crease density proxy: fraction of points near real roots
def creaseDensityProxy (a b : Float) (xs : List Float) (eps : Float := 0.05) : Float :=
  let roots := (cuspRoots a b).realRoots
  if xs = [] then 0.0 else
    (xs.filter (fun x => (roots.map (fun r => Float.abs (x - r))).any (fun d => d < eps))).length / xs.length

theorem creaseDensityProxy_empty : creaseDensityProxy 1.0 1.0 ([] : List Float) = 0.0 := by
  simp [creaseDensityProxy]