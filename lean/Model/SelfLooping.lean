-- Self-Looping Matrix: cosmological coupling & UV/IR inversion (A8)

-- Dark energy pumped by collapsed node of mass M under expansion
-- Pressure ~ kappa * M * (scale_factor - 1)
def cosmologicalCoupling (M scaleFactor kappa : Float) : Float :=
  kappa * M * (scaleFactor - 1.0)

theorem cosmologicalCoupling_zero : cosmologicalCoupling 5.0 1.0 1.0 = 0.0 := by
  norm_num [cosmologicalCoupling]

theorem cosmologicalCoupling_pos : cosmologicalCoupling 10.0 2.0 1.0 = 10.0 := by
  norm_num [cosmologicalCoupling]

-- UV/IR inversion: scale -> 1/scale (T-duality)
def uvIrInversion (scale : Float) : Float :=
  1.0 / scale

theorem uvIrInversion_involution : uvIrInversion (uvIrInversion 2.0) = 2.0 := by
  norm_num [uvIrInversion]

theorem uvIrInversion_one : uvIrInversion 1.0 = 1.0 := by
  norm_num [uvIrInversion]

-- Portal journey through Great Attractor
structure PortalJourney where
  phase : String
  scale : Float
  t : Float

def portalJourney (t T : Float) : PortalJourney :=
  if t < 0.5 then
    { phase := "compression", scale := 1.0 - 2.0 * t, t := t }
  else if t < 0.5 + 1e-12 then
    { phase := "inversion", scale := 0.0, t := t }
  else
    { phase := "expansion", scale := 2.0 * (t - 0.5), t := t }

theorem portalJourney_compression : (portalJourney 0.0 1.0).phase = "compression" := by
  norm_num [portalJourney]

theorem portalJourney_expansion : (portalJourney 0.75 1.0).phase = "expansion" := by
  norm_num [portalJourney]