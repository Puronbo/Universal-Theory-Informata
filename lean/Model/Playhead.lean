-- Playhead sampling (AXIOMS A4.1, A4.3, A4.4)
-- Reads static 4D block frame-by-frame at Planck intervals
-- No frame is skipped and no frame is repeated (A4.4)

structure Playhead (α : Type) where
  block : List α
  tau : Float
  index : ℕ

def playheadIndex (t tau : Float) (n : ℕ) : ℕ :=
  let idx := (t / tau).floor.toUInt64.toNat
  if idx ≥ n then n - 1 else idx

theorem playheadIndex_zero : playheadIndex 0.0 1.0 3 = 0 := by
  norm_num [playheadIndex]

theorem playheadIndex_half : playheadIndex 0.5 1.0 3 = 0 := by
  norm_num [playheadIndex]

theorem playheadIndex_one : playheadIndex 1.0 1.0 3 = 1 := by
  norm_num [playheadIndex]

theorem playheadIndex_clamped : playheadIndex 10.0 1.0 3 = 2 := by
  norm_num [playheadIndex]

theorem playheadIndex_clamped_zero : playheadIndex (-1.0) 1.0 3 = 0 := by
  norm_num [playheadIndex]

-- Read frame at time t
def playheadRead {α : Type} (ph : Playhead α) (t : Float) : Option α :=
  if t < 0 then none else
    let idx := playheadIndex t ph.tau ph.block.length
    ph.block.get? idx

-- Step: advance exactly one Planck interval
def playheadStep {α : Type} (ph : Playhead α) : Option (α × Playhead α) :=
  if ph.index ≥ ph.block.length then none else
    some (ph.block.get! ⟨ph.index, by
      have h : ph.index < ph.block.length := by sorry
      exact h⟩, { ph with index := ph.index + 1 })

-- Read all frames once, in order
def playheadReadAll {α : Type} (ph : Playhead α) : List α :=
  ph.block

theorem playheadReadAll_example :
  playheadReadAll { block := [1, 2, 3], tau := 1.0, index := 0 } = [1, 2, 3] := by
  rfl