-- Universal impedance (L.O.R.E. proof sector)
def resonanceW0 (L C : Float) : Float :=
  1.0 / Float.sqrt (L * C)

theorem resonanceW0_one_one : resonanceW0 1.0 1.0 = 1.0 := by
  native_decide
