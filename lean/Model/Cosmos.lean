-- Cosmological coupling, UV/IR inversion, scale midpoint, dimension circle (A8, A9, A11, A12)
def cosmologicalCoupling (M scale kappa : Float) : Float :=
  kappa * M * (scale - 1.0)

theorem cosmologicalCoupling_zero_scale : cosmologicalCoupling 10.0 1.0 1.0 = 0.0 := by
  native_decide

theorem cosmologicalCoupling_zero_M : cosmologicalCoupling 0.0 2.0 1.0 = 0.0 := by
  native_decide

def uvIrInversion (scale : Float) : Float :=
  1.0 / scale

theorem uvIrInversion_one : uvIrInversion 1.0 = 1.0 := by
  native_decide

theorem uvIrInversion_roundtrip : uvIrInversion (uvIrInversion 2.0) = 2.0 := by
  native_decide

def scaleMidpoint (micro macroScale : Float) : Float :=
  Float.sqrt (micro * macroScale)

theorem scaleMidpoint_example : scaleMidpoint 1.0 4.0 = 2.0 := by
  native_decide

def dimensionCircle (n : Nat) : List Float :=
  (List.range n).map (fun k => 2.0 * 3.141592653589793 * Float.ofNat k / Float.ofNat n)

theorem dimensionCircle_zero : dimensionCircle 0 = [] := by
  native_decide
