-- Recursion: fixed point of cos (A5.1 candidate)
def iterateOnce (f : Float -> Float) (x : Float) : Float := f x

-- Collatz spine identity (L.O.R.E.): 4^(k+1) = 3*spineSum(k) + 1
def collatzSpineSum (k : Nat) : Nat :=
  (4 ^ (k + 1) - 1) / 3

theorem collatzSpine_k0 : 4 ^ 1 = 3 * collatzSpineSum 0 + 1 := by
  native_decide

theorem collatzSpine_k1 : 4 ^ 2 = 3 * collatzSpineSum 1 + 1 := by
  native_decide
