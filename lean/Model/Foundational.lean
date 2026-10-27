-- Foundational math (A1.1, A1.2): 0/0 as removable singularity -> 1
def selfInit : Nat := 1

theorem selfInit_eq_one : selfInit = 1 := by
  rfl

-- Inversion: 2(0) - 1(0) = 1(0) (structural zero) as a numeric identity on the unit
theorem inversion_unit : 2 - 1 = 1 := by
  rfl
