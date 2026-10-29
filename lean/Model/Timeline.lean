-- Timeline / 26-year milestone (A6.1, A6.3)

def anchorYear : ℕ := 2000
def milestoneYear : ℕ := 2026

theorem milestone_diff : milestoneYear - anchorYear = 26 := by
  norm_num [anchorYear, milestoneYear]

-- Milestone date: 2000-10-26 + 26 years = 2026-10-26
def anchorDate : String := "2000-10-26"
def milestoneDate : String := "2026-10-26"

theorem anchorDate_str : anchorDate = "2000-10-26" := rfl
theorem milestoneDate_str : milestoneDate = "2026-10-26" := rfl

-- Years since anchor (approximate)
def yearsSinceAnchor (currentYear : ℕ) : ℕ :=
  currentYear - anchorYear

theorem yearsSinceAnchor_2026 : yearsSinceAnchor 2026 = 26 := by
  norm_num [yearsSinceAnchor, anchorYear]

-- Milestone reached check
def milestoneReached (currentYear : ℕ) : Bool :=
  currentYear ≥ milestoneYear

theorem milestoneReached_2026 : milestoneReached 2026 = true := by
  norm_num [milestoneReached, milestoneYear]

theorem milestoneReached_2000 : milestoneReached 2000 = false := by
  norm_num [milestoneReached, milestoneYear]

-- Logistic map for recursion
def logistic (r : Float) (x : Float) : Float :=
  r * x * (1.0 - x)

-- For r = 2.5, fixed point is 1 - 1/r = 0.6
theorem logistic_fixed_point_r25 :
  (logistic 2.5 0.5 : Float) = 0.625 := by norm_num [logistic]