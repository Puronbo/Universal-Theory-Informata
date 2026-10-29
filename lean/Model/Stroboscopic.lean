-- Stroboscopic sampling (A4.6)
-- Downsample a fine signal by `rate`, producing the frozen alias (blade)

def strobe {α : Type} (signal : List α) (rate : ℕ) : List α :=
  if rate = 0 then [] else signal.map (fun x => x) -- Simplified: actual implementation would use stride

-- For rate > 0, take every `rate`-th element
def strobe' {α : Type} (signal : List α) (rate : ℕ) : List α :=
  if rate = 0 then [] else
    (signal.zip (List.range signal.length)).filter (fun p => p.2 % rate = 0).map (fun p => p.1)

theorem strobe'_example : strobe' [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] 2 = [0, 2, 4, 6, 8] := by
  rfl

theorem strobe'_rate3 : strobe' [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] 3 = [0, 3, 6, 9] := by
  rfl

theorem strobe'_rate1 : strobe' [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] 1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] := by
  rfl

theorem strobe'_empty : strobe' ([] : List ℕ) 2 = [] := by
  rfl

-- Length property
theorem strobe'_length :
  ∀ (signal : List ℕ) (rate : ℕ), rate > 0 → (strobe' signal rate).length = (signal.length + rate - 1) / rate := by
  intro signal rate hrate
  have h : (strobe' signal rate).length = (signal.length + rate - 1) / rate := by
    sorry
  exact h