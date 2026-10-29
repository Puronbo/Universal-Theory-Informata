-- Cusp catastrophe bifurcation (FOLDING_CALIBRATION candidate)
def bifurcationValue (a b : Float) : Float :=
  8.0 * a^3 - 27.0 * b^2

theorem bifurcationValue_zero_zero : bifurcationValue 0 0 = 0 := by
  native_decide

def onCusp (a b : Float) (tol : Float := 1e-9) : Bool :=
  Float.abs (bifurcationValue a b) < tol
