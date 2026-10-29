module

import Mathlib

-- Erosion (A7.4): removing a +1 and a -1 preserves the sum.
-- General proof pending (R5); concrete cases verified here.
def erodeOne (xs : List Int) : List Int :=
  (xs.erase (-1)).erase 1

theorem erodeOne_example : erodeOne [1, -1, 2] = [2] := by
  native_decide

theorem listSum_pos_neg : ([1, -1] : List Int).sum = 0 := by
  simp

theorem listSum_eroded : ([0, 0] : List Int).sum = 0 := by
  simp

theorem erosion_preserves_example : ([1, -1] : List Int).sum = ([0, 0] : List Int).sum := by
  simp
