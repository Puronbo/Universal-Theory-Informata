-- Dynamic dark energy (A2.2, GROUNDING.md)
-- CPL equation of state, rho_Lambda(z), DESI-anchored predictions

import Mathlib.Analysis.SpecialFunctions.ExpLog

-- CPL equation of state: w(a) = w0 + wa * (1 - a)
def wCpl (a w0 wa : Float) : Float :=
  w0 + wa * (1.0 - a)

theorem wCpl_lambda : wCpl 1.0 (-1.0) 0.0 = -1.0 := by norm_num [wCpl]
theorem wCpl_phantom : wCpl 0.5 (-1.2) (-0.5) < -1.0 := by norm_num [wCpl]
theorem wCpl_quintom : wCpl 0.5 (-0.75) (-0.87) > -1.0 := by norm_num [wCpl]

-- rho_DE(z)/rho_DE(0) for CPL: (1+z)^{3(1+w0+wa)} * exp(-3*wa*z/(1+z))
def rhoLambdaRatio (z w0 wa : Float) : Float :=
  (1.0 + z) ^ (3.0 * (1.0 + w0 + wa)) *
    Float.exp (-3.0 * wa * z / (1.0 + z))

theorem rhoLambdaRatio_lambda : rhoLambdaRatio 1.0 (-1.0) 0.0 = 1.0 := by
  norm_num [rhoLambdaRatio]

theorem rhoLambdaRatio_present : rhoLambdaRatio 0.0 (-0.75) (-0.87) = 1.0 := by
  norm_num [rhoLambdaRatio]

-- Normalized delta: delta/rho0 = rho_DE(z)/rho_DE(0) - 1
def deltaNorm (z w0 wa : Float) : Float :=
  rhoLambdaRatio z w0 wa - 1.0

theorem deltaNorm_present : deltaNorm 0.0 (-0.75) (-0.87) = 0.0 := by
  norm_num [deltaNorm, rhoLambdaRatio]

theorem deltaNorm_past_positive_quintom : deltaNorm 1.0 (-0.75) (-0.87) > 0.0 := by
  have h : deltaNorm 1.0 (-0.75) (-0.87) > 0.0 := by
    norm_num [deltaNorm, rhoLambdaRatio, Float.exp, Float.add_assoc]
    <;>
    (try linarith [Real.exp_pos (-3.0 * (-0.87 : ℝ) * 1 / (1 + 1 : ℝ))]) <;>
    (try norm_num) <;>
    (try
      {
        -- Use numerical approximation
        have := Real.exp_pos (-3.0 * (-0.87 : ℝ) * 1 / (1 + 1 : ℝ))
        norm_num at *
        <;> linarith
      })
  exact h

-- Derivative at present: d(deltaNorm)/dz at z=0
def deltaDerivativePresent (w0 wa : Float) (h : Float := 1e-5) : Float :=
  (deltaNorm h w0 wa - deltaNorm 0.0 w0 wa) / h

theorem deltaDerivativePresent_positive_quintom :
  deltaDerivativePresent (-0.75) (-0.87) > 0.0 := by
  have h : deltaDerivativePresent (-0.75) (-0.87) > 0.0 := by
    norm_num [deltaDerivativePresent, deltaNorm, rhoLambdaRatio, Float.exp] <;>
    (try linarith) <;>
    (try norm_num) <;>
    (try
      {
        -- Numerical verification
        norm_num [Float.exp] at *
        <;> linarith
      })
  exact h

-- DESI DR2 reference values (GROUNDING.md)
structure DESIReference where
  w0_range : Prod Float Float
  wa_range : Prod Float Float
  sig_DESI_CMB : Float
  sig_with_SNe : Prod Float Float

def DESI_REFERENCE : DESIReference :=
  { w0_range := (-0.85, -0.66),
    wa_range := (-1.11, -0.61),
    sig_DESI_CMB := 3.1,
    sig_with_SNe := (2.8, 4.2) }

-- Prediction checks from GROUNDING.md
structure Predictions where
  P1_weakening_3sigma : Bool
  P2_amplitude_3sigma : Bool
  P3_phantom_sign_flip_needed : Bool
  quintom_B_quadrant : Bool

def checkPredictions (w0 wa sigma_w0 sigma_wa : Float) : Predictions :=
  { P1_weakening_3sigma := (wa < 0) && (Float.abs wa / max sigma_wa 1e-12 ≥ 3.0)
    P2_amplitude_3sigma := (Float.abs (w0 + 1.0) / max sigma_w0 1e-12 ≥ 3.0) && (Float.abs (w0 + 1.0) ≥ 0.1)
    P3_phantom_sign_flip_needed := w0 < -1.0
    quintom_B_quadrant := (w0 > -1.0) && (wa < 0.0) }

theorem checkPredictions_quintom :
  (checkPredictions (-0.75) (-0.87) 0.058 0.25).quintom_B_quadrant = true := by
  norm_num [checkPredictions, Predictions.quintom_B_quadrant]

theorem checkPredictions_phantom :
  (checkPredictions (-1.2) (-0.5) 0.1 0.2).P3_phantom_sign_flip_needed = true := by
  norm_num [checkPredictions, Predictions.P3_phantom_sign_flip_needed]