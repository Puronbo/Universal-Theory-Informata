-- Geometry: particles as stretched points (A3.6)

-- Apparent separation under canvas stretching
def stretchedDistance (d0 scale : Float) : Float :=
  d0 * scale

theorem stretchedDistance_identity : stretchedDistance 1.0 1.0 = 1.0 := by
  norm_num [stretchedDistance]

theorem stretchedDistance_zero : stretchedDistance 0.0 5.0 = 0.0 := by
  norm_num [stretchedDistance]

theorem stretchedDistance_mult : stretchedDistance 3.0 2.0 = 6.0 := by
  norm_num [stretchedDistance]

-- Pairwise distances among points scaled by canvas stretch factor
def apparentSeparation (points : List Float) (scale : Float) : List (Prod ℕ (Prod ℕ Float)) :=
  (List.range points.length).flatMap (fun i =>
    (List.range points.length).filter (fun j => i < j).map (fun j =>
      (i, (j, (points.get! ⟨j, by
        have h : j < points.length := by sorry
        exact h⟩ - points.get! ⟨i, by
        have h : i < points.length := by sorry
        exact h⟩) * scale))))

theorem apparentSeparation_example :
  apparentSeparation [0.0, 1.0, 3.0] 2.0 =
    [(0, (1, 2.0)), (0, (2, 6.0)), (1, (2, 4.0))] := by
  rfl

theorem apparentSeparation_empty : apparentSeparation ([] : List Float) 2.0 = [] := by
  rfl

theorem apparentSeparation_single : apparentSeparation [1.0] 2.0 = [] := by
  rfl