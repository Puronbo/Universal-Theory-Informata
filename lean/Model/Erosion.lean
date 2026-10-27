-- Erosion (A7.4): net-zero preservation
def listSum : List Int -> Int
  | [] => 0
  | x :: xs => x + listSum xs

theorem listSum_pos_neg : listSum [1, -1] = 0 := by
  rfl

theorem listSum_eroded : listSum [0, 0] = 0 := by
  rfl
