-- Ternary states and net-zero invariant (AXIOMS A0.2, A0.3)

inductive Ternary where
  | neg : Ternary   -- -1 reciprocal balance
  | zero : Ternary  -- 0 void
  | pos : Ternary   -- +1 active point
deriving Repr, DecidableEq

def ternaryToInt : Ternary → Int
  | Ternary.neg  => -1
  | Ternary.zero => 0
  | Ternary.pos  => 1

theorem ternaryToInt_neg_add_pos : ternaryToInt Ternary.neg + ternaryToInt Ternary.pos = 0 := by rfl
theorem ternaryToInt_zero : ternaryToInt Ternary.zero = 0 := by rfl

def netZero (xs : List Ternary) : Prop :=
  (xs.map ternaryToInt).sum = 0

theorem netZero_pos_neg : netZero [Ternary.pos, Ternary.neg] := by rfl
theorem netZero_eroded : netZero [Ternary.zero, Ternary.zero] := by rfl
theorem netZero_empty : netZero ([] : List Ternary) := by simp [netZero]

-- Ternary composition: average normalized to [-1, 1]
def ternaryCompose (xs : List Ternary) : Float :=
  if xs = [] then 0.0 else
    (xs.map (fun x => (ternaryToInt x : Float))).sum / xs.length / 1.0

theorem ternaryCompose_zero : ternaryCompose ([] : List Ternary) = 0.0 := by
  simp [ternaryCompose]

-- Ternarize: map real drive to nearest ternary state (thresholds ±1/3)
def ternarize (x : Float) : Ternary :=
  if x > 1.0 / 3.0 then Ternary.pos
  else if x < -1.0 / 3.0 then Ternary.neg
  else Ternary.zero

theorem ternarize_pos : ternarize (1.0 : Float) = Ternary.pos := by
  norm_num [ternarize]
  <;> rfl

theorem ternarize_neg : ternarize (-1.0 : Float) = Ternary.neg := by
  norm_num [ternarize]
  <;> rfl

theorem ternarize_zero : ternarize (0.0 : Float) = Ternary.zero := by
  norm_num [ternarize]
  <;> rfl