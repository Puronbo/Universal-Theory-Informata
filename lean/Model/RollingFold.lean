-- Rolling-fold duality (A2.5): 0 deg -> photon, 90 deg -> dark energy
def rollOrientation (angle : Float) : String :=
  let a := angle - 180.0 * (angle / 180.0).floor
  if a < 45.0 || a >= 135.0 then "photon" else "dark_energy"

theorem rollOrientation_zero : rollOrientation 0.0 = "photon" := by
  native_decide

theorem rollOrientation_ninety : rollOrientation 90.0 = "dark_energy" := by
  native_decide
