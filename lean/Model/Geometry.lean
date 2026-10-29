-- Geometry: particles as stretched points (A3.6)
def stretchedDistance (d0 scale : Float) : Float :=
  d0 * scale

theorem stretchedDistance_identity : stretchedDistance 1.0 1.0 = 1.0 := by
  native_decide

theorem stretchedDistance_zero : stretchedDistance 0.0 5.0 = 0.0 := by
  native_decide
