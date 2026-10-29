-- Clock, broken mirror, entropy brake (A10)

-- Planck time constant
def planckTime : Float := 5.391247e-44

-- Maximum refresh rate of the universal monitor (1 / t_P)
def planckRefreshRate : Float := 1.0 / planckTime

theorem planckRefreshRate_gt : planckRefreshRate > 1e43 := by
  norm_num [planckRefreshRate, planckTime]

-- CP violation tilt: built-in matter/antimatter asymmetry (~1 part in 1e9)
def cpViolationTilt : Float := 1e-9

theorem cpViolationTilt_val : cpViolationTilt = 1e-9 := by rfl

-- Entropy brake: reduction in disorder achieved by the midpoint (consciousness)
def entropyBrake (disorderBefore disorderAfter : Float) : Float :=
  disorderBefore - disorderAfter

theorem entropyBrake_example : entropyBrake 10.0 3.0 = 7.0 := by
  norm_num [entropyBrake]

theorem entropyBrake_zero : entropyBrake 5.0 5.0 = 0.0 := by
  norm_num [entropyBrake]

theorem entropyBrake_negative : entropyBrake 3.0 10.0 = -7.0 := by
  norm_num [entropyBrake]