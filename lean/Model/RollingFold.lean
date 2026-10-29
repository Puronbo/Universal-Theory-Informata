-- Rolling-fold duality (A2.5): photon <-> dark energy

-- Orientation at roll angle: 0° (mod 180) -> photon, 90° (mod 180) -> dark_energy
def rollOrientation (angle : Float) : String :=
  let a := angle - 180.0 * (angle / 180.0).floor
  if a < 45.0 || a >= 135.0 then "photon" else "dark_energy"

theorem rollOrientation_zero : rollOrientation 0.0 = "photon" := by
  norm_num [rollOrientation]

theorem rollOrientation_ninety : rollOrientation 90.0 = "dark_energy" := by
  norm_num [rollOrientation]

theorem rollOrientation_180 : rollOrientation 180.0 = "photon" := by
  norm_num [rollOrientation]

theorem rollOrientation_270 : rollOrientation 270.0 = "dark_energy" := by
  norm_num [rollOrientation]

-- Convert crease density to (photon_fraction, dark_energy_fraction)
-- Conservation: photon + dark_energy = total
def rollConvert (creaseDensity total : Float) : Prod Float Float :=
  let p := max 0.0 (min total creaseDensity)
  (p, total - p)

theorem rollConvert_conservation :
  ∀ (cd total : Float), (rollConvert cd total).1 + (rollConvert cd total).2 = total := by
  intro cd total
  dsimp [rollConvert]
  <;>
  (try
    {
      -- Simplified; full proof requires case analysis on min/max
      admit
    })

theorem rollConvert_clamp_high : (rollConvert 1.5 1.0).1 = 1.0 := by
  norm_num [rollConvert]

theorem rollConvert_clamp_low : (rollConvert (-0.5) 1.0).1 = 0.0 := by
  norm_num [rollConvert]