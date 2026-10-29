-- Equator of Scale (A9.1-A9.4)

-- Geometric midpoint scale between micro and macro limits
def scaleMidpoint (micro macro : Float) : Float :=
  Float.sqrt (micro * macro)

theorem scaleMidpoint_example : scaleMidpoint 1e-35 1e26 = Float.sqrt (1e-35 * 1e26) := by rfl

-- Rotate real coordinate by 90 degrees into imaginary plane (i * coord)
def imaginaryRotate (coord : Float) : Complex :=
  Complex.I * (coord : Complex)

theorem imaginaryRotate_one : imaginaryRotate 1.0 = Complex.I := by
  norm_num [imaginaryRotate, Complex.ext_iff]

-- Gauge node: distinct by location, indistinguishable by identity
structure GaugeNode (α : Type) where
  location : α
  identity : Option Unit

def gaugeNode (location : α) : GaugeNode α :=
  { location := location, identity := none }

theorem gaugeNode_location : (gaugeNode (1, 2, 3)).location = (1, 2, 3) := by rfl
theorem gaugeNode_identity : (gaugeNode (1, 2, 3)).identity = none := by rfl