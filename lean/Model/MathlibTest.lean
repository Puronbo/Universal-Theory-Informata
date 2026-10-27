import Mathlib

-- Net-zero: a +1 and -1 pair sums to zero (mathlib List.sum)
theorem net_zero_pair : ([1, -1] : List Int).sum = 0 := by
  simp

-- Erosion preserves the sum: [1,-1] -> [0,0]
theorem erosion_preserves_sum : ([1, -1] : List Int).sum = ([0, 0] : List Int).sum := by
  simp

-- Rolling fold: 0 deg and 180 deg same orientation (periodicity)
theorem roll_period : (0 : Nat) % 2 = (180 : Nat) % 2 := by
  native_decide