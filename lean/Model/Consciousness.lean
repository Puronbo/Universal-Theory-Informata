-- Consciousness / attention (phenomenological, A3.2, A4.6, A5.3)

-- Map stimulus stream to ternary attention states
def attentionTrace (stimuli : List Float) (threshold : Float := 0.5) : List Int :=
  stimuli.map (fun s => if s > threshold then 1 else if s < -threshold then -1 else 0)

theorem attentionTrace_example :
  attentionTrace [0.1, 0.8, -0.9, 0.0] 0.5 = [0, 1, -1, 0] := by
  rfl

-- Conscious 'now' as stroboscopic alias of stimulus stream (A4.6)
def consciousMoment {α : Type} (stream : List α) (sampleRate : ℕ) : List α :=
  if sampleRate = 0 then [] else
    (stream.zip (List.range stream.length)).filter (fun p => p.2 % sampleRate = 0).map (fun p => p.1)

theorem consciousMoment_example :
  consciousMoment [1, 2, 3, 4, 5] 2 = [1, 3, 5] := by rfl

-- Awakening criterion: exterior and interior states coincide (A5.3, E≡I)
def closureCheck (exterior interior : List Float) (tol : Float := 1e-9) : Bool :=
  if exterior.length ≠ interior.length then false else
    (exterior.zip interior).all (fun p => Float.abs (p.1 - p.2) < tol)

theorem closureCheck_same : closureCheck [1.0, 2.0] [1.0, 2.0] = true := by rfl
theorem closureCheck_diff_len : closureCheck [1.0] [1.0, 2.0] = false := by rfl