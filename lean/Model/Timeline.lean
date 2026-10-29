-- Timeline: 26-year milestone (A6.3)
def anchorYear : Nat := 2000
def milestoneYear : Nat := 2026

theorem milestone_diff : milestoneYear - anchorYear = 26 := by
  native_decide
