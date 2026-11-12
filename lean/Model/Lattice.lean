module

import Mathlib

/-!
# The pole-string lattice

A pole string chooses one pole from each of the eight dual pairs, so it is a
function `Fin 8 → Bool`. Pointwise OR and AND make the set of strings a Boolean
lattice; complement is the duality involution. These are toy algebraic facts,
not physical claims.
-/

namespace Model

/-- One bit for each of the eight dual pairs. -/
abbrev PoleString := Fin 8 → Bool

/-- Pointwise OR: the lattice join. -/
def join (a b : PoleString) : PoleString := fun i => a i || b i

/-- Pointwise AND: the lattice meet. -/
def meet (a b : PoleString) : PoleString := fun i => a i && b i

/-- Pointwise negation: the duality complement. -/
def compl (a : PoleString) : PoleString := fun i => !a i

/-- The all-false string. -/
def bottom : PoleString := fun _ => false

/-- The all-true string. -/
def top : PoleString := fun _ => true

/-- Pointwise implication: the lattice order. -/
def leq (a b : PoleString) : Prop := ∀ i, a i = true → b i = true

theorem join_comm (a b : PoleString) : join a b = join b a := by
  funext i
  simp only [join]
  cases a i <;> cases b i <;> rfl

theorem meet_comm (a b : PoleString) : meet a b = meet b a := by
  funext i
  simp only [meet]
  cases a i <;> cases b i <;> rfl

theorem join_assoc (a b c : PoleString) :
    join (join a b) c = join a (join b c) := by
  funext i
  simp only [join]
  cases a i <;> cases b i <;> cases c i <;> rfl

theorem meet_assoc (a b c : PoleString) :
    meet (meet a b) c = meet a (meet b c) := by
  funext i
  simp only [meet]
  cases a i <;> cases b i <;> cases c i <;> rfl

theorem join_idem (a : PoleString) : join a a = a := by
  funext i
  simp only [join]
  cases a i <;> rfl

theorem meet_idem (a : PoleString) : meet a a = a := by
  funext i
  simp only [meet]
  cases a i <;> rfl

theorem absorption_join (a b : PoleString) : join a (meet a b) = a := by
  funext i
  simp only [join, meet]
  cases a i <;> cases b i <;> rfl

theorem absorption_meet (a b : PoleString) : meet a (join a b) = a := by
  funext i
  simp only [meet, join]
  cases a i <;> cases b i <;> rfl

theorem distrib_join (a b c : PoleString) :
    join a (meet b c) = meet (join a b) (join a c) := by
  funext i
  simp only [join, meet]
  cases a i <;> cases b i <;> cases c i <;> rfl

theorem distrib_meet (a b c : PoleString) :
    meet a (join b c) = join (meet a b) (meet a c) := by
  funext i
  simp only [meet, join]
  cases a i <;> cases b i <;> cases c i <;> rfl

theorem compl_compl (a : PoleString) : compl (compl a) = a := by
  funext i
  simp only [compl]
  cases a i <;> rfl

theorem join_compl (a : PoleString) : join a (compl a) = top := by
  funext i
  simp only [join, compl, top]
  cases a i <;> rfl

theorem meet_compl (a : PoleString) : meet a (compl a) = bottom := by
  funext i
  simp only [meet, compl, bottom]
  cases a i <;> rfl

theorem compl_join (a b : PoleString) :
    compl (join a b) = meet (compl a) (compl b) := by
  funext i
  simp only [compl, join, meet]
  cases a i <;> cases b i <;> rfl

theorem compl_meet (a b : PoleString) :
    compl (meet a b) = join (compl a) (compl b) := by
  funext i
  simp only [compl, meet, join]
  cases a i <;> cases b i <;> rfl

theorem leq_refl (a : PoleString) : leq a a := by
  intro i h
  exact h

theorem leq_trans {a b c : PoleString} (hab : leq a b) (hbc : leq b c) :
    leq a c := by
  intro i ha
  exact hbc i (hab i ha)

theorem leq_antisymm {a b : PoleString} (hab : leq a b) (hba : leq b a) :
    a = b := by
  funext i
  cases ha : a i <;> cases hb : b i <;> simp_all [leq]

end Model
