-- Playhead sampling (AXIOMS A4.5)
def playheadIndex (t tau : Float) (n : Nat) : Nat :=
  let idx := (t / tau).floor.toUInt64.toNat
  if idx >= n then n - 1 else idx
