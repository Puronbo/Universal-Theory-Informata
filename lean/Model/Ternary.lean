-- Ternary states and net-zero invariant (AXIOMS A0.2, A0.3)
inductive Ternary where
  | neg : Ternary   -- -1 reciprocal balance
  | zero : Ternary  -- 0 void
  | pos : Ternary   -- +1 active point
deriving Repr, DecidableEq

def ternaryToInt : Ternary -> Int
  | Ternary.neg  => -1
  | Ternary.zero => 0
  | Ternary.pos  => 1

theorem ternaryToInt_neg_add_pos : ternaryToInt Ternary.neg + ternaryToInt Ternary.pos = 0 := by
  rfl

def netZero (xs : List Ternary) : Prop :=
  (xs.map ternaryToInt).sum = 0

theorem netZero_nil : netZero [] := by
  rfl

-- erosion: convert one pos and one neg to zero, preserving sum
def erodeOne : List Ternary -> List Ternary
  | [] => []
  | Ternary.pos :: rest =>
      -- find a neg to pair; simplified: replace first pos, drop first neg later
      Ternary.zero :: erodeOne rest
  | x :: rest => x :: erodeOne rest
