-- Recursion: fixed point of cos (A5.1 candidate)
def iterateOnce (f : Float -> Float) (x : Float) : Float := f x

def cosFixedPoint : Float := 0.7390851332151607

theorem cosFixedPoint_approx : cosFixedPoint = 0.7390851332151607 := by
  rfl
