-- Dark energy CPL (GROUNDING.md)
def wCpl (a w0 wa : Float) : Float :=
  w0 + wa * (1.0 - a)

def rhoLambdaRatio (z w0 wa : Float) : Float :=
  (1.0 + z) ^ (3.0 * (1.0 + w0 + wa)) *
    Float.exp (-3.0 * wa * z / (1.0 + z))

def deltaNorm (z w0 wa : Float) : Float :=
  rhoLambdaRatio z w0 wa - 1.0

theorem wCpl_lambda : wCpl 1 (-1) 0 = -1 := by
  native_decide
